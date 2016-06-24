# !/usr/bin/python

import json
import redis
from redis.exceptions import RedisError
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBServerError, InfluxDBClientError
from celery.schedules import crontab
from ovs.celery_run import celery
from ovs.extensions.db.etcd.configuration import EtcdConfiguration
from ovs.dal.lists.backendlist import BackendList
from ovs.lib.helpers.decorators import ensure_single
from ovs.log.log_handler import LogHandler
from ovs.dal.lists.vdisklist import VDiskList
from ovs.dal.hybrids.storagerouter import StorageRouter
from ovs.dal.lists.vpoollist import VPoolList
from ovs.dal.hybrids.vpool import VPool
from ovs.dal.lists.servicelist import ServiceList
from ovs.dal.hybrids.servicetype import ServiceType
from ovs.dal.lists.albanodelist import AlbaNodeList
from ovs.dal.lists.albabackendlist import AlbaBackendList
from ovs.extensions.plugins.albacli import AlbaCLI
from ovs.dal.hybrids.service import Service


class StatsmonkeyScheduledTaskController(object):
    _logger = LogHandler.get('lib', name='scheduled tasks')
    _logger.info('Send data task scheduling started')

    @staticmethod
    def _send_stats(points):

        db_key = '/ops/db'
        if not EtcdConfiguration.exists(db_key):
            StatsmonkeyScheduledTaskController._logger.error('{} config not found'.format(db_key))
            return

        db_config = EtcdConfiguration.get(db_key)

        transport = db_config.get('transport')
        host = db_config.get('host')
        port = db_config.get('port')
        password = db_config.get('password')
        database = db_config.get('database')

        if transport == 'influxdb':
            try:
                user = db_config.get('username')
                client = InfluxDBClient(host=host, port=port, username=user, password=password, database=database)
                StatsmonkeyScheduledTaskController._logger.info(points)
                client.write_points(points)
            except InfluxDBClientError as c:
                StatsmonkeyScheduledTaskController._logger.error(c.message)
            except InfluxDBServerError as s:
                StatsmonkeyScheduledTaskController._logger.error(s.message)
            except Exception as ex:
                StatsmonkeyScheduledTaskController._logger.error(ex.message)
        elif transport == 'redis':
            try:
                client = redis.Redis(host=host, port=port, password=password)
                StatsmonkeyScheduledTaskController._logger.info(points)
                client.lpush(database, points)
            except RedisError as ex:
                StatsmonkeyScheduledTaskController._logger.error(ex.message)
            except Exception as ex:
                StatsmonkeyScheduledTaskController._logger.error(ex.message)
        else:
            StatsmonkeyScheduledTaskController._logger.error("transport {0} not supported.".format(transport))

    @staticmethod
    def _pop_realtime_info(points):
        pop_points = [k for (k, v) in points.items() if k.endswith("_ps")]

        for point in pop_points:
            points.pop(point, None)

        return points

    @staticmethod
    @celery.task(name='statsmonkey.sender.get_backend_sizes',
                 schedule=crontab(minute='*', hour='*'))
    @ensure_single(task_name='statsmonkey.sender.get_backend_sizes')
    def get_backend_sizes():
        """
        Send backend sizes to InfluxDB
        """
        points = []
        backends = BackendList.get_backends()

        if len(backends) == 0:
            StatsmonkeyScheduledTaskController._logger.info("No backends found")
            return

        for b in backends:
            global_size = b.alba_backend.ns_statistics['global']
            entry = {
                'measurement': 'backend_size',
                'tags': {
                    'backend_name': b.name
                },
                'fields': {
                    'free': global_size['size'] - global_size['used'],
                    'used': global_size['used']
                }
            }
            points.append(entry)

        if len(points) == 0:
            StatsmonkeyScheduledTaskController._logger.info("No statistics found")
            return

        StatsmonkeyScheduledTaskController._send_stats(points)
        return points

    @staticmethod
    @celery.task(name='statsmonkey.sender.get_vdisks_stats',
                 schedule=crontab(minute='*', hour='*'))
    @ensure_single(task_name='statsmonkey.sender.get_vdisks_stats')
    def get_vdisks_stats():
        """
        Send vdisks statistics to InfluxDB
        """
        vdisks = VDiskList.get_vdisks()
        if len(vdisks) == 0:
            StatsmonkeyScheduledTaskController._logger.info("No vdisks found")
            return None

        for vdisk in vdisks:
            try:
                points = []
                metrics = StatsmonkeyScheduledTaskController._pop_realtime_info(vdisk.statistics)

                disk_name = vdisk.name
                failover_mode = vdisk.info['failover_mode']

                if failover_mode in ['OK_STANDALONE', 'OK_SYNC']:
                    failover_status = 0
                elif failover_mode == 'CATCHUP':
                    failover_status = 1
                elif failover_mode == 'DEGRADED':
                    failover_status = 2
                else:
                    failover_status = 3

                metrics['failover_mode_status'] = failover_status

                if vdisk.vmachine:
                    vm_name = vdisk.vmachine.name
                else:
                    vm_name = None

                vpool_name = VPool(vdisk.vpool_guid).name

                entry = {
                    'measurement': 'vdisk_stats',
                    'tags': {
                        'disk_name': disk_name,
                        'vm_name': vm_name,
                        'storagerouter_name': StorageRouter(vdisk.storagerouter_guid).name,
                        'vpool_name': vpool_name,
                        'failover_mode': vdisk.info['failover_mode']
                    },
                    'fields': metrics
                }
                points.append(entry)
                StatsmonkeyScheduledTaskController._send_stats(points)
                return points
            except Exception as ex:
                StatsmonkeyScheduledTaskController._logger.error(ex.message)
                return None
            return None

    @staticmethod
    @celery.task(name='statsmonkey.sender.get_backend_stats',
                 schedule=crontab(minute='*', hour='*'))
    @ensure_single(task_name='statsmonkey.sender.get_backend_stats')
    def get_backend_stats():
        """
        Send backend stats for each backend to InfluxDB
        """
        points = []
        abms = []
        abs = []

        for service in ServiceList.get_services():
            if service.type.name == ServiceType.SERVICE_TYPES.ALBA_MGR:
                abms.append(service.name)

        for ab in AlbaNodeList.get_albanodes():
            abs.append(ab.node_id)

        abms = list(set(abms))

        config = "etcd://127.0.0.1:2379/ovs/arakoon/{}/config".format(abms[0])
        decommissioning_osds = AlbaCLI.run('list-decommissioning-osds', config=config, to_json=True)

        filtered_osds = []

        for ab in abs:
            filtered_osds += [osd for osd in decommissioning_osds if osd['node_id'] == ab]

        abl = AlbaBackendList.get_albabackends()

        for ab in abl:
            try:
                stat = {
                    'measurement': 'backend_stats',
                    'tags': {
                        'backend_name': ab.name
                    },
                    'fields': {
                        'gets': ab.statistics['multi_get']['n'],
                        'puts': ab.statistics['apply']['n']
                    }
                }
                stat_asd = {
                    'decommissioning': len(filtered_osds),
                    'decommissioned': 0,
                    'claimed': 0,
                    'warning': 0,
                    'failure': 0,
                    'error': 0
                }

                for disks in ab.local_stack.values():
                    for disk in disks.values():
                        for asd in disk['asds'].values():
                            if asd['alba_backend_guid'] == ab.guid:
                                status = asd['status']
                                status_detail = asd['status_detail']
                                if status_detail == 'decommissioned':
                                    status = status_detail
                                if status not in stat_asd:
                                    stat_asd[status] = 0
                                stat_asd[status] += 1

                for status in stat_asd:
                    stat['fields'][status] = stat_asd[status]
                points.append(stat)
            except Exception as ex:
                StatsmonkeyScheduledTaskController._logger.error(ex.message)

        if len(points) == 0:
            StatsmonkeyScheduledTaskController._logger.info("No statistics found")
            return None

        StatsmonkeyScheduledTaskController._send_stats(points)
        return points

    @staticmethod
    @celery.task(name='statsmonkey.sender.get_disk_safety',
                 schedule=crontab(minute='*', hour='*'))
    @ensure_single(task_name='statsmonkey.sender.get_disk_safety')
    def get_disk_safety():
        """
        Send disk safety for each vpool and the amount of namespaces with the lowest disk safety
        """
        points = []
        abms = []

        for service in ServiceList.get_services():
            if service.type.name == ServiceType.SERVICE_TYPES.ALBA_MGR:
                abms.append(service.name)

        abms = list(set(abms))
        abl = AlbaBackendList.get_albabackends()
        for ab in abl:
            service_name = Service(ab.abm_services[0].service_guid).name
            if service_name not in abms:
                continue

            config = "etcd://127.0.0.1:2379/ovs/arakoon/{}/config".format(service_name)
            disk_safety = AlbaCLI.run('get-disk-safety', config=config, to_json=True)

            presets = ab.presets
            used_preset = None
            for preset in presets:
                try:
                    policies = preset['policy_metadata']
                    for policy in policies:
                        if policies[policy]['is_active'] and policies[policy]['in_use']:
                            used_preset = policy

                    if used_preset is not None:
                        used_preset = json.loads(used_preset.replace('(', '[').replace(')', ']'))
                        max_disk_safety = used_preset[1]

                        safety = {
                            'measurement': 'disk_safety',
                            'tags': {
                                'backend_name': ab.name,
                                'max_disk_safety': max_disk_safety,
                                'min_disk_safety': max_disk_safety
                            },
                            'fields': {
                                'amount_max_disk_safety': 0,
                                'amount_between_disk_safety': 0,
                                'amount_min_disk_safety': 0
                            }
                        }
                        stats = {}
                        for disk in disk_safety:
                            if disk['safety'] is not None:
                                if disk['safety'] not in stats:
                                    stats[disk['safety']] = 0
                                stats[disk['safety']] += 1
                        min_disk_safety = min(stats.keys())
                        safety['tags']['min_disk_safety'] = min_disk_safety

                        for stat in stats:
                            if stat == max_disk_safety:
                                safety['fields']['amount_max_disk_safety'] = stats[stat]
                            elif stat == min_disk_safety:
                                safety['fields']['amount_min_disk_safety'] = stats[stat]
                            else:
                                safety['fields']['amount_between_disk_safety'] += stats[stat]

                        points.append(safety)
                except Exception as ex:
                    StatsmonkeyScheduledTaskController._logger.error(ex.message)

        if len(points) == 0:
            StatsmonkeyScheduledTaskController._logger.info("No statistics found")
            return

        StatsmonkeyScheduledTaskController._send_stats(points)
        return points

    @staticmethod
    @celery.task(name='statsmonkey.sender.get_vpool_stats',
                 schedule=crontab(minute='*', hour='*'))
    @ensure_single(task_name='statsmonkey.sender.get_vpool_stats')
    def get_vpool_stats():
        """
        Send Vpool statistics to InfluxDB
        """
        points = []
        vpools = VPoolList.get_vpools()
        if len(vpools) == 0:
            StatsmonkeyScheduledTaskController._logger.info("No vpools found")
            return

        for vpool in vpools:
            try:
                metrics = StatsmonkeyScheduledTaskController._pop_realtime_info(vpool.statistics)
                vpool_name = vpool.name

                entry = {
                    'measurement': 'vpool_stats',
                    'tags': {
                        'vpool_name': vpool_name
                    },
                    'fields': metrics
                }
                points.append(entry)
            except Exception as ex:
                StatsmonkeyScheduledTaskController._logger.error(ex.message)

        if len(points) == 0:
            StatsmonkeyScheduledTaskController._logger.info("No statistics found")
            return

        StatsmonkeyScheduledTaskController._send_stats(points)
        return points

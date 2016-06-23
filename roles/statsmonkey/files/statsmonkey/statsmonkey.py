#!/usr/bin/python

import sys
import argparse
import ConfigParser
import subprocess
import datetime
import threading
import json
import psutil
import redis
from redis.exceptions import RedisError
from influxdb import InfluxDBClient
from influxdb.exceptions import *
from os import walk, listdir
from os.path import isfile, join, abspath, isdir, basename


class Statsmonkey():

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._read_config_file()

    def run_plugins(self):
        threads = []
        running_processes = [proc.cmdline() for proc in psutil.process_iter() if len(proc.cmdline()) > 1 and
                             self.config['plugins'] in proc.cmdline()[1]]

        for plugin in self._get_plugin_files():
            try:
                to_skip = False
                for process in running_processes:
                    if basename(plugin) in process[1] and not to_skip:
                        to_skip = True
                        self._print_message(basename(plugin), "plugin still running.")
                if not to_skip:
                    t = threading.Thread(target=self._send_stats, args=(plugin,))
                    threads.append(t)
                    t.start()
            except Exception, ex:
                self._print_message(ex.message)

    def _send_stats(self, plugin):
        """
        :param plugin: plugin file
        """
        points = []

        try:
            stats_file = "/tmp/{}.stats".format(basename(plugin))
            with open(stats_file, "w+") as output:
                subprocess.call(plugin, stdout=output)

            with open(stats_file, "r") as output:
                points = json.loads(output.read())

        except ValueError as ex:
            self._print_message("{0} error: {1}".format(basename(plugin), ex.message))
        except Exception as ex:
            self._print_message(ex.message)

        new_points = []
        for point in points:
            if point is not None:
                point['tags']['group'] = self.config['group']
                new_points.append(point)

        if len(new_points) == 0:
            self._print_message("No statistics found.")
            return

        transport = self.config['transport']
        host = self.config['host']
        port = self.config['port']
        password = self.config['password']
        database = self.config['database']

        if transport == 'influxdb':
            try:
                user = self.config['user']
                client = InfluxDBClient(host, port, user, password, database)
                client.write_points(new_points)
            except InfluxDBClientError as ex:
                self._print_message(ex.message)
            except InfluxDBServerError as ex:
                self._print_message(ex.message)
            except Exception as ex:
                self._print_message(ex.message)
        elif transport == 'redis':
            try:
                client = redis.Redis(host=host, port=port, password=password)
                client.lpush(database, points)
            except RedisError as ex:
                self._print_message(ex.message)
            except Exception as ex:
                self._print_message(ex.message)
        else:
            self._print_message("transport {0} not supported.".format(transport))

    def _get_plugin_files(self):
        """
        :return: Returns a list of files
        """
        etcd = False
        stats = []

        try:
            stats_key = '/ops/stats'
            if not EtcdConfiguration.exists(stats_key):
                self._print_message('{0} config not found'.format(stats_key))

            stats = EtcdConfiguration.get(stats_key).get('statistics')
            etcd = True
        except Exception:
            pass

        files = []
        plugin_path = self.config['plugins']
        if not isdir(plugin_path):
            self._print_message(plugin_path, "does not exists.")
            sys.exit(2)
        if len([name for name in listdir(plugin_path) if isfile(join(plugin_path, name))]) == 0:
            self._print_message(plugin_path, "does not contains plugins.")
            sys.exit(2)

        for dirPath, _, fileNames in walk(plugin_path):
            for f in fileNames:
                if isfile(join(dirPath, f)):
                    files.append(abspath(join(dirPath, f)))

        if etcd:
            if 'host' not in stats:
                files.remove('host')
            if 'alba_proxy' not in stats:
                files.remove('alba_proxy')

        return files

    def _read_config_file(self):
        """
        :return: Returns a Dictionary of the config file
        """
        try:
            config = {}
            parser = ConfigParser.ConfigParser()
            parser.read(self.config_file)
            for option in parser.options("statsmonkey"):
                config[option] = parser.get("statsmonkey", option)
            return config
        except ConfigParser.Error, ex:
            print ex.message

    @staticmethod
    def _print_message(*args):
        output = str(datetime.datetime.now())
        for arg in args:
            output += ' '
            output += str(arg)
        print output


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='How to use the statsmonkey')
    parser.add_argument('-C', '--config', type=str, required=False, default='/etc/statsmonkey/statsmonkey.conf',
                        help='config file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    monkey = Statsmonkey(args.config)
    monkey.run_plugins()

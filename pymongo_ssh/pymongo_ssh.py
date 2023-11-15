import getpass
from urllib import parse

import pandas as pd
import pymongo
from sshtunnel import SSHTunnelForwarder


class MongoSession:

    def __init__(self, host=None, user=None, password=None, key=None, uri=None, port=22, to_host='127.0.0.1',
                 to_port=27017, data_map=None,
                 use_ssh=True, db=None):
        if data_map is None:
            data_map = {}
        self.data_map = data_map

        host = (data_map.get("ssh_host"), port) if data_map.get("ssh_host") else (host, port)
        self.user = data_map.get("ssh_username") or user or getpass.getuser()
        self.password = password
        key = data_map.get("ssh_host_key") or key or '/home/{user}/.ssh/id_rsa'.format(user=user)
        self.uri = parse.urlparse(data_map.get("connection_uri")) if data_map.get("connection_uri") else parse.urlparse(
            uri)
        self.to_host = to_host
        self.uri = parse.urlparse(uri)
        self.connection = None
        self.use_ssh = use_ssh
        self.to_port = to_port
        self.db = db

        if uri:
            to_host = self.uri.hostname or to_host
            to_port = self.uri.port or to_port

        if self.use_ssh:
            if password:
                self.server = SSHTunnelForwarder(
                    host,
                    ssh_username=user,
                    ssh_password=password,
                    remote_bind_address=(to_host, to_port)
                )
            else:
                self.server = SSHTunnelForwarder(
                    host,
                    ssh_username=user,
                    ssh_pkey=key,
                    remote_bind_address=(to_host, to_port)
                )

        self.start()

    def start(self):
        if self.use_ssh:
            self.server.start()

            params = dict()

            if self.uri:

                if '@' in self.uri.netloc:
                    user_pass = self.uri.netloc.split('@', 1)[0]
                    if ':' in user_pass:
                        params['username'], params['password'] = user_pass.split(':', 1)
                    else:
                        params['username'] = user_pass

                if self.uri.query:
                    auth_mech = parse.parse_qs(self.uri.query)
                    params.update({key: auth_mech[key][0] for key in auth_mech})

            self.connection = pymongo.MongoClient(
                host=self.to_host,
                port=self.server.local_bind_port,
                **params)
        else:
            uri = "mongodb://{user}:{password}@{host}:{port}/?authSource=docsity&authMechanism=SCRAM-SHA-1".format(
                user=self.user, password=self.password, host=self.to_host,
                port=self.to_port)
            # self.connection = pymongo.MongoClient(host=self.to_host,
            #                                       port=self.to_port,
            #                                       username=self.user,
            #                                       password=self.password,
            #                                       authSource="docsity", authMechanism="SCRAM-SHA-1")
            self.connection = pymongo.MongoClient(uri)

    def pd_aggregate(self, col, pipeline):
        return pd.DataFrame(list(col.aggregate(pipeline)))

    def stop(self):
        if self.use_ssh:
            self.connection.close()
            self.server.stop()
            self.connection = None
            del self.connection
            self.server = None
        else:
            self.connection.close()
            self.connection = None
            del self.connection

    def close(self):
        self.stop()

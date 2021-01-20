import getpass
from urllib import parse

import pymongo
from sshtunnel import SSHTunnelForwarder


class MongoSession:

    def __init__(self, host, user=None, password=None, key=None, uri=None, port=22, to_host='127.0.0.1', to_port=27017):

        host = (host, port)
        user = user or getpass.getuser()
        key = key or '/home/{user}/.ssh/id_rsa'.format(user=user)
        self.to_host = to_host
        self.uri = parse.urlparse(uri)
        self.connection = None

        if uri:
            to_host = self.uri.hostname or to_host
            to_port = self.uri.port or to_port

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

    def stop(self):
        self.connection.close()
        self.server.stop(force=True)
        self.connection = None
        del self.connection
        self.server = None

    def close(self):
        self.stop()

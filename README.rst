ssh-pymongo
-----------
Python utilities to simplify connection with MongoDB through SSH tunnel.
Note: `uri` parameter is assumed as local, after ssh.

Where to get it
---------------
The source code is currently hosted on GitHub at:
https://github.com/pualien/pymongo-ssh

Binary installers for the latest released version are available at the `Python package index <https://pypi.org/project/pymongo-ssh/>`_

``pip install pymongo-ssh``

Example 1
---------

.. code:: python

    from pymongo_ssh import MongoSession

    session = MongoSession('db.example.com')
    db = session.connection['db-name']
    session.stop()
    # session.start()

Example 2
---------

.. code:: python

    session = MongoSession(
        host='db.example.com',
        uri='mongodb://user:password@127.0.0.1/?authSource=admin&authMechanism=SCRAM-SHA-256'
    )
    ...
    session.stop()

Example 3
---------

.. code:: python

    session = MongoSession(
        host='db.example.com',
        user='myuser',
        password='mypassword',
    )
    ...
    session.stop()

Example 4
---------

.. code:: python

    session = MongoSession(
        host='db.example.com',
        port='21',
        user='myuser',
        key='/home/myplace/.ssh/id_rsa2',
        to_port='37017',
        to_host='0.0.0.0'
    )
    ...
    session.stop()


========
py-cfenv
========

.. image:: https://img.shields.io/pypi/v/cfenv.svg
    :target: http://badge.fury.io/py/cfenv
    :alt: Latest version

.. image:: https://img.shields.io/travis/jmcarp/py-cfenv/master.svg
    :target: https://travis-ci.org/jmcarp/py-cfenv
    :alt: Travis-CI

**py-cfenv** is a tiny utility that simplifies interactions with Cloud Foundry environment variables, modeled after node-cfenv_.

Quickstart
----------

.. code-block:: python

    from cfenv import AppEnv

    env = AppEnv()
    env.name  # 'test-app'
    env.port  # 5000

    redis = env.get_service(label='redis')
    redis.credentials  # {'uri': '...', 'password': '...'}
    redis.get_url(host='hostname', password='password', port='port')  # redis://pass:host

Keys may change based on the service. To see what keys are available for the app's services:

.. code-block:: bash

    $ cf env my-app
    
    Getting env variables for app my-app in org my-org / space my-space as me@example.com...
    OK

    System-Provided:
    {
     "VCAP_SERVICES": {
      "redis": [
       {
        "credentials": {
         "hostname": "example.redis.host",
         "password": "verysecurepassword",
         "port": "30773",
         "ports": {
          "6379/tcp": "30773"
         },
         "uri": "redis://:verysecurepassword@example.redis.host:30773"
        },
        "label": "redis",
        "name": "example-redis",
        "plan": "standard",
        "provider": null,
        "syslog_drain_url": null,
        "tags": [
         "redis28",
         "redis"
        ],
        "volume_mounts": []
       }
      ]
     }
    }

.. _node-cfenv: https://github.com/cloudfoundry-community/node-cfenv/

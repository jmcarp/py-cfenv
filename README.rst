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

    redis = env.get_service('redis')
    redis.credentials  # {'url': '...', 'password': '...'}
    redis.get_url(host='hostname', password='password', port='port')  # redis://pass:host

.. _node-cfenv: https://github.com/cloudfoundry-community/node-cfenv/

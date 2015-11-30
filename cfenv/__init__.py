# -*- coding: utf-8 -*-

__version__ = '0.4.0'

import os
import json

import furl

class AppEnv(object):

    def __init__(self):
        self.app = json.loads(os.getenv('VCAP_APPLICATION', '{}'))
        self.services = [
            Service(each)
            for services in json.loads(os.getenv('VCAP_SERVICES', '{}')).values()
            for each in services
        ]

    @property
    def name(self):
        return self.app.get('name')

    @property
    def space(self):
        return self.app.get('space_name')

    @property
    def index(self):
        return os.getenv('CF_INSTANCE_INDEX')

    @property
    def port(self):
        port = (
            os.getenv('PORT') or
            os.getenv('CF_INSTANCE_PORT') or
            os.getenv('VCAP_APP_PORT')
        )
        return int(port) if port else None

    @property
    def bind(self):
        return self.app.get('host', 'localhost')

    @property
    def uris(self):
        return self.app.get('uris')

    def get_service(self, **kwargs):
        return next(
            (
                service for service in self.services
                if match(service.env, kwargs)
            ),
            None,
        )

    def get_credential(self, key, default=None):
        return next(
            (
                value for service in self.services
                for name, value in service.credentials.items()
                if key == name
            ),
            os.getenv(key, default),
        )

    def __repr__(self):
        return '<AppEnv name={name}>'.format(name=self.name)

class Service(object):

    def __init__(self, env):
        self.env = env
        self.credentials = self.env.get('credentials', {})

    @property
    def name(self):
        return self.env.get('name')

    def get_url(self, url='url', **keys):
        parsed = furl.furl(self.credentials.get(url, ''))
        for key, value in keys.items():
            setattr(parsed, key, self.credentials.get(value))
        return parsed.url

    def __repr__(self):
        return '<Service name={name}>'.format(name=self.name)

def match(target, patterns):
    for key, value in patterns.items():
        if target.get(key) != value:
            return False
    return True

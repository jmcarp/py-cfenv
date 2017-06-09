# -*- coding: utf-8 -*-

import os
import re
import json

import furl

__version__ = '0.5.3'

RegexType = type(re.compile(''))

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
        index = os.getenv('CF_INSTANCE_INDEX')
        return int(index) if index else None

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
        return self.app.get('uris', [])

    def get_service(self, **kwargs):
        return next(
            (
                service for service in self.services
                if match_all(service.env, kwargs)
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

def match_all(target, patterns):
    return all(
        match(target.get(key), pattern)
        for key, pattern in patterns.items()
    )

def match(target, pattern):
    if target is None:
        return False
    if isinstance(pattern, RegexType):
        return pattern.search(target)
    return pattern == target

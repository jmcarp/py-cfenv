# -*- coding: utf-8 -*-

import json

import pytest

from cfenv import AppEnv

@pytest.fixture
def application(monkeypatch):
    app = {
        'application_uris': [],
        'name': 'test-app',
        'space_name': 'dev',
        'uris': [],
    }
    monkeypatch.setenv('VCAP_APPLICATION', json.dumps(app))
    return app

@pytest.fixture
def services(monkeypatch):
    services = {
        'test-service': [
            {
                'name': 'test-service',
                'label': 'user-provided',
                'plan': 'free',
                'credentials': {
                    'url': 'https://test-service.com/',
                    'username': 'user',
                    'password': 'pass',
                },
            }
        ],
    }
    monkeypatch.setenv('VCAP_SERVICES', json.dumps(services))
    return services

@pytest.fixture
def env(application, services):
    return AppEnv()

class TestEnv:

    def test_name(self, env):
        assert env.name == 'test-app'

    @pytest.mark.parametrize(['key', 'value'], [
        ('PORT', '3000'),
        ('CF_INSTANCE_PORT', '4000'),
        ('VCAP_APP_PORT', '5000'),
    ])
    def test_port(self, key, value, env, monkeypatch):
        monkeypatch.setenv(key, value)
        assert env.port == int(value)

    def test_get_credential(self, env):
        assert env.get_credential('password') == 'pass'

class TestService:

    def test_name(self, env):
        service = env.get_service(name='test-service')
        assert service.name == 'test-service'

    def test_get_url(self, env):
        service = env.get_service(label='user-provided')
        url = service.get_url(url='url', username='username', password='password')
        assert url == 'https://user:pass@test-service.com/'

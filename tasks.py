# -*- coding: utf-8 -*-

from invoke import task, run

@task
def clean(ctx):
    run('rm -rf dist')
    run('rm -rf build')
    run('rm -rf cfenv.egg-info')

@task
def publish(ctx, test=False):
    """Publish to the cheeseshop."""
    clean(ctx)
    if test:
        run('python setup.py register -r test sdist bdist_wheel', echo=True)
        run('twine upload dist/* -r test', echo=True)
    else:
        run('python setup.py register sdist bdist_wheel', echo=True)
        run('twine upload dist/*', echo=True)

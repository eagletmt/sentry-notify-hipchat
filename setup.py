#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='sentry-notify-hipchat',
    version='0.1.4',
    description='A Sentry notification plugin for HipChat',
    author='Kohei Suzuki',
    author_email='eagletmt@gmail.com',
    url='https://github.com/eagletmt/sentry-notify-hipchat',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'sentry',
        'python-simple-hipchat',
    ],
    entry_points={
        'sentry.apps': [
            'notify_hipchat = sentry_notify_hipchat',
        ],
        'sentry.plugins': [
            'notify_hipchat = sentry_notify_hipchat.plugin:NotifyHipchatPlugin',
        ],
    },
)

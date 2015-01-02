# sentry-plugin-hipchat
[![PyPI version](https://badge.fury.io/py/sentry-notify-hipchat.svg)](http://badge.fury.io/py/sentry-notify-hipchat)

A Sentry notification plugin for HipChat.

[![screenshot](https://gyazo.wanko.cc/2cfd498688719b59917b41dfd7c97bee.png)](https://gyazo.wanko.cc/2cfd498688719b59917b41dfd7c97bee)

## Installation
```sh
pip install sentry-notify-hipchat
```

## Configuration
- token
    - HipChat API v1 token (required)
    - See also https://www.hipchat.com/docs/api/auth
- room
    - Room name or ID (required)
- new only
    - Notify new messages only (default: False)
- ignore muted
    - Don't notify muted events (default: True)
- notify
    - Enable "notify" flag (default: True)
    - See also https://www.hipchat.com/docs/api/method/rooms/message
- endpoint
    - HipChat API endpoint for HipChat Server users
    - https://www.hipchat.com/server

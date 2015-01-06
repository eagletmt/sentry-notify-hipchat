from django import forms
from hipchat import HipChat
from sentry.plugins import Plugin
from sentry.utils.strings import strip
import xml.sax.saxutils as saxutils

import sentry_notify_hipchat


DEFAULT_HIPCHAT_ENDPOINT = 'https://api.hipchat.com/v1/'


class NotifyHipchatForm(forms.Form):
    token = forms.CharField(help_text='HipChat API v1 token')
    room = forms.CharField(help_text='Room name or ID')
    new_only = forms.BooleanField(help_text='Notify new messages only', required=False)
    ignore_muted = forms.BooleanField(help_text="Don't notify muted events", required=False, initial=True)
    notify = forms.BooleanField(help_text='Enable "notify" flag', required=False, initial=True)
    endpoint = forms.CharField(help_text='HipChat API endpoint', required=False)


class NotifyHipchatPlugin(Plugin):
    title = 'HipChat Notification'
    slug = 'notify-hipchat'
    description = 'A notification plugin for HipChat'
    version = sentry_notify_hipchat.VERSION
    author = 'Kohei Suzuki'
    author_url = 'https://github.com/eagletmt'
    conf_key = 'notify-hipchat'
    project_conf_form = NotifyHipchatForm

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        if self.__should_notify(group, event, is_new):
            self.__notify(group, event, is_new)

    def __should_notify(self, group, event, is_new):
        if self.get_option('new_only', group.project) and not is_new:
            return False
        if self.get_option('ignore_muted', group.project) and group.is_muted():
            return False
        return True

    def __notify(self, group, event, is_new):
        project_name = '<strong>{0}</strong>'.format(saxutils.escape(group.project.name))
        times_seen = group.times_seen+1
        if is_new:
            times_seen = 1

        message = '''[{level}] {project} {message}<br>
        {culprit} ({count} times seen)<br>
        [<a href="{link}">View on Sentry</a>]
        '''.format(
            level=saxutils.escape(group.get_level_display().upper()),
            project=project_name,
            message=saxutils.escape(event.error()),
            culprit=saxutils.escape(strip(group.culprit)),
            link=saxutils.escape(group.get_absolute_url()),
            count=times_seen,
        )

        token = self.get_option('token', group.project)
        room = self.get_option('room', group.project)
        endpoint = self.get_option('endpoint', group.project) or DEFAULT_HIPCHAT_ENDPOINT
        notify = self.get_option('notify', group.project)

        hipchat = HipChat(token, endpoint)
        hipchat.message_room(room, 'Sentry', message, 'html', 'red', notify)

from django import forms
from hipchat import HipChat
from sentry.plugins.bases.notify import NotificationPlugin
from sentry.utils.strings import strip
import xml.sax.saxutils as saxutils

import sentry_notify_hipchat


DEFAULT_HIPCHAT_ENDPOINT = 'https://api.hipchat.com/v1/'


class NotifyHipchatForm(forms.Form):
    token = forms.CharField(help_text='HipChat API v1 token')
    room = forms.CharField(help_text='Room name or ID')
    notify = forms.BooleanField(help_text='Enable "notify" flag', required=False, initial=True)
    endpoint = forms.CharField(help_text='HipChat API endpoint', required=False)


class NotifyHipchatPlugin(NotificationPlugin):
    title = 'HipChat Notification'
    slug = 'notify-hipchat'
    description = 'A notification plugin for HipChat'
    version = sentry_notify_hipchat.VERSION
    author = 'Kohei Suzuki'
    author_url = 'https://github.com/eagletmt'
    conf_key = 'notify-hipchat'
    project_conf_form = NotifyHipchatForm

    def notify_users(self, group, event, fail_silently=False):
        project_name = '<strong>{0}</strong>'.format(saxutils.escape(group.project.name))
        times_seen = group.times_seen

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

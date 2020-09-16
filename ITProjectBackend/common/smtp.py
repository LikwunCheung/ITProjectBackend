# -*- coding: utf-8 -*-

import logging
import socks
import threading

from queue import Queue
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header

from ITProjectBackend.common.utils import mills_timestamp
from ITProjectBackend.common.choices import UserStatus, Status
from ITProjectBackend.common.config import *
from ITProjectBackend.account.models import RegisterRecord, User

logger = logging.getLogger('django')
connector = None
connected = False


def init_smtp():
    global connected, connector

    try:
        try:
            logger.info(u'[SMTP] Connecting Google SMTP Service: ' + GMAIL_ADDRESS + ':' + str(GMAIL_PORT))
            connector = SMTP(host=GMAIL_ADDRESS, port=GMAIL_PORT, timeout=10)
            connector.ehlo()
            connector.starttls()
            connector.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
        except Exception as e:
            logger.error('[SMTP] Connect Fail: ', e)
            return
        connector.set_debuglevel(1)
        connected = True
        logger.info(u'[SMTP] Connecting Google SMTP Service Success!')
    except Exception as e:
        logger.error('[SMTP] Connect Fail: ', e)


def send_email(sender, address, content):
    global connected, connector

    if not connected or not isinstance(connector, SMTP):
        return False

    try:
        logger.info(u'[SMTP] Sending Email: %s %s %s' % (sender, address, content))

        message = MIMEText(content, PLAIN, UTF8)
        message[FROM] = Header(sender, UTF8)
        message[SENDER] = Header(sender, UTF8)
        message[TO] = Header(address, UTF8)
        message[SUBJECT] = Header(INVITATION_TITLE, UTF8)

        connector.sendmail(GMAIL_ACCOUNT, address, message.as_string())
        return True
    except Exception as e:
        logger.info('SMTP Disconnected: ', e)
        init_smtp()
        return False


class SendEmailPool(threading.Thread):

    def __init__(self, size=128):
        self.count = 0
        self.size = size
        self.pool = Queue(self.size)
        threading.Thread.__init__(self)

    def put_task(self, id, coordinator, address, content):
        logger.info(u'[SMTP] Receive: %d %s %s' % (id, address, content))

        self.pool.put(dict(
            id=id,
            coordinator=coordinator,
            email=address,
            text=content,
        ))

    def consume(self):
        task = self.pool.get(block=True, timeout=None)

        logger.info(u'[SMTP] Send Email: %d %s' % (self.count, str(task)))
        invite = Invitation.objects.get(invitation_id=task['id'], status=InvitationStatus.waiting.value.key)
        user = User.objects.get(user_id=task['id'])

        if invite is None or invite.expired <= mills_timestamp():
            return

        if send_email(task['coordinator'], task['email'], task['text']):
            invite.status = InvitationStatus.sent.value.key
            invite.send_date = mills_timestamp()
            invite.save()
        else:
            self.pool.put(task)

    def run(self):
        while True:
            self.count += 1
            self.consume()

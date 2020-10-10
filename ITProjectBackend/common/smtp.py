# -*- coding: utf-8 -*-

import logging
import threading

from queue import Queue
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header

from django.db.models import ObjectDoesNotExist
from django.db.transaction import atomic

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
            connector = SMTP(host=GMAIL_ADDRESS, port=GMAIL_PORT, timeout=3)
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


def send_email(address, content):
    global connected, connector

    if not connected or not isinstance(connector, SMTP):
        return False

    try:
        logger.info(u'[SMTP] Sending Email: %s %s' % (address, content))

        message = MIMEText(content, PLAIN, UTF8)
        message[FROM] = Header(INVITATION_SENDER, UTF8)
        message[SENDER] = Header(INVITATION_SENDER, UTF8)
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

    def put_task(self, user_id, record_id, address, content):
        logger.info(u'[SMTP] Receive: %d %d %s %s' % (user_id, record_id, address, content))

        self.pool.put(dict(
            user_id=user_id,
            record_id=record_id,
            email=address,
            text=content,
        ))

    def consume(self):
        task = self.pool.get(block=True, timeout=None)

        logger.info(u'[SMTP] Send Email: %d %s' % (self.count, str(task)))
        try:
            record = RegisterRecord.objects.get(record_id=task['record_id'], status=Status.valid.key)
            user = User.objects.get(user_id=task['user_id'], status__lt=UserStatus.valid.key)
        except ObjectDoesNotExist as e:
            logger.info('[SMTP] %s' % e)
            return

        if record.expired <= mills_timestamp():
            timestamp = mills_timestamp()
            with atomic():
                user.status = UserStatus.expired.key
                user.update_date = timestamp
                record.status = Status.invalid.key
                record.status = timestamp
                user.save()
                record.save()

        if send_email(task['email'], task['text']):
            user.status = UserStatus.wait_accept.key
            user.update_date = mills_timestamp()
            user.save()
        else:
            self.pool.put(task)

    def run(self):
        while True:
            self.count += 1
            self.consume()

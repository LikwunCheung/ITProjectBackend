# -*- coding: utf-8 -*-

from .smtp import init_smtp, SendEmailPool


init_smtp()
smtp_thread = SendEmailPool(0)
smtp_thread.start()
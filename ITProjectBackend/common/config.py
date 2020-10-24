# -*- coding: utf-8 -*-

SESSION_REFRESH = 30 * 60
SINGLE_PAGE_LIMIT = 20

SALT = 'Zsl2&(91bsd%^sa1LD'

UTF8 = 'utf-8'
PLAIN = 'plain'
FROM = 'From'
TO = 'To'
SENDER = 'Sender'
SUBJECT = 'Subject'

HOMEPAGE = 'http://8.210.28.169:8885'
REGISTER_PAGE = '/validate'
FORGET_PAGE = '/forget/validate'
INVITATION_KEY = 'code'

PATTERN_FULLNAME = '<FULLNAME>'
PATTERN_URL = '<URL>'

GMAIL_ADDRESS = 'smtp.gmail.com'
GMAIL_PORT = 587
GMAIL_ACCOUNT = 'swen90013.2020.sp@gmail.com'
GMAIL_PASSWORD = 'fvwdissshcpobsdl'

INVITATION_TEMPLATE = 'Dear <FULLNAME>,\n\n' \
                      'Welcome to join ePortfolio platform!\n' \
                      'Please click the following verification link to accept invitation within 15 minutes!\n' \
                      '<URL>\n\n' \
                      'Regards,\n' \
                      'ePortfolio Support Team\n'
INVITATION_SENDER = 'ePortfolio'
INVITATION_TITLE = '[ePortfolio] Verify Your Email Address'
INVITATION_EXPIRED = 1000 * 60 * 15

FORGET_TEMPLATE = 'Dear <FULLNAME>,\n\n' \
                      'You are trying to reset your password!\n' \
                      'Please click the following verification link to reset you password in 5 minutes!\n' \
                      '<URL>\n\n' \
                      'Regards,\n' \
                      'ePortfolio Support Team\n'
FORGET_TITLE = '[ePortfolio] Reset Your Password'
FORGET_EXPIRED = 1000 * 60 * 5

DEFAULT_AVATAR = ''
DEFAULT_THEME = ''


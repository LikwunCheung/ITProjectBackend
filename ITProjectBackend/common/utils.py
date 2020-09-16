# -*- coding: utf-8 -*-

import logging
import json
import ujson
import time
import re

from django.http.response import HttpResponse

from ITProjectBackend.common.choices import MyEnum, RespCode
from ITProjectBackend.common.config import SESSION_REFRESH, HOMEPAGE, REGISTER_PAGE, INVITATION_KEY, SALT

logger = logging.getLogger('django')


def make_json_response(func=HttpResponse, resp=None):
    return func(ujson.dumps(resp), content_type='application/json')


def make_redirect_response(func=HttpResponse, resp=None):
    return func(ujson.dumps(resp), content_type='application/json', status=302)


def init_http_response(code, message):
    return dict(
        code=code,
        message=message,
        data=dict(),
    )


def init_http_response_my_enum(resp: MyEnum):
    return init_http_response(resp.key, resp.msg)


def check_body(func):
    """

    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):

        try:
            body = dict(ujson.loads(request.body))
            logger.info(body)
        except ValueError or json.JSONDecodeError as e:
            logger.info(request.body)
            resp = init_http_response_my_enum(RespCode.incorrect_body)
            return make_json_response(HttpResponse, resp)

        return func(request, body, *args, **kwargs)
    return wrapper


def check_user_login():
    """
    Disable for testing
    :param roles:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        user = request.session.get('user', {})
        if not user or 'id' not in user or 'is_login' not in user:
            resp = init_http_response_my_enum(RespCode.need_login)
            return make_json_response(HttpResponse, resp)

        request.session.set_expiry(SESSION_REFRESH)
        return func(request, *args, **kwargs)
    return wrapper


def body_extract(body: dict, obj: object):
    """
    Extract parameters from the request body
    :param body:
    :param obj:
    :return:
    """
    for i in obj.__dict__.keys():
        if i in body:
            obj.__setattr__(i, body.get(i))


def mills_timestamp():
    return int(time.time() * 1000)


def email_validate(email):
    return re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email)


def get_invitation_link(key):
    return HOMEPAGE + REGISTER_PAGE + '?' + INVITATION_KEY + '=' + key

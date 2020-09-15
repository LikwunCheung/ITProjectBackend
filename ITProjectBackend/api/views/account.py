# -*- coding: utf-8 -*-

import logging

from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import ObjectDoesNotExist
from django.db import transaction

from ITProjectBackend.common.utils import check_user_login, check_body, body_extract, mills_timestamp, init_http_response, make_json_response
from ITProjectBackend.common.choices import RespCode, UserStatus
from ITProjectBackend.api.dto.dto import LoginDTO
from ITProjectBackend.account.models import User, RegisterRecord


@require_http_methods(['POST'])
@check_body
def login(request, body, *args, **kwargs):
    """
    Login

    :param request:
    :param body:
    :param args:
    :param kwargs:
    :return:
    """

    login_dto = LoginDTO()
    body_extract(body, login_dto)

    if login_dto.is_empty:
        resp = init_http_response(RespCode.invalid_parameter.key, RespCode.invalid_parameter.msg)
        return make_json_response(HttpResponse, resp)

    try:
        user = User.objects.get(email=login_dto.email, password=login_dto.password_md5, status=UserStatus.valid.key)
    except ObjectDoesNotExist as e:
        resp = init_http_response(RespCode.login_fail.key, RespCode.login_fail.msg)
        return make_json_response(HttpResponse, resp)

    session_data = dict(
        id=user.user_id,
        name=user.full_name,
        is_login=True,
    )
    request.session['user'] = session_data

    data = dict(
        user_id=user.user_id,
        name=user.full_name,
        theme=user.theme,
        avatar=user.avatar_url,
    )
    resp = init_http_response(RespCode.success.value.key, RespCode.success.value.msg)
    resp['data'] = data
    return make_json_response(HttpResponse, resp)


@require_http_methods(['POST'])
@check_body
def register(request, body, *args, **kwargs):
    """
    Register

    :param request:
    :param body:
    :param args:
    :param kwargs:
    :return:
    """

    register_dto = None
# -*- coding: utf-8 -*-

import logging
import random
import string

from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import ObjectDoesNotExist
from django.db import transaction

from ITProjectBackend.common.utils import check_user_login, check_body, body_extract, mills_timestamp, \
    init_http_response_my_enum, make_json_response
from ITProjectBackend.common.choices import RespCode, UserStatus, Delete, Status
from ITProjectBackend.api.dto.dto import LoginDTO, RegisterDTO
from ITProjectBackend.account.models import User, RegisterRecord
from ITProjectBackend.common.config import DEFAULT_AVATAR, DEFAULT_THEME, INVITATION_EXPIRED

logger = logging.getLogger('django')


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
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(HttpResponse, resp)

    try:
        user = User.objects.get(email=login_dto.email, password=login_dto.password_md5, status=UserStatus.valid.key)
    except ObjectDoesNotExist as e:
        resp = init_http_response_my_enum(RespCode.login_fail)
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
    resp = init_http_response_my_enum(RespCode.success)
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

    register_dto = RegisterDTO()
    body_extract(body, register_dto)
    timestamp = mills_timestamp()

    if register_dto.is_empty:
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(HttpResponse, resp)

    """
    Check if the user register record expired, and if the user already existed
    """
    existed_user = User.objects.filter(email=register_dto.email, status__lte=UserStatus.valid.key).first()
    if existed_user is not None:
        if existed_user.status == UserStatus.valid.key:
            resp = init_http_response_my_enum(RespCode.account_existed)
            return make_json_response(HttpResponse, resp)
        existed_record = RegisterRecord.objects.filter(user_id=existed_user.user_id, status=Status.valid.key).first()
        if existed_record is not None and existed_record.expired <= timestamp:
            logger.info('Registration Expired: %s' % existed_user)
            with transaction.atomic():
                existed_record.status = Status.invalid.key
                existed_user.status = UserStatus.expired.key
                existed_record.save()
                existed_user.save()

    expired = timestamp + INVITATION_EXPIRED  # 1min
    code = ''.join([''.join(random.sample(string.ascii_letters + string.digits, 8)) for i in range(4)])

    try:
        with transaction.atomic():
            user = User(email=register_dto.email, password=register_dto.password_md5, avatar_url=DEFAULT_AVATAR,
                        first_name=register_dto.first_name, last_name=register_dto.last_name, theme=DEFAULT_THEME,
                        status=UserStatus.created.key, is_delete=Delete.non_delete.key, create_date=timestamp,
                        update_date=timestamp)
            user.save()

            record = RegisterRecord(user_id=user.user_id, code=code, expired=expired, status=Status.valid.key,
                                    is_delete=Delete.non_delete, create_date=timestamp, update_date=timestamp)
            record.save()

    except Exception as e:
        logger.error(e)
        resp = init_http_response_my_enum(RespCode.server_error)
        return make_json_response(HttpResponse, resp)

    resp = init_http_response_my_enum(RespCode.success)
    return make_json_response(HttpResponse, resp)

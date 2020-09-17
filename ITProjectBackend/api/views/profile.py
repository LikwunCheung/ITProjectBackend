# -*- coding: utf-8 -*-

import logging

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import ObjectDoesNotExist

from ITProjectBackend.common.utils import check_user_login, check_body, body_extract, mills_timestamp, \
    init_http_response_my_enum, make_json_response, get_invitation_link
from ITProjectBackend.common.choices import RespCode, UserStatus
from ITProjectBackend.account.models import User
from ITProjectBackend.api.dto.dto import UpdateProfileDTO

logger = logging.getLogger('django')


@require_http_methods(['POST', 'GET'])
@check_user_login
def profile_router(request, *args, **kwargs):
    if request.method == 'POST':
        return update_profile(request, *args, **kwargs)
    elif request.method == 'GET':
        return get_profile(request, *args, **kwargs)


def get_profile(request, *args, **kwargs):

    user_id = request.session.get('user').get('id')

    try:
        user = User.objects.get(user_id=user_id, status=UserStatus.valid.key)
    except ObjectDoesNotExist as e:
        logger.info("Get Profile: %s" % e)
        resp = init_http_response_my_enum(RespCode.server_error)
        return make_json_response(HttpResponse, resp)

    resp = init_http_response_my_enum(RespCode.success)
    resp['data'] = dict(
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=user.avatar_url,
        theme=user.theme,
    )
    return make_json_response(HttpResponse, resp)


@check_body
def update_profile(request, body, *args, **kwargs):

    update_profile_dto = UpdateProfileDTO()
    body_extract(body, update_profile_dto)
    timestamp = mills_timestamp()

    user_id = request.session.get('user').get('id')

    try:
        user = User.objects.get(user_id=user_id, status=UserStatus.valid.key)
    except ObjectDoesNotExist as e:
        logger.info("Update Profile: %s" % e)
        resp = init_http_response_my_enum(RespCode.server_error)
        return make_json_response(HttpResponse, resp)

    if update_profile_dto.first_name:
        user.first_name = update_profile_dto.first_name
    if update_profile_dto.last_name:
        user.last_name = update_profile_dto.last_name
    if update_profile_dto.avatar:
        user.avatar_url = update_profile_dto.avatar
    if update_profile_dto.theme:
        user.last_name = update_profile_dto.theme
    if update_profile_dto.password:
        user.password = update_profile_dto.password_md5
    user.update_date = timestamp
    user.save()

    resp = init_http_response_my_enum(RespCode.success)
    return make_json_response(HttpResponse, resp)





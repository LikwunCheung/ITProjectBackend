# -*- coding: utf-8 -*-

import logging

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import ObjectDoesNotExist

from ITProjectBackend.common.utils import check_user_login, check_body, body_extract, mills_timestamp, \
    init_http_response_my_enum, make_json_response, get_invitation_link
from ITProjectBackend.common.choices import RespCode, UserStatus, Status
from ITProjectBackend.tab.models import TabPage
from ITProjectBackend.api.dto.dto import TabDTO

logger = logging.getLogger('django')


@require_http_methods(['POST', 'GET'])
@check_user_login
def tab_router(request, *args, **kwargs):
    tab_id = None
    if isinstance(kwargs, dict):
        tab_id = kwargs.get('id', None)
    if request.method == 'GET':
        if not tab_id:
            return multi_get_tab(request, *args, **kwargs)
        return get_tab(request, tab_id, *args, **kwargs)
    elif request.method == 'POST':
        if not tab_id:
            return add_tab(request, *args, **kwargs)
        return update_tab(request, tab_id, *args, **kwargs)


def multi_get_tab(request, *args, **kwargs):

    user_id = request.session.get('user').get('id')

    tabs = TabPage.objects.filter(user_id=user_id, status=Status.valid.key).order_by('create_date')
    tabs = [dict(
        tab_id=t.tab_id,
        title=t.title,
    ) for t in tabs]

    resp = init_http_response_my_enum(RespCode.success)
    resp['data'] = dict(
        tabs=tabs,
    )
    return make_json_response(HttpResponse, resp)


def get_tab(request, tab_id, *args, **kwargs):

    user_id = request.session.get('user').get('id')

    try:
        tab = TabPage.objects.get(user_id=user_id, tab_id=tab_id, status=Status.valid.key)
    except ObjectDoesNotExist as e:
        logger.info('Get Tab: %s' % e)
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(HttpResponse, resp)

    resp = init_http_response_my_enum(RespCode.success)
    resp['data'] = dict(
        title=tab.title,
        content=tab.content,
        update_time=tab.update_date,
    )
    return make_json_response(HttpResponse, resp)


@check_body
def add_tab(request, body, *args, **kwargs):

    user_id = request.session.get('user').get('id')
    timestamp = mills_timestamp()

    tab_dto = TabDTO()
    body_extract(body, tab_dto)

    if tab_dto.is_empty:
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(HttpResponse, resp)

    tab = TabPage(user_id=user_id, title=tab_dto.title, content=tab_dto.content, status=Status.valid.key,
                  create_date=timestamp, update_date=timestamp)
    tab.save()

    resp = init_http_response_my_enum(RespCode.success)
    resp['data'] = dict(
        tab_id=tab.tab_id,
        title=tab.title,
    )
    return make_json_response(HttpResponse, resp)


@check_body
def update_tab(request, body, *args, **kwargs):

    tab_id = kwargs.get('id')
    user_id = request.session.get('user').get('id')

    tab_dto = TabDTO()
    body_extract(body, tab_dto)

    try:
        tab = TabPage.objects.get(tab_id=tab_id, user_id=user_id, status=Status.valid.key)

        if tab_dto.title:
            tab.title = tab_dto.title
        if tab_dto.content:
            tab.content = tab_dto.content
        tab.update_date = mills_timestamp()
        tab.save()
    except ObjectDoesNotExist as e:
        logger.info('Update Tab: %s' % e)
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(HttpResponse, resp)

    resp = init_http_response_my_enum(RespCode.success)
    return make_json_response(HttpResponse, resp)


@require_http_methods(['POST'])
@check_user_login
def delete_tab(request, *args, **kwargs):
    tab_id = kwargs.get('id', None)
    user_id = request.session.get('user').get('id')

    if not tab_id:
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(HttpResponse, resp)

    try:
        tab = TabPage.objects.get(tab_id=tab_id, user_id=user_id, status=Status.valid.key)

        tab.status = Status.invalid.key
        tab.update_date = mills_timestamp()
        tab.save()
    except ObjectDoesNotExist as e:
        logger.info('Delete Tab: %s' % e)
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(HttpResponse, resp)

    resp = init_http_response_my_enum(RespCode.success)
    return make_json_response(HttpResponse, resp)

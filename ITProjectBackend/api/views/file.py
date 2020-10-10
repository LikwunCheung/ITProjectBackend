# -*- coding: utf-8 -*-

import logging
import os

from django.conf import settings
from django.http import HttpResponseBadRequest, StreamingHttpResponse
from django.views.decorators.http import require_http_methods

from ITProjectBackend.common.utils import check_user_login, make_json_response, init_http_response_my_enum, \
    get_validate_code, file_iterator
from ITProjectBackend.common.choices import RespCode

logger = logging.getLogger('django')
file_path = settings.FILE_PATH


@require_http_methods(['POST', 'GET'])
@check_user_login
def file_router(request, *args, **kwargs):
    file_id = None
    if isinstance(kwargs, dict):
        file_id = kwargs.get('id', None)
    if request.method == 'GET' and file_id:
        return download_file(request, file_id, *args, **kwargs)
    elif request.method == 'POST':
        if file_id:
            return update_file(request, file_id, *args, **kwargs)
        else:
            return upload_file(request, *args, **kwargs)
    return make_json_response(HttpResponseBadRequest, None)


def download_file(request, file_name, *args, **kwargs):

    if not file_name:
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(resp=resp)
    if not os.path.exists(file_path + '/' + file_name + '.jpg'):
        resp = init_http_response_my_enum(RespCode.invalid_file)
        return make_json_response(resp=resp)

    resp = StreamingHttpResponse(file_iterator(os.path.join(file_path, file_name + '.jpg')), content_type='image/jpeg')
    resp['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name + '.jpg')
    return resp


def update_file(request, file_name, *args, **kwargs):

    picture = request.FILES.get('picture', None)
    if not picture or not file_name:
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(resp=resp)

    with open(os.path.join(file_path, file_name + '.jpg'), 'wb+') as f:
        for chunk in picture.chunks():
            f.write(chunk)

    data = dict(
        file_id=file_name,
    )
    resp = init_http_response_my_enum(RespCode.success, data)
    return make_json_response(resp=resp)


def upload_file(request, *args, **kwargs):

    picture = request.FILES.get('picture', None)
    if not picture:
        resp = init_http_response_my_enum(RespCode.invalid_parameter)
        return make_json_response(resp=resp)

    file_name = get_validate_code(3)
    logger.info('[FILE] Writing File ' + file_path + '/' + file_name + '.jpg')

    # while os.path.exists(file_path + '/' + file_name + '.jpg'):
    #     file_name = get_validate_code(3)

    with open(os.path.join(file_path, file_name + '.jpg'), 'wb+') as f:
        for chunk in picture.chunks():
            f.write(chunk)

    data = dict(
        file_id=file_name,
    )
    resp = init_http_response_my_enum(RespCode.success, data)
    return make_json_response(resp=resp)

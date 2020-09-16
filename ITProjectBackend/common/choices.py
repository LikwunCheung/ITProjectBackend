# -*- coding: utf-8 -*-

from enum import Enum


class Choice(object):
    key = None
    msg = None

    def __init__(self, key: int, msg: str):
        self.key = key
        self.msg = msg


class MyEnum(Enum):

    @property
    def key(self):
        return self.value.key

    @property
    def msg(self):
        return self.value.msg


class RespCode(MyEnum):
    success = Choice(0, 'success')
    server_error = Choice(-1, 'server error')
    invalid_parameter = Choice(-2, 'invalid parameter')
    login_fail = Choice(-3, 'login fail')
    need_login = Choice(-4, 'need login')
    account_existed = Choice(-5, 'existed account')
    invalid_operation = Choice(-6, 'invalid operation')
    permission_deny = Choice(-7, 'permission deny')
    incorrect_body = Choice(-8, 'incorrect body')


class UserStatus(MyEnum):
    created = Choice(1, 'created')
    wait_accept = Choice(2, 'wait accept')
    valid = Choice(3, 'valid')
    expired = Choice(4, 'expired')
    invalid = Choice(5, 'invalid')


class Status(MyEnum):
    invalid = Choice(0, 'invalid')
    valid = Choice(1, 'valid')


class Delete(MyEnum):
    non_delete = Choice(0, 'non delete')
    deleted = Choice(1, 'deleted')



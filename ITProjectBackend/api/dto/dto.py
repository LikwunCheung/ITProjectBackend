# -*- coding: utf-8 -*-

import hashlib

from ITProjectBackend.common.config import SALT
from ITProjectBackend.common.utils import email_validate


class LoginDTO(object):

    def __init__(self):
        self.email = None
        self.password = None

    @property
    def password_md5(self):
        return hashlib.sha3_256((self.password + SALT).encode()).hexdigest()

    @property
    def is_empty(self):
        return not self.email or not self.password

    @property
    def invalid_email(self):
        return not email_validate(self.email)


class RegisterDTO(object):

    def __init__(self):
        self.email = None
        self.password = None
        self.first_name = None
        self.last_name = None

    @property
    def password_md5(self):
        return hashlib.sha3_256((self.password + SALT).encode()).hexdigest()

    @property
    def is_empty(self):
        return not self.email or not self.password or not self.first_name or not self.last_name

    @property
    def invalid_email(self):
        return not email_validate(self.email)


class UpdateProfileDTO(object):

    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.avatar = None
        self.theme = None
        self.password = None

    @property
    def password_md5(self):
        return hashlib.sha3_256((self.password + SALT).encode()).hexdigest()


class TabDTO(object):

    def __init__(self):
        self.title = None
        self.content = None

    @property
    def is_empty(self):
        return not self.title or not self.content


class ResetPasswordDTO(object):

    def __init__(self):
        self.code = None
        self.password = None

    @property
    def is_empty(self):
        return not self.code or not self.password

    @property
    def password_md5(self):
        return hashlib.sha3_256((self.password + SALT).encode()).hexdigest()


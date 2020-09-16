# -*- coding: utf-8 -*-

import hashlib

from ITProjectBackend.common.config import SALT


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

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
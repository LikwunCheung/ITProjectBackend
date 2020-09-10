# -*- coding: utf-8 -*-
from django.db import models


class Account(models.Model):

    account_id = models.AutoField(db_column='id', primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)

    deleted = models.IntegerField(blank=False, null=False)
    create_date = models.BigIntegerField(blank=False, null=False)
    create_by = models.IntegerField(blank=True, null=True)
    update_date = models.BigIntegerField(blank=False, null=False)
    update_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'account'


class Profile(models.Model):

    profile_id = models.AutoField(db_column='id', primary_key=True)
    account_id = models.IntegerField(blank=False, null=False, db_index=True)
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=False, null=False)
    email = models.CharField(max_length=128, null=False)
    role = models.IntegerField(blank=False, null=False)

    deleted = models.IntegerField(blank=False, null=False)
    create_date = models.BigIntegerField(blank=False, null=False)
    create_by = models.IntegerField(blank=True, null=True)
    update_date = models.BigIntegerField(blank=False, null=False)
    update_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'profile'

    def get_name(self):
        return self.first_name + ' ' + self.last_name
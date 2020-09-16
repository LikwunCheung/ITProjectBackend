# -*- coding: utf-8 -*-
from django.db import models


class TabPage(models.Model):

    tab_id = models.AutoField(db_column='id', primary_key=True)
    user_id = models.IntegerField(blank=False, null=False)
    title = models.CharField(max_length=256, blank=False, null=False)
    content = models.TextField(max_length=65535)
    status = models.IntegerField(blank=False, null=False)
    create_date = models.BigIntegerField(blank=False, null=False)
    update_date = models.BigIntegerField(blank=False, null=False)

    class Meta:
        db_table = 'tab_page'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from app.models import Dashboard, Survey
from app.models import Activity, File

admin.site.register(Dashboard)
admin.site.register(File)
admin.site.register(Activity)
admin.site.register(Survey)

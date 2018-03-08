# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django import forms

import re

from .models import ServiceUserAsk

class ServiceUserAskForm(forms.ModelForm):

    class Meta:
        model = ServiceUserAsk
        fields = ['name', 'mobile', 'detail', 'question_type']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}&'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号非法', code='invalid')
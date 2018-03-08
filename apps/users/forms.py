# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django import forms

import re
from captcha.fields import CaptchaField


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=20)


class UserRegisterForm(forms.Form):

    captcha = CaptchaField()
    password = forms.CharField( required=True, min_length=8, max_length=20)
    email = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        REGEX_EMAIL = '^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$'
        P = re.compile(REGEX_EMAIL)
        if P.match(email):
            return email
        else:
            raise forms.ValidationError(u'邮箱格式错误', code='invalid')


class UserForgetPwdForm(forms.Form):

    captcha = CaptchaField()
    email = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        REGEX_EMAIL = '^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$'
        P = re.compile(REGEX_EMAIL)
        if P.match(email):
            return email
        else:
            raise forms.ValidationError(u'邮箱格式错误', code='invalid')


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=8, max_length=20)
    password2 = forms.CharField(required=True, min_length=8, max_length=20)


class UserAddressForm(forms.Form):
    consignee = forms.CharField(required=True, min_length=2, max_length=20)
    mobile = forms.CharField(required=True, max_length=11)
    province = forms.CharField(required=True)
    city = forms.CharField(required=True)
    town = forms.CharField(required=True)
    address = forms.CharField(required=True, min_length=10, max_length=150)


    def clean_consignee(self):
        consignee = self.cleaned_data['consignee']
        REGEX_MOBILE = '(?=[\x21-\x7e]+)[^A-Za-z0-9]'
        p = re.compile(REGEX_MOBILE)
        if p.match(consignee):
            raise forms.ValidationError(u'寄件人姓名包含特殊字符', code='invalid')
        else:
            return consignee

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}&'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号非法', code='invalid')


class UserInfoForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11)
    province = forms.CharField(required=True)
    city = forms.CharField(required=True)
    town = forms.CharField(required=True)

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}&'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号非法', code='invalid')

    def clean_province(self):
        province = self.cleaned_data['province']
        if province == 'null':
            raise forms.ValidationError(u'省份为空', code='invalid')
        else:
            return province

    def clean_city(self):
        city = self.cleaned_data['city']
        if city == 'null':
            raise forms.ValidationError(u'城市为空', code='invalid')
        else:
            return city

    def clean_town(self):
        town = self.cleaned_data['town']
        if town == 'null':
            raise forms.ValidationError(u'区县为空', code='invalid')
        else:
            return town






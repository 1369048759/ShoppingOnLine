# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django import forms

import  re

class InvoiceForPersonForm(forms.Form):
    inv_payee = forms.CharField(required=True, min_length=2, max_length=550)
    inv_phone = forms.CharField(required=True, max_length=11)
    inv_email = forms.CharField(required=True, max_length=50)
    inv_taxno = forms.CharField(required=False, max_length=18)

    def clean_inv_phone(self):
        inv_phone = self.cleaned_data['inv_phone']
        REGEX_inv_phone = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}&'
        p = re.compile(REGEX_inv_phone)
        if p.match(inv_phone):
            return inv_phone
        else:
            raise forms.ValidationError(u'手机号非法', code='invalid')

    def clean_inv_email(self):
        inv_email = self.cleaned_data['inv_email']
        REGEX_inv_email = '^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$'
        p = re.compile(REGEX_inv_email)
        if p.match(inv_email):
            return inv_email
        else:
            raise forms.ValidationError(u'邮箱格式错误', code='invalid')


class InvoiceForOrgForm(forms.Form):
    inv_payee = forms.CharField(required=True, min_length=2, max_length=50)
    inv_phone = forms.CharField(required=True, max_length=11)
    inv_email = forms.CharField(required=True, max_length=50)
    inv_taxno = forms.CharField(required=True, max_length=18)
    inv_email = forms.CharField(required=True, max_length=50)

    def clean_inv_phone(self):
        inv_phone = self.cleaned_data['inv_phone']
        REGEX_inv_phone = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}&'
        p = re.compile(REGEX_inv_phone)
        if p.match(inv_phone):
            return inv_phone
        else:
            raise forms.ValidationError(u'手机号非法', code='invalid')

    def clean_inv_email(self):
        inv_email = self.cleaned_data['inv_email']
        REGEX_inv_email = '^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$'
        p = re.compile(REGEX_inv_email)
        if p.match(inv_email):
            return inv_email
        else:
            raise forms.ValidationError(u'邮箱格式错误', code='invalid')

    def clean_inv_taxno(self):
        inv_taxno = self.cleaned_data['inv_taxno']
        REGEX_ID = '^(\d{15}$|^\d{18}$|^\d{17}(\d|X|x))$'
        p = re.compile(REGEX_ID)
        if p.match(inv_taxno):
            return inv_taxno
        else:
            raise forms.ValidationError(u'身份证非法', code='invalid')
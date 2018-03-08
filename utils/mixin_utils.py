# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
	@method_decorator(login_required(login_url='/users/login/'))
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin,self).dispatch(request, *args, **kwargs)
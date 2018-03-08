from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

from random import Random
import  json, time, datetime

from shopping.settings import EMAIL_FROM
from utils.mixin_utils import LoginRequiredMixin
from carts.models import CartsOrder
from mobiles.models import Mobile
from parts.models import Parts
from .models import UserProfile, EmailVerifyRecord, UserAddress
from .forms import UserLoginForm, UserRegisterForm, UserForgetPwdForm, ModifyPwdForm
from .forms import UserAddressForm, UserInfoForm
# Create your views here.


def random_str(randomlength = 16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwSsYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_email(email, send_type):
    if send_type == 'register':
        code = random_str(16)
    if send_type == 'forget':
        code = random_str(32)
    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '金立手机账号激活链接'
        email_body = '请点击下面的链接激活你的账号:http://192.168.255.133:8000/users/active/{0}'.format(code)
    if send_type == 'forget':
        email_title = '金立手机密码修改链接'
        email_body = '请点击下面的链接激活你的账号:http://192.168.255.133:8000/users/modify/{0}'.format(code)
    status = 0
    try:
        status = send_mail(email_title, email_body , EMAIL_FROM, [email])
    except Exception as e:
        None
    if status:
        email_record.save()
    return status

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserLoginView(View):
    def get(self, request):
        return render(request, 'login.html', {

        })

    def post(self, request):
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('{"status" : "success"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail", "msg":"用户未激活"}', content_type='application/json')
            else:
                return HttpResponse('{"status" : "fail", "msg":"用户名或密码错误"}', content_type='application/json')
        else:
            login_form_errors = json.loads(json.dumps(login_form.errors))
            if 'username' in login_form_errors.keys():
                return HttpResponse('{"username":"请输入用户名"}', content_type='application/json')
            if 'password' in login_form_errors.keys():
                return HttpResponse('{"password":"密码至少8位，最多20位"}', content_type='application/json')


class UserRegisterView(View):
    def get(self, request):
        register_form = UserRegisterForm()
        return render(request, 'register.html', {
            'register_form' : register_form
        })

    def post(self, request):
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=email):
                return HttpResponse('{"user":"该邮箱已被注册"}', content_type='application/json')
            else:
                user_profile = UserProfile()
                user_profile.username = email
                user_profile.email = email
                user_profile.password = make_password(password)
                user_profile.is_active = False
                status = send_email(email, 'register')
                if status:
                    user_profile.save()
                    return HttpResponse('{"status":"success"}', content_type='application/json')
                else:
                    return HttpResponse('{"msg":"该邮箱不存在"}', content_type='application/json')


        else:
            register_form_errors = json.loads(json.dumps(register_form.errors))

            if 'email' in register_form_errors.keys():
                if register_form_errors['email'][0] == 'This field is required.':
                    return HttpResponse('{"email":"请输入邮箱"}', content_type='application/json')
                else:
                    return HttpResponse('{"email":"邮箱格式错误"}', content_type='application/json')

            if 'password' in register_form_errors.keys():
                return HttpResponse('{"password":"密码至少8位，最多20位"}', content_type='application/json')

            if 'captcha' in register_form_errors.keys():
                if register_form_errors['captcha'][0] == 'Invalid CAPTCHA':
                    return HttpResponse('{"captcha":"验证码错误"}', content_type='application/json')
                else:
                    return HttpResponse('{"captcha":"请输入验证码"}', content_type='application/json')


class UserForgetPwdView(View):
    def get(self, request):
        register_form = UserRegisterForm()
        return render(request, 'forgetpwd.html', {
            'register_form' : register_form
        })

    def post(self, request):
        forgetpwd_form = UserForgetPwdForm(request.POST)
        email = request.POST.get('email', '')
        if forgetpwd_form.is_valid():
            if UserProfile.objects.filter(email=email):
                status = send_email(email, 'forget')
                if status:
                    return HttpResponse('{"status":"success"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail"}', content_type='application/json')
            else:
                return HttpResponse('{"user":"该用户不存在"}', content_type='application/json')
        else:
            forgetpwd_form_errors = json.loads(json.dumps(forgetpwd_form.errors))

            if 'email' in forgetpwd_form_errors.keys():
                if forgetpwd_form_errors['email'][0] == 'This field is required.':
                    return HttpResponse('{"email":"请输入邮箱"}', content_type='application/json')
                else:
                    return HttpResponse('{"email":"邮箱格式错误"}', content_type='application/json')

            if 'captcha' in forgetpwd_form_errors.keys():
                if forgetpwd_form_errors['captcha'][0] == 'Invalid CAPTCHA':
                    return HttpResponse('{"captcha":"验证码错误"}', content_type='application/json')
                else:
                    return HttpResponse('{"captcha":"请输入验证码"}', content_type='application/json')


class UserActiveView(View):
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        status = 0
        if records:
            for record in records:
                try:
                    user = UserProfile.objects.get(email=record.email)
                    user.is_active = True
                    user.save()
                    #激活一次就可以删除所有相关的记录，所以用filter
                    EmailVerifyRecord.objects.filter(email=record.email, send_type='register').delete()
                    status = 1
                    break
                except Exception as e:
                    None
        if status:
            return render(request, 'active.html', {
                'msg' : '您的账户已经成功激活，请尽情使用吧'
            })
        else:
            return render(request, 'active.html', {
                'msg': '验证码有误，请重新点击激活链接进行激活'
            })


class ModifyPwdView(View):
    def get(self, request, modify_code):

        if EmailVerifyRecord.objects.filter(code=modify_code):
            return render(request, 'modifypwd.html', {
                'modify_code' : modify_code
            })
        else:
            return render(request, 'active.html', {
                'msg': '链接已经失效，请重新在忘记密码页面填写相关信息'
            })

    def post(self, request, modify_code):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            records = EmailVerifyRecord.objects.filter(code=modify_code)
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return HttpResponse('{"status":"fail", "msg":"两次密码不一致"}', content_type='application/json')
            else:
                status = 0
                if records:
                    for record in records:
                        try:
                            user = UserProfile.objects.get(email=record.email)
                            user.password = make_password(password1)
                            user.save()
                            EmailVerifyRecord.objects.filter(email=record.email, send_type='forget').delete()
                            status = 1
                            break
                        except Exception as e:
                            None
                if status:
                    return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            modifypwd_form_errors = json.loads(json.dumps(modifypwd_form.errors))
            if 'password1' in modifypwd_form_errors.keys():
                if modifypwd_form_errors['password1'][0] == 'This field is required.':
                    return HttpResponse('{"password1":"请输入新密码"}', content_type='application/json')
                else:
                    return HttpResponse('{"password1":"新密码至少8位，最多20位"}', content_type='application/json')

            if 'password2' in modifypwd_form_errors.keys():
                if modifypwd_form_errors['password2'][0] == 'This field is required.':
                    return HttpResponse('{"password2":"请输入确认密码"}', content_type='application/json')
                else:
                    return HttpResponse('{"password2":"确认密码至少8位，最多20位"}', content_type='application/json')


class UserAddressCheckView(LoginRequiredMixin, View):
    def post(self, request):
        if request.POST.get('remove', ''):
            try:
                user_address_id = int(request.POST.get('user_address_id', 0))
                user_address = UserAddress.objects.get(id=user_address_id)
                user_address.delete()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        user_address_form = UserAddressForm(request.POST)
        if user_address_form.is_valid():

            user_address_id = int(request.POST.get('user_address_id', 0))
            if user_address_id:
                try:
                    user_address = UserAddress.objects.get(id=user_address_id)
                    user_address.consignee = request.POST.get('consignee','')
                    user_address.mobile = request.POST.get('mobile', '')
                    user_address.province = request.POST.get('province', '')
                    user_address.city = request.POST.get('city', '')
                    user_address.town = request.POST.get('town', '')
                    user_address.address = request.POST.get('address', '')
                    user_address.save()
                    return HttpResponse('{"status":"success"}',content_type='application/json')
                except Exception as e:
                    return HttpResponse('{"status":"fail"}', content_type='application/json')
            else:
                user_address = UserAddress()
                user_address.consignee = request.POST.get('consignee', '')
                user_address.mobile = request.POST.get('mobile', '')
                user_address.province = request.POST.get('province', '')
                user_address.city = request.POST.get('city', '')
                user_address.town = request.POST.get('town', '')
                user_address.address = request.POST.get('address', '')
                user_address.user_id = request.user.id
                user_address.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            user_address_form_errors = json.loads(json.dumps(user_address_form.errors))
            if 'consignee' in user_address_form_errors.keys():
                if user_address_form['consignee'][0] == 'This field is required.':
                    return HttpResponse('{"status":"invalid","consignee":"请输入收件人姓名"}' ,content_type='application/json')
                elif user_address_form['consignee'][0] == '寄件人姓名包含特殊字符':
                    return HttpResponse('{"status":"invalid","consignee":"收件人姓名包含特殊字符"}',
                                        content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid","consignee":"请输入正确收件人姓名2-20个字"}',content_type='application/json')

            if 'mobile' in user_address_form_errors.keys():
                if user_address_form_errors['mobile'][0] == 'This field is required.':
                    return HttpResponse('{"status":"invalid","mobile":"请输入联系电话"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid","mobile":"手机号非法"}', content_type='application/json')

            if ('town' in user_address_form_errors.keys()) | ('city' in user_address_form_errors.keys()):
                return HttpResponse('{"status":"invalid","address":"请选择地址"}', content_type='application/json')

            if 'address' in user_address_form_errors.keys():
                if user_address_form_errors['address'][0] == 'This field is required.':
                    return HttpResponse('{"status":"invalid","address_detial":"请填写收件地址"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid","address_detial":"请填写正确的收货地址，10-60个字"}', content_type='application/json')


class Cartsorder(object):
    def print(self):
        pass
    # def __init__(self,order_number, order_times, carts, status, order_price):
    #     self.order_number = order_number
    #     self.order_times =  order_times
    #     self.carts = carts
    #     self.status = status
    #     self.order_price = order_price


class UserCenterMyOrderView(LoginRequiredMixin, View):
    def get(self, request):
        carts_orders_list = []
        carts_orders = CartsOrder.objects.filter(user_id=request.user.id)
        for carts_order in carts_orders:
            order = CartsOrder()
            order.order_number = carts_order.order_number
            order.order_times = carts_order.order_times
            order.carts = json.loads(carts_order.carts)
            order.order_price = carts_order.order_price
            order.status = carts_order.is_playment
            carts_orders_list.append(order)
            print(order.order_number)
        return render(request, 'usercenter-order-list.html', {
            'carts_orders_list' : carts_orders_list
        })


class UserCenterMyOrderCancelView(LoginRequiredMixin, View):
    def get(self, request, order_number):
        try:
            carts_order = CartsOrder.objects.get(order_number=order_number)
            carts_order.is_playment = 3
            carts_order.save()
            return HttpResponseRedirect('/users/order_list')
        except Exception as e:
            return render(request, 'active.html', {
                'msg': '订单不存在',
                'status': 1
            })


class UserCenterMyOrderDetailView(LoginRequiredMixin, View):
    def get(self, request,order_number):

        try:
            carts_order = CartsOrder.objects.get(order_number=order_number)
            carts = json.loads(carts_order.carts)
            return render(request, 'usercenter-order-detail.html', {
                'carts_order' : carts_order,
                'carts' : carts
            })
        except Exception as e:
            return render(request, 'active.html', {
                'msg' : '订单不存在',
                'status' : 1
            })


class UserCenterCashView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-cash.html', {

        })


class UserCenterRecycleView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-recycle.html', {

        })


class UserCenterAddressView(LoginRequiredMixin, View):
    def get(self, request):
        user_addresses = UserAddress.objects.filter(user_id=request.user.id)
        return render(request, 'usercenter-address.html', {
            'user_addresses' : user_addresses
        })


class UserCenterAddressModifyView(LoginRequiredMixin, View):
    def post(self, request):
        user_address_form = UserAddressForm(request.POST)
        if user_address_form.is_valid():
            user_address_id = int(request.POST.get('user_address_id', ''))
            user_address = UserAddress.objects.get(id=user_address_id)
            user_address.consignee = request.POST.get('consignee', '')
            user_address.mobile = request.POST.get('mobile', '')
            user_address.province = request.POST.get('province', '')
            user_address.city = request.POST.get('city', '')
            user_address.town = request.POST.get('town', '')
            user_address.address = request.POST.get('address', '')
            user_address.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            try:
                user_address_form_error = json.loads(json.dumps(user_address_form.errors))
                if 'consignee' in user_address_form_error.keys():
                    if user_address_form_error['consignee'][0] == 'This field is required.':
                        return HttpResponse('{"status":"invalid", "consignee":"请输入收货人姓名"}',
                                            content_type='application/json')
                    elif user_address_form_error['consignee'][0] == '寄件人姓名包含特殊字符':
                        return HttpResponse('{"status":"invalid", "consignee":"收货人姓名包含特殊字符"}',
                                            content_type='application/json')
                    else:
                        return HttpResponse('{"status":"invalid", "consignee":"收货人姓名在2-10个字之间"}',
                                            content_type='application/json')

                if 'mobile' in user_address_form_error.keys():
                    if user_address_form_error['mobile'][0] == 'This field is required.':
                        return HttpResponse('{"status":"invalid", "mobile":"请输入联系人电话"}',
                                            content_type='application/json')
                    else:
                        return HttpResponse('{"status":"invalid", "mobile":"电话号码格式错误"}',
                                            content_type='application/json')

                if 'city' in user_address_form_error.keys():
                    return HttpResponse('{"status":"invalid", "city":"请选择城市"}',
                                        content_type='application/json')
                if 'town' in user_address_form_error.keys():
                    return HttpResponse('{"status":"invalid", "town":"请选择城镇"}',
                                        content_type='application/json')

                if 'address' in user_address_form_error.keys():
                    if user_address_form_error['address'][0] == 'This field is required.':
                        return HttpResponse('{"status":"invalid", "address":"请输入收货地址"}',
                                            content_type='application/json')
                    else:
                        return HttpResponse('{"status":"invalid", "address":"收货地址在10-150字之间"}',
                                            content_type='application/json')
            except Exception as e:
                print(e)


class UserCenterAddressDelView(LoginRequiredMixin, View):
    def post(self, request):
        user_address_id = int(request.POST.get('user_address_id', ''))
        user_address = UserAddress.objects.get(id=user_address_id)
        user_address.delete()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UserCenterAddressNewView(LoginRequiredMixin, View):
    def post(self, request):
        user_address_form = UserAddressForm(request.POST)
        if user_address_form.is_valid():
            user_address = UserAddress()
            user_address.user_id = request.user.id
            user_address.consignee = request.POST.get('consignee', '')
            user_address.mobile = request.POST.get('mobile', '')
            user_address.province = request.POST.get('province', '')
            user_address.city = request.POST.get('city', '')
            user_address.town = request.POST.get('town', '')
            user_address.address = request.POST.get('address', '')
            user_address.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            try:
                user_address_form_error = json.loads(json.dumps(user_address_form.errors))
                if 'consignee' in user_address_form_error.keys():
                    if user_address_form_error['consignee'][0] == 'This field is required.':
                        return HttpResponse('{"status":"invalid", "consignee":"请输入收货人姓名"}',
                                            content_type='application/json')
                    elif user_address_form_error['consignee'][0] == '寄件人姓名包含特殊字符':
                        return HttpResponse('{"status":"invalid", "consignee":"收货人姓名包含特殊字符"}',
                                            content_type='application/json')
                    else:
                        return HttpResponse('{"status":"invalid", "consignee":"收货人姓名在2-10个字之间"}',
                                            content_type='application/json')

                if 'mobile' in user_address_form_error.keys():
                    if user_address_form_error['mobile'][0] == 'This field is required.':
                        return HttpResponse('{"status":"invalid", "mobile":"请输入联系人电话"}',
                                            content_type='application/json')
                    else:
                        return HttpResponse('{"status":"invalid", "mobile":"电话号码格式错误"}',
                                            content_type='application/json')

                if 'city' in user_address_form_error.keys():
                    return HttpResponse('{"status":"invalid", "city":"请选择城市"}',
                                        content_type='application/json')
                if 'town' in user_address_form_error.keys():
                    return HttpResponse('{"status":"invalid", "town":"请选择城镇"}',
                                        content_type='application/json')

                if 'address' in user_address_form_error.keys():
                    if user_address_form_error['address'][0] == 'This field is required.':
                        return HttpResponse('{"status":"invalid", "address":"请输入收货地址"}',
                                            content_type='application/json')
                    else:
                        return HttpResponse('{"status":"invalid", "address":"收货地址在10-150字之间"}',
                                            content_type='application/json')
            except Exception as e:
                print(e)


class UserCenterUserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        birthdayYear = user.birday.strftime('%Y')
        birthdayMonth = user.birday.strftime('%m')
        birthdayDay = user.birday.strftime('%d')
        return render(request, 'usercenter-userinfo.html', {
            'user':user,
            'birthdayYear':birthdayYear,
            'birthdayMonth':birthdayMonth,
            'birthdayDay':birthdayDay
        })

    def post(self, request):
        userinfo_form = UserInfoForm(request.POST)
        if userinfo_form.is_valid():
            try:
                user = UserProfile.objects.get(id=request.user.id)
                user.gender = int(request.POST.get('gender', 0))
                user.mobile=  request.POST.get('mobile')
                user.province = request.POST.get('province', '')
                user.city = request.POST.get('city', '')
                user.town = request.POST.get('town', '')
                times = str(request.POST.get('selYear')) + '-' + str(request.POST.get('selMonth')) + '-' + str(request.POST.get('selDay'))
                t = time.strptime(times, "%Y-%m-%d")
                y, m, d = t[0:3]
                user.birday = datetime.datetime(y, m, d)
                user.save()
                return HttpResponse('{"status":"success","msg":"个人资料修改成功"}', content_type='application/json')
            except Exception as e:
                print(e)
        else:
            userinfo_form_errors = json.loads(json.dumps(userinfo_form.errors))
            if 'mobile' in userinfo_form_errors.keys():
                if userinfo_form_errors['mobile'][0] == 'This field is required.':
                    return HttpResponse('{"status":"invalid", "mobile":"请输入手机号码"}',
                                        content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid", "mobile":"手机号码非法"}',
                                        content_type='application/json')

            if 'province' in userinfo_form_errors.keys():
                return HttpResponse('{"status":"invalid", "city":"请选择省份"}',
                                        content_type='application/json')


            if 'city' in userinfo_form_errors.keys():
                if userinfo_form_errors['city'][0] == '城市为空':
                    return HttpResponse('{"status":"invalid", "city":"请在下拉列表中重新选择省份"}',
                                        content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid", "city":"请选择城市"}',
                                        content_type='application/json')

            if 'town' in userinfo_form_errors.keys():

                return HttpResponse('{"status":"invalid", "town":"请在下拉列表中重新选择城市"}',
                                        content_type='application/json')


class IndexView(View):
    def get(self, request):
        if request.user.id:
            nick_name = UserProfile.objects.get(id=request.user.id).nick_name
            return render(request, 'index.html', {
                'nick_name':nick_name
            })
        else:
            return render(request, 'index.html', {

            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')

























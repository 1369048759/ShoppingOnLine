from django.shortcuts import render
from django.views.generic import View
from django.http import  HttpResponse
from parts.models import Parts
from mobiles.models import  Mobile
from users.models import UserProfile

import json
from random import Random
from datetime import datetime

from utils.mixin_utils import LoginRequiredMixin
from users.models import  UserAddress
from users.forms import UserAddressForm
from .forms import InvoiceForPersonForm, InvoiceForOrgForm
from .models import CartsForUser, RecentlyView, ElectronicInvoice
from .models import CartsOrder, PaymentBank
from django.http import HttpResponseRedirect

# Create your views here.

def random_number(randomlength = 8):
    str = ''
    chars = '0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

class CartsInfo(object):
    def __init__(self):
        self.product_id = 0
        self.name = ''
        self.image = ''
        self.price = ''
        self.quantity = ''
        self.total_price = 0
        self.category = 0

def obj_json(obj):
    return {
        'product_id' : obj.product_id,
        'name' : obj.name,
        'image' : obj.image,
        'price' : obj.price,
        'quantity' : obj.quantity,
        'total_price' : obj.total_price,
        'category' : obj.category

    }

class CartForUser():
    def __init__(self, *args, **kwargs):
        self.item = {}
        self.all_price = 0

    def add_items_user(self, user_id, product, quantity, category):
        product_id = product.id
        price = product.price
        name = product.name
        image = product.image
        cart_user = None
        item = None
        try:
            cart_user = CartsForUser.objects.get(user_id=user_id, status=0)
            item = json.loads(cart_user.cart)
        except Exception as e:
            None
        if cart_user and name in item:
            cart_user.price += quantity * price
            item[name]['quantity'] += quantity
            item[name]['total_price'] = quantity * price
            try:
                cart = json.dumps(item, default=obj_json)
            except Exception as e:
                print(e)
            cart_user.cart = cart
            cart_user.save()

        else:
            try:
                if not cart_user:
                    cart_user = CartsForUser()

                product = CartsInfo()
                product.product_id = product_id
                product.name = name
                product.image = str(image)
                product.price = price
                product.quantity = quantity
                product.total_price = quantity * price
                product.category = category

                #要是字段为空的时候，注意item中是没有数据结构的，需要重新获取
                if not item:
                    self.item[name] = product
                    #获取数据结构
                    item = self.item
                else:
                    item[name] = product

                cart = json.dumps(item, default=obj_json)
                cart_user.user_id = user_id
                cart_user.cart = cart
                cart_user.price += product.total_price
                cart_user.save()

            except Exception as e:
                print(e)

        return  [item, cart_user.price]

    def redu_quantity(self, name, request):
        try:
            cart_user = CartsForUser.objects.get(user_id=request.user.id, status=0)
            item = json.loads(cart_user.cart)
            if item[name]['quantity'] > 1:
                item[name]['quantity'] -= 1
                item[name]['total_price'] -= item[name]['price']
                cart_user.price -= item[name]['price']
            cart = json.dumps(item, default=obj_json)
            cart_user.cart = cart
            cart_user.save()
        except Exception as e:
            print(e)

    def add_quantity(self, name, request):
        try:
            cart_user = CartsForUser.objects.get(user_id=request.user.id, status=0)
            item = json.loads(cart_user.cart)
            item[name]['quantity'] += 1
            item[name]['total_price'] += item[name]['price']
            cart_user.price += item[name]['price']
            cart = json.dumps(item, default=obj_json)
            cart_user.cart = cart
            cart_user.save()
        except Exception as e:
            print(e)

    def del_product(self, name, request):
        try:
            cart_user = CartsForUser.objects.get(user_id=request.user.id, status=0)
            item = json.loads(cart_user.cart)
            total_price = item.pop(name)['total_price']
            cart = json.dumps(item, default=obj_json)
            cart_user.cart = cart
            cart_user.price -= total_price
            cart_user.save()
            return [item, cart_user.price]
        except Exception as e:
            print(e)
            return {'',''}


class CartForVisitor():
    def __init__(self, *args, **kwargs):
        self.item = {}
        self.all_price = 0

    #添加购物车
    def add_items_visitor(self,product, quantity, category):
        product_id = product.id
        price = product.price
        name = product.name
        image = product.image

        if name in self.item:
            product = self.item[name]
            self.all_price += quantity * price
            product.quantity += quantity
            product.total_price = quantity * price
        else:
            try:
                product = CartsInfo()
            except Exception as e:
                print(e)
            product.product_id = product_id
            product.name = name
            product.image = image
            product.price = price
            product.quantity = quantity
            product.total_price = quantity * price
            product.category = category
            self.item[name] = product
            self.all_price += product.total_price
        return [self.item, self.all_price]

    #减少商品数量
    def redu_quantity(self, name):
        product = self.item[name]
        if product.quantity > 1:
            product.quantity -= 1
            product.total_price -= product.price
            self.all_price -= product.price
            self.item[name] = product
    #添加商品数据
    def add_quantity(self, name):
        product = self.item[name]
        product.quantity += 1
        product.total_price += product.price
        self.all_price += product.price
        self.item[name] = product

    #删除商品
    def del_product(self, name):
        product = self.item[name]
        self.all_price -= product.total_price
        self.item.pop(name)


class CartsDelView(View):
    def get(self, request, product_name):
        name = product_name
        if not request.user.id:
            cart = request.session.get('cart_visitor', None)

            if name in cart.item.keys():#为空就不删除，不然会报错
                cart.del_product(name)

            products = cart.item
            price = cart.all_price
            if len(cart.item) == 0:
                #购物车为空时候，清空总价，防止出错
                cart.all_price = 0
                request.session['cart_visitor'] = cart
                return HttpResponseRedirect('/service/empty')
            else:
                request.session['cart_visitor'] = cart
                return HttpResponseRedirect('/carts/add/')
        else:
            item = CartForUser().del_product(name, request)
            if len(item) == 0:
                return HttpResponseRedirect('/service/empty')
            products = item[0]
            price = item[1]
            return HttpResponseRedirect('/carts/add/')


class CartsModifyView(View):
    def post(self, request):
        if not request.user.id:
            name = request.POST.get('product_name', '')
            style = request.POST.get('style',  '')
            cart = request.session.get('cart_visitor', None)
            if style == 'redu':
               cart.redu_quantity(name)

            if style == 'add':
                cart.add_quantity(name)

            request.session['cart'] = cart

            #解决F5刷新表单重复提交问题，重定向到另一个页面
            return HttpResponseRedirect('/carts/add/')
        else:
            name = request.POST.get('product_name', '')
            style = request.POST.get('style', '')

            if style == 'redu':
                CartForUser().redu_quantity(name, request)

            if style == 'add':
                CartForUser().add_quantity(name, request)

            return HttpResponseRedirect('/carts/add/')


class CartsAddView(View):

    def get(self, request):
        if not request.user.id:
            cart = request.session.get('cart_visitor', None)
            if cart and len(cart.item) == 0:
                return render(request, 'carts-empty.html', {

                })
            products = cart.item

            request.session['cart_visitor'] = cart
            products = cart.item
            price = cart.all_price

            return render(request, 'carts-list.html', {
                'products': products,
                'price': price
            })

        else:
            try:
                recent_products = {}
                recents = RecentlyView.objects.filter(user_id=request.user.id).order_by('-add_times')[:4]
                for recent in recents:
                    if recent.product_type == 1:
                        try:
                            mobile = Mobile.objects.get(id=recent.product_id)
                            recent_products[mobile] = 1
                        except Exception as e:
                            None
                    else :
                        try:
                            part = Parts.objects.get(id=recent.product_id)
                            recent_products[part] = 2
                        except Exception as e:
                            None

                carts_user = CartsForUser.objects.get(user_id=request.user.id, status=0)

                products = json.loads(carts_user.cart)
                price = carts_user.price

                if carts_user.price == 0:
                    carts_user.delete()
                    return render(request, 'carts-empty.html', {})

                return render(request, 'carts-list.html', {
                    'products' : products,
                    'price' : price,
                    'recent_products' : recent_products
                })
            except Exception as e:
                print(e)
                return render(request, 'carts-empty.html', {})

    def post(self, request):
        #未登入的user_id == None
        user_id = request.user.id
        product_id = int(request.POST.get('product_id', 0))
        quantity = int(request.POST.get('quantity', 0))
        category = int(request.POST.get('category', 0))
        product = 0

        #判断商品种类 手机或者配件
        if category == 2:
            try:
                product = Parts.objects.get(id=product_id)
            except Exception as e:
                None
        if category == 1:
            try:
                product = Mobile.objects.get(id=product_id)
            except Exception as e:
                None


        if user_id:
            cart_user = None
            cart = CartForUser()
            item = cart.add_items_user(user_id, product, quantity, category)

            # products = json.loads(CartsForUser.objects.get(user_id=user_id).cart)

        else:
            cart = request.session.get('cart_visitor', None)
            #对购物车进行操作
            if not cart:
                cart = CartForVisitor()
                item = cart.add_items_visitor(product, quantity, category)
            else:
                item = cart.add_items_visitor(product, quantity, category)

            request.session['cart_visitor'] = cart
        products = item[0]
        price = item[1]

        recent_products = {}
        recents = RecentlyView.objects.filter(user_id=request.user.id).order_by('-add_times')[:4]
        for recent in recents:
            if recent.product_type == 1:
                try:
                    mobile = Mobile.objects.get(id=recent.product_id)
                    recent_products[mobile] = 1
                except Exception as e:
                    None
            else:
                try:
                    part = Parts.objects.get(id=recent.product_id)
                    recent_products[part] = 2
                except Exception as e:
                    None

        return render(request, 'carts-list.html', {
            'products': products,
            'price': price,
            'category' : category,
            'recent_products' : recent_products
        })


class CartsCheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            user_addresses = UserAddress.objects.filter(user_id=request.user.id).order_by('id')

            carts_user = CartsForUser.objects.get(user_id=request.user.id, status=0)
            products = json.loads(carts_user.cart)
            price = carts_user.price
            if price > 99:
                result_price = price
            else:
                result_price = price -10

            return render(request, 'carts-checkout.html', {
                'user_addresses' : user_addresses,
                'products' : products,
                'price' : price,
                'result_price' : result_price
            })
        except Exception as e:
            return render(request, 'active.html', {
                'msg': '您的购物车没有任何商品',
                'status': 1,

            })

    def post(self, request):
        try:
            address_id = int(request.POST.get('address', 0))
            playment_type = int(request.POST.get('payment', 1))
            personcompany = request.POST.get('personcompany', '')
            if personcompany == '个人':
                personcompany = 1
            else:
                personcompany = 2
            inv_payee = request.POST.get('inv_payee', '')
            inv_phone = request.POST.get('inv_phone', '')
            inv_email = request.POST.get('inv_email', '')
            inv_taxno = request.POST.get('inv_taxno', '')
            order_number = datetime.now().strftime('%Y%m%d') + str(request.user.id) + random_number()
            address = UserAddress.objects.get(id=address_id)
            address = address.address + "(" + address.consignee + "收" + ")" + address.mobile

            invoice = ElectronicInvoice()
            invoice.invoice_title = personcompany
            invoice.inv_payee = inv_payee
            invoice.inv_phone = inv_phone
            invoice.inv_email = inv_email
            invoice.inv_taxno = inv_taxno
            invoice.order_number = order_number
            invoice.save()

            carts_order = CartsOrder()
            carts_order.order_number = order_number
            carts_order.address = address
            carts_order.playment_type = playment_type
            carts_order.delivery_type = playment_type

            carts_user = CartsForUser.objects.get(user_id=request.user.id, status=0)
            carts_order.carts = carts_user.cart
            carts_order.order_price = carts_user.price
            carts_order.user_id = request.user.id
            carts_order.save()
            carts_user.status = 1
            carts_user.save()
            msg = {}
            msg['order_number'] = order_number
            return HttpResponse(json.dumps(msg))
        except Exception as e:
            print(e)


class CartsInvoiceCheckView(LoginRequiredMixin, View):
    def post(self, request):
        personcompany = request.POST.get('personcompany', '')
        if personcompany == '个人':
            invoice_form = InvoiceForPersonForm(request.POST)
        else:
            invoice_form = InvoiceForOrgForm(request.POST)
        if invoice_form.is_valid():
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            invoice_form_errors = json.loads(json.dumps(invoice_form.errors))
            if 'inv_payee' in invoice_form_errors.keys():
                if invoice_form_errors['inv_payee'][0] == 'This field is required.':
                    return HttpResponse('{"status":"invalid", "inv_payee":"请输入姓名"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid", "inv_payee":"请输入正确的姓名，2-50个字"}', content_type='application/json')
            if 'inv_phone' in invoice_form_errors.keys():
                if invoice_form_errors['inv_phone'][0] == 'This field is required.':
                    return HttpResponse('{"status":"invalid", "inv_phone":"请输入正确的手机号"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid", "inv_phone":"手机号格式不正确"}',content_type='application/json')
            if personcompany == '单位':
                if 'inv_taxno' in invoice_form_errors.keys():
                    if invoice_form_errors['inv_taxno'][0] == 'This field is required.':
                        return HttpResponse('{"status":"invalid", "inv_taxno":"请输入纳税人识别号"}',content_type='application/json')
                    else:
                        return HttpResponse('{"status":"invalid", "inv_taxno":"纳税人识别号错误"}',content_type='application/json')

            if 'inv_email' in invoice_form_errors.keys():
                if invoice_form_errors['inv_email'][0] == 'This field is required.':
                    return HttpResponse('{"status":"invalid", "inv_email":"请输入邮箱"}',content_type='application/json')
                else:
                    return HttpResponse('{"status":"invalid", "inv_email":"邮箱格式错误"}', content_type='application/json')


class CartsPlaymentView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            order_number = request.GET.get('order_number', '')
            carts_order = CartsOrder.objects.get(order_number=order_number)
            order_price = carts_order.order_price
            return render(request, 'carts-playment.html', {
                'order_number' : order_number,
                'order_price' : order_price
            })
        except Exception as e:
            return render(request, 'active.html', {
                'msg': '订单不存在',
                'status': 1
            })

    def post(self, request):
        try:
            bank = request.POST.get('bank', '')
            order_number = request.POST.get('order_number', '')
            bank_name = PaymentBank.objects.get(nick_name=bank).name
            carts_order = CartsOrder.objects.get(order_number=order_number)
            carts_order.payment_bank = bank_name
            carts_order.is_playment = 2
            carts_order.save()
            order_price = carts_order.order_price
            return render(request, 'carts-success.html', {
                'order_number':order_number,
                'bank_name':bank_name,
                'order_price':order_price
            })
        except Exception as e:
            return render(request, 'active.html', {
                'msg': '订单不存在',
                'status': 1
            })












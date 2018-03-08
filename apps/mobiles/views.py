from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from carts.models import RecentlyView
from .models import  Mobile, MobileImage ,TypicalSpecification
# Create your views here.

class MobileListView(View):
    def get(self, request):
        mobiles = Mobile.objects.all()
        category = int(request.GET.get('cate', 0))
        appearance = int(request.GET.get('appea', 0))
        qus = int(request.GET.get('qu', 0))
        series = int(request.GET.get('ser', 0))

        if category:
            mobiles = mobiles.filter(category=category)

        if appearance:
            mobiles = mobiles.filter(appearance=appearance)

        if series:
            mobiles = mobiles.filter(series=series)

        if qus:
            if qus == 1:
                mobiles = mobiles.order_by('price')
            if qus == 2:
                mobiles = mobiles.order_by('sale_nums')
        else:
            mobiles = mobiles.order_by('add_times')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(mobiles, 12, request=request)

        mobiles = p.page(page)
        return render(request, 'mobile-list.html', {
            'mobiles' : mobiles,
            'category' : category,
            'appearance' : appearance,
            'series' : series,
            'qus' : qus
        })


class MobileInfoView(View):
    def get(self, request, mobile_id):

        try:
            mobile_id = int(mobile_id)
            mobile = Mobile.objects.get(id=mobile_id)
            mobile_image_1 = MobileImage.objects.filter(mobile_id=mobile_id, category=1).order_by('index')
            mobile_image_2 = MobileImage.objects.filter(mobile_id=mobile_id, category=2).order_by('index')
            typical = TypicalSpecification.objects.get(mobile_id=mobile_id)

            if request.user.id:
                try:
                    recent = RecentlyView.objects.get(user_id=request.user.id, product_id=mobile_id, product_type=1)
                    recent.save()
                except Exception as e:
                    recent = RecentlyView()
                    recent.user_id = request.user.id
                    recent.product_id = mobile_id
                    recent.product_type = 1
                    recent.save()

            return render(request, 'mobile-info.html', {
                'mobile': mobile,
                'mobile_image_1': mobile_image_1,
                'mobile_image_2': mobile_image_2,
                'typical': typical
            })
        except Exception as e:
            return render(request, 'active.html', {
                'status': 1,
                'msg': '暂时没有该商品，请浏览其他商品'
            })


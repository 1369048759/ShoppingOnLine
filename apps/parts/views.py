from django.shortcuts import render
from django.views.generic import View

from carts.models import RecentlyView
from .models import Parts, PartsImage, TypicalSpecification
# Create your views here.

class PartsListView(View):
    def get(self, request):
        category_dic = [
            '后盖','保护壳/套','电池','耳机','数据线','保护膜','充电器','移动电源','无线传输','自拍杆'
        ]

        model_dic = [
            'M6S','M7Plus','M6','M6Plus','M2017','W909','S9','F106','F5'
        ]

        parts_list = Parts.objects.all()
        sort = int(request.GET.get('sort', 0))
        adaptation = int(request.GET.get('model', 0))
        quees = int(request.GET.get('quee', 0))
        if sort:
            parts_list = parts_list.filter(category=sort)
        if adaptation:
            parts_list = parts_list.filter(adaptation=adaptation)
        if quees:
            if quees == 1:
                parts_list = parts_list.order_by('price')
            if quees == 2:
                parts_list = parts_list.order_by('-sale_nums')
        else:
            parts_list = parts_list.order_by('add_times')

        return render(request, 'parts-list.html', {
            'category_dic' : category_dic,
            'model_dic' : model_dic,
            'parts_list' : parts_list,
            'sort' : sort,
            'adaptation' : adaptation,
            'quees' : quees
        })


class PartsInfoView(View):
    def get(self, request, parts_id):
        try:
            parts_id = int(parts_id)
            parts = 0
            parts = Parts.objects.get(id=parts_id)
            if request.user.id:
                try:
                    recent = RecentlyView.objects.get(user_id=request.user.id, product_id=parts_id, product_type=2)
                    recent.save()
                except Exception as e:
                    recent = RecentlyView()
                    recent.user_id = request.user.id
                    recent.product_id = parts_id
                    recent.product_type = 2
                    recent.save()

            parts_image_1 = PartsImage.objects.filter(parts_id=parts_id, category=1).order_by('index')
            parts_image_2 = PartsImage.objects.filter(parts_id=parts_id, category=2).order_by('index')
            parameters = TypicalSpecification.objects.filter(parts_id=parts_id)
            return render(request, 'parts-info.html', {
                'parts': parts,
                'parts_image_1': parts_image_1,
                'parts_image_2': parts_image_2,
                'parameters': parameters
            })
        except Exception as e:
            return render(request, 'active.html', {
                'status' : 1,
                'msg' : '暂时没有该商品，请浏览其他商品'
            })




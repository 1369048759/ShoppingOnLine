from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import  json

from .models import ServiceHelp, ExperienceStore, ServiceNetworkStation, District, \
    City, BrokenScreenQuestion
from .forms import ServiceUserAskForm
# Create your views here.

class ServiceHelpDetailView(View):
    def get(self, request, service_type, service_id):
        try:
            service_detail = ServiceHelp.objects.get(service_id=int(service_id), service_type=int(service_type))

        except Exception as e:
            return render(request, 'service-detail.html', {

            })

        return render(request, 'service-detail.html', {
            'service_detial' : service_detail,
            'service_type' : service_type,
            'service_id' : service_id
        })


class ServiceHelpListView(View):
    def get(self, request):

        sort = request.GET.get('sort','')

        service_help = ServiceHelp.objects.all()
        if sort == '':
            FAQS = service_help.filter(Q(service_type=9)|Q(service_type=10)|Q(service_type=11))
        elif sort == '售后':
            FAQS = service_help.filter(service_type=9)
        elif sort == '售前':
            FAQS = service_help.filter(service_type=10)
        elif sort == '使用':
            FAQS = service_help.filter(service_type=11)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(FAQS, 10, request=request)

        FAQS = p.page(page)

        return render(request, 'service-list.html', {
            'FAQS' : FAQS,
            'sort' : sort
        })


class ServiceUserAskView(View):
    def get(self, request):
        return render(request, 'service-user-ask.html', {

        })

    def post(self, request):
        service_user_ask_form = ServiceUserAskForm(request.POST)
        if service_user_ask_form.is_valid():
            service_user_ask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(service_user_ask_form.errors))


class ExperienceStoreView(View):
    def get(self, request):
        experience_stores = ExperienceStore.objects.all()
        return render(request, 'experience-store.html', {
            'experience_stores' : experience_stores
        })


class ServiceNetworkStationView(View):
    def get(self, request):
        service_network_station = ServiceNetworkStation.objects.all()
        districts = list(set([network_station.district for network_station in service_network_station]))

        return render(request, 'service-network-station.html', {
            'service_network_station' : service_network_station,
            'districts' : districts,
        })

    def post(self, request):

        service_network_station = ServiceNetworkStation.objects.all()
        districts = list(set([network_station.district for network_station in service_network_station]))

        province_id = int(request.POST.get('s_province', ''))
        city_id = request.POST.get('s_city', '')
        servince_net = request.POST.get('s_servince_net', 0)
        province = 0
        if province_id:

            try:
                province = District.objects.get(id=province_id)
            except Exception as e:
                None
            service_network_station = service_network_station.filter(district=province_id)
            citys = City.objects.filter(district=province_id)
            city = 0
            if city_id:
                try:
                    city = City.objects.get(id=city_id)
                except Exception as e:
                    None
                if city.district_id == province_id:
                    service_network_station = service_network_station.filter(city=city_id)
                else:
                    city = 0
        if servince_net:
            service_network_station = service_network_station.filter(category=servince_net)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(service_network_station, 6, request=request)

        service_network_station = p.page(page)

        return render(request, 'service-network-station.html', {
            'service_network_station': service_network_station,
            'districts': districts,
            'province' : province,
            'citys' : citys,
            'city': city,
            'servince_net' : servince_net
        })


class ServiceBrokenScreenView(View):
    def get(self, request):
        broken_screen_questions = BrokenScreenQuestion.objects.filter(category=1).order_by('add_times')
        return render(request, 'service-borken-screen.html', {
            'broken_screen_questions' : broken_screen_questions
        })


class ServiceIMEIView(View):
    def get(self, request):
        return render(request, 'service-IMEI.html', {

        })


class ServiceHintView(View):
    def get(self, request):
        return  render(request, 'hint.html', {

        })


class ServiceOutsiteRepairView(View):
    def get(self, request):
        questions = BrokenScreenQuestion.objects.filter(category=2)
        return render(request, 'service-outsite-repair.html', {
            'questions' : questions
        })


class ServiceEmptyView(View):
    def get(self, request):
        return render(request, 'carts-empty.html', {

        })

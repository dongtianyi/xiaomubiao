
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator
from django.urls import reverse

from .forms import ClockInForm, SetUpForm
from .models import ClockIn, SetUp
from django.conf import settings
from django.views.generic import DeleteView
import datetime


@login_required
def goal_home_view(request):
    if request.method == "GET":
        user = request.user
        # 检测是否目标配置
        # now = datetime.datetime.now()
        if not SetUp.objects.filter(user_id=user.id).exists():
            # 如果没有设置目标, 进入到目标设置页面
            return HttpResponseRedirect(reverse('goal_setup'))
        clockin_form = ClockInForm(user)
        # get all clock in data
        clock_ins = ClockIn.objects.filter(user_id=user.id)
        paginator = Paginator(clock_ins, settings.PAGE_SIZE)
        page_number = request.GET.get('page')
        page_clockin = paginator.get_page(page_number)
        template_name = 'goal/goal_home.html'
        return render(request, template_name, {'clockin_form': clockin_form, "page_clockin": page_clockin})
    elif request.method == "POST":
        user = request.user
        form = ClockInForm(user, request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
        return HttpResponseRedirect(reverse('clockin'))


@login_required
def goal_setup_view(request):
    if request.method == "GET":
        user = request.user
        setups = SetUp.objects.filter(user_id=user.id)
        setup_form = SetUpForm()
        template_name = 'goal/goal_setup.html'
        return render(request, template_name, {'setup_form': setup_form, "setups": setups})
    elif request.method == "POST":
        user = request.user
        form = SetUpForm(request.POST)
        if form.is_valid():
            form.save(user_id=user.id)
        return HttpResponseRedirect(reverse('goal_setup'))


@login_required
def all_setup_veiw(request):
    '''
    所有人目标
    '''
    # user = request.user
    setups = SetUp.objects.filter()
    paginator = Paginator(setups, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_setup = paginator.get_page(page_number)
    template_name = 'goal/all_setup.html'
    return render(request, template_name, {"page_setup": page_setup})


@login_required
def all_clockin_view(request):
    '''
    所有人的打卡
    '''
    # user = request.user
    clockIns = ClockIn.objects.filter()
    paginator = Paginator(clockIns, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_clockIns = paginator.get_page(page_number)
    template_name = 'goal/all_clockin.html'
    return render(request, template_name, {"page_clockIns": page_clockIns})


class ClockInDeleteView(DeleteView):
    '''
    删除打卡记录
    '''
    model = ClockIn

    def get_success_url(self):
        success_url = reverse("clockin")
        return success_url

    def get_object(self, *args, **kwargs):
        obj = super(ClockInDeleteView, self).get_object(*args, **kwargs)
        if datetime.datetime.now().date() > obj.created_time.date():
            raise 
        return obj

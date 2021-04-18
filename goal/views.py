
from django.core.exceptions import PermissionDenied, MiddlewareNotUsed
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
from django.views.generic import DeleteView, View
import datetime
from .goal_exceptions import CannotDeleteException
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import get_first_day_week, get_last_day_week


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
    setups = SetUp.objects.filter(status=True)
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
    clockIns = ClockIn.objects.filter().order_by("user", "setup")
    paginator = Paginator(clockIns, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_clockIns = paginator.get_page(page_number)
    template_name = 'goal/all_clockin.html'
    return render(request, template_name, {"page_clockIns": page_clockIns})


class ClockInDeleteView(LoginRequiredMixin, DeleteView):
    '''
    删除打卡记录
    '''
    model = ClockIn

    def get_success_url(self):
        success_url = reverse("clockin")
        return success_url

    # def get_object(self, *args, **kwargs):
    #     obj = super(ClockInDeleteView, self).get_object(*args, **kwargs)
    #     if datetime.datetime.now().date() > obj.created_time.date():
    #         raise CannotDeleteException("非当日打卡不能删除")
    #     return obj


class SettlementView(LoginRequiredMixin, View):
    '''
    查看当周或者上周完成情况
    '''

    def get(self, request):
        # <view logic>
        '''
        谁 目标(id) 目标次数 打卡次数 是否完成
        [
            {
                "user": "name",
                "setup": "goal",
                "times": 2,
                "clock_time": 3,
                "clock_status": Ture
            },
            {
                "user": "name",
                "setup": "goal",
                "times": 2,
                "clock_time": 3,
                "clock_status": Ture
            },
        ]
        '''
        # 获取指定日期:
        week = request.GET.get('week')
        if week and week.lower() == "last":
            week_day = datetime.datetime.today() - datetime.timedelta(days=7)
            is_current_week = False
        else:
            week_day = datetime.datetime.today()
            is_current_week = True
        start_date = get_first_day_week(week_day)
        end_date = get_last_day_week(week_day)
        # print(start_date, end_date)
        clock_result = []
        setups = SetUp.objects.filter(status=True).order_by("user")
        for setup in setups:
            clock_count = ClockIn.objects.filter(
                setup=setup, created_time__range=(start_date, end_date)).count()
            if clock_count < setup.times:
                clock_status = False
            else:
                clock_status = True
            result = {
                "user": setup.user.last_name,
                "setup": setup.name + "(id=" + str(setup.id) + ")",
                "times": setup.times,
                "clock_time": clock_count,
                "clock_status": clock_status,
            }
            clock_result.append(result)
        template_name = 'goal/goal_settlement.html'
        paginator = Paginator(clock_result, settings.PAGE_SIZE)
        page_number = request.GET.get('page')
        page_clock_result = paginator.get_page(page_number)
        return render(
            request,
            template_name,
            {
                'page_clock_result': page_clock_result,
                "start_date": start_date,
                "end_date": end_date,
                "is_current_week": is_current_week,
            }
        )

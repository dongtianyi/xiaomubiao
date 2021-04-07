
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator
from django.urls import reverse

from .forms import ClockInForm
from .models import ClockIn


@login_required
def goal_home_view(request):
    if request.method == "GET":
        user = request.user
        # now = datetime.datetime.now()
        clockin_form = ClockInForm(user)
        # get all clock in data
        clock_ins = ClockIn.objects.filter(user_id=user.id)
        paginator = Paginator(clock_ins, 2)
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

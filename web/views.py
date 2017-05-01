# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
import requests

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

from web.forms import AnonForm
from web.models import Tip


def verify_recaptcha(request):

    x = requests.post("https://www.google.com/recaptcha/api/siteverify",data={'secret':'6LflTR4UAAAAAARPmPGtO-wO6J1o505fkeVLOYeF','response':request.POST.get("g-recaptcha-response")})
    print x.text
    return x.text[15]=='t'


def home(request):
    if request.method == 'POST':
        try:
            form = AnonForm(request.POST)
            if form.is_valid() and verify_recaptcha(request):
                tip = form.save()
                code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
                while Tip.objects.filter(code=code).__len__() > 0:
                    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
                tip.code = code
                tip.save()
                ret = {'code': code}
                return render(request, 'success.html', ret)
        except Exception as e:
            print e
    else:
        form = AnonForm()

    return render(request, 'home.html', {'form': form})


def search(request):
    try:
        if request.method == 'POST' and verify_recaptcha(request):
            tip = Tip.objects.get(code=request.POST.get('code'))
            ret={'message':tip.response}
            return render(request,'reply.html',ret)
        elif request.method == 'GET':
            return render(request, 'reply.html')
    except Exception as e:
        print e
    return HttpResponseRedirect("/")


def tips(request):
    tip_list = Tip.objects.all()
    ret={}
    ret['tips']=tip_list
    return render(request,'tips.html',ret)


def view_tip(request):
    if request.method == "GET":
        t=Tip.objects.get(pk=request.GET.get("pk"))
        form = AnonForm(instance=t)

        return render(request, 'tip.html', {'form': form, 'response':t.response})
    tip = Tip.objects.get(pk=request.GET.get("pk"))
    tip.response = request.POST.get("response")
    tip.save()
    return redirect("/tips/")
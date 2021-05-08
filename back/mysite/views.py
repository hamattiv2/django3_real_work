import os
from urllib import request, parse
import json, ssl
import payjp
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.models import Article
from mysite.forms import UserCreateForm, ProfileForm
# Create your views here.

def indexview(request):
    context = {
        'ranks': Article.objects.all().order_by('-count')[:2],
        'articles': Article.objects.all()[:3]
    }
    return render(request, 'mysite/index.html', context)


def loginview(request):
    context = {}

    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('index')
        else:
            context['error_messages'] = 'メールアドレスかパスワードが誤っています'
    else:
        if request.user.is_authenticated:
            return render(request, 'mysite/index.html', context)
        else:
            return render(request, 'mysite/register/login.html', context)


def logoutview(request):
    logout(request)
    return redirect('login')


def signupview(request):
    context = {}
    
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
            messages.success(request, 'ユーザー登録が完了しました')
            login(request, user)
            return redirect('index')
        else:
            context['error_messages'] = form.errors
    return render(request, 'mysite/register/signup.html', context)


@login_required
def mypageview(request):
    context = {
            'form': ProfileForm(instance=request.user.profile)
        }
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'プロフィールの更新が完了しました')
            return render(request, 'mysite/register/mypage.html', context)
    else:
        return render(request, 'mysite/register/mypage.html', context)


def contactview(request):
    context = {
        'recaptcha_site_key': os.environ['RECAPTCHA_SITE_KEY']
    }
    if request.method == 'POST':
        recaptcha_token = request.POST.get('g-recaptcha-response')
        res = grecaptcha_request(recaptcha_token)
        if not res:
            messages.error(request, 'reCaptcha認証に失敗しました')
            return render(request, 'mysite/contact.html', context)

        subject = 'お問い合わせ'
        message = request.POST.get('contact')
        email_from = os.environ['EMAIL_HOST_USER']
        email_to = [request.POST.get('email'), os.environ['EMAIL_HOST_USER']]
        try:
            send_mail(subject, message, email_from, email_to)
            messages.success(request, 'お問い合わせが完了しました')
            redirect('contact')
        except Exception as e:
            messages.error(request, 'お問い合わせに失敗しました')
    
    return render(request, 'mysite/contact.html', context)

def grecaptcha_request(token):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    url = "https://www.google.com/recaptcha/api/siteverify"
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    data = {
        'secret': os.environ['RECAPTCHA_SECRET_KEY'],
        'response': token,
    }
    data = parse.urlencode(data).encode()
    req = request.Request(
        url,
        method="POST",
        headers=headers,
        data=data,
    )
    f = request.urlopen(req, context=context)
    response = json.loads(f.read())
    f.close()
    return response['success']


def donateview(request):
    context = {
        'public_key': os.environ['PAYJP_PUBLIC_KEY']
    }

    payjp.api_key = os.environ['PAYJP_SECRET_KEY']

    if request.method == 'POST':
        customer = payjp.Customer.create(
                        email='pykensyo@gmail.com',
                        card=request.POST.get('payjp-token')
                    )
        charge = payjp.Charge.create(
                    amount=request.POST.get('amount'),
                    currency='jpy',
                    customer=customer.id,
                    description='寄付テスト'    
                )
        context['charge'] = charge

        subject = '寄付完了'
        message = '{}円の寄付が完了したしました。\nありがとうございます'.format(request.POST.get('amount'))
        email_from = os.environ['EMAIL_HOST_USER']
        email_to = [request.POST.get('email')]
        send_mail(subject, message, email_from, email_to)
        messages.success(request, '寄付が完了しました')
        return redirect('donate')

    return render(request, 'mysite/donate.html', context)

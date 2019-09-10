#coding: utf-8
from django.shortcuts import render
from django.core.mail import send_mail
from service.models import Services
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    service = Services.objects.order_by('-id')[:1]
    h_water = service[0].hot_water
    c_water = service[0].cold_water
    n = '\n'
    message = '{}{}{}{}{}{}{}'.format('Огородная 93/95, кв. 84', n, 'Горячая вода: ', str(h_water), n, 'Холодная вода: ', str(c_water))
    context = {
        'title': 'Отправить показания водяных счетчиков',
        'message' : message
                     }
    return render(request, 'send_mail/index.html', context)
@login_required
def success(request): 
    #today = timezone.now()
    month = timezone.now().strftime('%B')
    year = timezone.now().strftime('%Y')
    theme = 'Показания счетчиков за ' + month + ' ' + year
    email = request.POST.get('email', '')
    message = request.POST.get('message', '')
    send_mail(theme, str(message), 'neex@nm.ru', [email], fail_silently=False)
    return render(request, 'send_mail/success.html')
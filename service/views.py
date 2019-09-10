
from django.shortcuts import render, redirect
from service.models import Services, Consumption
from .forms import AddForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



def home(request):
    
    service = Services.objects.order_by('-id')
    paginator = Paginator(service, 6)
    page = request.GET.get('page')
    service = paginator.get_page(page)
    context = {
        'service': service,
        'title': 'Показания счетчиков',
               }
    
    return render(request, 'service/index.html', context)

@login_required
def consuming(request):
    
    consumption = Consumption.objects.order_by('-id')
    paginator = Paginator(consumption, 6)
    page = request.GET.get('page')
    consumption = paginator.get_page(page)
    context = {
        'consumption': consumption,
        'title': 'Расход',
               }
    return render(request, 'service/consumption.html', context)

@login_required
def consuming_upd(request):
    
    Consumption.objects.all().delete()
    service = Services.objects.all()
    
    for item in range (len(service)-1):
        hot_water = service[item+1].hot_water - service[item].hot_water
        cold_water = service[item+1].cold_water - service[item].cold_water
        electricity = service[item+1].electricity - service[item].electricity
        gaz = service[item+1].gaz - service[item].gaz
        pub_date = service[item+1].pub_date
        consumption = Consumption.objects.create(hot_water=hot_water,
                                                cold_water=cold_water,
                                                electricity=electricity,
                                                gaz=gaz,
                                                pub_date=pub_date
                                                    )
        consumption.save()
    consumption = Consumption.objects.order_by('-id')
    paginator = Paginator(consumption, 6)
    page = request.GET.get('page')
    consumption = paginator.get_page(page)
    context = {
        'consumption': consumption,
        'title': 'Расход',
               }
    return render(request, 'service/consumption.html', context)


@login_required
def add(request):
    

    if request.method == "POST":
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.pub_date = timezone.now()
            service.save()
            service = Services.objects.order_by('-id')[:2]
            hot_water = service[0].hot_water - service[1].hot_water
            cold_water = service[0].cold_water - service[1].cold_water
            electricity = service[0].electricity - service[1].electricity
            gaz = service[0].gaz - service[1].gaz
            consumption = Consumption.objects.create(hot_water=hot_water,
                                                     cold_water=cold_water,
                                                     electricity=electricity,
                                                     gaz=gaz,
                                                     pub_date=timezone.now()
                                                    )
            consumption.save()
            return redirect('service:home')
    else:
        form = AddForm()
    context = {
        'form': form,
        'title': 'Добавить показания счетчиков',
               }
    return render(request, 'service/add.html', context)

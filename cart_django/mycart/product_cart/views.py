from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, Http404
from .models import Product, Cart, Estimation, Comit, Answer_comit, Clik, \
    Plyer, Level
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import matplotlib.pyplot as plt
import os
from loguru import logger


def index(request):
    product_list = Product.objects.all()
    comit_list = Comit.objects.all()
    for product in product_list:
        Estimation.objects.get_or_create(
            product=product)

    estimation_dict = {estimation.product.id: estimation for estimation in
                       Estimation.objects.all()}
    comit_dict = {product.id: Comit.objects.filter(product=product) for product
                  in product_list}
    answer_comit = {comit.id: Answer_comit.objects.filter(comit=comit) for
                    comit in comit_list}

    context = {
        'answer_comit': answer_comit,
        'product_list': product_list,
        'estimation_dict': estimation_dict,
        'comit_dict': comit_dict
    }
    return render(request, 'product_cart/index.html', context=context)


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        Cart.objects.create(product=product)
        return redirect('index')
    return HttpResponse("Invalid request", status=400)


def cart(request):
    product_list = Cart.objects.all()
    context = {
        'product_list': product_list
    }
    return render(request, 'product_cart/cart.html', context=context)


def delete_cart(request):
    print(request.method)
    if request.method == "POST":
        cart_id = request.POST.get('cart_id')
        Cart.objects.filter(id=cart_id).delete()
        return redirect('cart')
    return HttpResponse("Invalid request", status=400)


def estimation(request):
    if request.method == 'POST':
        laik = request.POST.get('laik')
        dlaik = request.POST.get('dlaik')
        product_id = request.POST.get('product_id')
        estimation_instance = Estimation.objects.get(product_id=product_id)

        if laik:
            estimation_instance.laik += 1
            estimation_instance.save()
        elif dlaik:
            estimation_instance.dlaik += 1
            estimation_instance.save()

        return redirect('index')

    return HttpResponse("Invalid request", status=400)


def comit(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        comment_text = request.POST.get('comit')
        Comit.objects.create(product=product, comit=comment_text)
        return redirect('index')
    return HttpResponse("Invalid request", status=400)


def answer_comit(request):
    if request.method == 'POST':
        comit_id = request.POST.get('comit_id')
        comit = Comit.objects.get(id=comit_id)
        comment_text = request.POST.get('answer_comit')
        Answer_comit.objects.create(comit=comit, answer=comment_text)
        return redirect('index')
    return HttpResponse("Invalid request", status=400)


def calculation(request):
    if request.method == 'POST':
        list_a = [['' for i in range(6)] for j in range(6)]
        list_a[0][0] = int(request.POST.get('x1'))
        list_a[0][-1] = int(request.POST.get('x2'))
        list_a[-1][0] = int(request.POST.get('x3'))
        list_a[-1][-1] = int(request.POST.get('x4'))

        delt = list_a[0][0] - list_a[0][-1]
        delt2 = list_a[-1][0] - list_a[-1][-1]

        for i in range(6):
            if list_a[0][i] == '':
                list_a[0][i] = list_a[0][i - 1] - (delt / 4)

        for i in range(6):
            if list_a[-1][i] == '':
                list_a[-1][i] = list_a[-1][i - 1] - (delt2 / 4)

        delt_x = [(list_a[0][i] - list_a[-1][i]) for i in range(6)]

        for i in range(6):
            for j in range(6):
                if list_a[i][j] == '':
                    list_a[i][j] = list_a[i - 1][j] - (delt_x[j] / 4)

        plt.imshow(list_a, cmap="coolwarm", interpolation="nearest")
        plt.colorbar()
        plt.title("Тепловая карта")
        image_path = os.path.join(settings.MEDIA_ROOT, 'heatmap.png')
        plt.savefig(image_path)
        plt.close()

        context = {
            'list_a': list_a,
            'image_path': image_path
        }

        download_file(request)

        return render(request, 'product_cart/calculation.html',
                      context=context)

    return render(request, 'product_cart/calculation.html')


def download_file(request):
    # абсолютный путь к файлу на сервере
    file_path = os.path.join(settings.MEDIA_ROOT, 'heatmap.png')

    if not os.path.exists(file_path):
        raise Http404("Файл не найден")

    # открываем файл в бинарном режиме и возвращаем его клиенту
    response = FileResponse(open(file_path, 'rb'),
                            as_attachment=True,
                            # принудительно скачивать
                            filename='heatmap.png'
                            # имя файла у клиента
                            )
    return response


logger.add("file_log.log", rotation='10 mb', level='DEBUG')


class ClickCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clik
        fields = ['count']


class ClickCounterView(APIView):
    def get(self, request):
        logger.debug("GET cliker")
        ip = get_client_ip(request)
        plyer = Plyer.objects.get_or_create(ip=ip)[0]

        counter, created = Clik.objects.get_or_create(plaer=plyer)
        level, created = Level.objects.get_or_create(plaer=plyer)

        serializer = ClickCounterSerializer(counter)
        data = {
            'count': serializer.data['count'],
            'level': level.level
        }
        return Response(data)

    def post(self, request):
        logger.debug("Post clicer!")
        ip = get_client_ip(request)
        plyer = Plyer.objects.get_or_create(ip=ip)[0]
        level, created = Level.objects.get_or_create(plaer=plyer)

        counter, created = Clik.objects.get_or_create(plaer=plyer)
        if level.level == 1:
            counter.count += 1
            counter.save()
        elif level.level == 2:
            counter.count += 5
            counter.save()
        elif level.level == 3:
            counter.count += 10
            counter.save()
        elif level.level == 4:
            counter.count += 50
            counter.save()
        elif level.level == 5:
            counter.count += 150
            counter.save()
        elif level.level == 6:
            counter.count += 300
            counter.save()
        elif level.level == 7:
            counter.count += 10000
            counter.save()
        #logger.debug("Изменение счета")
        serializer = ClickCounterSerializer(counter)
        data = {
            'count': serializer.data['count'],
            'level': level.level
        }
        return Response(data)


def clic(request):
    ip = get_client_ip(request)
    playr = Plyer.objects.get_or_create(ip=ip)
    if not playr:
        Plyer.objects.create(plyer=ip)

    return render(request, 'product_cart/clik.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PurchaseLevelView(APIView):
    def post(self, request):
        #logger.debug("POST purchaser")
        ip = get_client_ip(request)
        plyer = Plyer.objects.get_or_create(ip=ip)[0]
        counter, created = Clik.objects.get_or_create(plaer=plyer)
        level, created = Level.objects.get_or_create(plaer=plyer)
        prais = [0, 10, 500, 1000, 1500, 3000, 5000, 10000]

        if level.level < 7 and counter.count >= prais[level.level]:
            counter.count = counter.count - prais[level.level]
            counter.save()
            level.level += 1
            level.save()

        return Response({'level': level.level, 'count': counter.count})


class AutoClick(APIView):
    def post(self, request):

        ip = get_client_ip(request)
        plyer = Plyer.objects.get_or_create(ip=ip)[0]
        counter, created = Clik.objects.get_or_create(plaer=plyer)
        level, created = Level.objects.get_or_create(plaer=plyer)

        if level.level == 7 and counter.count >= 1000:
            counter.count -= 1000
            counter.save()
            level.level += 1
            level.save()

        return Response({'level': level.level, 'count': counter.count})


class ErrorCheck(APIView):
    def get(self, request):
        log_content = ''
        log = open("C:/Users/Home/Documents/test/cart_django/mycart/file_log.log", 'r')
        print(log)
        if not log.read():
            message = 'Нет ошибок или лог не найден.'
        else:
            message = 'Error'
        log.close()

        return render(request, 'product_cart/error.html',
                      {'log_content': message})


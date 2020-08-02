from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Douban
from django.db.models import Avg

def hello(request):
    return HttpResponse("Welcome to use Django!")

def index(request):
    shorts = Douban.objects.all()
    # 评论数量
    counter = Douban.objects.all().count()

    # 平均星级
    # star_value = T1.objects.values('n_star')
    star_avg = f" {Douban.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f} "

    # 情感倾向
    sent_avg = f" {Douban.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = Douban.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = Douban.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()
    return render(request, 'result.html', locals())



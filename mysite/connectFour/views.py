from django.shortcuts import render
from django.http import HttpResponse
import sys
from connectFour.ApiConnectFour import apiConnectFour
#url(r'^products/$', 'viewname', name='urlname')

print("===========================")
print(sys.path)
print("===========================")


def index(request):
        TEMPLATE_DIRS = ('/home/django/myproject/templates',)
        return render(request, './index.html')


def api(request):
    board = request.GET['board']
    player = request.GET['player']
    return HttpResponse(apiConnectFour(board,player))
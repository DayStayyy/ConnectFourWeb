from django.http import HttpResponse
from Api.backends.ApiConnectFour import apiConnectFour

# Create your views here.

def apiConnectFourF(request):
    board = request.GET['board']
    level = request.GET['level']
    return HttpResponse(apiConnectFour(board,level))

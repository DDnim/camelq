
from camelq.server_trade import bitflyer, binance
from camelq.struct_account import account
from django.shortcuts import render

def main(request):
    context          = {}
    return render(request, 'home.html', context)
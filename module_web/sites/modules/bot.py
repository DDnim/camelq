from django.shortcuts import render
from camelq.module_bot import TestTrade_MA20180721

def main(request):
    context          = {}
    d_server = TestTrade_MA20180721.quant()
    context['datas'] = d_server.run()
    return render(request, 'bot.html', context)
from camelq.server_data import cyptowat 
import json, datetime
from django.shortcuts import render, HttpResponse


def main(request):
    context          = {}
    market_info = []
    d_server = cyptowat.cyptowat()
    l = d_server.ticker_list()
    for key ,item in l.items():
        market_info.append({'market' : key.split(":")[0], 'product' : key.split(":")[1],'price' : item})
    context['params'] =market_info

    l = d_server.get_ohlc('bitfinex', 'btcusd', '900')
    data = []
    for item in l:
        if not 0 in item[1:4]:
            data.append([datetime.datetime.fromtimestamp(item[0]).strftime('%Y/%m/%d %H:%M'), item[1], item[4],item[3],item[2]])
    context['datas'] = data

    #printmarket_info)
    return render(request, 'market.html', context)

def ohlc(request):
    market = request.GET.get('market')
    product = request.GET.get('product')
    periods = request.GET.get('periods')
    d_server = cyptowat.cyptowat()
    l = d_server.get_ohlc(market, product, periods)
    data = []
    for item in l:
        if not 0 in item[1:4]:
            data.append([datetime.datetime.fromtimestamp(item[0]).strftime('%Y/%m/%d %H:%M'),item[1],item[4],item[3],item[2]])
    return HttpResponse(json.dumps(data), content_type="application/json")
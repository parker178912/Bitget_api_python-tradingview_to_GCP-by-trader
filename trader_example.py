import bitget.mix.market_api as market
import bitget.mix.account_api as accounts
import bitget.mix.position_api as position
import bitget.mix.order_api as order
import bitget.mix.plan_api as plan
import bitget.mix.trace_api as trace
import json, time, hmac, base64, requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    api_key = ""        # put your api_key
    secret_key = ""     # put your secret_key
    passphrase = ""     # put your passphrase

    orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
    closeApi = trace.TraceApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
    # get Tradingview message
    data = json.loads(request.data)
    # depends on your stategy order_id on tradingview
    if data['strategy']['order_id'] == 'Long Exit':
        data['strategy']['order_id'] = 'close_long'
    if data['strategy']['order_id'] == 'Short Exit':
        data['strategy']['order_id'] = 'close_short'    
    if data['strategy']['order_id'] == 'Short Entry':
        data['strategy']['order_id'] = 'open_short'
    if data['strategy']['order_id'] == 'Long Entry':
        data['strategy']['order_id'] = 'open_long' 
    if data['strategy']['order_id'] == 'Close entry(s) order Long Entry':
        data['strategy']['order_id'] = 'close_long'
    if data['strategy']['order_id'] == 'Close entry(s) order Short Entry':
        data['strategy']['order_id'] = 'close_short' 
    
    if data['ticker'] == 'BTCUSDT.P':
        data['ticker'] = 'BTCUSDT'
    if data['ticker'] == 'ETHUSDT.P':
        data['ticker'] = 'ETHUSDT'   
        
    data['strategy']['position_size'] = abs(data['strategy']['position_size'])
    
    if (data['strategy']['order_id'] == 'open_long' or data['strategy']['order_id'] == 'open_short'):
        tracking = closeApi.current_track(symbol=data['ticker']+'_UMCBL', productType='umcbl', pageSize=20, pageNo=1)       
        if len(tracking['data'])!=0:
            trackingNo1 = tracking['data'][0]['trackingNo']
            closeApi.close_track_order(symbol=data['ticker']+'_UMCBL',trackingNo=trackingNo1)              
        orderApi.place_order(symbol=data['ticker']+'_UMCBL', marginCoin='USDT', size=data['strategy']['position_size'],side=data['strategy']['order_id'], orderType='market', timeInForceValue='normal')
    elif (data['strategy']['order_id'] == 'close_long' or data['strategy']['order_id'] == 'close_short'):
        tracking = closeApi.current_track(symbol=data['ticker']+'_UMCBL', productType='umcbl', pageSize=20, pageNo=1)
        trackingNo1 = tracking['data'][0]['trackingNo']
        closeApi.close_track_order(symbol=data['ticker']+'_UMCBL',trackingNo=trackingNo1)              
    return{
        'message':'success'
    }
## Bitget_api_python tradingview_to_heroku by trader
`用python將tradingview的訊息打包後發送開平倉訊息至heroku雲端站台`
 
### bitget 資料夾
>裡面放了bitget預設的指令，若有需要可以在程式內利用import去提取
```
import bitget.mix.order_api as order
```
### app、requirements
>使用GCP當作雲端站台時所需要的子項目

### trader_example
> 交易員開平倉程式碼範例

### tradingview_msg_example
>在tradingview alert中訊息欄所放置之訊息，可藉由快訊提取自己所需的部分在程式中使用

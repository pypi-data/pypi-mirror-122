# alphav_client_python

A simple API client for the AlphaVantage API: https://www.alphavantage.co/documentation/ 

Desenvolvido durante o curso > InovAção Afro - CESAR / SHARE RH

by @blogdomarcio (Claudio Marcio)

## Time Series Stock APIs

```
Funções: 

- intraday_series
- daily_series
- daily_adjusted_series
- weekly_series
- weekly_adjusted_series
- monthly_series
- monthly_adjusted_series
- quote_series
```

<pre>

from alphav_client_python import stock_series

stock = stock_series.StockTimeSeries()

d1 = astock.intraday_series('TIME_SERIES_WEEKLY', 'IBM', 60min', slice='year1month1')
print('intraday_series', d1)

d2 = stock.daily_series('TIME_SERIES_WEEKLY', 'IBM',)
print('daily_series', d2)

d3 = stock.daily_adjusted_series('TIME_SERIES_WEEKLY', 'IBM',)
print('daily_adjusted_series', d3)

d4 = stock.weekly_series('TIME_SERIES_WEEKLY', 'IBM')
print('weekly_series', d4)  

d5 = stock.weekly_adjusted_series('TIME_SERIES_WEEKLY', 'IBM',)
print('daily_series', d5)

d6 = stock.monthly_series('TIME_SERIES_WEEKLY', 'IBM',)
print('daily_adjusted_series', d6)

d7 = stock.weekly_adjusted_series('TIME_SERIES_WEEKLY', 'IBM',)
print('daily_series', d7)

d8 = stock.monthly_series('TIME_SERIES_WEEKLY', 'IBM',)
print('daily_adjusted_series', d8)

</pre>

## Crypto Currencies
```
Função:

currency_exchange_rate
```
<pre>

from alphav_client_python import cryptocurrencies

crypto = cryptocurrencies.CryptoCurrencies()

d1 = crypto.currency_exchange_rate('CURRENCY_EXCHANGE_RATE', 'BTC', 'CNY',)
print('Realtime Currency Exchange Rate', d1['Realtime Currency Exchange Rate'])

</pre>

## Technical Indicators

```
Funções: 

- sma
- ema
```
<pre>

from alphav_client_python import tecnical_indicators

tech = tecnical_indicators.TechnicalIndicators()

d1 = tech.sma('SMA', 'IBM', 'weekly', '10', 'open')
print('sma', d1['Technical Analysis: SMA'])

d2 = tech.ema('EMA', 'IBM', 'weekly', '10', 'open')
print('ema', d2['Technical Analysis: EMA'])

</pre>
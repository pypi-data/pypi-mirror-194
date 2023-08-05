# BOTGUS

INDICADORES DE BOT GUS / 19 INDICADORES EN PYTHON BY FRANCISCO ALAS

## Indicador RSI

- Formato de función: `rsi(datos, venta_rsi, compra_rsi, rsi_periodo, ema_rsi, ema_mediamovil, ema_longitud, habilita_cruce)`
- Forma de llamar: `senial_rsi = botgus.rsi(datos, int(70), int(30), int(14), str("ema"), str("sma"), int(5), str("si"))`
- Función devuelve: `comprar`, `vender`, `ninguna`

## Indicador Bandas de Bollinger

- Formato de función: `bb(datos, precio_actual, porcentaje_banda_arriba, porcentaje_banda_abajo, longitud, desviacion)`
- Forma de llamar: `senial_bb = botgus.bb(datos, float(precio), float(0.05), float(0.05), int(5), int(2))`
- Función devuelve: `comprar`, `vender`, `ninguna`

## Indicador Medias Móviles

- Formato de función: `ma(datos, periodo, periodo1, ma_tipo)`
- Forma de llamar: `senial_ma = botgus.ma(datos, int(5), int(20), str("sma"))`
- Función devuelve: `comprar`, `vender`, `ninguna`

## Indicador Bloque de Órdenes

- Formato de función: `ob(datos, periodo, umbral)`
- Forma de llamar: `senial_ob = botgus.ob(datos, int(2), float(0.0))`
- Función devuelve: `comprar`, `vender`, `ninguna`

## Indicador Supertrend

- Formato de función: `supertrend(datos, atr_longitud, factor, numero_velas)`
- Forma de llamar: `senial_supertrend = botgus.supertrend(datos, int(10), int(3), int(2))`
- Función devuelve: `comprar`, `vender`, `ninguna`

## Indicador Estocástico

- Formato de función: `estocastico(df, k_periodo, d_periodo, arriba_k, arriba_d, abajo_k, abajo_d, solo_estocasticok)`
- Forma de llamar: `senial_estocastico = botgus.estocastico(datos, int(14), int(3), int(80), int(80), int(20), int(20), str("no"))`
- Función devuelve: `comprar`, `vender`, `ninguna`

## Indicador Ichimoku

- Formato de función: `ichimoku(data, conversion_line_periods, base_line_periods, leading_span_b_length, lagging_span_length)`
- Forma de llamar: `senial_ichimoku = botgus.ichimoku(datos, int(9), int(26), int(52), int(26))`
- Función devuelve: `comprar`, `vender`, `ninguna`

## INDICADOR MACD

-Formato de funcion: `macd(df,rapidaema,lentoema,senialperiodo,usar_divergencia,cruce)`
-Forma de llamar: `senial_macd=botgus.macd(datos,int(12),int(26),int(9),"si","si")`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR TENDENCIA

-Formato de funcion: `tendencia(df,cualma,ma1,ma2,ma3)`
-Forma de llamar: `senial_tendencia=botgus.tendencia(datos,str("sma"),int(20),int(50),int(100))`
-Funcion devuelve: `ALCISTA`,`TENDICIA ALCISTA INICIA`,`BAJISTA`,`TENDENCIA BAJISTA INICIA`

## INDICADOR PIVOTES

-Formato de funcion: `pivot(df,tipo)`
-Forma de llamar: `pp,so1,re1,so2,re2=botgus.pivot(datospivot,"tradicional")`
Tipos de pivot: `tradicional,classic,fibonacci,woodie,camarilla`
-Funcion devuelve: `pp,so1,re1,so2,re2`

## INDICADOR DMI

-Formato de funcion: `dmi(df,period,perioddi)`
-Forma de llamar: `senial_dmi=botgus.dmi(datos,int(14),int(14))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR AROON

-Formato de funcion: `aroon(df,periodoaron)`
-Forma de llamar: `senial_aroon=botgus.aroon(datos,int(14))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR CHANDELIER EXIT

-Formato de funcion: `ce(df, atr_period, atrmulti)`
-Forma de llamar: `senial_ce=botgus.ce(datos,int(22),int(3))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR RVI

-Formato de funcion: `rvi(df, longitud)`
-Forma de llamar: `senial_rvi=botgus.rvi(datos,int(10))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR WILLIAM %R

-Formato de funcion: `william_r(df,periodo,venta,compra)`
-Forma de llamar: `senial_williamr=botgus.william_r(datos,int(14),int(-20),int(-80))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR CANAL DE KELTNER

-Formato de funcion: `kc(df,precio,cual, longitud, multipl, atrlongi,porcentaje_banda_arriba,porcentaje_banda_abajo)`
-Forma de llamar: `senial_kc=botgus.kc(datos,float(precio),"ema",int(20),int(2),int(10),float(0.00),float(0.00))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR COPPOCK CURVE

-Formato de funcion: `coppock_curve(df, roclargo, roccorto, wma, umbral)`
-Forma de llamar: `senial_coppock=botgus.coppock_curve(datos,int(14),int(11),int(10),float(0))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR OSCILADOR ASOMBROSO

-Formato de funcion: `ao(df, corto,largo)`
-Forma de llamar: `valorasombroso=botgus.ao(datos,int(5),int(34))`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

## INDICADOR SQUEEZE MOMENTUM BY LAZYBEAR

-Formato de funcion: `squeeze_momentum(df, length, mult, lengthKC, multKC, useTrueRange)`
-Forma de llamar:  `senial_squeeze=botgus.squeeze_momentum(datos,int(20),float(2.0),int(20),float(1.5),True)`
-Funcion devuelve: `comprar`,`vender`,`ninguna`

FUNCION PARA OBTENER DATOS HISTORICOS DE BINANCE O CUALQUIER OTRO SOLO MODIFICAR CON LA API

PARA INDICADORES EJEMPLO DE FUNCION obtenerdatos()

EJEMPLO:
temporalidad="1M"
cripto="BTC"
estable="USDT"
def obtenerdatos():
    if temporalidad=="1M":
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_1MINUTE, "4 hours ago UTC")
    if temporalidad=="5M":
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_5MINUTE, "17 hours ago UTC")
    if temporalidad=="15M":
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_15MINUTE, "3 days ago UTC")
    if temporalidad=="30M":
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_30MINUTE, "5 days ago UTC")
    if temporalidad=="1H":
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_1HOUR, "9 days ago UTC")
    if temporalidad=="4H":
        klines = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_4HOUR, "34 days ago UTC")
    data = pd.DataFrame(klines)
    data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
    datos = data[['open', 'high', 'low', 'close','volume']].astype(float)
    df=datos.copy()
    return df
    
PARA EL INDICADOR PIVOT UTILIZAR DATOS HISTORICOS PARA DIARIO O SEMANAL obtenerdatospivot(tiempo)
EJEMPLO: obtenerdatospivot("diario")
def obtenerdatospivot(tiempo):
    if tiempo=="diario":
        klinesa = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_1DAY, "5 days ago UTC")
    elif tiempo=="semanal":
        klinesa = client.get_historical_klines(cripto + estable, Client.KLINE_INTERVAL_1WEEK, "2 weeks ago UTC")
    dataa = pd.DataFrame(klinesa)
    dataa.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
    df = dataa[['open','high', 'low', 'close']].astype(float)
    return df
 
MAS INFORMACION DE USO EN:
WWW.BOTGUS.COM
https://github.com/jrchico/
import pandas as pd
import numpy as np 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                          INDICADOR RSI  OK TEST 1M,5M,15M,30M,1H,4H                                                                        #
#  senial_rsi=rsi(datos,int(70),int(30),int(14),str("ema"),str("sma"),int(14),str("si"))
#  rsi(datos,venta_rsi,compra_rsi,rsi_periodo,ema_rsi,ema_mediamovil,ema_longitud,habilita_cruce)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def rsi(datos,venta_rsi,compra_rsi,rsi_periodo,ema_rsi,ema_mediamovil,ema_longitud,habilita_cruce):
    #Calcular el valor de RSI
    fuente_datos = datos['close'].astype(float).diff()
    arriba = fuente_datos.clip(lower=0)
    abajo = -1 * fuente_datos.clip(upper=0)
    if ema_rsi == "ema":
        ma_arriba = arriba.ewm(com = rsi_periodo - 1, adjust=True, min_periods = rsi_periodo).mean()
        ma_abajo = abajo.ewm(com = rsi_periodo - 1, adjust=True, min_periods = rsi_periodo).mean()
    elif ema_rsi=="sma":
        ma_arriba = arriba.rolling(rsi_periodo).mean()
        ma_abajo = abajo.rolling(rsi_periodo).mean()
    rsi_media = ma_arriba / ma_abajo
    rsi_calculo_final=100 - (100/(1 + rsi_media))
    rsi_valor = rsi_calculo_final.iloc[-1]
    senial="ninguna"
    if habilita_cruce=='si':
        # Agregamos el cálculo de la media móvil simple o exponencial
        if ema_mediamovil == 'sma':
            ma_valores = rsi_calculo_final.rolling(ema_longitud).mean()
        elif ema_mediamovil == 'ema':
            ma_valores = rsi_calculo_final.ewm(span=ema_longitud).mean()
        # Agregamos el cálculo de la media móvil
        ma_valor = ma_valores.iloc[-1]
        # cruce
        if float(rsi_valor) > float(venta_rsi) and float(rsi_valor) < float(ma_valor):
           senial="vender"
        elif float(rsi_valor) < float(compra_rsi) and float(rsi_valor) > float(ma_valor):
            senial="comprar"
        else:
            senial = 'ninguna'
    else:
        if float(rsi_valor) > float(venta_rsi):
            senial="vender"
        elif float(rsi_valor) < float(compra_rsi):
            senial="comprar"
        else:
            senial="ninguna"
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR BANDAS DE BOLLINGER   OK TEST 1M,5M,15M,30M,1H,4H                                                         #
#  senial_bb=bb(datos,float(precio),float(0.05),float(0.05),int(5),int(2))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def bb(datos,precio_actual,porcentaje_banda_arriba,porcentaje_banda_abajo, longitud, desviacion):                        
    datos['media'] = datos['close'].rolling(window=longitud).mean()
    media_movil = datos['close'].rolling(window=longitud).mean()
    desviacion_estandar = datos['close'].rolling(window=longitud).std(ddof=0)
    banda_superior = media_movil.astype(float) + desviacion * desviacion_estandar.astype(float)
    banda_inferior = media_movil.astype(float) - desviacion * desviacion_estandar.astype(float)
    ultima_media = datos['media'].iloc[-1]
    ultima_banda_superior = banda_superior.iloc[-1]
    ultima_banda_inferior = banda_inferior.iloc[-1]

    xabajo=float(ultima_banda_inferior) + ((float(porcentaje_banda_abajo)/100)*float(ultima_banda_inferior))
    valorcomprarya=float(xabajo)

    xrriba=float(ultima_banda_superior) - ((float(porcentaje_banda_arriba)/100)*float(ultima_banda_superior))
    valorgananciavender=float(xrriba)

    if float(precio_actual) >= float(valorgananciavender):
        senial="vender"
    elif float(precio_actual) <= float(valorcomprarya):
        senial="comprar"
    else:
        senial="ninguna" 

    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR MEDIAS MOVILES   OK TEST 1M,5M,15M,30M,1H,4H                                                              #
#      senial_ma=ma(datos,int(5),int(20),str("sma"))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def ma(datos, periodo, periodo1, ma_tipo):
    cierre=datos['close']
    if ma_tipo == 'sma':
        ma_1 = cierre.rolling(window=periodo).mean()
        ma_2 = cierre.rolling(window=periodo1).mean()
    elif ma_tipo == 'ema':
        ma_1 = cierre.ewm(span=periodo).mean()
        ma_2 = cierre.ewm(span=periodo1).mean()
    elif ma_tipo == 'wma':
        weights = list(range(1,periodo+1))
        ma_1 = cierre.rolling(window=periodo).apply(lambda x: np.dot(x, weights)/sum(weights))
        weights1 = list(range(1,periodo1+1))
        ma_2 = cierre.rolling(window=periodo1).apply(lambda x: np.dot(x, weights1)/sum(weights1))
    media1=ma_1.iloc[-1]
    media2=ma_2.iloc[-1]

    if float(media1) > float(media2):
        senial="comprar"
    elif float(media1) < float(media2):
        senial="vender"
    else:
        senial = "ninguna"

    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR BLOQUE DE ORDENES OK TEST 1M,5M,15M,30M,1H,4H                                                             #
#  senial_bo=botgus.ob(datos,int(2),float(0.0))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def ob(datos, periodo, umbral):
    ob_period = periodo + 1
    absmove = abs(datos['close'][ob_period] - datos['close'][1]) / datos['close'][ob_period] * 100
    relmove = absmove >= umbral
    bullishOB = datos['close'][ob_period] < datos['open'][ob_period]
    upcandles = sum([1 for i in range(1, periodo + 1) if datos['close'][i] > datos['open'][i]])
    OB_bull = bullishOB and upcandles == periodo and relmove
    bearishOB = datos['close'][ob_period] > datos['open'][ob_period]
    downcandles = sum([1 for i in range(1, periodo + 1) if datos['close'][i] < datos['open'][i]])
    OB_bear = bearishOB and downcandles == periodo and relmove
    if OB_bull:
        return "comprar"
    elif OB_bear:
        return "vender"
    else:
        return "ninguna"
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR SUPERTREND OK TEST 1M,5M,15M,30M,1H,4H                                                                    #
#  senial_supertrend=supertrend(datos,int(10),int(3),int(2))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def supertrend(datos,atr_longitud,factor,numero_velas):
    price_diffs = [datos['high'].astype(float) - datos['low'].astype(float),datos['high'].astype(float) - datos['close'].astype(float).shift(),datos['close'].astype(float).shift() - datos['low'].astype(float)]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    atr = true_range.ewm(alpha=1/atr_longitud,min_periods=atr_longitud).mean() 
    hl2 = (datos['high'].astype(float) + datos['low'].astype(float)) / 2
    final_upperband = upperband = hl2 + (factor * atr)
    final_lowerband = lowerband = hl2 - (factor * atr)
    supertrend = [True] * len(datos)
    for i in range(1, len(datos.index)):
        curr, prev = i, i-1
        if datos['close'].astype(float)[curr] > final_upperband[prev]:
            supertrend[curr] = True
        elif datos['close'].astype(float)[curr] < final_lowerband[prev]:
            supertrend[curr] = False
        else:
            supertrend[curr] = supertrend[prev]
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]
        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan
    lista=pd.DataFrame({'Supertrend': supertrend}, index=datos.index)
    super8=lista.iloc[-8].bool()
    super7=lista.iloc[-7].bool()
    super6=lista.iloc[-6].bool()
    super5=lista.iloc[-5].bool()
    super4=lista.iloc[-4].bool()
    super3=lista.iloc[-3].bool()
    super2=lista.iloc[-2].bool()
    super1=lista.iloc[-1].bool()

    if numero_velas==1:
        if super1==True and super2==False and super3==False:
            seniales="comprar"
        elif super1==False and super2==True and super3==True:
            seniales="vender"
        else:
            seniales="ninguna" 

    elif numero_velas==2:
        if super1==True and super2==True and super3==False and super4==False:
            seniales="comprar"

        elif super1==False and super2==False and super3==True and super4==True:
            seniales="vender"
        else:
            seniales="ninguna" 
    elif numero_velas==3:
        if super1==True and super2==True and super3==True and super4==False and super5==False:
            seniales="comprar"

        elif super1==False and super2==False and super3==False and super4==True and super5==True:
            seniales="vender"
        else:
            seniales="ninguna" 
    elif numero_velas==4:
        if super1==True and super2==True and super3==True and super4==True and super5==False and super6==False:
            seniales="comprar"
        elif super1==False and super2==False and super3==False and super4==False and super5==True and super6==True:
            seniales="vender"
        else:
            seniales="ninguna" 
    elif numero_velas==5:
        if super1==True and super2==True and super3==True and super4==True and super5==True and super6==False and super7==False:
            seniales="comprar"
        elif super1==False and super2==False and super3==False and super4==False and super5==False and super6==True and super7==True:
            seniales="vender"
        else:
            seniales="ninguna" 
    elif numero_velas==6:
        if super1==True and super2==True and super3==True and super4==True and super5==True and super6==True and super7==False and super8==False:
            seniales="comprar"
        elif super1==False and super2==False and super3==False and super4==False and super5==False and super6==False and super7==True and super8==True:
            seniales="vender"
        else:
            seniales="ninguna" 
   
    return seniales
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR ESTOCASTICO OK TEST 1M,5M,15M,30M,1H,4H                                                                   #
#    senial_estocastico=estocastico(datos,int(14),int(3),int(80),int(80),int(20),int(20),str("no"))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def estocastico(df,k_periodo,d_periodo,arriba_k,arriba_d,abajo_k,abajo_d,solo_estocasticok):
    high_roll = df["high"].rolling(k_periodo).max()
    low_roll = df["low"].rolling(k_periodo).min()
    num = df["close"].astype(float) - low_roll.astype(float)
    denom = high_roll.astype(float) - low_roll.astype(float)
    df["%K"] = (num / denom) * 100
    df["%D"] = df["%K"].rolling(d_periodo).mean()
    estocasticok=df["%K"].iloc[-1]
    estocasticod=df["%D"].iloc[-1]
    if solo_estocasticok=="si":
        if float(estocasticok) >= float(arriba_k):
            senial="vender"
        if float(estocasticok) <= float(abajo_k):
            senial="comprar"
        else:
            senial="ninguna"  
    else:
        if float(estocasticok) >= float(arriba_k) and float(estocasticod) >= float(arriba_d) and float(estocasticok) < float(estocasticod):
            senial="vender"
        if float(estocasticok) <= float(abajo_k) and float(estocasticod) <= float(abajo_d) and float(estocasticok) > float(estocasticod):
            senial="comprar"
        else:
            senial="ninguna" 
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR ICHIMOKU OK TEST 1M,5M,15M,30M,1H,4H                                                                      #
#   senial_ichimoku=ichimoku(datos,int(9),int(26),int(52),int(26))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def ichimoku(data, conversion_line_periods, base_line_periods, leading_span_b_length, lagging_span_length):
    high_prices = data['high']
    low_prices = data['low']
    close_prices = data['close']
    tenkan_sen = (high_prices.rolling(window=conversion_line_periods).max() + low_prices.rolling(window=conversion_line_periods).min()) / 2
    kijun_sen = (high_prices.rolling(window=base_line_periods).max() + low_prices.rolling(window=base_line_periods).min()) / 2
    leading_span_a = ((tenkan_sen + kijun_sen) / 2).shift(base_line_periods)
    leading_span_b = ((high_prices.rolling(window=leading_span_b_length).max() + low_prices.rolling(window=leading_span_b_length).min()) / 2).shift(base_line_periods)
    lagging_span = close_prices.shift(-lagging_span_length)
    data['tenkan_sen'] = tenkan_sen
    data['kijun_sen'] = kijun_sen
    data['leading_span_a'] = leading_span_a
    data['leading_span_b'] = leading_span_b
    data['lagging_span'] = lagging_span
    if float(tenkan_sen.iloc[-1]) > float(kijun_sen.iloc[-1]):
        senial = "comprar"
    elif float(tenkan_sen.iloc[-1]) < float(kijun_sen.iloc[-1]):
        senial = "vender"
    else:
        senial = "ninguna"
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR MACD OK TEST 1M,5M,15M,30M,1H,4H                                                                          #
#       senial_macd=macd(datos,int(12),int(26),int(9),"si","si")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def macd(df,rapidaema,lentoema,senialperiodo,usar_divergencia,cruce):
    k = df['close'].ewm(span=rapidaema, adjust=False, min_periods=rapidaema).mean()
    d = df['close'].ewm(span=lentoema, adjust=False, min_periods=lentoema).mean()
    macd = k - d
    macd_s = macd.ewm(span=senialperiodo, adjust=False, min_periods=senialperiodo).mean()
    macd_h = macd - macd_s
    macdb=macd.iloc[-1]
    macdsenial=macd_s.iloc[-1]
    if cruce=="si":
        # Buscar divergencia bajista
        if df['close'].iloc[-1] > df['close'].iloc[-2] and macd.iloc[-1] < macd.iloc[-2]:
            senial_divergencia = "vender"
        # Buscar divergencia alcista
        elif df['close'].iloc[-1] < df['close'].iloc[-2] and macd.iloc[-1] > macd.iloc[-2]:
            senial_divergencia = "comprar"
        else:
            senial_divergencia = "ninguna"
        # Aplicar señal MACD normal
        if float(macdb) > float(macdsenial) and float(macdb) < 0 and float(macdsenial) < 0:
            senial_normal = "comprar"
        elif float(macdb) < float(macdsenial) and float(macdb) > 0 and float(macdsenial) > 0:
            senial_normal = "vender"
        else:
            senial_normal = "ninguna"

        if usar_divergencia=="si":
            # Combinar señal normal y divergencia
            if senial_divergencia == "comprar" and senial_normal == "comprar":
                senial = "comprar"
            elif senial_divergencia == "vender" and senial_normal == "vender":
                senial = "vender"
            else:
                senial = "ninguna"
        else:
            senial=senial_normal
    else:
        if float(macdb) > 0:
            senial = "comprar"
        elif float(macdb) < 0:
            senial = "vender"
        else:
            senial = "ninguna" 

    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                            INDICADOR TENDENCIA OK TEST 1M,5M,15M,30M,1H,4H                                                                                 #
#   senial_tendencia=tendencia(datos,str("sma"),int(20),int(50),int(100))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def tendencia(df,cualma,ma1,ma2,ma3):
    if cualma=="sma":
        mavalor1 = df['close'].rolling(ma1).mean().iloc[-1]
        mavalor2 = df['close'].rolling(ma2).mean().iloc[-1]
        mavalor3 = df['close'].rolling(ma3).mean().iloc[-1]
    elif cualma=="ema":
        mavalor1 = df['close'].ewm(span=ma1, min_periods=ma1).mean().iloc[-1]
        mavalor2 = df['close'].ewm(span=ma2, min_periods=ma2).mean().iloc[-1]
        mavalor3 = df['close'].ewm(span=ma3, min_periods=ma3).mean().iloc[-1]

    if float(mavalor1) > float(mavalor2) and float(mavalor1) > float(mavalor3):
        senial="ALCISTA"

    if float(mavalor1) > float(mavalor2) and float(mavalor1) < float(mavalor3):
        senial="TENDICIA ALCISTA INICIA"

    if float(mavalor1) < float(mavalor2) and float(mavalor1) < float(mavalor3):
        senial="BAJISTA"

    if float(mavalor1) < float(mavalor2) and float(mavalor1) > float(mavalor3):
        senial="TENDENCIA BAJISTA INICIA"

    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                            INDICADOR PIVOTES OK TEST 1M,5M,15M,30M,1H,4H                                                                                   #
#  pp,so1,re1,so2,re2=pivot(datospivot,"tradicional")
#  para esto usamos los datos diario o semanal
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def pivot(df,tipo):
    alto=df['high'].iloc[-2]
    bajo=df['low'].iloc[-2]
    cierre=df['close'].iloc[-2]
    open=df['open'].iloc[-1]

    if tipo=="tradicional":
        pp = ((alto + bajo + cierre))/3
        re1 = (pp *2) - bajo
        so1 = (pp *2) - alto
        re2 = pp  + (alto - bajo)
        so2 = pp - (alto - bajo)

    if tipo=="classic":
        pp = ((alto + bajo + cierre))/3
        pivot_range = alto - bajo
        re1 = (pp *2) - bajo
        so1 = (pp *2) - alto
        re2 = pp  + 1 * pivot_range
        so2 = pp  - 1 * pivot_range
    elif tipo=="fibonacci":
        pp = ((alto + bajo + cierre))/3
        pivot_range = alto - bajo
        re1 = pp + 0.382 * pivot_range
        so1 = pp - 0.382 * pivot_range
        re2 = pp + 0.618 * pivot_range
        so2 = pp - 0.618 * pivot_range
    elif tipo=="woodie":
        pp = ((alto + bajo + open *2))/4
        pivot_range = alto - bajo
        re1 = pp * 2 - bajo
        so1 = pp *2 - alto
        re2 = pp + 1 * pivot_range
        so2 = pp - 1 * pivot_range
    elif tipo=="camarilla":
        pp = ((alto + bajo + cierre))/3
        pivot_range = alto - bajo
        re1 = cierre + pivot_range * 1.1 / 12.0
        so1 = cierre - pivot_range * 1.1 / 12.0
        re2 = cierre + pivot_range * 1.1 / 6.0
        so2 = cierre - pivot_range * 1.1 / 6.0


    return pp,so1,re1,so2,re2
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                            INDICADOR DMI OK TEST 1M,5M,15M,30M,1H,4H                                                                                       #
#  senial_dmi=dmi(datos,int(14),int(14))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def dmi(df,period,perioddi,conadx,umbral):
    df = df.copy()
    alphate = 1 / period
    adxperiodo = 1 / perioddi
    df['H-L'] = df['high'] - df['low']
    df['H-C'] = np.abs(df['high'] - df['close'].shift(1))
    df['L-C'] = np.abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis = 1)
    del df['H-L'], df['H-C'], df['L-C']
    df['ATR'] = df['TR'].ewm(alpha = adxperiodo, adjust = False).mean()
    df['H-pH'] = df['high'] - df['high'].shift(1)
    df['pL-L'] = df['low'].shift(1) - df['low']
    df['+DX'] = np.where((df['H-pH'] > df['pL-L']) & (df['H-pH'] > 0),df['H-pH'],0.0)
    df['-DX'] = np.where((df['H-pH'] < df['pL-L']) & (df['pL-L'] > 0),df['pL-L'],0.0)
    del df['H-pH'], df['pL-L']
    df['S+DM'] = df['+DX'].ewm(alpha = adxperiodo, adjust = False).mean()
    df['S-DM'] = df['-DX'].ewm(alpha = adxperiodo, adjust = False).mean()
    df['+DMI'] = (df['S+DM'] / df['ATR']) * 100
    df['-DMI'] = (df['S-DM'] / df['ATR']) * 100
    masx=df['+DMI'].iloc[-1]
    menosx=df['-DMI'].iloc[-1]
    df['DX'] = (np.abs(df['+DMI'] - df['-DMI']) / (df['+DMI'] + df['-DMI'])) * 100
    df['ADX'] = df['DX'].ewm(alpha = alphate, adjust = False).mean()
    del df['DX'], df['ATR'], df['TR'], df['-DX'], df['+DX'], df['+DMI'], df['-DMI']
    adxx=df['ADX'].iloc[-1]
    if conadx=="si":
        if float(masx) > float(menosx) and float(adxx) > float(umbral):
            senial="comprar"
        elif float(masx) < float(menosx) and float(adxx) > float(umbral):
            senial="vender"
        else:
            senial="ninguna" 
    else:
        if float(masx) > float(menosx):
            senial="comprar"
        elif float(masx) < float(menosx):
            senial="vender"
        else:
            senial="ninguna" 

    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                            INDICADOR AROON OK TEST 1M,5M,15M,30M,1H,4H                                                                                     #
#  senial_aroon=aroon(datos,int(14))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def aroon(df,periodoaron):
    df['up'] = 100 * df['high'].rolling(periodoaron + 1).apply(lambda x: x.argmax()) / periodoaron
    df['dn'] = 100 * df['low'].rolling(periodoaron + 1).apply(lambda x: x.argmin()) / periodoaron
    varriba=df['up'].iloc[-1]
    vabajo=df['dn'].iloc[-1]
    if float(varriba) > float(vabajo):
        senial="comprar"
    elif float(varriba) < float(vabajo):
        senial="vender"
    else:
        senial="ninguna" 
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                            INDICADOR CHANDELIER EXIT OK TEST 1M,5M,15M,30M,1H,4H                                                                           #
#  senial_ce=chandelier_exit(datos,int(22),int(3))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def ce(df, atr_period, atrmulti):
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['range'] = df['high'] - df['low']
    df['Avg TR'] = df['range'].rolling(atr_period).mean()
    rolling_high = df["high"].rolling(atr_period).max()
    rolling_low = df["low"].rolling(atr_period).min()
    comprach = rolling_high - df['Avg TR'] * atrmulti
    ventach = rolling_low + df['Avg TR'] * atrmulti
    cierre_Actual=df['close'].iloc[-1]
    compra_Actual=comprach.iloc[-1]
    venta_actual=ventach.iloc[-1]
    if float(cierre_Actual) > float(compra_Actual):
        senial="comprar"
    elif float(cierre_Actual) < float(venta_actual):
        senial="vender"
    else:
        senial="ninguna"
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR RVI OK TEST 1M,5M,15M,30M,1H,4H                                                                           #
#    senial_rvi=rvi(datos,int(10))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def rvi(df, longitud):
    open=df['open']
    close=df['close']
    high=df['high']
    low=df['low']
    a = close - open
    b = 2 * (close.shift(1) - open.shift(1))
    c = 2 * (close.shift(2) - open.shift(2))
    d = close.shift(3) - open.shift(3)
    numerator = a + b + c + d
    e = high - low
    f = 2 * (high.shift(1) - low.shift(1))
    g = 2 * (high.shift(2) - low.shift(2))
    h = high.shift(3) - low.shift(3)
    denominator = e + f + g + h
    rvi = numerator.rolling(longitud).mean() / denominator.rolling(longitud).mean()
    rvi1 = 2 * rvi.shift(1)
    rvi2 = 2 * rvi.shift(2)
    rvi3 = rvi.shift(3)
    rvi_signal = (rvi + rvi1 + rvi2 + rvi3) / 6
    rvivalor=rvi.iloc[-1]
    rvisenial=rvi_signal.iloc[-1]
    if float(rvivalor) > float(rvisenial) and float(rvivalor) < 0 and float(rvisenial) < 0:
        senial="comprar"
    elif float(rvivalor) < float(rvisenial) and float(rvisenial) > 0 and float(rvivalor) > 0:
        senial="vender"
    else:
        senial="ninguna" 
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                        INDICADOR WILLIAM OK TEST 1M,5M,15M,30M,1H,4H                                                                       #
#    senial_williamr=william_r(datos,int(14),int(-20),int(-80))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def william_r(df,periodo,venta,compra):
    highh = df['high'].rolling(periodo).max() 
    lowl = df['low'].rolling(periodo).min()
    wr = -100 * ((highh - df['close']) / (highh - lowl))
    v_william=wr.iloc[-1]
    if float(v_william) > float(venta):
        senial="vender"
    elif float(v_william) < float(compra):
        senial="comprar"
    else:
        senial="ninguna" 
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                               INDICADOR CANAL DE KELTNER OK TEST 1M,5M,15M,30M,1H,4H                                                                       #
#    senial_kc=kc(datos,float(precio),"ema",int(20),int(2),int(10),float(0.00),float(0.00))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def kc(df,precio,cual, longitud, multipl, atrlongi,porcentaje_banda_arriba,porcentaje_banda_abajo):
    tr1 = pd.DataFrame(df['high'] - df['low'])
    tr2 = pd.DataFrame(abs(df['high'] - df['close'].shift()))
    tr3 = pd.DataFrame(abs(df['low'] - df['close'].shift()))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.ewm(alpha = 1/atrlongi).mean()
    if cual=="sma":
        kc_middle = df['close'].rolling(longitud).mean()
        kc_upper = df['close'].rolling(longitud).mean() + multipl * atr
        kc_lower = df['close'].rolling(longitud).mean() - multipl * atr
    elif cual=="ema":
        kc_middle = df['close'].ewm(span=longitud, min_periods=longitud).mean()
        kc_upper = df['close'].ewm(span=longitud, min_periods=longitud).mean() + multipl * atr
        kc_lower = df['close'].ewm(span=longitud, min_periods=longitud).mean() - multipl * atr
    kc_arriba=kc_upper.iloc[-1]
    kc_abajo=kc_lower.iloc[-1]
    xabajokc=float(kc_abajo) + ((float(porcentaje_banda_abajo)/100)*float(kc_abajo))
    valorcompraryakc=float(xabajokc)
    xrribakc=float(kc_arriba) - ((float(porcentaje_banda_arriba)/100)*float(kc_arriba))
    valorgananciavenderkc=float(xrribakc)
    if float(precio) > float(valorgananciavenderkc):
        senial="vender"
    elif float(precio) < float(valorcompraryakc):
        senial="comprar"
    else:
        senial="ninguna" 

    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                               INDICADOR COPPOCK CURVE OK TEST 1M,5M,15M,30M,1H,4H                                                                          #
#      senial_coppock=coppock_curve(datos,int(14),int(11),int(10),float(0))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def coppock_curve(df, roclargo, roccorto, wma, umbral):
    close = df['close']
    differencea = close.diff(roclargo)
    nprev_valueses = close.shift(roclargo)
    longROC = (differencea / nprev_valueses) * 100
    difference = close.diff(roccorto)
    nprev_values = close.shift(roccorto)
    shortROC = (difference / nprev_values) * 100
    ROC = longROC + shortROC
    weights = np.arange(1, wma + 1)
    wma = ROC.rolling(wma).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw = True)
    valor_cc = wma.iloc[-1]
    if float(valor_cc) > float(umbral):
        senial = "comprar"
    elif float(valor_cc) < float(-umbral):
        senial = "vender"
    else:
        senial = "ninguna" 
    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                               INDICADOR ASOMBROSO OK TEST 1M,5M,15M,30M,1H,4H                                                                              #
#      valorasombroso=ao(datos,int(5),int(34))
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def ao(df, corto,largo):
    # calculamos el medio
    medio = (df['high'] + df['low']) / 2
    # calculamos las medias
    cor=medio.rolling(corto).mean()
    lar=medio.rolling(largo).mean()
    #restamos los promedios
    ocilador=cor - lar
    valor_ao=ocilador.iloc[-1]
    if float(valor_ao) > 0:
        senial="comprar"
    elif float(valor_ao) < 0:
        senial="vender"
    else:
        senial="ninguna" 

    return senial
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                               INDICADOR SQUEEZE OK TEST 1M,5M,15M,30M,1H,4H                                                                              #
#   senial_squeeze=squeeze_momentum(datos,int(20),float(2.0),int(20),float(1.5),True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def squeeze_momentum(df, length, mult, lengthKC, multKC, useTrueRange):
    source = df['close']
    tr = df['high'] - df['low']
    ma = source.rolling(window=lengthKC).mean()
    range_ma = tr.rolling(window=lengthKC).mean() if useTrueRange else source.rolling(window=lengthKC).std()
    upperKC = ma + range_ma * multKC
    lowerKC = ma - range_ma * multKC
    basis = source.rolling(window=length).mean()
    dev = mult * source.rolling(window=length).std()
    upperBB = basis + dev
    lowerBB = basis - dev
    sqzOn = (lowerBB > lowerKC) & (upperBB < upperKC)
    sqzOff = (lowerBB < lowerKC) & (upperBB > upperKC)
    noSqz = ~(sqzOn | sqzOff)
    # Calcular las barras del histograma
    ema_kc = source.ewm(span=lengthKC, adjust=False).mean()
    hist = (source - ema_kc).fillna(0)

    # Calcular la señal de trading
    signals = pd.Series('ninguna', index=df.index)
    if sqzOff.iloc[-2] and sqzOn.iloc[-1]:
        if hist.iloc[-1] > 0:
            signals.iloc[-1] = 'comprar'
        elif hist.iloc[-1] < 0:
            signals.iloc[-1] = 'vender'
    return signals.iloc[-1]
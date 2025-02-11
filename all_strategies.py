
import numpy as np
import pandas as pd
import talib
from talib import MA_Type

# 這是我們的策略的部分
# 主要只是要算出進出的訊號 signals 跟何時持有部位 positions
# 底下是一個突破系統的範例

def Breakout_strategy(df):
    # Donchian Channel
    df['20d_high'] = np.round(pd.Series.rolling(df['Close'], window=20).max(), 2)
    df['10d_low'] = np.round(pd.Series.rolling(df['Close'], window=10).min(), 2)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['Close'][t] > df['20d_high'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['Close'][t] < df['10d_low'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def RSI_7030_strategy(df):
    df['RSI'] = talib.RSI(df['Close'].values)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['RSI'][t-1] < 30:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['RSI'][t-1] > 70:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def RSI_8020_strategy(df):
    """
    RSI < 20: buy
    RSI > 80: sell
    """
    df['RSI'] = talib.RSI(df['Close'].values)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['RSI'][t-1] < 20:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['RSI'][t-1] > 80:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def BBands_strategy(df):
    df['UBB'], df['MBB'], df['LBB'] = talib.BBANDS(df['Close'].values, matype=MA_Type.T3)

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['Close'][t] < df['LBB'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['Close'][t] > df['UBB'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def 第一組_strategy(df):
    close=pd.DataFrame(df["Close"])
    short_win = 12    # 短期EMA平滑天数
    long_win  = 26    # 長期EMA平滑天数
    macd_win  = 20    # DEA線平滑天数
    macd_tmp  =  talib.MACD( df['Close'].values,fastperiod = short_win ,slowperiod = long_win ,signalperiod = macd_win )
    df['DIF'] =macd_tmp [ 0 ]
    df['DEA'] =macd_tmp [ 1 ]
    df['MACD']=macd_tmp [ 2 ]
    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['DIF'][t] > 0 and df['DEA'][t] >0 and df['DIF'][t] > df['DEA'][t] and df['DIF'][t-1]<df['DEA'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['DIF'][t] < 0 and df['DEA'][t] < 0 and df['DIF'][t] < df['DEA'][t] and df['DIF'][t-1]>df['DEA'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def Team3_strategy(df):
    """
    主要使用BBand + 5MA策略，
    中軌為20ma，上下軌為正負1.5sd
    # 若5MA開始向上突破下軌，低檔買進
    # 若收盤價向下跌破中軌，獲利了結趕快落跑
    """

    df['5ma'] = pd.Series.rolling(df['Close'], window=5).mean()
    # bbands策略,N=20
    df['20ma'] = pd.Series.rolling(df['Close'], window=20).mean()
    df['SD'] = pd.Series.rolling(df['Close'], window=20).std()
    # 上軌=20ma+1.5sd ,中軌=20ma, 下軌=20ma-1.5sd
    df['upbbands'] = df['20ma']+1.5*df['SD']
    df['midbbands']=df['20ma']
    df['lowbbands'] = df['20ma']-1.5*df['SD']

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if  (df['5ma'][t] > df['lowbbands'][t-1]):
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif  (df['Close'][t] < df['midbbands'][t-1]):
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def 中山南拳寶寶_strategy(df):
    """
    WMSR < 80時進場
    WMSR > 20時出場
    """
    df['low9'] = df['Low'].rolling(window=9).min()
    df['high9'] = df['High'].rolling(window=9).max()
    df['WMSR'] = 100*((df['high9'] - df['Close']) / (df['high9'] - df['low9']) )

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['WMSR'][t] < 80:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['WMSR'][t] > 20:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df


def JuianJuian4715_strategy(df):
    """
    ##strategy:以20MA為中心，上下各2個標準差為範圍的一個軌道操作方式。
    ##買進訊號:
    #1.價格由下向上 穿越下軌線時，是買進訊號
    #2.價格由下向上 穿越中間線時，股價可能加速向上，是加碼買進訊號
    #3.價格在中間線與上軌線之間波動時，為多頭市場，可作多
    """
    has_position = False
    df['signals'] = 0

    ave = pd.Series.rolling(df['Close'], window=20).mean()
    std = pd.Series.rolling(df['Close'], window=20).std()
    df['ave']= pd.Series.rolling(df['Close'], window=20).mean()
    df['upper'] = ave + 2*std
    df['lower'] = ave -2*std

    for t in range(2, df['signals'].size):
        if df['upper'][t] > df['ave'][t-1]:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['lower'][t] < df['ave'][t-1]:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df

def 大盜韓不住_strategy(df):
    """
    乖離率,乖離率代表的就是投資者的平均報酬率，當股價漲離平均成本很多的時候，
    就可能會有大的獲利賣壓出現，讓股價往均線跌回,當股價跌出平均成本太多的時候，攤平或逢低的買盤可能會進入
    乖離率<-3% 進場 , >3.5% 出場
    """
    has_position = False
    df['6d'] = pd.Series.rolling(df['Close'], window=6).mean()
    df['BIAS'] = (df['Close'] - df['6d'] )/df['6d']
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['BIAS'][t] < -0.02:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['BIAS'][t] > 0.025:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df

def 財運滾滾來_strategy(df):
    """
    進場訊號:黃金交叉(20MA>60MA)、今日收盤價跌破前日BBANDS下限、乖離率(BIAS)小於-0.05[三項條件同時符合即進場]
    出場訊號:死亡交叉(20MA<60MA)、今日收盤價漲破前日BBANDS上限、乖離率(BIAS)大於 0.1[三項條件同時符合即出場]
    """
    df['20MA'] = pd.Series.rolling(df['Close'], window=20).mean()
    df['60MA'] = pd.Series.rolling(df['Close'], window=60).mean()
    df['UBB'], df['MBB'], df['LBB'] = talib.BBANDS(df['Close'].values, matype=MA_Type.T3)
    df['BIAS']= (df['Close']-df['20MA'])/df['20MA']

    has_position = False
    df['signals'] = 0
    for t in range(2, df['signals'].size):
        if df['20MA'][t] > df['60MA'][t] and df['Close'][t] < df['LBB'][t-1] and df['BIAS'][t] < -0.05:
            if not has_position:
                df.loc[df.index[t], 'signals'] = 1
                has_position = True
        elif df['20MA'][t] < df['60MA'][t] and df['Close'][t] > df['UBB'][t-1] and df['BIAS'][t] > 0.1:
            if has_position:
                df.loc[df.index[t], 'signals'] = -1
                has_position = False

    df['positions'] = df['signals'].cumsum().shift()
    return df

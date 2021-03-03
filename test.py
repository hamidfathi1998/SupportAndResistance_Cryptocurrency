import trendln
import matplotlib.pyplot as plt
from Binance import Binance

exchange = Binance(filename = 'credentials.txt')

defualt_candel= 1000
symbolList = ["BTCUSDT","ETHUSDT"]
symbolTimeFrame = ["1m","5m","10m","15m","30m","1h","4h","1d"]

#-----------------------------  Select Symbol
def selectSymbol():
    print()
    str_s = ""
    print("default symbol (use by number)")
    for i in range(0,len(symbolList)):
        str_s =str_s + str(i) + "   " + symbolList[i]
        str_s = str_s if i == len(symbolList)-1 else (str_s + " | ")

    print(str_s)
    inp = str(input("Please Enter your symbol (for exit enter the q): "))
    if inp == "q":
          return -1
    return symbolList[int(inp)] if inp.strip().isdigit() else inp
    
#-----------------------------  Select timeframe
def selectTimeframe():
    print()
    str_t = ""
    print("default timeframe (use by number)")
    for i in range(0,len(symbolTimeFrame)):
        str_t =str_t + str(i) + "   " + symbolTimeFrame[i]
        str_t = str_t if i == len(symbolTimeFrame)-1 else (str_t + " | ")
    print(str_t)
    inpT = str(input("Please Enter your timeframe : "))    
    return symbolTimeFrame[int(inpT)] if inpT.strip().isdigit() else inpT

#-----------------------------  download data from binance and prepare Data
def donData(symbol,defualt_timeStyle):
    hist = exchange.GetSymbolKlines(symbol, defualt_timeStyle, defualt_candel)
    # prepare Data
    hist.rename(columns={'open':'Open'}, inplace=True)
    hist.rename(columns={'high':'High'}, inplace=True)
    hist.rename(columns={'low':'Low'}, inplace=True)
    hist.rename(columns={'close':'Close'}, inplace=True)
    hist.rename(columns={'date':'Date'}, inplace=True)
    hist.set_index('Date', inplace=True)
    temp = hist['time']
    hist = hist.assign(volume=hist['time'])
    del hist['time']
    hist.rename(columns={'volume':'Time'}, inplace=True)
    return hist


#-----------------------------  illustrate chart
def illustrateChart(fig,ifSave=False,filename="chart",formatC = "svg"):
    fig.set_size_inches(22, 9)
    if ifSave:
        plt.savefig(filename+"."+formatC, format=formatC)
    plt.show()
    plt.clf() #clear figure


while True:
    symbol = selectSymbol()
    if symbol == -1:
        break
    
    timeframe = selectTimeframe()

    hist = donData(symbol,timeframe)

    fig = trendln.plot_support_resistance(hist.Close,fromwindows=False,title_txt = symbol + " / " + timeframe) # requires matplotlib - pip install matplotlib
    illustrateChart(fig,True)

    fig = trendln.plot_sup_res_date((hist.Low, hist.High),hist[-100:].index,
                                    fromwindows=False,title_txt = symbol + " / " + timeframe) # requires matplotlib - pip install matplotlib
    illustrateChart(fig)  

    

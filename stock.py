#Predict Stock Price
def sma(a,b,stat):
    sma=0
    for x in range(b-a):
        sma+=stat[a+x]
    sma/=b-a
    return sma
def ema(days,stat):
    ema=sma(0,days,stat)
    n=2/(days+1)
    for x in range(len(stat)-days):
        ema=(stat[days+x]*n)+(ema*(1-n))
    return ema
def rsi(days,stat):
    um=0
    dm=0
    for x in range(days):
        if stat[len(stat)-1-x]>stat[len(stat)-2-x]:
            um+=stat[len(stat)-1-x]-stat[len(stat)-2-x]
        else:
            dm+=stat[len(stat)-2-x]-stat[len(stat)-1-x]
    if dm==0:
        dm=0.01
    rs=um/dm
    rsi=100-(100/(1+rs))
    return rsi
def macd(stat):
    macd=ema(12,stat)-ema(26,stat)
    macdlist=[]
    for x in range(9):
        macdlist.append(ema(12,stat[:len(stat)-9+x])-ema(26,stat[:len(stat)-9+x]))
    signal=ema(9,macdlist)
    histogram=macd-signal
    return macd,histogram
def macd2(stat):
    macd2list=[]
    for x in range(6):
        macd2list.append(macd(stat[:len(stat)-1-x])[1])
    histogramslope=rsi(5,macd2list)
    return histogramslope
def stoch(stat):
    def faststochfunc(stat):
        numerator=stat[len(stat)-1]-min(stat[len(stat)-14:])
        denominator=max(stat[len(stat)-14:])-min(stat[len(stat)-14:])
        if denominator==0:
            denominator=0.01
        return (numerator/denominator)*100
    faststoch=faststochfunc(stat)
    slowstoch=0
    for x in range(3):
        slowstoch+=faststochfunc(stat[:len(stat)-1-x])
    slowstoch/=3
    return faststoch,slowstoch
def bband(stat):
    mean=sma(0,len(stat),stat)
    statstdevp=[]
    for x in stat:
        statstdevp.append((x-mean)**2)
    stdevp=sma(0,len(statstdevp),statstdevp)**(1/2)
    lowband=mean-(stdevp*2)
    highband=mean+(stdevp*2)
    return mean,lowband,highband
def stockpredictor():
    restart="Y"
    while restart!="N":
        print("For your interested stock:")
        stat=[]
        totaldays=int(input("Enter the number of days of stock price you want to input (at least 42):"))
        while totaldays<42:
            totaldays=int(input("At least 6 weeks."))
        for x in range(totaldays):
            if x==0:
                userinput=input("What's the closing stock price for this day, in dollars?")
            if x==1:
                userinput=input("What about the previous day's closing price?")
            if x>1:
                userinput=input("What about %s days before?"%(x)) 
            stat.append(float(userinput))
        stat.reverse()
        tuple(stat)
        print("List of stock prices from past to present:")
        print(stat)
        valuersi=rsi(14,stat)
        valuemacdhis=macd2(stat)
        valuestoch=stoch(stat)[1]
        valuebband=bband(stat)
        print("RSI:",valuersi)
        print("MACD:",macd(stat)[0])
        print("STOCH:",valuestoch)
        print("BBAND:",valuebband[1:3])
        bullindicator=0
        if valuersi<30:
            bullindicator+=1
        if valuemacdhis<30:
            bullindicator+=1
        if valuestoch<20:
            bullindicator+=1
        if stat[len(stat)-1]<valuebband[2]+((valuebband[0]-valuebband[2])/2):
            bullindicator+=1
        if bullindicator==0:
            print("We really do not recommend buying this at all.")
        if bullindicator==1:
            print("We do not recommend buying this.")
        if bullindicator==2:
            print("We are not sure about this stock. It might go up, but it might go down.")
        if bullindicator==3:
            print("We think this stock will probably go up.")
        if bullindicator==4:
            print("We think this stock will almost definitely go up. You should buy it.")
        if bullindicator==5:
            print("Oh hello, this is an easter egg for those of you who opened up this program.")
        print("Thank you for using our program and good luck with your stock market.")
        restart=input("Do you want to restart the program? (Y for Yes and N for No)")
stockpredictor()



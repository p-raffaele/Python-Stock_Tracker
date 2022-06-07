from bs4 import BeautifulSoup
from matplotlib import pyplot
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
import datetime
import requests

def price_tracking_btc():

    html_text = requests.get("https://coinmarketcap.com/currencies/bitcoin/").text
    soup = BeautifulSoup(html_text,'lxml')    
    price = soup.find('div', class_='priceValue').text
    price = price.lstrip('$')
    price = price.replace(',','')
    market_cap = soup.find('div', class_='statsValue').text
    market_cap = market_cap.lstrip('$')
    return float(price),market_cap

def stock_chart(time_vector,price_vector):
    pyplot.plot(time_vector,price_vector, linestyle="dashed", marker="o")
    #some graphics
    pyplot.title('Stock chart:')
    pyplot.xlabel('Time, expressed as hours,seconds')
    pyplot.ylabel('Price variation')
    pyplot.show()

def get_time():
    now = datetime.datetime.now()
    day = datetime.datetime.now()
    spec_format = datetime.datetime.now()
    spec_format = spec_format.strftime('%H.%M')
    spec_format = float(spec_format)
    now = now.strftime('%H:%M:%S')
    day = day.strftime('%d %B %Y')
    return now,day,spec_format
        
def stock_tracker(chart = True):
    print('Getting ready the environment ...')
    minutes = int(input('After how many minutes do you want the calculation to be done?\n>'))
    #Why it asks minutes? Because if you extract the value every second it likely to be
    #at the same values of before, therefore it will create a dull shell.
    #Because Google will block the request and send the same values.
    while minutes < 1:
        minutes = int(input('It cannot be less than one minute! Enter numbers bigger or equal than one:\n>'))
    message = 'At what price do you want to be alerted?Bear in mind the asset is circulating at:'+ str(price_tracking_btc()[0])+ '\n>'
    price_alert = float(input(message))
    message = 'Do you want to activate the stock chart? (It will be drawn every 10 minutes)Y/n:' + '\n>'
    activate_chart = input(message)
    while activate_chart != 'Y' and activate_chart != 'n':
        message = 'Do you want to activate the stock chart? (It will be drawn every 10 minutes)Y/n:' + '\n>'
        activate_chart = input(message)
    if activate_chart == 'Y':
        chart = True
    else:
        chart = False
    notification = AudioSegment.from_file(file = 'Simple_notification.wav')
    asset = 'Bitcoin (BTC)'
    currency = 'USD'
    cycle = 0
    collect_price = []
    collect_time = []
    while True:
        if cycle % 4 == 0:
            print('\nThe asset value is being calculated on',get_time()[1])
        print('Stock:',asset)
        print('Price:',price_tracking_btc()[0],currency)
        print('Current Volume:',price_tracking_btc()[1],currency)
        print('Time:', get_time()[0],'\n')
        #print('Calculation no:',cycle)
        collect_price.append(price_tracking_btc()[0])
        collect_time.append(get_time()[2])
        if cycle == 10 and chart == True:
            #a stock chart is drawn every 10 minutes
            stock_chart(collect_time,collect_price)
        if price_tracking_btc()[0] >= price_alert:
            print('Warning!! The price is currently above', str(price_alert))
            for times in range(5):
                play(notification)
        sleep(60*minutes)
        cycle += 1

stock_tracker()
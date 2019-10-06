import requests
import time
from datetime import datetime
import mysql.connector


conn = mysql.connector.connect(host="",user="perchelac",password="", database="")
cursor = conn.cursor()
#conn.close()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cryptoprice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_price DATETIME,
    btc_price_usd FLOAT(12),
    xtz_price_usd FLOAT(12),
    btc_price_euro FLOAT(12),
    xtz_price_euro FLOAT(12)
);
""")

'''
Idée :
BUG insertion de date
rajouter entre chaque 30 secondes de combien le prix monte ou descend
'''

BTCusdLast = 0
XTZusdLast = 0

def get_data():
    while True:
        app_key = ''
        url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,XTZ&tsyms=USD,EUR&api_key=' + app_key
        res = requests.get(url)
        data = res.json()

        dateBrut = datetime.now()
        timeNow = dateBrut.strftime('%Y-%m-%d %H:%M:%S')

        BTCusd = data['BTC']['USD']
        BTCeuro = data['BTC']['EUR']
        XTZusd = data['XTZ']['USD']
        XTZeuro = data['XTZ']['EUR']

        global BTCusdLast
        global XTZusdLast

        BTCusdDrop2 = BTCusdLast-(BTCusdLast*0.02)
        XTZusdDrop2 = XTZusdLast-(XTZusdLast*0.02)
        BTCusdUp2 = BTCusdLast+(BTCusdLast*0.02)
        XTZusdUp2 = XTZusdLast+(XTZusdLast*0.02)

        cursor.execute("INSERT INTO cryptoprice (date_price, btc_price_usd, xtz_price_usd, btc_price_euro, xtz_price_euro) VALUES(%s, %s, %s,  %s,  %s)", (timeNow, BTCusd, XTZusd, BTCeuro, XTZeuro))
        conn.commit()

        print ('---------------------------')
        print (timeNow)
        print ('---------------------------')
        if BTCusd<=BTCusdDrop2:
            print ('ALERTE - Chute de \033[31m2%\033[0m du BTC en 30 secondes!')
        if XTZusd<=XTZusdDrop2:
            print ('ALERTE - Chute de \033[31m2%\033[0m du XTZ en 30 secondes!')
        if BTCusd>=BTCusdUp2 and BTCusdLast!=0:
            print ('ALERTE - Augmentation de \033[32m2%\033[0m du BTC en 30 secondes!')
        if XTZusd>=XTZusdUp2 and XTZusdLast!=0:
            print ('ALERTE - Augmentation de \033[32m2%\033[0m du XTZ en 30 secondes!')
        if BTCusdLast==BTCusd:
            print ('BTC : {}$'.format(BTCusd) + ' ({}€)'.format(BTCeuro))
        if BTCusdLast<BTCusd:
            print ('BTC : \033[32m{}\033[0m$'.format(BTCusd) + ' ({}€)'.format(BTCeuro))
        if BTCusdLast>BTCusd:
            print ('BTC : \033[31m{}\033[0m$'.format(BTCusd) + ' ({}€)'.format(BTCeuro))
        if XTZusdLast==XTZusd:
            print('XTZ : {}$'.format(XTZusd) + ' ({}€)'.format(XTZeuro))
        if XTZusdLast<XTZusd:
            print('XTZ : \033[32m{}\033[0m$'.format(XTZusd) + ' ({}€)'.format(XTZeuro))
        if XTZusdLast>XTZusd:
            print('XTZ : \033[31m{}\033[0m$'.format(XTZusd) + ' ({}€)'.format(XTZeuro))

        BTCusdLast = BTCusd
        XTZusdLast = XTZusd

        #Temps avant de relancer la boucle
        time.sleep(120)


get_data()
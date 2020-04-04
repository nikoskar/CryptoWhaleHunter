import time
import sys
import requests
from os.path import exists
from bs4 import BeautifulSoup as bs

script, filename = sys.argv

def main(filename):
    try:
        #send the request to the site and check for download errors with
        #raise_for_status()
        req = requests.get('your link here')
        req.raise_for_status()
    except Exception as e:
        print e
    else:
        SoupData = bs(req.text, "html.parser")

        #the data list represents the table as taken from the html code of
        #https://etherscan.io/txs
        #It's a list containing lists. Each nested list represents a row from the
        #table. Every list has size = 7 and contains the following info:
        #[TxHash, Block, Age, From, To, Value, TxFee]
        data =[]
        table = SoupData.tbody
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values

    #this is optional and not necessary. Could be used for future data analysis

    whaleList = {}
    
    #I use 10K as a flag cause i have noticed that whales tend to split the big
    #amounts to 10-20K transactions and spread them to multiple wallets.
    for i in data:
        _ ,_ ,_ ,_ , current, amount, _ = i
        #filter and store transactions from 20K+
        if float(str(amount[:2])) > float(20):
            whaleList[str(current)] = float(str(amount[:3]))


    for key, value in whaleList.iteritems():
        print key + 5 * "." + str(value)
        txt = open(filename, 'a')
        txt.write(key + 5 * "." + str(value) + '\n')
        txt.close()



if __name__ == '__main__':

    try:
        exists(filename)
    except Exception as e:
        print (e)
    else:
        print "[+]Hello! Welcome to Whale Hunter!"
        time.sleep(3)
        print "[+]This script traces crypto whales parsing info from ##############"
        time.sleep(3)
        print "[+]You can terminate the script anytime by pressing CTRL-Z"
        time.sleep(3)
        raw_input("[+]If you are ready to find some whales press RETURN")
        while 1:
            main(filename)
            #extract data from the source with a 15s time difference
            time.sleep(15)

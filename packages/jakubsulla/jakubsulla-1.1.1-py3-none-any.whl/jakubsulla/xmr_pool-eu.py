import requests
import json
import datetime
from prettytable import PrettyTable
from termcolor import colored
import os
import time
#============
data = requests.get(f"https://web.xmrpool.eu:8119/stats_address?address=46wGfkBen7J6gkF39yWU7Xg1zRJNYMh5hZdakpqrNuerNqpb7wWwN3bgSm7sWeVRMyjbuTnhGXtt5GXemiVJrd1KESEJ5Hr").json()
date = datetime.datetime.now().strftime('%d/%m/%Y')
Time = datetime.datetime.now().strftime('%H:%M:%S')
rawBalance = data["stats"]["balance"]
#===
def lastShare():
	RawlastShare = int(data["stats"]["lastShare"])
	localtime = milliseconds = int(time.time())
	lastShare = localtime - RawlastShare
	day = lastShare // (24 * 3600)
	lastShare = lastShare % (24 * 3600)
	hour = lastShare // 3600
	lastShare %= 3600
	minutes = lastShare // 60
	lastShare %= 60
	seconds = lastShare
	if day == 0:
		if hour == 0:
			if minutes == 0:
				return str(seconds) + " SEC ago"
			return str(minutes) + " MIN, " + str(seconds) + " SEC ago"
		return str(hour) + " H, " + str(minutes) + " MIN, " + str(seconds) + " SEC ago"
	return str(day) + " D, " + str(hour) + " H, " + str(minutes) + " MIN, " + str(seconds) + " SEC ago"
#===
try:
	ALLhashRate = data["stats"]["hashrate"] + "/s"
except KeyError:
	ALLhashRate = "0 H/s"
rawLastReward = data["stats"]["last_reward"]
#===
def getBalance(rawBalance):
	unit = 13
	lenRaw = len(rawBalance)
	nulls = unit - lenRaw
	count = nulls - 1
	balance = "0."
	for i in range(count):
		balance = balance + "0"
	balance = balance + rawBalance
	balance = balance + " XMR"
	return(balance)
#===
def XMRtoCZK(balance):
	exchangeRateURL = 'https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=czk'
	exchangeRate = requests.get(exchangeRateURL).json()
	czk = exchangeRate["monero"]["czk"]
	balance = balance.replace(" XMR", "")
	czk = float(czk)
	balance = float(balance)
	czk = czk * balance
	czk = round(czk, 4)
	czk = str(czk) + " CZK"
	return(czk)
workers = 0
myTable = PrettyTable(["Worker/Rig ID", "HashRate"])
while True:
	try:
		data["perWorkerStats"][workers]
		id = data["perWorkerStats"][workers]["workerId"]
		try:
			hashRate = data["perWorkerStats"][workers]["hashrate"]
		except KeyError:
			hashRate = "0 H/s"
		myTable.add_row([id, hashRate])
		workers = workers + 1
	except IndexError:
		break
#=========================
time.sleep(1)
print(colored("Connected", "green"))
print("Date: " + date)
print("Time: " + Time)
print("Pending Balance: " + getBalance(rawBalance))
print("Pending Balance: " + XMRtoCZK(getBalance(rawBalance)))
print("Last Block Reward: " + getBalance(rawLastReward))
print("Last Block Reward: " + XMRtoCZK(getBalance(rawLastReward)))
print("Last Share Submitted: ", lastShare())
print("Hash Rate: " + ALLhashRate)
print("Number of workers: " + str(workers))
print(myTable)

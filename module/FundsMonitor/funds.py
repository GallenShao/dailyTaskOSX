# -*- coding: UTF-8 -*-

import re
import os
import sys
import json
from config import get_config

if sys.version_info.major == 2:
	from urllib2 import urlopen
elif sys.version_info.major == 3:
	from urllib.request import urlopen
else:
	print('Python 4? Not Supported.')
	exit()


def send_dialog(content, title):
	script = u'osascript -e \'tell app "System Events" to display dialog "%s" with title "%s"\' &> /dev/null' % (content, title)
	os.system(script.encode('utf-8'))


def send_noti(content, title, subtitle=''):
	script = u'osascript -e \'display notification "%s" with title "%s" subtitle "%s"\'' % (content, title, subtitle)
	os.system(script.encode('utf-8'))


sina_open_api = 'https://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=%s'
# sina_funds_url = 'http://finance.sina.com.cn/fund/quotes/%s/bc.shtml'
# pattern = re.compile(u'<div class="top_fixed_fund_dwjz">单位净值：(.*?)\(<span class="font_data_red">(.*?)%</span>\)</div>')
def funds_monitor(code):
	try:
		r = urlopen(sina_open_api % code)
		result = r.read().decode('utf-8')
		result = json.loads(result)['result']['data']['data']
		for item in result:
			item['jjjz'] = float(item['jjjz'])
		for index in range(0, len(result) - 1):
			result[index]['rate'] = 100 * (result[index]['jjjz'] - result[index + 1]['jjjz']) / result[index + 1]['jjjz']

		return result
	except:
		return None


def rate_judge(rate):
	if rate >= 5:
		desc = u'火箭式上涨！！！'
		need_alert = True
	if rate >= 3:
		desc = u'暴涨！！'
		need_alert = True
	elif rate >= 2:
		desc = u'大幅上涨！'
		need_alert = True
	elif rate >= 1:
		desc = u'上涨，'
		need_alert = False
	elif rate <= -5:
		desc = u'断崖式下跌！！！'
		need_alert = True
	elif rate <= -3:
		desc = u'暴跌！！'
		need_alert = True
	elif rate <= -2:
		desc = u'大幅下跌！'
		need_alert = True
	elif rate <= -1:
		desc = u'下跌，'
		need_alert = False
	else:
		desc = u'正常波动，'
		need_alert = False

	return need_alert, desc


def history_judge(history):
	count = 1
	is_up = history[0]['rate'] > 0
	total_rate = history[0]['rate']
	for index in range(1, len(history) - 1):
		if is_up ^ (history[index]['rate'] > 0):
			break
		count += 1
		total_rate = 100 * (history[0]['jjjz'] - history[index + 1]['jjjz']) / history[index + 1]['jjjz']
	return count > 2, count, total_rate


if __name__ == '__main__':
	config = get_config()
	funds = [item for item in config['funds'] if item['enable']]

	alert = ''
	message_template = u'昨日价格%s涨跌幅%.2f%%，单位净值%.2f。\n'
	history_template = u'已连续%s【%d】天，%d天内整体%s幅度%.2f%%。\n'

	for fund in funds:
		history = funds_monitor(fund['code'])
		if history is None:
			notification += u'[%s] 价格爬取失败' % fund['short']
			continue

		yesterday = history[0]
		rate_need_alert, desc = rate_judge(yesterday['rate'])
		history_need_alert, days, total_rate = history_judge(history)

		# show notification
		notification = u'【%s】' % fund['short']
		notification += message_template % (desc, yesterday['rate'], yesterday['jjjz'])
		send_noti(notification, fund['name'])

		# calc alert
		if rate_need_alert or history_need_alert:
			alert += u'【%s】【%s】\n' % (fund['short'], fund['name'])
			alert += message_template % (desc, yesterday['rate'], yesterday['jjjz'])
			if history_need_alert:
				desc = u'上涨' if yesterday['rate'] > 0 else u'下跌'
				alert += history_template % (desc, days, days, desc, total_rate)
			alert += '\n'

	if alert:
		send_dialog(alert, u"基金监控")


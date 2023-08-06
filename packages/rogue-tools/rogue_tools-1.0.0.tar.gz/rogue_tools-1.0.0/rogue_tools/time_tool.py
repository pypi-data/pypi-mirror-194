import time
def time_stamp():
	'''
	超精准时间戳
	'''
	return int(round(time.time() * 1000000))


def time_stamp_s():
	'''
	秒级时间戳
	'''
	return int(round(time.time()))

def time_stamp_ms():
	'''
	超精准时间戳
	'''
	return int(round(time.time() * 1000))

def get_now_time():
	return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
def get_now_date():
	return time.strftime("%Y-%m-%d", time.localtime())

def get_next_date(days=1):
	'''
	之前的时间，默认一天后,也可以负数呀
	'''
	return time.strftime("%Y-%m-%d", time.localtime(time.time()-86400*days))

def get_next_hour(hour=1):
	'''
	之前的时间，默认一小时前,也可以负数呀，还可以小数呀
	'''
	return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()-3600*hour))

def countdown(sleep_time):
	print(f'countdown:{sleep_time}/{sleep_time}')
	for i in range(1,sleep_time+1):
		time.sleep(1)
		print(f'countdown:{sleep_time-i}/{sleep_time}')

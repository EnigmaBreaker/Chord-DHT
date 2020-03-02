def hextoint(s):
	# if(s[0:2] == '0x'):
	# 	return int(s, 0)
	return int('0x'+s, 0)

def addHI(h, i, m):
	return hex((hextoint(h) + i) % 2**m)[2:]	

def inRange(key, first, last, n):
	if(last > first):
		if(key == None):
			print(first, key, last)
		return first < key < last

	last += n
	if(first > key):
		key += n

	return first < key < last

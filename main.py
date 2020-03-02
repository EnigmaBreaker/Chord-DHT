from chord import Chord
import sys
from helper import inRange

def test1(chord, nums):
	keys = []

	i = 0
	while(i < nums):
		key = chord.addMsg(i)
		if(key == None):
			print("Duplicate key")
		else:
			keys.append(key)
			i+=1

	# for i in range(nums):
	# 	key = chord.addMsg(i)
	# 	if(key == None):
	# 		print("Dupicate key")
	# 		i-=1
	# 	else:
	# 		keys.append(key)

	for i in range(nums):
		if(chord.lookup(keys[i]) == i):
			# print("Lookup: {} {} {}".format(keys[i], i, True))
			pass
		else:
			print("Lookup: {} {}".format(i, False))
			break

if __name__ == "__main__":
	chord = Chord(int(sys.argv[1]))
	# chord.print_chord()
	# test1(chord, 1000000)
	chord.deleteRandomNode(int(sys.argv[1])//2)
	chord.print_chord()
	test1(chord, 1000000)


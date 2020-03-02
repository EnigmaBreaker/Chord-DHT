from chord import Chord
import sys
from helper import inRange

if __name__ == "__main__":
	chord = Chord(int(sys.argv[1]))
	chord.print_chord()

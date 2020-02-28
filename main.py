from chord import Chord
import sys

if __name__ == "__main__":
	chord = Chord(int(sys.argv[1]))
	chord.print_chord()
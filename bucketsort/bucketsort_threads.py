from __future__ import with_statement

import sys
import threading

NUM_BUCKETS = 94

def _read_file_to_array(filename):
	with open(filename) as f:
		totalLines = int(f.readline()) # ignore first line
		return f.read().splitlines()


def	_write_array_to_file(array_name, file_name):
	with open(file_name, 'w') as f:
		for item in array_name:
			f.write(item + '\n')

"""
	I simply get the decimal number of the ascii code of the first character and subtract 33.
	The magic number 33 is because the universe of possible values is between 0x21 and 0x7E.
"""
def _hash_function(s):
	return ord(s[:1]) - 33


def _sort_buckets(buckets, begin_index, end_index):
	for i in xrange(begin_index, end_index):
		buckets[i].sort()


def bucketsort(input_numbers, num_threads=1):
	#1 create the buckets
	#buckets = {i:[] for i in range(0, NUM_BUCKETS)}
	buckets = dict((i, []) for i in range(0,NUM_BUCKETS))

	#2 insert the numbers in the corresponding buckets, since we have 93 buckets the leading character will work as the key and hashing function
	for item in input_numbers:
		buckets[_hash_function(item)].append(item)

	#4 sort buckets
	if(num_threads > 1):
		chunk_size = NUM_BUCKETS / num_threads
		threads = []
		for i in xrange(0, num_threads):
			begin_index = i * chunk_size
			end_index 	= ((i + 1) * chunk_size)
			if ( i == num_threads - 1 and NUM_BUCKETS % num_threads > 0 ):
				end_index += NUM_BUCKETS % num_threads
			t = threading.Thread(target=_sort_buckets, args=(buckets, begin_index, end_index,))
			t.start()
			threads.append(t)
		for t in threads:
			t.join()
	else:
		for _, bucket in buckets.items(): # items() returns (key, value) pairs
			bucket.sort()
		
	#5 concat buckets
	final_result = []
	for i in range(0, NUM_BUCKETS):
		final_result.extend(buckets[i])

	return final_result

def main():
	if len(sys.argv) >= 2:

		# bucketsort.py input_file -p number_processes
		if sys.argv[2] == '-p':
			numbers = _read_file_to_array(sys.argv[1])
			buckets = bucketsort(numbers, int(sys.argv[3]))
			_write_array_to_file(buckets, 'bucketsort_p_' + sys.argv[3] + '.out')

		# bucketsort.py input_file -s
		elif sys.argv[2] == '-s':
			numbers = _read_file_to_array(sys.argv[1])
			buckets = bucketsort(numbers)
			_write_array_to_file(buckets, 'bucketsort_s.out')
	else:
		print "usage: bucketsort.py [inputfile] [-p] [num_threads]"


if __name__ == '__main__':
	main()
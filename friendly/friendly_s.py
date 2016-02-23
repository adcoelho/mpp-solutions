import sys

from fractions import gcd
from multiprocessing import Process, Queue

def find_friendly_numbers(start_number, end_number):
	last = end_number - start_number + 1
	the_num = [0 for i in range(last)]
	num = [0 for i in range(last)]
	den = [0 for i in range(last)]

	for i in xrange(start_number, end_number + 1):
		ii = i - start_number
		sum_ = 1 + i
		the_num[ii] = i
		done = i
		factor = 2

		while factor < done:
			if i % factor == 0:
				sum_ += (factor + (i / factor))
				done = i / factor

				if done == factor:
					sum_ -= factor

			factor += 1

		num[ii] = sum_
		den[ii] = i
		n = gcd(num[ii], den[ii])
		num[ii] = num[ii] / n
		den[ii] = den[ii] / n

	for i in xrange(0, last):
		for j in xrange(i + 1, last):
			if num[i] == num[j] and den[i] == den[j]:
				print '{} and {} are FRIENDLY'.format(the_num[i], the_num[j])

def main():
	if len(sys.argv) <= 1:
		print "usage: friendly_s.py [inputfile]"
	else:
		with open(sys.argv[1]) as f:
			while True:
				line_contents = f.readline().split(' ')
		
				if int(line_contents[0]) == 0 and int(line_contents[1]) == 0:
					break

				print "Number " + line_contents[0] + " to " + line_contents[1],
				
				friendly_numbers = find_friendly_numbers(int(line_contents[0]), int(line_contents[1]))


# ATENCAO AO INPUT ZERO
if __name__ == '__main__':
	main()
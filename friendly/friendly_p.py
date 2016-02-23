import sys
from fractions import gcd 
from multiprocessing import Process, Array

NUM_PROCS = 8


def find_friendly_numbers(start_number, end_number, shared_num, shared_den):
	last = end_number - start_number + 1
	num = [-1 for i in range(last)]
	den = [-1 for i in range(last)]

	for i in xrange(start_number, end_number + 1):
		ii = i - start_number
		sum_ = 1 + i
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

	for i in xrange(start_number, end_number + 1):
		ii = i - start_number
		try:
			shared_num[i - aux] = num[ii]
			shared_den[i - aux] = den[ii]
		except:
			print i

def print_results(start_index, end_index, shared_num, shared_den):
	for i in xrange(start_index, end_index):
		for j in xrange(i + 1, last):
			if shared_num[i] == shared_num[j] and shared_den[i] == shared_den[j]:
				print '{} and {} are FRIENDLY'.format(i + start_number, j + start_number)


if __name__ == '__main__':
	results = []

	if len(sys.argv) <= 2:
		print "usage: friendly_p.py [inputfile] [num_processes]"
	else:
		NUM_PROCS = int(sys.argv[2])

		with open(sys.argv[1]) as f:
			while True:
				line_contents = f.readline().split(' ')

				if int(line_contents[0]) == 0 and int(line_contents[1]) == 0:
					break

				print "Number " + line_contents[0] + " to " + line_contents[1],

				start_number = int(line_contents[0])
				aux = start_number
				end_number = int(line_contents[1])
				chunk_size = (end_number - start_number) / NUM_PROCS
				last = end_number - start_number + 1
				procs = []
				the_num = [i for i in range(last)]
				shared_num = Array('i', range(last+1))
				shared_den = Array('i', range(last+1))

				for i in range(NUM_PROCS):
					if i == NUM_PROCS - 1:
						p = Process(target=find_friendly_numbers,
									args=(	start_number + (chunk_size * i),
											start_number + (chunk_size * (i + 1) +
												((end_number - start_number) % NUM_PROCS)),
											shared_num,
											shared_den))
					else:
						p = Process(target=find_friendly_numbers,
									args=(	start_number + (chunk_size * i),
											start_number + (chunk_size * (i + 1)),
											shared_num,
											shared_den))

					p.start()
					procs.append(p)

				for p in procs:
					p.join()

				sub_chunk = last / NUM_PROCS
				procs = []
				n = shared_num[:]
				d = shared_den[:]

				for i in range(NUM_PROCS):
					if i == NUM_PROCS - 1:
						p = Process(target=print_results,
									args=(	sub_chunk * i,
											sub_chunk * (i + 1) + (last % NUM_PROCS),
											n,
											d))
					else:
						p = Process(target=print_results,
									args=(	sub_chunk * i,
											sub_chunk * (i + 1),
											n,
											d))

					p.start()
					procs.append(p)

				for p in procs:
					p.join()

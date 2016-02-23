import sys

from multiprocessing import Process, Queue


def read_clauses(filename):
	with open(filename) as f:
		first_line = f.readline().split(' ')
		num_clauses = int(first_line[0])
		num_vars = int(first_line[1])
		clauses = [	[x*0 for x in range(num_clauses)],
					[x*0 for x in range(num_clauses)],
					[x*0 for x in range(num_clauses)]]

		for i in xrange(0, num_clauses):
			current_line = f.readline().split(' ')
			clauses[0][i] = int(current_line[0])
			clauses[1][i] = int(current_line[1])
			clauses[2][i] = int(current_line[2])

		return num_clauses, num_vars, clauses


def solve_clauses(num_clauses, num_vars, clauses):
	iVar = []
	max_number = 2**num_vars
	current = 0
	
	for i in range(num_vars):
		iVar.append(2**i)

	for n in xrange(max_number):
		for c in xrange(num_clauses):
			var = clauses[0][c]
			if var > 0 and (n & iVar[var - 1]) > 0:
				current = c
				continue
			elif var < 0 and (n & iVar[-var - 1] == 0):
				current = c
				continue

			var = clauses[1][c]
			if var > 0 and (n & iVar[var - 1]) > 0:
				current = c
				continue
			elif var < 0 and (n & iVar[-var - 1] == 0):
				current = c
				continue

			var = clauses[2][c]
			if var > 0 and (n & iVar[var - 1]) > 0:
				current = c
				continue
			elif var < 0 and (n & iVar[-var - 1] == 0):
				current = c
				continue

			break

		if current == num_clauses - 1:
			return n

	return -1


def solve_clauses_p(num_clauses, num_vars, clauses, num_procs):
	out_q = Queue()
	max_number = 2**num_vars
	chunk_size = max_number / num_procs
	iVar = []
	counter = 0
	for i in range(num_vars):
		iVar.append(2**i)

	for i in xrange(num_procs):
		end_index = chunk_size * (i+1)
		
		if i == num_procs - 1:
			end_index += max_number % num_procs

		p = Process(
				target = _solve_clauses_p_aux,
				args = (num_clauses,
						clauses,
						chunk_size * i,
						end_index,
						iVar,
						out_q))
		p.start()

	# Waits for the first result to be calculated
	while True:
		result = out_q.get(block=True)
		counter += 1

		if result != -1 or counter >= num_procs:
			break

	return result
	

def _solve_clauses_p_aux(num_clauses, clauses, start_index, end_index, iVar, out_q):
	current = 0

	for n in xrange(start_index, end_index):
		for c in xrange(num_clauses):
			current = c
			var = clauses[0][c]
			if var > 0 and (n & iVar[var - 1]) > 0:
				continue # clause is true
			elif var < 0 and (n & iVar[-var - 1] == 0):
				continue # clause is true

			var = clauses[1][c]
			if var > 0 and (n & iVar[var - 1]) > 0:
				continue # clause is true
			elif var < 0 and (n & iVar[-var - 1] == 0):
				continue # clause is true

			var = clauses[2][c]
			if var > 0 and (n & iVar[var - 1]) > 0:
				continue # clause is true
			elif var < 0 and (n & iVar[-var - 1] == 0):
				continue # clause is true

			current = -1
			break # clause is false

		if current == num_clauses - 1:
			out_q.put(n)
			return n

	out_q.put(-1)
	return -1


def main():
	
	# python 3sat.py input_file.in -p num_procs
	input_file = sys.argv[1]
	num_clauses, num_vars, clauses = read_clauses(input_file)
	
	# python 3sat.py input_file.in -p num_procs
	if len(sys.argv) > 1 and sys.argv[2] == '-p':
		solution = solve_clauses_p(num_clauses, num_vars, clauses, int(sys.argv[3]))
	
	# python 3sat.py input_file.in -s
	else:
		solution = solve_clauses(int(first_line[0]), int(first_line[1]), clauses)
		
	if solution >= 0:
		print 'Solution found [{}]: '.format(str(solution)),
		for i in range(num_vars):
			print "%d" % int((solution & long(2**i)) / long(2**i)),
	else:
		print 'Solution not found.'

	return


if __name__ == '__main__':
	main()
###
### Example usage:
###   $ python checker.py -i ../input/small1.in -r "101"
###

from __future__ import print_function
import argparse

parser = argparse.ArgumentParser(description='Checker for 3SAT problem')
parser.add_argument('-i', '--input',
                    required=True,
                    help='Input with clauses')
parser.add_argument('-r', '--result',
                    required=True,
                    help='Resultant bit string')

def main():
    args = parser.parse_args()

    f = open(args.input, "r")
    N, L = [int(s) for s in f.readline().split()]

    R = args.result.replace(" ", "")

    if len(R) > L:
        print("Error: Number %s has too many variables" % (R))
        exit(1)

    for i in range(N):
        idx1, idx2, idx3 = [int(s) for s in f.readline().split()]
        lit1 = '0' if idx1 >= 0 else '1'
        lit2 = '0' if idx2 >= 0 else '1'
        lit3 = '0' if idx3 >= 0 else '1'

        idx1 = abs(idx1)-1
        idx2 = abs(idx2)-1
        idx3 = abs(idx3)-1

        if R[idx1] == lit1 and R[idx2] == lit2 and R[idx3] == lit3:
            print("Error: Clause %d evaluated to False" % (i+1))
            exit(1)
    f.close()

    print("Success: Number %s is a solution to 3SAT" % (R))

if __name__ == "__main__":
    main()

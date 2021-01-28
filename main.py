from movie import MovieSolver

import sys

filename = sys.argv[1]

m = MovieSolver(filename)
m.fill_seats()
m.generate_output()

print("Final state of seating:")
m.displaySeating()
print("Output written to out.txt")
    # def generate_output(self):
    #     pass

    # def combine_gaps(self):
    #     pass



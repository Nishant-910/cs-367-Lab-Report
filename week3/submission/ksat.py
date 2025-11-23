import string as st
import random as rnd
from itertools import combinations

def ask_int(msg):
    return int(input(msg))

def create_random_clauses(num_clauses, vars_per_clause, total_vars):
    letters = list(st.ascii_lowercase[:total_vars])
    capitals = [l.upper() for l in letters]
    symbols = letters + capitals

    max_attempts = 18
    unique_clauses = set()
    all_combs = list(combinations(symbols, vars_per_clause))

    attempt = 0
    while len(unique_clauses) < num_clauses and attempt < max_attempts:
        clause = tuple(sorted(rnd.sample(all_combs, 1)[0]))
        if clause not in unique_clauses:
            unique_clauses.add(clause)
        attempt += 1

    return [list(c) for c in unique_clauses]

def main():
    print("Random Clause Generator")
    num_clauses = ask_int("Enter the number of clauses: ")
    vars_per_clause = ask_int("Enter the number of variables in a clause: ")
    total_vars = ask_int("Enter the total number of variables: ")

    for idx, clause in enumerate(create_random_clauses(num_clauses, vars_per_clause, total_vars), 1):
        print(f"{clause}")

if __name__ == "__main__":
    main()
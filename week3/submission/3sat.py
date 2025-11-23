import string as st
import random as rnd
from itertools import combinations
import numpy as np

def ask_int(msg):
    return int(input(msg))

def generate_formulas(num_formulas, vars_per_formula, total_vars):
    letters = list(st.ascii_lowercase[:total_vars])
    capitals = [l.upper() for l in letters]
    symbols = letters + capitals
    max_iter, unique_forms = 20, set()
    all_combs = list(combinations(symbols, vars_per_formula))
    i = 0
    while len(unique_forms) < num_formulas and i < max_iter:
        new_form = tuple(sorted(rnd.choice(all_combs)))
        if new_form not in unique_forms:
            unique_forms.add(new_form)
        i += 1
    return [list(f) for f in unique_forms]

def generate_assignment(symbols, total_vars):
    low = list(np.random.choice(2, total_vars))
    high = [1 - x for x in low]
    return dict(zip(symbols, low + high))

def evaluate_formula(formulas, assignment):
    return sum(any(assignment[v] for v in f) for f in formulas)

def hill_climb(formulas, assignment, current_score, last_step, step_count):
    base_assign = assignment.copy()
    best_score, best_assign = current_score, assignment.copy()
    for k, v in assignment.items():
        step_count += 1
        new_assign = assignment.copy()
        new_assign[k] = 1 - v
        score = evaluate_formula(formulas, new_assign)
        if score > best_score:
            last_step, best_score, best_assign = step_count, score, new_assign.copy()
    if best_score == current_score:
        return base_assign, best_score, f"{last_step}/{step_count - len(assignment)}"
    return hill_climb(formulas, best_assign, best_score, last_step, step_count)

def beam_search(formulas, assignment, beam_width, step_count):
    if evaluate_formula(formulas, assignment) == len(formulas):
        return assignment, f"{step_count}/{step_count}"
    candidates = []
    for k, v in assignment.items():
        step_count += 1
        new_assign = assignment.copy()
        new_assign[k] = 1 - v
        score = evaluate_formula(formulas, new_assign)
        candidates.append((new_assign, score, step_count))
    best = sorted(candidates, key=lambda x: x[1])[-beam_width:]
    if len(formulas) in [c[1] for c in best]:
        sol = next(c for c in best if c[1] == len(formulas))
        return sol[0], f"{sol[2]}/{step_count}"
    return beam_search(formulas, best[-1][0], beam_width, step_count)

def variable_neighborhood(formulas, assignment, neighborhood_size, step_count):
    if evaluate_formula(formulas, assignment) == len(formulas):
        return assignment, f"{step_count}/{step_count}", neighborhood_size
    candidates = []
    for k, v in assignment.items():
        step_count += 1
        new_assign = assignment.copy()
        new_assign[k] = 1 - v
        score = evaluate_formula(formulas, new_assign)
        candidates.append((new_assign, score, step_count))
    best = sorted(candidates, key=lambda x: x[1])[-neighborhood_size:]
    if len(formulas) in [c[1] for c in best]:
        sol = next(c for c in best if c[1] == len(formulas))
        return sol[0], f"{sol[2]}/{step_count}", neighborhood_size
    return variable_neighborhood(formulas, best[-1][0], neighborhood_size + 1, step_count)

def main():
    num_formulas = int(input("Formula count: "))
    vars_per_formula = int(input("Variables per formula: "))
    total_vars = int(input("Total variables: "))
    formulas = generate_formulas(num_formulas, vars_per_formula, total_vars)
    symbols = list(st.ascii_lowercase[:total_vars]) + [c.upper() for c in st.ascii_lowercase[:total_vars]]
   
    for idx, f in enumerate(formulas, 1):
        print(f"\n{idx}: {f}")
        assignment = generate_assignment(symbols, total_vars)
        score = evaluate_formula(f, assignment)
        _, hc_score, hc_path = hill_climb(f, assignment, score, 1, 1)
        bs_assign, bs_path = beam_search(f, assignment, 3, 1)
        vn_assign, vn_path, vn_size = variable_neighborhood(f, assignment, 1, 1)
        print(f"HC: S={hc_score}, P={hc_path}")
        print(f"BS: S={evaluate_formula(f, bs_assign)}, P={bs_path}")
        print(f"VND: S={evaluate_formula(f, vn_assign)}, P={vn_path}, N={vn_size}")

if __name__ == "__main__":
    main()
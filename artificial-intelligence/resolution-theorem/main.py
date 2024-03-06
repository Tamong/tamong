# CS 4365 AI
# Homework 3
# Name: Jimmy Harvin, Philip Wallis
# Date: 11/10/2023
# Description: This program implements the resolution theorem proving
#              algorithm to determine if a given clause is valid or not.
#              The program takes in a file containing a knowledge base
#              and a clause to validate. The program outputs the
#              knowledge base after resolution and whether the clause
#              is valid or not.

# Usage: python main.py <input_file>

import re
import sys


# Reads the clauses from the input file
def read_clauses(filename):
    clauses = []
    with open(filename, errors="ignore") as input_file:
        for i, line in enumerate(input_file):
            # Remove newlines and trailing whitespace
            line = re.sub(r"\n", "", line)
            line = re.sub(r"[ \t]+$", "", line)

            cl = []
            for c in line.split(" "):
                cl.append(c)
            clauses.append(cl)
    return clauses


# Resolves two clauses
def resolve(c1, c2, clauses):
    resolved_clause = c1 + c2
    resolved = None
    clause_map = {}

    # Check if the two clauses are the same
    for r1 in resolved_clause:
        if r1 not in clause_map.keys():
            clause_map[r1] = 0

    resolved = list(clause_map.keys())
    ors = list(clause_map.keys())

    # Check if the two clauses are resolvable
    for l1 in c1:
        for l2 in c2:
            if is_negation(l1, l2):
                resolved.remove(l1)
                resolved.remove(l2)

                # Check if the resolved clause is empty
                if len(resolved) == 0:
                    return False
                elif is_implication_true(resolved):
                    return True
                else:
                    for cl in clauses:
                        if get_difference(resolved, cl) == []:
                            return True
                    return resolved

    if resolved == ors:
        return True


# Returns true if the two literals are negations of each other
def is_negation(literal1, literal2):
    if literal1 == ("~" + literal2) or literal2 == ("~" + literal1):
        return True

    return False


# Returns the difference between two lists
def get_difference(list1, list2):
    difference = []

    # Check if item in list1 is not in list2
    for item in list1:
        if item not in list2:
            difference.append(item)

    # Same as above but for list2
    for item in list2:
        if item not in list1 and item not in difference:
            difference.append(item)

    return difference


# Returns true if the implication is true
def is_implication_true(resolved):
    for r1 in resolved:
        for r2 in resolved:
            if is_negation(r1, r2):
                return True
    return False


if __name__ == "__main__":
    clause_number = 1
    clauses = read_clauses(sys.argv[1])

    to_prove = clauses[-1]
    del clauses[-1]

    for cl in clauses:
        print(f"{clause_number}. {' '.join(cl)} {{}}")
        clause_number += 1

    for c in range(len(to_prove)):
        if "~" in to_prove[c]:
            to_prove[c] = to_prove[c].replace("~", "")
        else:
            to_prove[c] = "~" + to_prove[c]

    for c in to_prove:
        clauses.append([c])
        print(f"{clause_number}. {' '.join([c])} {{}}")
        clause_number += 1

    cli = 1
    while cli < clause_number - 1:
        clj = 0
        while clj < cli:
            # Resolve the two clauses
            result = resolve(clauses[cli], clauses[clj], clauses)

            # If resolved
            if result is True:
                clj += 1
                continue
            # If contradiction
            elif result is False:
                print(f"{clause_number}. Contradiction {{{cli + 1},{clj + 1}}}")
                print("Valid")
                sys.exit(0)
            # If not resolved
            else:
                new_clause_number = clause_number
                new_clause = " ".join(result)
                print(f"{new_clause_number}. {new_clause} {{{cli + 1},{clj + 1}}}")
                clause_number += 1
                clauses.append(result)
            clj += 1
        cli += 1
    # If no contradiction
    print("Fail")

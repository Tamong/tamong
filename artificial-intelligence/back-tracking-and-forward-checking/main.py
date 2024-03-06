# Jimmy Harvin
# Philip Wallis

import sys
import copy


# class for keeping track of and evaluating variable constraints
class Constraint:
    def __init__(self, variable1, operator, variable2):
        self.variable1 = variable1
        self.operator = operator
        self.variable2 = variable2

    def __str__(self):
        return self.variable1 + " " + self.operator + " " + self.variable2

    def evaluate(self, value1, value2):
        if self.operator == ">":
            return value1 > value2
        elif self.operator == "<":
            return value1 < value2
        elif self.operator == "=":
            return value1 == value2
        elif self.operator == "!":
            return value1 != value2

    def operand(self):
        return self.variable2

    def reverse(self):
        if self.operator == ">":
            return Constraint(self.variable2, "<", self.variable1)
        elif self.operator == "<":
            return Constraint(self.variable2, ">", self.variable1)
        elif self.operator == "=":
            return Constraint(self.variable2, "=", self.variable1)
        elif self.operator == "!":
            return Constraint(self.variable2, "!", self.variable1)


branch_counter = 1


# display the current assignments at the end of a branch
def print_assignments(var_dict, fail):
    global branch_counter
    output_str = str(branch_counter) + ". "
    branch_counter += 1
    var_keys = list(var_dict.keys())
    for var in var_keys:
        if var != var_keys[0]:
            output_str = output_str + ", "
        output_str = output_str + var + "=" + str(var_dict[var])

    output_str = output_str + "  " + fail
    print(output_str)


# read in variables file and creates a dictionary for each domain
def read_var_file(file_name):
    with open(file_name, "r") as file:
        domains = {}

        for line in file:
            domain = line.split(" ")
            null_terminator = len(domain[len(domain) - 1]) - 1
            if domain[len(domain) - 1][null_terminator] == "\n":
                domain[len(domain) - 1] = domain[len(domain) - 1][:null_terminator]
            if not domain[len(domain) - 1].isnumeric():
                domain.pop(len(domain) - 1)
            domains[domain.pop(0)[0]] = domain

        for var in domains.keys():
            for i in range(len(domains[var])):
                domains[var][i] = int(domains[var][i])

        return domains


# read in constraints file and create a dictionary of constraints for each variable
def read_con_file(file_name):
    with open(file_name, "r") as file:
        constraints = {}

        for line in file:
            elements = line.split(" ")
            constraint = Constraint(elements[0], elements[1], elements[2][0])
            reverse_constraint = constraint.reverse()

            if elements[0] in constraints:
                constraints[elements[0]] = constraints[elements[0]] + [constraint]
            else:
                constraints[elements[0]] = [constraint]

            if elements[2][0] in constraints:
                constraints[elements[2][0]] = constraints[elements[2][0]] + [
                    reverse_constraint
                ]
            else:
                constraints[elements[2][0]] = [reverse_constraint]

        return constraints


# tiebreaker for choosing variable, chooses most constraining or first alphabetically
def most_constraining_variable(variables, constraints, assignments):
    max_constraints = -1
    result = []
    for var in variables:
        con_count = 0
        for constraint in constraints[var]:
            if constraint.operand() not in assignments:
                con_count += 1

        if con_count > max_constraints:
            max_constraints = con_count
            result = [var]
        elif con_count == max_constraints:
            result = result + [var]

    if len(result) > 0:
        result.sort()
        return result[0]
    else:
        return False


# iterates through unassigned variables and finds the smallest domain
# domains only consist of possible values checked with current assignments and constraints
def fc_most_constrained_variable(domains, constraints, assignments):
    possible_domains = copy.deepcopy(domains)

    for var in assignments.keys():
        for constraint in constraints[var]:
            removal_list = []
            for val in possible_domains[constraint.operand()]:
                if not constraint.evaluate(assignments[var], val):
                    removal_list = removal_list + [val]

            for invalid in removal_list:
                new_domain = possible_domains[constraint.operand()]
                new_domain.remove(invalid)
                possible_domains[constraint.operand()] = new_domain

    result = []
    min_length = float("inf")
    for var in possible_domains.keys():
        if var not in assignments:
            if len(possible_domains[var]) < min_length:
                min_length = len(possible_domains[var])
                result = [var]
            elif len(possible_domains[var]) == min_length:
                result = result + [var]

            if len(possible_domains[var]) == 0:
                return False

    if len(result) == 1:
        return result[0]
    else:
        return most_constraining_variable(result, constraints, assignments)


# iterates through unassigned variables and finds the smallest domain
def most_constrained_variable(domains, constraints, assignments):
    result = []
    min_length = float("inf")
    for var in domains.keys():
        if var not in assignments:
            if len(domains[var]) < min_length:
                min_length = len(domains[var])
                result = [var]
            elif len(domains[var]) == min_length:
                result = result + [var]

    if len(result) == 1:
        return result[0]
    else:
        return most_constraining_variable(result, constraints, assignments)


# iterates through variable domain to find the least constraining value
# domain only consists of possible values checked with current assignments and constraints
def fc_least_constraining_value(variable, domains, constraints, assignments):
    possible_domains = copy.deepcopy(domains)

    for var in assignments.keys():
        if var in assignments:
            for constraint in constraints[var]:
                removal_list = []
                for val in possible_domains[constraint.operand()]:
                    if not constraint.evaluate(assignments[var], val):
                        removal_list = removal_list + [val]

                for invalid in removal_list:
                    new_domain = possible_domains[constraint.operand()]
                    new_domain.remove(invalid)
                    possible_domains[constraint.operand()] = new_domain

    max_head_count = -1
    result = []
    for val in possible_domains[variable]:
        head_count = 0

        for var in possible_domains.keys():
            if var not in assignments:
                for remaining_val in possible_domains[var]:
                    val_not_constrained = True
                    for constraint in constraints[var]:
                        if constraint.operand() == variable:
                            if not constraint.evaluate(remaining_val, val):
                                val_not_constrained = False

                    if val_not_constrained:
                        head_count += 1

        if head_count > max_head_count:
            max_head_count = head_count
            result = [val]
        elif head_count == max_head_count:
            result = result + [val]

    if len(result) > 0:
        result.sort()
        return result[0]
    else:
        result = domains[variable]
        result.sort()
        return result[0]


# iterates through variable domain to find the least constraining value
def least_constraining_value(variable, domains, constraints, assignments):
    max_head_count = -1
    result = []
    for val in domains[variable]:
        head_count = 0

        for var in domains.keys():
            if var not in assignments:
                for remaining_val in domains[var]:
                    val_not_constrained = True
                    for constraint in constraints[var]:
                        if constraint.operand() == variable:
                            if not constraint.evaluate(remaining_val, val):
                                val_not_constrained = False

                    if val_not_constrained:
                        head_count += 1

        if head_count > max_head_count:
            max_head_count = head_count
            result = [val]
        elif head_count == max_head_count:
            result = result + [val]

    if len(result) > 0:
        result.sort()
        return result[0]
    else:
        result = domains[variable]
        result.sort()
        return result[0]


# backtracking procedure that invokes forward checking functions, returns correct assignments or False
def fc_backtracking(domains, constraints, assignments):
    valid = True
    for var in constraints.keys():
        for constraint in constraints[var]:
            if var in assignments and constraint.operand() in assignments:
                if not constraint.evaluate(
                    assignments[var], assignments[constraint.operand()]
                ):
                    valid = False
            else:
                valid = False

    if valid:
        print_assignments(assignments, "solution")
        return assignments

    curr_var = fc_most_constrained_variable(domains, constraints, assignments)
    if curr_var is False:
        print_assignments(assignments, "failure")
        return False

    adjusted_domains = copy.deepcopy(domains)
    for possible_val in domains[curr_var]:
        best_val = fc_least_constraining_value(
            curr_var, adjusted_domains, constraints, assignments
        )

        assignments[curr_var] = best_val
        result = fc_backtracking(adjusted_domains, constraints, assignments)
        if result is not False:
            return result
        else:
            del assignments[curr_var]
            removed_domain = adjusted_domains[curr_var]
            removed_domain.remove(best_val)
            adjusted_domains[curr_var] = removed_domain

    return False


# standard recursive backtracking procedure, returns correct assignments or False
def backtracking(domains, constraints, assignments):
    all_assigned = True
    for var in constraints.keys():
        if var not in assignments:
            all_assigned = False
    if all_assigned:
        return assignments

    valid = True
    for var in assignments.keys():
        for constraint in constraints[var]:
            if constraint.operand() in assignments:
                if not constraint.evaluate(
                    assignments[var], assignments[constraint.operand()]
                ):
                    valid = False
    if not valid:
        print_assignments(assignments, "failure")
        return False

    curr_var = most_constrained_variable(domains, constraints, assignments)

    adjusted_domains = copy.deepcopy(domains)
    for possible_val in domains[curr_var]:
        best_val = least_constraining_value(
            curr_var, adjusted_domains, constraints, assignments
        )

        assignments[curr_var] = best_val
        result = backtracking(adjusted_domains, constraints, assignments)

        if result is not False:
            valid = True
            for var in constraints.keys():
                for constraint in constraints[var]:
                    if not constraint.evaluate(
                        result[var], result[constraint.operand()]
                    ):
                        valid = False

            if valid:
                return result
            else:
                print_assignments(assignments, "failure")

        del assignments[curr_var]
        removed_domain = adjusted_domains[curr_var]
        removed_domain.remove(best_val)
        adjusted_domains[curr_var] = removed_domain

    return False


# backtracking with forward checking
def forward_checking(domains, constraints):
    assignments = {}

    fc_backtracking(domains, constraints, assignments)


# backtracking without forward checking
def normal_checking(domains, constraints):
    assignments = {}

    result = backtracking(domains, constraints, assignments)
    if result is not False:
        valid = True
        for var in constraints.keys():
            for constraint in constraints[var]:
                if not constraint.evaluate(result[var], result[constraint.operand()]):
                    valid = False

        if valid:
            print_assignments(result, "solution")


if __name__ == "__main__":
    var_file = sys.argv[1] if len(sys.argv) > 1 else None
    con_file = sys.argv[2] if len(sys.argv) > 2 else None
    con_procedure = sys.argv[3] if len(sys.argv) > 3 else None

    var_domains = read_var_file(var_file)

    all_constraints = read_con_file(con_file)

    for key in var_domains.keys():
        if key not in all_constraints:
            all_constraints[key] = []

    if con_procedure == "fc":
        forward_checking(var_domains, all_constraints)
    else:
        normal_checking(var_domains, all_constraints)

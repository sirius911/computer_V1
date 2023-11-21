# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parsing.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: clorin <clorin@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/11 01:35:31 by clorin            #+#    #+#              #
#    Updated: 2023/11/21 22:55:38 by clorin           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from polynome import PowerFunction, Polynome

def prepare_expression(str_val):
    """
    take the string expression
    return a well formatted 2 dimensional tab
    format expression [+|-|""][0-9*][*X[^[0-9*]]]
    """
    str_val = str_val.replace(" ", "").replace("\t", "").replace("\n", "").replace("+", " +").replace("-",
        " -").replace(
        "=", " = ")
    expres = str_val.split("=")
    index = 0
    while index < len(expres):
        expres[index] = expres[index].strip()
        index += 1
    return expres

def parser(e):
    """
        input : expression 
    """
    X = ('X' in e)
    index = 0
    len_elem = len(e)
    if e[0] == "-":
        index = 1
    if e[0] == "+":
        index = 1
    while index < len_elem and ((e[index] == ".") or (e[index].isdigit())):
        index += 1
    if index == len_elem - 1 and e[index] == "X":
        # only +X ou -X
        q = e.replace("+", "").replace("-", "")
        if len(q) == 1 and q == "X":
            if e[0] == "-":
                poid_x = -1
            else:
                poid_x = 1
            power = 1
            return (PowerFunction(float(poid_x), int(power), X))
    if index == len_elem and e[index - 1] == ".":
        print("Error format [{0}]".format(e))
        return None
    try:
        if (len(e) == 1):
            poid_x = float(e[:index])
        else:
            if (index == len(e)):
                poid_x = float(e[:index])
            elif e[index] == "X":
                if (e[0] == '+' or e[0] == '-') and e[1] == 'X':
                    if (e[0] == '-'):
                        poid_x = -1
                    else:
                        poid_x = 1
                elif e[0] == 'X':
                    poid_x = 1
                else:
                    poid_x = float(e[:index])
            else:
                poid_x = float(e[:index])
    except ValueError:
        print("Error format [{0}]".format(e))
        return None
    power = 0
    if index < len_elem:
        if e[index] == "*" or e[index] == "X":
            if e[index] == "*":
                index += 1
            if index < len_elem and e[index] == "X":
                index += 1
                if index < len_elem and (e[index] == "^" or e[index].isdigit()):
                    if not e[index].isdigit():
                        index += 1
                    if index == len_elem:
                        print("Error format : the power of the unknown element is not indicated : [{0}]".format(e))
                        return None
                    else:
                        power = e[index:]
                        if not power.isdigit():
                            print(
                                "Error format : the power of the unknown element is not well formatted: [{0}] int expected".format(e))
                            return None
                elif index == len_elem:
                    power = 1
                else:
                    print("Error format : the element [{0}] is not well formatted".format(e))
                    return None
            else:
                print("Error format: The expression is not well formatted in element [{0}]".format(e))
                return None
        else:
            print("Error format: The expression is not well formatted in element [{0}]".format(e))
            return None
    return (PowerFunction(float(poid_x), int(power), X))

def parse_expression(expression):
    """
        extract information in the expression 
        return a Polynome
    """
    polynome = Polynome()
    left_part = expression[0].split(" ")
    right_part = expression[1].split(" ")
    if len(left_part[0]) == 0 or len(right_part[0]) == 0:
        print("Error: sign '=' alone in expression.")
        exit(0)
    for e in left_part:
        polynome.add(parser(e), +1)
    for e in right_part:
        polynome.add(parser(e), -1)
    return polynome
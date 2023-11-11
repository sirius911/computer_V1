# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computer_v1.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: clorin <clorin@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/10 17:26:50 by clorin            #+#    #+#              #
#    Updated: 2023/11/11 17:14:28 by clorin           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from parsing import parse_expression, prepare_expression
from colors import colors

def usage():
    print("Usage : \npython3 main.py '[aX2] + bX + c = 0]'")

def titre():
    print("   ____                            _             __     ___ ")
    print("  / ___|___  _ __ ___  _ __  _   _| |_ ___ _ __  \ \   / / |")
    print(" | |   / _ \| '_ ` _ \| '_ \| | | | __/ _ \ '__|  \ \ / /| |")
    print(" | |__| (_) | | | | | | |_) | |_| | ||  __/ |      \ V / | |")
    print("  \____\___/|_| |_| |_| .__/ \__,_|\__\___|_|       \_/  |_|")
    print("                      |_|                                   ")

def main(_str):
    titre()
    polynome = parse_expression(prepare_expression(_str))
    print(f"Reduced form: {colors.blue}{polynome}{colors.reset}")
    max_pow = polynome.max_power()
    print(f"Polynomial degree: {colors.blue}{max_pow}{colors.reset}")
    if max_pow > 2:
        print("Error: The Polynomial degree is stricly greater than 3, I can't solve")
        exit(0)
    else:
        _,_,_,delta = polynome.delta()
        print(f"Discriminant Δ = {colors.yellow}{delta}{colors.reset}")
        _, _ = polynome.solution()
    # print(polynome.f(x1), polynome.f(x2))


if __name__ == "__main__":
    if len(sys.argv) == 2 :
        _str = sys.argv[1]
        nb_equal = len(_str.split("="))
        if nb_equal > 2:
            print("Error, multiple '=' found in the expression.")
            exit(0)
        elif nb_equal == 1:
            _str += " = 0"
        main(_str)    
    else:
        usage()

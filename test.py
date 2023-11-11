# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: clorin <clorin@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/11 13:47:10 by clorin            #+#    #+#              #
#    Updated: 2023/11/11 17:57:33 by clorin           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import subprocess
import os

from termcolor import colored
from computer_v1 import main
from colors import remove_color_codes
from utils import REELS
import re

equations_test = [
    {'equation': 'coucou = 42', 'reduct': None, 'discr': None, 'result': None, 'valid': False},
    {'equation': '', 'reduct': None, 'discr': None, 'result': None, 'valid': False},
    {'equation': '=', 'reduct': None, 'discr': None, 'result': None, 'valid': False},
    {'equation': '5X - 4 = ', 'reduct': None, 'discr': None, 'result': None, 'valid': False},
    {'equation': ' = 2X^2', 'reduct': None, 'discr': None, 'result': None, 'valid': False},
    {'equation': '5x - 4 = 0', 'reduct': None, 'discr': None, 'result': None, 'valid': False},
    {'equation': '2X^3 - 5X^2 +4X -21 = 0', 'reduct': '-21.0 +4.0x -5.0x² +2.0x³ = 0', 'discr': None, 'result': None, 'valid': False},
    {'equation': '5X - 4 = 0', 'reduct': '-4.0 +5.0x = 0', 'discr': 25, 'result': 0.8, 'valid': True},
    {'equation': '2X + 3 = 0', 'reduct': '3.0 +2.0x = 0', 'discr': 4, 'result': -1.5, 'valid': True},
    {'equation': 'X^2 - 1 = 0', 'reduct': '-1.0 +x² = 0', 'discr': 4, 'result': [-1.0, 1.0], 'valid': True},  
    {'equation': '3X - 6 = 0', 'reduct': '-6.0 +3.0x = 0', 'discr': 9, 'result': 2.0, 'valid': True},
    {'equation': '3.0X = 6', 'reduct': '-6.0 +3.0x = 0', 'discr': 9, 'result': 2.0, 'valid': True},
    {'equation': '3X-6', 'reduct': '-6.0 +3.0x = 0', 'discr': 9, 'result': 2.0, 'valid': True},
    {'equation': 'X = 6', 'reduct': '-6.0 +x = 0', 'discr': 1.0, 'result': 6.0, 'valid': True},
    {'equation': '0X^1= 6', 'reduct': '-6.0 +0.0x = 0', 'discr': 0.0, 'result': None, 'valid': True},
    {'equation': '0X^1= 0', 'reduct': '+0.0x = 0', 'discr': 0.0, 'result': REELS, 'valid': True},
    {'equation': '0 =   2X^2 - 3X - 5', 'reduct': '5.0 +3.0x -2.0x² = 0', 'discr': 49.0, 'result':[2.5, -1.0], 'valid': True},
    {'equation': '4X2 -6X - 12 = 0', 'reduct': '-12.0 -6.0x +4.0x² = 0', 'discr': 228.0, 'result': [-1.1374586088176875,2.6374586088176875], 'valid': True},
    {'equation': '\t4X2 -6X - \t12 \n= 0', 'reduct': '-12.0 -6.0x +4.0x² = 0', 'discr': 228.0, 'result': [-1.1374586088176875,2.6374586088176875], 'valid': True},
    {'equation': '4X^2 -6*X = 12', 'reduct': '-12.0 -6.0x +4.0x² = 0', 'discr': 228.0, 'result': [-1.1374586088176875,2.6374586088176875], 'valid': True},
    {'equation': '3X^2 - 6X2 + 10X - 45 = 4X2 - X +2', 'reduct': '-47.0 +11.0x -7.0x² = 0', 'discr': -1195.0, 'result': ['0.7857142857142857 -i-2.4691980024919435', '0.7857142857142857 +i-2.4691980024919435'], 'valid': True}, #complex
]

def extract_result(lines):
    """
        export result of polynome.solving from line output
    """
    reduced_form = None
    discriminant = None
    result = None
    valid_result = True
    for line in lines:
        if line.startswith('Error'):
            valid_result = False
            break
        elif line.startswith('Reduced form:'):
            reduced_form = line[len('Reduced form:'):].strip()
        elif line.startswith('Discriminant Δ ='):
            discriminant = float(line.split('=')[1].strip())
        elif line.startswith('Discriminant is strictly positive, the two solution are:'):
            solutions_match = re.search(r'x1 = (.+) & x2 = (.+)', lines[lines.index(line) + 1])
            if solutions_match:
                result = [float(solutions_match.group(1).strip()), float(solutions_match.group(2).strip())]
        elif line.startswith('Discriminant is negative, the solutions are in complex:'):
            solutions_match = re.search(r'x1 = (.+) & x2 = (.+)', lines[lines.index(line) + 1])
            if solutions_match:
                result = [(solutions_match.group(1).strip()), (solutions_match.group(2).strip())]
        elif line.startswith('The solution is'):
            result = float(line[len('The solution is '):].strip())
        elif line.startswith('All the x ∈ ℝ are the sollution !!'):
            result = REELS
    return (reduced_form, discriminant, result, valid_result)

def test(equation):
    """
    exec command computer_v1 with the equation
    and return if the result is expected
    """
    script_path = os.path.abspath('computer_v1.py')
    valid_equ = equation['valid']
    eq = equation['equation']
    print(f"[{equation['equation']}] ", end = '')
    if not valid_equ:
        print(f"[{colored('Invalid', 'yellow')}]", end='')
    print(" => ", end='')
    command = ['python3', script_path, eq]
    output = subprocess.check_output(command, universal_newlines=True)
    output = remove_color_codes(output)
    lines = output.split('\n')
    reduced_form, discriminant, result, valid_result = extract_result(lines)
    good = True
    if valid_result == valid_equ:
        if reduced_form != equation['reduct']:
            good = False
            print(f"❌ reduced form = {colored(reduced_form, 'yellow')} expected : {colored(equation['reduct'], 'yellow')}")
        if discriminant != equation['discr']:
            good = False
            print(f"❌ Δ = {colored(discriminant, 'yellow')} expected : {colored(equation['discr'], 'yellow')}")
        if result != equation['result']:
            good = False
            print(f"❌ result = {colored(result, 'yellow')} expected {colored(equation['result'], 'yellow')}")
    else:
        good = False
        print(f"❌ valid = {colored(str(valid_result), 'yellow')} expected : {colored(str(valid_equ), 'yellow')}")
    if good:
        print(f"✅")
    return good

def main():
    good_test = True
    for equation in equations_test:
        good_test = test(equation) and good_test
    print(f"\n GLOBAL RESULT : ", end='')
    if good_test:
        print(f"✅")
    else:
        print(f"❌") 

if __name__ == "__main__":
    main()
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    polynome.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: clorin <clorin@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/11 01:41:38 by clorin            #+#    #+#              #
#    Updated: 2023/11/21 22:56:16 by clorin           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cmath
from collections import OrderedDict
from utils import get_unicode_exponent, REELS
from colors import colors

class PowerFunction:
    """
        Class representing the expression aX^b.
        This function is a general form of a power function,
        where a is the coefficient, X is the variable, and b is the exponent.
        if X is false _coefficient is the Constant
    """
    def __init__(self, a, b, X):
        self._coefficient = a
        self._exponent = b
        if b == 0:
            self.X = False
        else:
            self.X = X

    def __str__(self):
        if self.X:
            a = ('' if abs(self._coefficient) == 1 else f"{self._coefficient:+}")
            if a == '':
                if self._coefficient > 0:
                    a = '+'
                else:
                    a = '-'
            return (f"{a}x{get_unicode_exponent(self._exponent)}")
        else:
            return (f"{self._coefficient:+}")
        
    def add_coef(self, x):
        self._coefficient += x

class Polynome:
    """
        Class representing a Polynome
        a dict of Powerfonction 
    """
    def __init__(self):
        self.poly = dict()
        self.constant = 0

    def get_coeff(self, power):
        """
            return the coefficient of the polynome with power
            or 0 if it does'nt exist
        """
        if power in self.poly:
            return self.poly[power]._coefficient
        else:
            return 0

    def add(self, pf, sign):
        """
            add a Powerfonction pf
        """
        to_del = []
        if pf:
            if not pf.X:
                self.constant += (sign * pf._coefficient)
            else:
                if pf._exponent in self.poly.keys():
                    for expo, powerFunction in self.poly.items():
                        if expo == pf._exponent:
                            powerFunction.add_coef(sign * pf._coefficient)
                            if powerFunction._coefficient:
                                self.poly[pf._exponent] = powerFunction
                            else:
                                # to delete
                                to_del.append(pf._exponent)
                else:
                    self.poly[pf._exponent] = PowerFunction(sign * pf._coefficient, pf._exponent, pf.X)
            #del all coefficient = 0
            for d in to_del:
                del self.poly[d]
            self.sort()
        else:
            exit(0)
            
    def __str__(self):
        ret = ''
        if len(self.poly) > 0:
            if self.constant:
                ret += f"{self.constant} "
            for _, pf in self.poly.items():
                ret += pf.__str__() + ' '
            ret += "= 0"
        else:
            ret = f"{self.constant} = 0"
        return ret
    
    def sort(self):
        """
        sort the poly dict
        """
        dictionnaire_trie = OrderedDict(sorted(self.poly.items(), key = lambda x: x[1]._exponent))
        self.poly = dictionnaire_trie

    def max_power(self):
        """
            return the power max of polynome dict
        """
        last_key = 0
        if self.poly:
            last_key = list(self.poly.keys())[-1]
        return last_key
    
    def delta(self):
        """
        in a polynome : Ax²+Bx+C=0
        return A, B, C and Δ = B² - 4AC or None
        """
        A = self.get_coeff(2)
        B = self.get_coeff(1)
        C = self.constant
        delta = (B * B) - (4 * A * C)
        return (A,B,C,delta)
    
    def f(self, x):
        """
        calcul the polynome with X=x
        """
        total = 0
        for _, pf in self.poly.items():
            coef = pf._coefficient
            expo = pf._exponent
            total += coef * (x ** expo)
        total += self.constant
        return total
    
    def solution(self):
        """
            solv the polynome and return x1 & x2
        """
        x1 = x2 = None
        A , B, C, delta = self.delta()
        if A == 0:
            #linear form
            if B != 0:
                x1 = x2 = -(C / B)
                print(f"{colors.yellow}It's a linear equation.{colors.reset}")
                print(f"The solution is {colors.green}{x1}{colors.reset}")
            else:
                if C != 0:
                    print(f"{colors.red}There's no solution !!{colors.reset}")
                else:
                    print(f"All the {colors.green}x{colors.reset} ∈ {colors.yellow}{REELS}{colors.reset} are the solution !!")    
                    x1 = x2 = REELS
        elif delta == 0:
            x1 = x2 = (-B) / (2 * A)
            print(f"{colors.yellow}Discriminant = 0{colors.reset}, the unique solution is : {colors.green}{x1}{colors.reset}")
        elif delta > 0:
            x1 = (-B - (delta ** 0.5)) / (2 * A)
            x2 = (-B + (delta ** 0.5)) / (2 * A)
            print(f"Discriminant is strictly positive, the two solution are:")
            print(f"x1 = {colors.green}{x1}{colors.reset} & x2 = {colors.green}{x2}{colors.reset}")
        else:
            r = (abs(delta) **  0.5)
            print(f"Discriminant is negative, the solutions are in complex:")
            x1 = f"{colors.blue}{(-B)/(2*A)}{colors.reset} {colors.red}-i{colors.reset}{colors.green}{r/(2*A)}{colors.reset}"
            x2 = f"{colors.blue}{(-B)/(2*A)}{colors.reset} {colors.red}+i{colors.reset}{colors.green}{r/(2*A)}{colors.reset}"
            print(f"x1 = {x1} & x2 = {x2}")
        return (x1, x2)

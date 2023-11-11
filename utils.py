# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    utils.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: clorin <clorin@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/11 01:39:49 by clorin            #+#    #+#              #
#    Updated: 2023/11/11 17:11:01 by clorin           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from colors import colors

REELS = 'ℝ'

exposants_dict = {
    0: '⁰',
    1: '¹',
    2: '²',
    3: '³',
    4: '⁴',
    5: '⁵',
    6: '⁶',
    7: '⁷',
    8: '⁸',
    9: '⁹'
}

def get_unicode_exponent(exponent):
    """
        return exponent int
        3 -> ³
    """
    ret = ''
    chaine = str(abs(exponent))
    if len(chaine) == 1:
        if exponent > 1 :
            return exposants_dict[int(chaine)]
        else:
            return ""
    for c in chaine:
        ret += exposants_dict[int(c)]
    return ret

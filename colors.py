# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    colors.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: clorin <clorin@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/11 12:30:30 by clorin            #+#    #+#              #
#    Updated: 2023/11/11 17:11:37 by clorin           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class colors:
    green = '\033[92m' # vert
    blue = '\033[94m' # blue
    yellow = '\033[93m' # jaune
    red = '\033[91m' # rouge
    reset = '\033[0m' #gris, couleur normales

def remove_color_codes(input_string):
    """
        remove the color's Code in a string
    """
    color_codes = [colors.green, colors.blue, colors.yellow, colors.red, colors.reset]

    for code in color_codes:
        input_string = input_string.replace(code, '')

    return input_string
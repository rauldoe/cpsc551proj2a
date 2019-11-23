# clear;python3 arithmetic_server.py
# clear;python arithmetic_server.py

import re

import Arithmetic

srv = Arithmetic.Arithmetic()

doProcess = True

while doProcess:
    output = srv._in((re.compile("^[-+/*]$"), int, int))
    calc = output['output']
    
    answer = 0
    operator = calc[0]
    left = int(calc[1])
    right = int(calc[2])

    if (operator == '-'):
        answer = left - right
    elif (operator == '+'):
        answer = left + right
    elif (operator == '/'):
        answer = left / right
    elif (operator == '*'):
        answer = left * right

    ret = srv._out(['result', answer])

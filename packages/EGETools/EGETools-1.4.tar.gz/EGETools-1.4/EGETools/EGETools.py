"""
Copyright (c) 2023, Alexander Blinov

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice,
 this list of conditions and the following disclaimer.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import re

def isPalindrome(number):
    if str(number) == str(number)[::-1]:
        return True
    else:
        return False


def getDividers(number):
    mas = []

    if int(number ** 0.5) ** 2 == number:
        mas.append(int(number ** 0.5))

    for i in range(1, int(number ** 0.5) + 1):
        if number % i == 0:
            mas.append(i)
            mas.append(number // i)

    return sorted(list(set(mas)))


def maxDividerNotEqualsToNumber(number):
    mas = []

    if int(number ** 0.5) ** 2 == number:
        mas.append(number ** 0.5)

    for i in range(2, int(number ** 0.5)):
        if number % i == 0:
            mas.append(i)
            return number // i


def notEvenIndexDigits(number):
    ret = []

    for k in range(1, len(str(number)) + 1, 2):
        ret.append(k)

    return ret


def notEvenDigits(number):
    ret = []

    for k in str(number):
        if int(k) % 2 != 0:
            ret.append(int(k))

    return ret


def sumOfDigits(number):
    ret = 0

    for g in str(number):
        ret += int(g)

    return ret


def decToBase(a, base):
    dict_ = '0123456789abcdefghi'
    s = ''
    while a != 0:
        s = str(dict_[a % base]) + s
        a //= base
    return s


def checkMask(number, mask):
    return bool(re.compile(mask.replace('?', '[0-9]').replace('*', '([0-9]+|)') + "$").match(str(number)))

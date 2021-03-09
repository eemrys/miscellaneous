import math
from copy import deepcopy


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits[len(bits) % 8:], 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0' 

def str_to_bin_list(text):
    binarr = []
    for t in text:
        binarr.append(int(t))
    return binarr

def bin_list_to_str(arr):
    string = ''
    for a in arr:
        string += str(a)
    return string

def add_ctrl_bits(arrIn):
    arr = deepcopy(arrIn)
    n = len(arr)
    position = 0
    i = 1
    while position < n:
        arr.insert(position, 0)
        position = int(math.pow(2, i) - 1)
        i += 1
        n += 1
    arr = control_bits(arr)
    return arr

def control_bits(arrIn):
    arr = deepcopy(arrIn)
    n = len(arr)
    position = 0
    i = 1
    while position < n:
        sumcontrol = 0
        j = position
        while j < n:
            endBatch = n if j + (position + 1) >= n else j + (position + 1) 
            stratBatch = j+1 if j == position else j
            batch = [arr[b] for b in range(stratBatch, endBatch)]
            sumcontrol += sum(batch)
            j = j + (position + 1)*2
        arr[position] = sumcontrol % 2
        position = int(math.pow(2, i) - 1)
        i += 1
    arr.append(sum(arr) % 2)
    return arr

def check_bits(arr):
    correctArr = deepcopy(arr)
    oneError = False
    moreErrors = False
    n = len(arr) - 1
    correctArr = control_bits(correctArr[:-1])
    errors = 0
    for i, v in enumerate(correctArr[:-1]):
        if v != arr[i]:
            errors += (i + 1)
    errors -= 1
    if errors >= 0:
        if errors < n:
            correctArr = deepcopy(arr)
            correctArr[errors] = int(not correctArr[errors])
        correctArr[-1] = sum(correctArr[:-1]) % 2
        if errors > n or correctArr[-1] != arr[-1]:
            moreErrors = True
        else:
            oneError = True
    return correctArr, oneError, moreErrors

def del_control_bits(arr):
    newArr = []
    power = 1
    for i, v in enumerate(arr[:-1]):
        if i != (power - 1):
            newArr.append(v)
        else:
            power *= 2
    return newArr
    

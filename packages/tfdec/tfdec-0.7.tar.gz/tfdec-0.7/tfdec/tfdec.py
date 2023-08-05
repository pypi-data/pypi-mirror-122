def fromdec(num, radix):
    num = abs(num)
    radnum = ""
    while (num >= 1):
        if (num < radix):
            radnum = str(num)+radnum
            break
        mod = num%radix
        radnum = str(mod)+radnum
        num = num//radix
    return int(radnum)


def todec(num, radix):
    num = abs(num)
    decnum = 0
    for i in range(0, len(str(num))):
        if (int(str(num)[i]) >= radix ):
            return -1
    for i in range(0, len(str(num))):
        f = int(str(num)[i])*(radix**(len(str(num))-1-i))
        decnum += f
    return int(decnum)

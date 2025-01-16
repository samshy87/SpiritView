
def float_1750A_32bit_toDecimal(inBytes):
    theSign = 1
    theExp = (inBytes & 0xFF)
    theMantissa = (inBytes >> 8)
    theFraction = 0

    if (theExp>>7) == 1:
        theExp = ~theExp
    
    if (theMantissa>>23) == 1:
        theSign = -1
        theMantissa = ~theMantissa
        
    for i in range(23):
        if (theMantissa>>(22-i)) & 0x1 == 1:
            theFraction += 2**(-(i+1))
    
    return((theFraction * theSign * (2**theExp)))




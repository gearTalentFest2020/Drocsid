# table = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
table = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
getval = lambda val: table.index(val) if val in table else int(val)
setval = lambda val: table[val] if val < len(table) else str(val)
def B2D(val:str, base:int, delimiter:str):
    integ = val.split(".")[0]
    if "." in val:
        frac = val.split(".")[1]
    else:
        frac = "0"
    if delimiter != "":
        integ = integ.split(delimiter)
        frac = frac.split(delimiter)
    else:
        frac = list(frac)
        integ = list(integ)
    integ = "".join(integ)
    frac = "".join(frac)
    resint = 0
    resfrac = 0.0
    # print(integ, frac)
    for i in range(len(integ)):
        resint += getval(integ[-1-i])*pow(base, i)
    for i in range(len(frac)):
        resfrac += getval(frac[i])/(base**(i+1))
    # print(resint, resfrac)
    return [str(resint), str(resfrac)]

def D2B(val:list, base:int, delimiter:str, prec:int):
    integ = val[0]
    frac = val[1]
    resint = []
    resfrac = []
    # print(integ, frac)
    while integ != "0":
        r = int(integ)%base
        resint = [setval(r)] + resint
        integ = str(int(integ)//base)
    p = 0
    while frac != "0.0" and p < prec:
        p += 1
        i = (float(frac)*base)//1
        # print(int(i))
        resfrac += [setval(int(i))]
        # print(str(float(frac)*base))
        if "e" in frac:
            frac = str((float(frac)*base)-int((float(frac)*base)))
        else:
            frac = "0." + str(float(frac)*base).split(".")[1]
        # print(frac)
    resint = delimiter.join(resint)
    resfrac = delimiter.join(resfrac)
    if resfrac == "":
        resfrac = "0"
    return str(resint + "." + resfrac)

def convert(val:str, src_base:int, dest_base:str, src_delimiter:str="", dest_delimiter:str="", prec:int=36):
    # assert prec == int(prec), "precision must be an integer"
    # assert src_base == int(src_base), "src_base must be an integer"
    # assert dest_base == int(dest_base), "dest_base must be an integer"
    # assert src_base > 1, "src_base must be greater than 1"
    # assert dest_base > 1, "dest_base must be greater than 1"
    if prec == int(prec):
        if src_base > 1 and dest_base > 1 and src_base == int(src_base) and dest_base == int(dest_base):
            return D2B(B2D(val, src_base, src_delimiter), dest_base, dest_delimiter, prec)
        else:
            print("Invalid base. Base should be an integer greater than 1.")
    else:
        print("Invalid precision. Precision should be an integer")


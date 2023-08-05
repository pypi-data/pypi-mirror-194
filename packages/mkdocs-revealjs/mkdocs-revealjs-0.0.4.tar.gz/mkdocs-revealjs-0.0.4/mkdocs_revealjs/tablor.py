import giacpy as g
from giacpy import giac, assume, pi, derive, factor, simplify, solve, tabvar

import subprocess
import shlex

X = 0
FPX = 1
FX = 2
FPPX = F2X = 3

SPACE = '" "'
PLUS_SIGN = '"+"'
MINUS_SIGN = '"-"'
PLUS_INFINITY = "+infinity"
MINUS_INFINITY = "-infinity"
DOUBLE_BAR = '"||"'
HIDDEN_SIGN = '"h"'

UP_ARROW = '"↑"'
DOWN_ARROW = '"↓"'
WHAT = '"- (∩)"'
ELSE = '"- (∪)"'

print("HELLO FROM INSIDE")

# a, x,y,z = g.giac('a, x,y,z')
# g.assume('x>-pi && x<pi')
# l = g.solve('x^2-1=0',x)


def get_derivee(f:str,x:str):
    return factor(simplify(derive(f,x)))

def get_name_variable(fx: str):
    """ returns function name 'f', and function variable 'x'
    from string like "f(x)=x^3"
    """
    i_po = fx.index("(")
    i_pf = fx.index(")")
    i_eq = fx.index("=")
    if i_po < i_eq and i_pf < i_eq:
        return fx[:i_po], fx[i_po+1:i_pf]
    else:
        return "f", "x"

def get_latex(s:str):
    """ Converts Giac Expression to LaTex,
    AND then to python str,
    AND removes leading and tailing quotes,
    to be TeX-ready to be directly inserted in VarTables
    """
    s = str(g.latex(s))[1:-1]
    s = s.replace(" ", "")
    return s

def get_tabvar(s:str, x:str):
    g.assume(f"{x}>=-1 && {x}<=1")
    return tabvar(s, x)

def get_listeVI(tabvar):
    VI = []
    for i in range(len(tabvar[FPX])):
        if tabvar[FPX][i] == DOUBLE_BAR:
            if not tabvar[X][i] in VI:
                VI.append(tabvar[X][i])
    return VI

def est_VI(candidatVI, tabvar):
    return candidatVI in get_listeVI(tabvar)

def escape_Tex_for_Python(s:str):
    newS = r""
    for c in s:
        if c == "{":
            c = r"{{"
        if c == "}":
            c = r"}}"
        newS += c
    return newS

def get_function_body(fx: str):
    """ returns function body 'x^3'
    from string like "f(x)=x^3"
    """
    i_eq = fx.index("=")
    return fx[i_eq+1:]

def get_solve(eqIneq:str, x:str)->list:
    return solve(eqIneq, x)
    # return g.resoudre(eqIneq, x)

def get_icas(command:str, content):
    # Start of Popen
    cmd_parts = [f"""icas '{command}'"""]
    i = 0
    p = {}
    for cmd_part in cmd_parts:
        try:
            cmd_part = cmd_part.strip()
            if i == 0:
                p[0]=subprocess.Popen(shlex.split(cmd_part),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                p[i]=subprocess.Popen(shlex.split(cmd_part),stdin=p[i-1].stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            i += 1
        except Exception as e:
            err = str(e) + ' : ' + str(cmd_part)
            return (
                '<pre>Error : ' + err + '</pre>'
                '<pre>' + content + '</pre>').split('\n')
    (output, err) = p[i-1].communicate()
    exit_code = p[0].wait()
    output = output.decode("utf-8")
    i_co = output.index("list[")
    i_cf = output.index("]")
    # str to list
    output = output[i_co+5:i_cf+1].split(",")
    # list to Pygen.list
    output = giac(output)    
    return output

def get_xValuesInInterval(fpx:str, x:str, a:str , b:str)->list:
    fpx = factor(simplify(fpx))
    x = giac(f"{x}")
    # print(f"{x}>={a} && {x}<{b}")
    assume(f"{x}>={a} && {x}<={b}")
    return solve(f"{fpx}*({x}-{a})*({x}-{b})=0", x)
    # return g.resoudre(eqIneq, x)

def get_factor(s:str):
    return factor(s)

def get_xValues_from(tabvar):
    l = []
    for i in range(1,len(tabvar[X])):
        if tabvar[X][i] not in l and tabvar[X][i] != SPACE:
            l.append(tabvar[X][i])
    return l

# def get_fpxValues_from(tabvar):
#     l = []
#     for i in range(1,len(tabvar[FPX])):
#         fpxEl = tabvar[FPX][i]
#         if fpxEl not in l:
#             if fpxEl == 0:
#                 print("Adding 0")
#                 l.append("0")
#             elif fpxEl == PLUS_SIGN:
#                 print("Adding +")
#                 l.append("+")
#             elif fpxEl == MINUS_SIGN:
#                 print("Adding -")
#                 l.append("-")
#             elif fpxEl == DOUBLE_BAR:
#                 print("Adding double bar d")
#                 l.append("d")
#             elif fpxEl == PLUS_INFINITY:
#                 print("Adding +infinity")
#                 l.append("+infinity")
#             elif fpxEl == MINUS_INFINITY:
#                 print("Adding -infinity")
#                 l.append("-infinity")
#             else:
#                 print("ERROR : adding", tabvar[FPX][i])
#                 l.append(tabvar[FPX][i])
#     return l

def get_fpxValues_from(tabvar):
    l = []
    for i in range(1,len(tabvar[FPX])):
        fpxEl = tabvar[FPX][i]
        l.append(fpxEl)
        # if fpxEl == 0:
        #     l.append("0")
        # elif fpxEl == PLUS_SIGN:
        #     l.append("+")
        # elif fpxEl == MINUS_SIGN:
        #     l.append("-")
        # elif fpxEl == DOUBLE_BAR:
        #     l.append("d")
        # elif fpxEl == PLUS_INFINITY:
        #     l.append("+infinity")
        # elif fpxEl == MINUS_INFINITY:
        #     l.append("-infinity")
        # else:
        #     # print("Adding other Value :", tabvar[FPX][i])
        #     l.append(tabvar[FPX][i])
    return l

def get_fxValues_from(tabvar):
    return tabvar[FX][1:]

def get_xValuesTkz(xValuesTex:list)->str:
    """prepares xValues for insertion into TkzTab VarTable
    """
    xValues = r""
    for value in xValuesTex:
        value = escape_Tex_for_Python(value)
        xValues += rf"""${value}$, """
    xValues = xValues.rstrip(" ")[:-1]
    xValues = rf"""{{{xValues}}}"""
    return xValues

def get_fpxValuesTkz(fpxValues:list)->str:
    """prepares fpxValues for insertion into TkzTabLine VarTable
    """
    # print("fpxValues from INSIDE TkZ=", fpxValues)
    # print("type(fpxValues[0)] (-infinity) from INSIDE TkZ=", type(fpxValues[0]))
    fpxValuesTkz = r""
    lastAddedWasDoubleBar = False
    for value in fpxValues:
        # value = escape_Tex_for_Python(value)
        if value == 0:
            # print("Adding 0 Detected..")
            fpxValuesTkz += r"z, "
            lastAddedWasDoubleBar = False
        elif value == PLUS_SIGN:
            # print("Adding Plus Sign Detected..")
            fpxValuesTkz += r"+, "
            lastAddedWasDoubleBar = False
        elif value == MINUS_SIGN:
            # print("Adding Minus Sign Detected..")
            fpxValuesTkz += r"-, "
            lastAddedWasDoubleBar = False
        elif value == HIDDEN_SIGN:
            # print("Adding Hidden Sign Detected..")
            fpxValuesTkz += r"h, "
            lastAddedWasDoubleBar = False
        elif value == MINUS_INFINITY:
            # print("Adding Minus Infinity Detected..")
            fpxValuesTkz += rf"-\infty, "   # BREAKING : NO DOLLAR SIGN AROUND -\infty
            lastAddedWasDoubleBar = False
        elif value == PLUS_INFINITY:
            # print("Adding Plus Infinity Detected..")
            fpxValuesTkz += rf"+\infty, "   # BREAKING : NO DOLLAR SIGN AROUND +\infty
            lastAddedWasDoubleBar = False
        elif value == DOUBLE_BAR and not lastAddedWasDoubleBar:
            print("Adding Double Bar Detected..")
            fpxValuesTkz += r"d, "
            lastAddedWasDoubleBar = True
        else:
            print("Adding Other Value Detected..=", value)
            fpxValuesTkz += rf"{get_latex(value)}, "
            lastAddedWasDoubleBar = False
    fpxValuesTkz = fpxValuesTkz.rstrip(" ")[:-1]    # rstrip last space and comma
    fpxValuesTkz = rf"""{{{fpxValuesTkz}}}"""
    return fpxValuesTkz

def get_fxValuesListOfTuples(fxValues):
    listOfTuples = []
    for i in range(len(fxValues)):
        if fxValues[i] == UP_ARROW:
            listOfTuples.append((fxValues[i-1], fxValues[i], fxValues[i+1]))
        elif fxValues[i] == DOWN_ARROW:
            listOfTuples.append((fxValues[i-1], fxValues[i], fxValues[i+1]))
    return listOfTuples

def get_fxValuesBy(triple):
    center = 1
    s = r""
    if triple[center] == UP_ARROW:
        s += rf"- / {triple[0]}, + / {triple[2]}"
    elif triple[center] == DOWN_ARROW:
        s += rf"+ / {triple[0]}, - / {triple[2]}"
    return s

def get_variation_indexes(fxValues):
    l = []
    for i in range(len(fxValues)):
        if fxValues[i] == UP_ARROW:
            l.append(i)
        elif fxValues[i] == DOWN_ARROW:
            l.append(i)
    return l 

def get_fxValuesTkz(fxValues:list)->str:
    """prepares fxValues for insertion into TkzTabVar VarTable
    """
    # i_varList = get_variation_indexes(fxValues)
    fxValuesTkz = r""
    # lastAddedWasDoubleBar = False
    last = len(fxValues) - 1
    i = 0
    firstArrow = False
    while i <= last:
        # print("i=", i)
        if i == last:
            if lastVar == UP_ARROW:
                # fxValuesTkz += rf"- /${get_latex(fxValues[i-2])}$, + / ${get_latex(fxValues[i])}$, "
                fxValuesTkz += rf"- / ${get_latex(fxValues[i])}$, "
            else: # lastVar = DOWN_ARROW
                # fxValuesTkz += rf"+/ ${get_latex(fxValues[i-2])}$, - / ${get_latex(fxValues[i])}$, "
                fxValuesTkz += rf"+ / ${get_latex(fxValues[i])}$, "
        if fxValues[i] == UP_ARROW:
            lastVar = UP_ARROW
            # if i+1 != last:
            if fxValues[i+1] != "+infinity":
                fxValuesTkz += rf"- / ${get_latex(fxValues[i-1])}$, + / ${get_latex(fxValues[i+1])}$, "
                i += 2
            elif fxValues[i+1] == "+infinity":
                if i+1 != last: # get Limit after Discontinuity
                    fxValuesTkz += rf"- / ${get_latex(fxValues[i-1])}$, +D- / ${get_latex(fxValues[i+1])}$ / ${get_latex(fxValues[i+2])}$, "
                    i += 3
                else: # i+1 = last
                    # fxValuesTkz += rf"- / ${get_latex(fxValues[i-1])}$, +D / ${get_latex(fxValues[i+1])}$, "
                    fxValuesTkz += rf"- / ${get_latex(fxValues[i-1])}$, + / ${get_latex(fxValues[i+1])}$, "
        if fxValues[i] == DOWN_ARROW:
            lastVar = DOWN_ARROW
            # if i+1 != last:
            if fxValues[i+1] != "-infinity":
                fxValuesTkz += rf"+ / ${get_latex(fxValues[i-1])}$, - / ${get_latex(fxValues[i+1])}$, "
                i += 2
            elif fxValues[i+1] == "-infinity":
                if i+1 != last: # get Limit after discontinuity
                    fxValuesTkz += rf"+ / ${get_latex(fxValues[i-1])}$, -D+ / ${get_latex(fxValues[i+1])}$ / ${get_latex(fxValues[i+2])}$, "
                    i += 3
                else: # i+1 = last
                    # fxValuesTkz += rf"+ / ${get_latex(fxValues[i-1])}$, -D / ${get_latex(fxValues[i+1])}$, "
                    fxValuesTkz += rf"+ / ${get_latex(fxValues[i-1])}$, - / ${get_latex(fxValues[i+1])}$, "
        i += 1
    fxValuesTkz = fxValuesTkz.rstrip(" ")[:-1]    # rstrip last space and comma
    fxValuesTkz = rf"""{{{fxValuesTkz}}}"""
    return fxValuesTkz

def getFirstArrow(l):
    for i in range(len(l)):
        if l[i] == UP_ARROW:
            return i, UP_ARROW
        elif l[i] == DOWN_ARROW:
            return i, DOWN_ARROW
    return -1, "NOARROW"

def split_interval(interval):
    I = interval
    print("Interval I1=", I)
    i_eq = I.index("=") if "=" in I else -1
    if i_eq >= 0:
        I = I[I.index("=")+1:]
    # i_comma = I.index(",") if "=" in I else -1
    # if i_comma >= 0:
    #     I.replace(",", ";")
    openLeft = True if I[0] == "]" else False
    openRight = True if I[-1] == "[" else False
    I = I[1:-1]
    print("I2=", I)
    i_sep = I.index(";")
    a = I[:i_sep]
    b = I[i_sep+1:]
    # a = g.latex(a)
    # b = g.latex(b)
    print("openLeft=", openLeft)
    print("a=", a)
    print("b=", b)
    print("openRight=", openRight)
    return openLeft, a, b, openRight

if __name__ == "__main__":
    fprime = get_derivee("x^2")
    print("Hey")


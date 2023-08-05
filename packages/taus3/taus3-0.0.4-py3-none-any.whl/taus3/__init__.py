import random
import os
import datetime

########8###########
pi = 22 / 7
def developerName():
    print("Taus Hasan")

#####################
def add(*a):
    print(sum(a), "\n")


def multi(*args):
    z = 1
    for num in args:
        z *= num
    print("Answer is ", z, "\n")


def divr(a, b):
    x = a / b
    y = a % b
    print(f"Qoutient is {x} and remainder is {y}\n")


def div(a, b):
    x = a / b
    print(x)


def minus(a, b):
    print("Answer is ", a - b, "\n")


def pow(a, b):
    x = a ** b
    print("Answer is ", x, "\n")



######################

def ran(a):
    x = random.choice(a)
    print(x)


def gennum(a, b):
    b = random.randint(a, b)
    print(b)


def mix(a):
    b = random.shuffle(a)
    print(a)


############################

def weight(kg):
    x = kg * 9.81
    print(x, " Newton")


def weightinmoon(a):
    x = a * 9.81
    y = x / 6
    print(y, " Newton")


#####################

def cwd():
    cwd = os.getcwd()
    print("Current working directory:", cwd)


def createFile(fd):
    try:
        with open(fd, 'x') as f:
            print( f"{fd} is created")
    except:
        print(f"File {fd} already exists...")


def viewFile(a):
    with open(a, "r+") as f:
        for x in f:
            print(x)


def writeFile(a, b):
    with open(a, "a") as f:
        f.write(b)


def deleteFile(a):
    if os.path.exists(a):
        os.remove(a)
        print(f"File {a} deleted")
    else:
        print(f"The file {a} does not exist")


def deleteFolder(a):
    try:
        os.rmdir(a)
    except:
        print(f"Folder {a} not found...")


############################

def unitary(a, b, c):
    fi = (b / a) * c
    print(fi)


def percent(a, b):
    fi = (b / a) * 100
    print(fi)


def fileAttack():
    a = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    b = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    c = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    d = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    e = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    f = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    g = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    h = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    i = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    j = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    k = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    l = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    m = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    n = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    o = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    # p = "1","2","3""4","5","6","7","8","9","0"]
    q = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    r = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    s = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    t = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    u = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    v = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    w = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    x = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "s", "t", "u",
         "v", "w", "x", "y", "z"]
    y = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|", "]", "}", "[", "{", "'", ";", ":",
         "/", "?", ".", ">", ",", "<"]

    z = [".txt", ".java", ".js", ".py", ".json", ".db", ".docx", ".apk", ".exe", ".mp3", ".mp4", ".sketch", ".blend",
         ".html", ".css"]

    aa = random.choice(a)
    bb = random.choice(b)
    cc = random.choice(c)
    dd = random.choice(d)
    ee = random.choice(e)
    ff = random.choice(f)
    gg = random.choice(g)
    hh = random.choice(h)
    ii = random.choice(i)
    jj = random.choice(j)
    kk = random.choice(k)
    ll = random.choice(l)
    mm = random.choice(m)
    nn = random.choice(n)
    oo = random.choice(o)
    pp = random.randint(1, 999)
    qq = random.choice(q)
    rr = random.choice(r)
    ss = random.choice(s)
    tt = random.choice(t)
    uu = random.choice(u)
    vv = random.choice(v)
    ww = random.choice(w)
    xx = random.choice(x)
    yy = random.choice(y)
    zz = random.choice(z)
    ct = datetime.datetime.now()

    me = (f"{aa}{bb}{cc}{dd}{ee}{ff}{gg}{hh}{ii}{jj}{kk}{ll}{ct}{mm}{nn}{oo}{pp}{qq}{rr}{ss}{tt}{uu}{vv}{ww}{xx}{yy}{zz}")
    with open(me, 'x') as f:
       print(f"{me} is created")


def factor(a):
    lr = 1
    n = a
    ur = n

    for i in range(lr, ur + 1):
        if (n % i == 0):
            print(i)

def multiple(a):
    lr = 1
    n = a
    ur = n

    for i in range(lr, ur + 1):
        if (n % i == 0):
            print(i)

def getWord(a):
    with open(a, "r") as file:
        allText = file.read()

        words = list(map(str, allText.split()))
        x = random.choice(words)
        print(x)

def numLine(a,b):
    for i in range(a,b):
        print(i)


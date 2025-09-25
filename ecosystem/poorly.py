'''
ここではきれいに書くのがめんどくさかった関数を置きまくる
'''
# 仮の変数
eiyou = 0

def decomposer(eco):
    s = eco.status
    pass

def weather(eco):
    s = eco.status
    w = eco.status["天気"]
    if w == "clear":
        s["水"] *= 0.99
    elif w == "rain":
        s["水"] *= 1.01
    elif w == "snow":
        s["水"] *= 1.005
    elif w == "sunder":
        s["植物"] *= 0.995
        s["水"] *= 1.02

def killevent(eco, num):
    s = eco.status
    s["植物"] *= num
    s["草食動物"] *= num
    s["肉食動物"] *= num
    s["人間"] *= num

bottom = 10000
def water(eco):
    w = eco.status["水"]
    if w < bottom:
        killevent(eco, 0.97)

def industry(eco):
    s = eco.status
    i = s["工場"]
    c = s["Society"]
    if c in ["3.0","4.0","5.0","6.0"]:
        
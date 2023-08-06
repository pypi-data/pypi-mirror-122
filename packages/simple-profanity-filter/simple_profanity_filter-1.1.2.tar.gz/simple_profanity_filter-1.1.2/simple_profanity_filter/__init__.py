badwords = [
    'хуй', 'хуи', 'хуё', 'хуе', 'хую', 'хуя', 'ёб', 'еба', 'ебе', 'ебу', 'ебо', 'еби', 'ебну', 'ебл', 'ебё', 'сука',
    'суки',
    'сучк', 'блят', 'бляд', 'блях', 'пизд',
    'сперм', 'гей', 'геи', 'даун', 'дебил', 'урод', 'муда', 'идиот', 'гонд', 'ганд', 'пидр', 'пенд',
    'пидор',
    'остолоб', 'педрил', 'говн', 'гавн', 'матьчек', 'матьжив', 'матьвканав', 'чекнимать', 'долба', 'долбо', 'хер',
    'лох', 'педик', 'педе',
    'педофил', 'порн', 'секс', 'шлю', 'потаск', 'траха', 'трахн', 'траху', 'простит', 'раком', 'анал', 'орал', 'минет',
    'куни', 'хентай'
]


def contain_profanity(text: str):
    global s1, t
    s = message.text
    ch = 1
    if '****' in s:
        ch = 0
    s = s.lower()
    s1 = ""
    t = 0
    spp = ""
    t = 0
    for i in range(1, len(s)):
        if t == 0 and s[i - 1] == 's' and s[i] == 'h':
            spp += 'ш'
            i += 2
            t = 1
        elif t == 0 and s[i - 1] == 'y' and s[i] == 'a':
            spp += 'я'
            i += 2
            t = 1
        else:
            if t == 0:
                spp += s[i - 1]
            t = 0

    if t == 0:
        spp += s[len(s) - 1]
    s = spp
    s1 = ""
    for i in range(len(s)):
        if 'а' <= s[i] <= 'я' or 'a' <= s[i] <= 'z':
            s1 += s[i]
        if s[i] == '@':
            s1 += 'а'
        if s[i] == '$':
            s1 += 'с'
        if s[i] == '^':
            s1 += 'л'
        if s[i] == '!':
            s1 += 'и'
    s = s1
    s1 = ""
    for idx in range(len(s)):
        if 'а' <= s[idx] <= 'я':
            s1 += s[idx]
        elif s[idx] == '0':
            s1 += 'o'
        elif s[idx] == '3':
            s1 += 'з'
        elif s[idx] == 'a':
            s1 += 'а'
        elif s[idx] == 'b':
            s1 += 'б'
        elif s[idx] == 'c':
            s1 += 'с'
        elif s[idx] == 'd':
            s1 += 'д'
        elif s[idx] == 'e':
            s1 += 'е'
        elif s[idx] == 'f':
            s1 += 'ф'
        elif s[idx] == 'g':
            s1 += 'г'
        elif s[idx] == 'h':
            s1 += 'х'
        elif s[idx] == 'i':
            s1 += 'и'
        elif s[idx] == 'j':
            s1 += 'ж'
        elif s[idx] == 'k':
            s1 += 'к'
        elif s[idx] == 'l':
            s1 += 'л'
        elif s[idx] == 'm':
            s1 += 'м'
        elif s[idx] == 'n':
            s1 += 'н'
        elif s[idx] == 'o':
            s1 += 'о'
        elif s[idx] == 'p':
            s1 += 'п'
        elif s[idx] == 'r':
            s1 += 'р'
        elif s[idx] == 's':
            s1 += 'с'
        elif s[idx] == 't':
            s1 += 'т'
        elif s[idx] == 'u':
            s1 += 'у'
        elif s[idx] == 'v':
            s1 += 'в'
        elif s[idx] == 'x':
            s1 += 'х'
        elif s[idx] == 'y':
            s1 += 'у'
        elif s[idx] == 'z':
            s1 += 'з'
    for i in range(len(badwords)):
        if badwords[i] in s1:
            t = 1
    return t or (ch == 0)
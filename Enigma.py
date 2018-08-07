#!/usr/bin/env python
import sys
import tty
import termios
import signal
import telepot
from telepot.loop import MessageLoop
from pprint import pprint


class classRotor:
    overflow = False
    index = 0
    aL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    aR = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']

    def __init__(self):
        pass

    def rotorforward(self, char):
        intero = ord(char) - 65
        p = intero + self.index
        if p >= 26:
            p = p - 26
        print('p: ' + str(p))
        Ll = self.aL[p]
        print('Ll: '+Ll)
        for i in range(26):
            if self.aR[i] == Ll:
                Ir = i
        Ir = Ir - self.index
        if Ir < 0:
            Ir = Ir + 26
        print('out: ' + chr(Ir + 65))
        return chr(Ir + 65)

    def rotorbackward(self, char):
        intero = ord(char) - 65
        p = intero + self.index
        if p >= 26:
            p = p - 26
        print('p: ' + str(p))
        Lr = self.aR[p]
        print('Lr: '+Lr)
        for i in range(26):
            if self.aL[i] == Lr:
                Il = i
        Il = Il - self.index
        if Il < 0:
            Il = Il + 26
        print('out: ' + str(Il))
        return chr(Il + 65)

    # incrementing rotor index
    def increment(self, increment):
        self.overflow = False
        if increment is True:
            self.index += 1
            # se il rotore supera la z torna alla a
            if self.index >= 26:
                self.index = 0
                # il disco successivo ruota
                self.overflow = True


class classCrypt:
    R1 = classRotor()
    R2 = classRotor()
    R3 = classRotor()
    mL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    mR = ['Q', 'W', 'E', 'R', 'C', 'Y', 'U', 'I', 'H', 'P', 'Z', 'S', 'V', 'T', 'X', 'J', 'A', 'D', 'L', 'N', 'G', 'M', 'B', 'O', 'F', 'K']
    p1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    p2 = ['L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'K']

    def __init__(self):
        pass

    def setRotors(self, i1, i2, i3):
        self.R1.index = i1
        self.R2.index = i2
        self.R3.index = i3

    def Mirror(self, char):
        for i in range(26):
            if char == self.mL[i]:
                print('mL: ' + self.mL[i])
                print('mR: ' + self.mR[i])
                return self.mR[i]

    def PlugFill(self, twins):
        for i in range(len(twins)):
            self.p1[i] = twins[i][0]
            self.p2[i] = twins[i][1]

    def PlugBoard(self, char):
        for i in range(10):
            if self.p1[i] == char:
                return self.p2[i]
            if self.p2[i] == char:
                return self.p1[i]
            return char

    def Parse(self, txt):
        if txt == "/start":
            self.setRotors(0, 0, 0)
            return "ok"
        elif "/crypt" in txt:
            txt = txt.upper()
            mex = txt.split(' ')
            out = ""
            # per ogni parola separata da spazi
            for j in range(len(mex)):
                # no /crypt
                if j != 0:
                    # per ogni lettera della parola
                    for i in range(len(mex[j])):
                        if ord(mex[j][i]) < 65 and ord(mex[j][i]) > 91:
                            return "encode only letters [A..Z]"
                    # per ogni lettera della parola
                    for i in range(len(mex[j])):
                        out = out + self.Crypt(mex[j][i])
                    # spazio tra le parole
                    out = out + " "
            return out

        elif "/key" in txt:
            mex = txt.split(' ')
            if not mex[1].isdigit() or int(mex[1]) > 25 or int(mex[1]) < 0:
                return "usage: /key [0..25] [0..25] [0..25] "
            if not mex[2].isdigit() or int(mex[2]) > 25 or int(mex[2]) < 0:
                return "usage: /key [0..25] [0..25] [0..25] "
            if not mex[3].isdigit() or int(mex[3]) > 25 or int(mex[3]) < 0:
                return "usage: /key [0..25] [0..25] [0..25] "
            self.setRotors(int(mex[1]), int(mex[2]), int(mex[3]))
            return "ok"
        elif "/plug" in txt:
            txt = txt.upper()
            mex = txt.split(' ')
            mex.pop(0)
            if len(mex) > 10:
                return "insert [1..10] plug"
            self.PlugFill(mex)
            return "ok"
        elif "/help" in txt:
            txt = "/start to set rotors to 0\r\n"
            txt = txt + "/crypt: to crypt words or a sentence\r\n"
            txt = txt + "/key: to change rotor settings\r\n"
            txt = txt + "/plug to change plug settings\r\n"
            return txt
        else:
            return "unknown command"

    def Crypt(self, char):
        var = self.PlugBoard(char)
        # print('----- Rotor 1 -----')
        var = self.R1.rotorforward(var)
        # print('----- Rotor 2 -----')
        var = self.R2.rotorforward(var)
        # print('----- Rotor 3 -----')
        var = self.R3.rotorforward(var)
        # print('----- Mirror -----')
        var = self.Mirror(var)
        # print('----- Rotor 3 -----')
        var = self.R3.rotorbackward(var)
        # print('----- Rotor 2 -----')
        var = self.R2.rotorbackward(var)
        # print('----- Rotor 1 -----')
        var = self.R1.rotorbackward(var)
        # print('-------------------')
        var = self.PlugBoard(var)
        self.R1.increment(True)
        self.R2.increment(self.R1.overflow)
        self.R3.increment(self.R2.overflow)
        pprint(str(self.R1.index) + ":" + str(self.R2.index) + ":" + str(self.R3.index))
        return var


class classTelegram:
    crypt = classCrypt()
    EnigmaBot = telepot.Bot("639030075:AAHAghY9CHRaradDCsPqGZOWMzHHiSNUyoE")

    def init(self):
        self.EnigmaBot = telepot.Bot("639030075:AAHAghY9CHRaradDCsPqGZOWMzHHiSNUyoE")
        # me = self.EnigmaBot.getMe()
        # pprint(me)
        # resp = self.EnigmaBot.getUpdates()
        # pprint(resp)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # print(content_type, chat_type, chat_id)
        # print(msg)
        txt = msg['text']
        result = self.crypt.Parse(txt)
        self.EnigmaBot.sendMessage(chat_id, result)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
# print('Press Ctrl+C')
# signal.pause()


def getchar():
    # Returns a single character from standard input
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def main():
    print("Enigma Emulator")
    # telegram
    bot = classTelegram()
    MessageLoop(bot.EnigmaBot, bot.handle).run_as_thread()
    crypt = classCrypt()
    while 1:
        tmp = input("Inserire comando:")
        print(tmp)
        result = crypt.Parse(tmp)
        print(result)


main()

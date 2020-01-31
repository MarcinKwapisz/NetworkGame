import socket
import sys
import time
import random

gracze =2
file = open("log.txt","w+")
buff = 8192

def zap(msg):
    file.write(msg)

def logowanie(conn):
    msg = conn.recv(buff).decode("utf-8")
    zap(msg)
    msg2 = msg.split()
    if msg2[0]=="LOGIN" and len(msg2)>1:
        return msg[6::]
    else:
        return None

watki = []
nazwy = ["GUARD", "PRIEST", "BARON", "HANDMAIDEN", "PRINCE", "KING", "COUNTESS", "PRINCESS"]
dousuwania = [["GUARD",1],["PRIEST", 2],["BARON", 3],["HANDMAIDEN",4],["PRINCE", 5],["KING",6],["COUNTESS",7],["PRINCESS",8]]
i = 1
host = "127.0.0.1"
port = 8888         # arbitrary non-privileged port

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
print("Socket created")

try:
    soc.bind((host, port))
except:
    print("Bind failed. Error : " + str(sys.exc_info()))
    sys.exit()

soc.listen(6)
print("Socket now listening")

while i<=gracze: #6
    connection, address = soc.accept()
    ip, port = str(address[0]), str(address[1])
    print("Connected with " + ip + ":" + port)
    zap("Connected with " + ip + ":" + port)
    connection.sendall(b'CONNECT\n')
    zap("CONNECT\n")
    licznik = 0
    while licznik < 100:
        login = logowanie(connection)
        if login != None:
            pkt=0
            watki.append([connection,login,pkt,[],i])
            i+=1
            connection.sendall(b'OK\n')
            zap("OK\n")
            break
        else:
            connection.sendall(b'ERROR\n')
            zap("ERROR\n")
            licznik=+1
win = 0
while 1:
    for i in watki:
        if i[2]==4:
            msg = ("GAME WINNER "+i[1]+"\nFINAL RESULT "+watki[0][1]+" "+watki[0][2]+" "+watki[1][1]+" "+watki[1][2]+" "+watki[2][1]+" "+watki[2][2]+" "+watki[3][1]+" "+watki[3][2]+" "+watki[4][1]+" "+watki[4][2])
            zap(msg)
            for j in watki:
                j[0].sendall(msg.encode())
            win = 1
            break
    if win == 1:
        break
    cards = [["GUARD", 1], ["GUARD", 1], ["GUARD", 1], ["GUARD", 1], ["GUARD", 1], ["GUARD", 1], ["GUARD", 1],
             ["GUARD", 1], ["GUARD", 1], ["GUARD", 1],
             ["PRIEST", 2], ["PRIEST", 2], ["PRIEST", 2], ["BARON", 3], ["BARON", 3], ["BARON", 3], ["BARON", 3],
             ["BARON", 3], ["HANDMAIDEN", 4],
             ["HANDMAIDEN", 4], ["PRINCE", 5], ["PRINCE", 5], ["KING", 6], ["COUNTESS", 7], ["PRINCESS", 8]]
    random.shuffle(watki)
    numer = 0
    for i in watki:
        i[4] = numer
        numer+=1
        card = random.choice(cards)
        cards.remove(card)
        msg = ('START '+str(i[4])+' '+card[0]+'\n')
        zap(msg)
        i[0].sendall(msg.encode())
        i[3] = [card]
    maiden = []
    out = []
    while 1:
        if len(cards) == 0:
            msg = ("ROUND END\nROUND RESULT " + watki[0][1] + " "+watki[0][2]+" "+watki[1][1]+" "+watki[1][2]+" "+watki[2][1]+" "+watki[2][2]+" "+watki[3][1]+" "+watki[3][2]+" "+watki[4][1]+" "+watki[4][2])
            zap(msg)
            for kk in watki:
                kk[0].sendall(msg.encode())

        skip = []
        for i in watki:
            if i[4] in out:
                continue
            if i[4] in skip:
                skip.remove(i[4])
                continue
            card = random.choice(cards)
            cards.remove(card)
            i[3].append(card)
            msg = ('YOUR MOVE '+card[0]+'\n')
            zap(msg)
            i[0].sendall(msg.encode())
            licznik=0
            reka = []
            for j in i[3]:
                reka.append(j[0])   #tymczasowo zapisujemy swoja reke
            while 1:
                msg = i[0].recv(buff).decode("utf-8")
                zap(msg)
                msgOrg = msg
                msg = msg.split()
                # print(msg)
                if ("KING" in reka and "COUNTESS" in reka)or("PRINCE" in reka and "COUNTESS" in reka):
                    msg="CHOOSE COUNTESS"
                    i[0].sendall(msg.encode())
                    i[3].remove(dousuwania[6])
                    continue
                if len(msg)<=1:
                    i[0].sendall(b'ERROR\n')
                    zap("ERROR\n")
                elif msg[0] == "CHOOSE" and len(msg)>=1:
                    if msg[1] not in reka:
                        i[0].sendall(b'ERROR\n')
                        zap("ERROR\n")
                    elif msg[1]  == "GUARD" and len(msg)>3:
                        try:
                            t = int(msg[2])
                            if msg[3] == "GUARD" or msg[3] not in nazwy:
                                i[0].sendall(b'ERROR\n')
                                zap("ERROR\n")
                            elif t in range(numer+1) and t not in out and t not in maiden:
                                i[0].sendall(b'OK\n')
                                i[3].remove(dousuwania[0])
                                zap("OK\n")
                                tmp = []
                                for tt in watki[t][3]:
                                    tmp.append(tt[0])
                                if msg[3] in tmp:
                                    out.append(msg[2])
                                    msg = ("ELIMINATED " + str(i[4])+"\n")
                                    zap(msg)
                                    for ll in watki:
                                        ll[0].sendall(msg.encode())
                                break
                        except ValueError:
                            i[0].sendall(b'ERROR\n')
                            zap("ERROR\n")

                    elif msg[1] == "PRIEST" and len(msg)>2:
                        try:
                            t = int(msg[2])
                            if t in range(numer+2) and t not in out and t not in maiden:
                                skip.append(t)
                                i[3].remove(dousuwania[1])
                                continue
                            else:
                                i[0].sendall(b'ERROR\n')
                                zap("ERROR")
                        except ValueError:
                            i[0].sendall(b'ERROR\n')
                            zap("ERROR")
                    elif msg[1] == "BARON":
                        if msg[2] in kolejka:
                            pass
                    elif msg[1] == "HANDMAIDEN":
                        maiden.append(i[4])
                        i[0].sendall(b'OK\n')
                        i[3].remove(dousuwania[3])
                    elif msg[1] == "PRINCE":
                        try:
                            t = int(msg[2])
                            if t in maiden:
                                i[3].remove(dousuwania[4])
                                i[0].sendall(b'OK\n')
                                break
                            if "PRINCESS" in watki[t][3][0]:
                                i[3].remove(dousuwania[4])
                                out.append(t)
                                msg = ("ELIMINATED " + str(i[4])+"\n")
                                zap(msg)
                                for ll in watki:
                                    ll[0].sendall(msg.encode())
                                break
                            else:
                                watki[t][3]=[]
                                if len(cards) == 0:
                                    break
                                else:
                                    i[3].remove(dousuwania[4])
                                    card = random.choice(cards)
                                    watki[t][3].append(card)
                                    cards.remove(card)
                                    watki[t][0].sendall(("New card "+card+" "+str(watki[t][4])).encode())
                        except ValueError:
                            i[0].sendall(b'ERROR\n')
                            zap("ERROR\n")
                    elif msg[1] == "KING" and len(msg)>1:
                        try:
                            t = int(msg[2])
                            if t in range(numer+1) and t not in out and t not in maiden:
                                i[3].remove(dousuwania[5])
                                tmp = i[3]
                                i[3] = watki[t][3]
                                i[0].sendall(watki[t][3][0].encode())
                                watki[t][3] = tmp
                                i[0].sendall(tmp[0].encode())
                                i[0].sendall(b'OK\n')

                            else:
                                i[0].sendall(b'ERROR\n')
                                zap("ERROR\n")
                        except ValueError:
                            i[0].sendall(b'ERROR\n')
                            zap("ERROR\n")
                    elif msg[1] == "PRINCESS":
                        i[0].sendall(b'OK\n')
                        out.append(i[4])
                        msg = ("ELIMINATED "+str(i[4])+"\n")
                        zap(msg)
                        for ll in watki:
                            ll[0].sendall(msg.encode())
                    else:
                        licznik+=1
                        print(licznik)
                        if licznik == 100:
                            kolejka.remove(i)
                            break
                    for k in watki:
                        msgOrg = "MOVE "+msgOrg[7::]
                        k[0].sendall(msgOrg.encode())
                        break
                else:
                    i[0].sendall(b'ERROR\n')
                    licznik=+1
                    if licznik == 100:
                        kolejka.remove(i)
                        break
            if len(out) ==gracze-1:
                for l in watki:
                    if l[4] not in out:
                        l[2] = +1
                        msg = ("ROUND WINNER " + str(l[1]) + "\nROUND RESULT " + str(watki[0][1]) + " " + str(watki[0][2]) + " " +
                               str(watki[1][1]) + " " + str(watki[1][2])) #+ " " + str(watki[2][1]) + " " + str(watki[2][2]) + " " +
                               # str(watki[3][1]) + " " + str(watki[3][2]) + " " + str(watki[4][1]) + " " + str(watki[4][2]))
                        zap(msg)
                        ll[0].sendall(msg.encode())
                break
        break
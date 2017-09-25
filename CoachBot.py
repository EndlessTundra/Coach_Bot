#!/usr/bin/python
# -*- coding: utf-8 -*-
## A Horrible Bot written by EndlessTundra to help you speedrun ##

import socket
import string
import random
from Config import SERVER, PORT, OAUTH, BOTNAME, CHANNEL, ENTRANCE, ANTIKAPPA
readbuffer = ""


def connect_to_twitch():
    s = socket.socket()
    s.connect((SERVER, PORT))
    s.send("PASS " + OAUTH + "\r\n")
    s.send("IDENT " + BOTNAME + "\r\n")
    s.send("NICK " + BOTNAME + "\r\n")
    s.send("JOIN #" + CHANNEL + "\r\n")
    return s

def joinRoom(s):
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = readbuffer + s.recv(2040)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            print(line)
            Loading = loadingComplete(line)

    sendMessage(s, ENTRANCE)

def loadingComplete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True


def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send(messageTemp + "\r\n")
    print("Sent: " + messageTemp)

def getUser(line):
    seperate = line.split(":", 2)
    user = seperate[1].split("!", 1)[0]
    return user

def getMessage(line):
    seperate = line.split(":", 2)
    message = seperate[2]
    return message



s = connect_to_twitch()

joinRoom(s)


while True:
    readbuffer = readbuffer + s.recv(2040)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        if "PING" in line:
            #print "Found PING"
            #print(line)
            s.send('PONG %s\r\n' % line.split()[1])

        else:
            #print(line)
            user = getUser(line)
            message = getMessage(line)

            #print(message)

            if "!help" in message:
                sendMessage(s, "CoachBot Commands: \"!coach, !congrats, !romance, !addcoach TEXT, !addcongrats TEXT, !addromance TEXT\"")

            if "!uptime" in message:
                sendMessage(s, "Link has been failing for a long time at this point.")

            if "Kappa" in message:
                if ANTIKAPPA == "yes":
                    sendMessage(s, "Don't lie " + user + ", you meant it and you know it!")

            if "!coach" in message:
                random_coach_encouragement = random.choice(open("Coaching.txt").readlines())
                sendMessage(s, random_coach_encouragement)

            if "!congrats" in message:
                random_congrats = random.choice(open("Congrats.txt").readlines())
                sendMessage(s, random_congrats)

            if "!romance" in message:
                random_romance = random.choice(open("Romance.txt").readlines())
                sendMessage(s, random_romance)

            if "!gameover" in message:
                sendMessage(s, "Everything was going great until I decided to suck.")

            if "!addcoach" in message:
                new_coach = message[10:]
                f = open("Coaching.txt","a+")
                f.write(new_coach + "\r\n")
                f.close()
                sendMessage(s, "CoachBot has learned new ways of encouraging our youth!")

            if "!addcongrats" in message:
                new_congrats = message[13:]
                f = open("Congrats.txt","a+")
                f.write(new_congrats + "\r\n")
                f.close()
                sendMessage(s, "CoachBot has learned a new way to be snide!")

            if "!addromance" in message:
                new_romance = message[12:]
                f = open("Romance.txt","a+")
                f.write(new_romance + "\r\n")
                f.close()
                sendMessage(s, "CoachBot has learned more about love!")
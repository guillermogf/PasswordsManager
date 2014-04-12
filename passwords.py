#!/usr/bin/python
#coding: utf-8
#
# Copyright (C) 2013-2014 Guillermo Gómez Fonfría
# <guillermo.gf@openmailbox.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from sys import argv, exit
from commands import getoutput
from os import system
from time import sleep
from getpass import getpass
import os.path

vers = "0.3"
usern = getoutput("logname")
dbpath = "/home/" + usern + "/.config/passwordsmanager/passwords.txt"


def help():
    print("Usage: " + argv[0] + " ARGS\n")
    print("\t-h\t--help\t\tShows this menu and exits")
    print("\t-v\t--version\tShows version and exits")
    print("\t-s\t--service\tShows entries (if any) related to the " +
          "SERVICE\n\t\t\t\tspecified")
    print("\t-w\t--web\t\tShows entries (if any) related to the LINK" +
          "\n\t\t\t\tspecified")
    print("\t-e\t--email\t\tShows entries (if any) related to the EMAIL" +
          "\n\t\t\t\tspecified")
    print("\t-u\t--user\t\tShows entries (if any) related to the USER" +
          "\n\t\t\t\tspecified")
    print("\t-A\t--all\t\tShows all entries")
    print("\t-a\t--add\t\tAdd new entry to database")
    print("\t-r\t--remove\tRemove a specific entry from the database")
    print("\t-d\t--delete\tDelete complete database")
    print("\t-E\t--export\tExport database (in plain text) to specified" +
          "\n\t\t\t\tfolder")
    print("\t-b\t--backup\tBackup (encoded text) to specified folder")
    print("\t-i\t--import\tImport from specified file. Both plain text" +
          "\n\t\t\t\texport or encoded backup")


def version():
    print("Passwords Manager v" + vers)
    print("Copyright © 2013-2014 Guillermo Gómez Fonfría")
    print("License GPLv3: GNU GPL version 3")
    print("\nThis is free sotware: you can redistribute it and/or modify " +
          "it under the terms of the GNU General Public License as " +
          "published by the Free Software Foundation, either version 3 of" +
          " the License, or (at your option) any later version.")
    print("\nThis program is distributed in the hope that it will be useful," +
          " but WITHOUT ANY WARRANTY; without even the implied warranty of " +
          "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU " +
          "General Public License for more details.")
    print("\nYou should have received a copy of the GNU General Public " +
          "License along with this program. If not, see {http://www.gnu.org" +
          "/license/}.")
    exit()


def error(description):
    print("ERROR: " + description)
    print("\nUSAGE: " + argv[0] + " [ARGS] + [SERVICE]")
    print("For more information run " + argv[0] + " --help")


def check():
    if getoutput("mkdir ~/.config/passwordsmanager") == "":
        system("touch " + dbpath)
        try:
            fl = open(dbpath)
            fl.close()
        except:
            system("touch " + dbpath)


def opendb():
    if not os.path.isfile(dbpath):  # Check if db exists & create if not
        db = open(dbpath, "w")
        db.close()
    db = open(dbpath)
    db = db.read()
    db = db.decode("base64")
    return db


def search(field):
    passwords = opendb()
    passwords = passwords.split("\n")
    passwords.remove("")

    site = []
    for i in passwords:
        i = i.split(" - ")
        if field == "ws":
            site.append(i[0])
        elif field == "lk":
            site.append(i[1])
        elif field == "em":
            site.append(i[2])
        elif field == "usr":
            site.append(i[3])
    return site


def show(site, match):
    passwords = opendb()
    if passwords == "":
        print("Database is empty!")
        exit()
    passwords = passwords.split("\n")
    passwords.remove("")
    n = 0
    for i in site:
        if i == match:
            n = n + 1
            index = site.index(i)
            site.insert(index, "")
            site.pop(index + 1)
            tmp = passwords[index]
            passwords.insert(index, "")
            passwords.pop(index + 1)
            tmp = tmp.split(" - ")
            print("\nOccurrence nº" + str(n))
            print("Web Service: " + tmp[0])
            print("Link: " + tmp[1])
            print("Email: " + tmp[2])
            print("User: " + tmp[3])
            print("Password: " + tmp[4])

    if n == 0:
        print("Password not found on database")
        exit()


def add():
    print("Fill in required (*) fields")
    while True:
        ws = raw_input("Web Service*: ")
        lk = raw_input("Link: ")
        em = raw_input("Email: ")
        usr = raw_input("User*: ")
        pss = getpass("Password*: ")
        pss2 = getpass("Repeat your password*: ")
        if ws != "" and usr != "" and pss != "" and pss == pss2:
            if lk == "":
                lk = " "
            if em == "":
                em = " "
            sure = raw_input("Check if everything is correct. Continue? " +
                             "Y(es)|N(o)\n")
            if sure.lower() in ("y", "yes"):
                break
        else:
            print("\nYou MUST fill in all required (*) fields. Also make " +
                  "sure you wrote the same password\n")

    db = opendb()
    db += ws + " - " + lk + " - " + em + " - " + usr + " - " + pss + "\n"
    db = db.encode("base64")
    ndb = open(dbpath, "w")
    ndb.write(db)
    ndb.close()
    sleep(1)
    print("New entry saved succesfully!")


def delete():
    sure = raw_input("Are you sure that you want to remove your complete " +
                     "passwords database?\n(This CANNOT be undone)\nY(es)|" +
                     "N(o)\n")
    if sure.lower() in ("y", "yes"):
        system("rm " + dbpath)
        sleep(1.5)
        print("Database removed succesfully")
    else:
        print("Cancelling and exiting...")


def remove():
    print("Remove specific entries\n")
    print("Fill in at least one of the fields")
    while True:
        ws = raw_input("Web Service: ")
        lk = raw_input("Link: ")
        em = raw_input("Email: ")
        usr = raw_input("User: ")
        if ws != "" or lk != "" or em != "" or usr != "":
            break
        print("You MUST fill in at least ONE of the fields")

    if ws != "":
        site = search("ws")
        match = ws
    elif lk != "":
        site = search("lk")
        match = lk
    elif em != "":
        site = search("em")
        match = em
    elif usr != "":
        site = search("usr")
        match = usr

    passwords = opendb()
    if passwords == "":
        print("Database is empty!")
        exit()
    passwords = passwords.split("\n")
    passwords.remove("")

    n = 0
    for i in site:
        if i == match:
            n = n + 1
            index = site.index(i)
            site.insert(index, "")
            site.pop(index + 1)
            tmp = passwords[index]
            tmp = tmp.split(" - ")
            print("\nOccurrence nº" + str(n))
            print("Web Service: " + tmp[0])
            print("Link: " + tmp[1])
            print("Email: " + tmp[2])
            print("User: " + tmp[3])
            print("Password: " + tmp[4])
            sure = raw_input("Do you want to delete this entry?\n(This " +
                             "CANNOT be undone)\nY(es)|N(o)\n")
            if sure.lower() in ("y", "yes"):
                passwords.pop(index)
                db = ""
                for i in passwords:
                    db += i + "\n"
                db = db.encode("base64")
                ndb = open(dbpath, "w")
                ndb.write(db)
                ndb.close()
                sleep(1)
                print("Entry deleted succesfully!")

    if n == 0:
        print("Password not found on database")
        exit()


def export():
    db = opendb()
    if argv[1] in ("-b", "--backup"):
        db = db.encode("base64")
    try:
        bckp = open(argv[2], "w")
    except:
        print("No file was specified!")
        exit()
    bckp.write(db)
    bckp.close()
    sleep(1)
    print("Database exported succesfully to " + argv[2])


def imprt():
    print("Are you sure you want to import a new database?")
    print("By doing this you will delete your current database (which " +
          "CANNOT be undone)")
    print("It could also cause some errors if the new file is damaged")
    sure = raw_input("Continue? Y(es)|N(o)\n")
    if sure not in ("y", "yes"):
        exit()
    inptfile = open(argv[2])
    inpt = inptfile.read()
    inptfile.close()
    if len(inpt.split(" - ")) > 1:
        inpt.split(" - ")  # Way to check if plain or base64 should be improved
        inpt = inpt.encode("base64")
    outputfile = open(dbpath, "w")
    outputfile.write(inpt)
    outputfile.close()
    print("Database imported!\nNow check if the file wasn't damaged")
    exit()


def show_all():
    db = opendb()
    db = db.split("\n")
    db.remove("")
    n = 0
    for i in db:
        n = n + 1
        i = i.split(" - ")
        print("\nOccurrence nº" + str(n))
        print("Web Service: " + i[0])
        print("Link: " + i[1])
        print("Email: " + i[2])
        print("User: " + i[3])
        print("Password: " + i[4])


def main():
    if argv[1] in ("-s", "--service"):
        site = search("ws")
    elif argv[1] in ("-w", "--web"):
        site = search("lk")
    elif argv[1] in ("-e", "--email"):
        site = search("em")
    elif argv[1] in ("-u", "--user"):
        site = search("usr")
    show(site, argv[2])


#Check if db already exits and create an empty one if not
check()

if len(argv) == 1:
    error("No arguments specified!")
elif argv[1] in ("-h", "--help"):
    help()
elif argv[1] in ("-v", "--version"):
    version()
elif argv[1] in ("-a", "--add"):
    add()
elif argv[1] in ("-r", "--remove"):
    remove()
elif argv[1] in ("-d", "--delete"):
    delete()
elif argv[1] in ("-s", "--service", "-w", "--web",
                 "-e", "--email", "-u", "--user"):
    if len(argv) == 2:
        error("No SERVICE, LINK, EMAIL or USER specified")
    else:
        main()
elif argv[1] in ("-A", "--all"):
    show_all()
elif argv[1] in ("-E", "--export", "-b", "--backup"):
    if len(argv) == 2:
        error("No file specified")
    else:
        export()
elif argv[1] in ("-i", "--import"):
    if len(argv) == 2:
        error("No file specified")
    else:
        imprt()
else:
        error("Argument not recognized")

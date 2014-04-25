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

from sys import exit
from getpass import getpass
import os.path
import argparse

vers = "0.3"
dbpath = os.path.expanduser("~/.config/passwordsmanager/passwords.txt")


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


def check():
    if not os.path.isfile(dbpath):
        if not os.path.exists(os.path.dirname(dbpath)):
            os.makedirs(os.path.dirname(dbpath))
        db = open(dbpath, "a")
        db.close()


def opendb():
    db = open(dbpath)
    db = db.read()
    db = db.decode("base64")
    db = db.rstrip("\n")
    return db


def writedb(content, path=dbpath):
    if not content.endswith("\n"):  # Check if it ends w/ trailing newline
        content = content + "\n"
    try:
        db = open(path, "w")
    except IOError:
        print("You don't have perimission to write to that file!")
        exit(1)
    db.write(content)
    db.close()


def search(field):
    passwords = opendb()
    passwords = passwords.split("\n")

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
            print("\nEntry nº" + str(n))
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
    if db != "":
        db += "\n"
    db += ws + " - " + lk + " - " + em + " - " + usr + " - " + pss + "\n"
    db = db.encode("base64")
    writedb(db)
    print("New entry saved succesfully!")


def delete():
    sure = raw_input("Are you sure that you want to remove your complete " +
                     "passwords database?\n(This CANNOT be undone)\nY(es)|" +
                     "N(o)\n")
    if sure.lower() in ("y", "yes"):
        db = open(dbpath, "w")
        db.close()
        print("Database removed succesfully")
    else:
        print("Cancelling and exiting...")


def remove():
    passwords = opendb()
    if passwords == "":
        print("Database is empty!")
        exit()

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

    passwords = passwords.split("\n")

    n = 0
    for i in site:
        if i == match:
            n = n + 1
            index = site.index(i)
            site.insert(index, "")
            site.pop(index + 1)
            tmp = passwords[index]
            tmp = tmp.split(" - ")
            print("\nEntry nº" + str(n))
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
                writedb(db)
                print("Entry deleted succesfully!")

    if n == 0:
        print("Password not found on database")
        exit()


def export():
    db = opendb()
    if args.backup:
        db = db.encode("base64")
        path = args.backup
    else:
        path = args.export
    writedb(db, path)
    print("Database exported succesfully to " + path)


def imprt():
    print("Are you sure you want to import a new database?")
    print("By doing this you will delete your current database (which " +
          "CANNOT be undone)")
    print("It could also cause some errors if the new file is damaged")
    sure = raw_input("Continue? Y(es)|N(o)\n")
    if sure not in ("y", "yes"):
        exit()
    inptfile = open(args.imprt)
    inpt = inptfile.read()
    inptfile.close()
    if len(inpt.split(" - ")) > 1:
        inpt.split(" - ")  # Way to check if plain or base64 should be improved
        inpt = inpt.encode("base64")
    writedb(inpt)
    print("Database imported!\nNow check if the file wasn't damaged")
    exit()


def show_all():
    db = opendb()
    if db == "":
        print("Database is empty!")
        exit()
    db = db.split("\n")
    n = 0
    for i in db:
        n = n + 1
        i = i.split(" - ")
        print("\nEntry nº" + str(n))
        print("Web Service: " + i[0])
        print("Link: " + i[1])
        print("Email: " + i[2])
        print("User: " + i[3])
        print("Password: " + i[4])


#Check if db already exits and create an empty one if not
check()

parser = argparse.ArgumentParser(description="Passwords Manager allows you " +
                                 "to easily store your account data.")

args_group = parser.add_mutually_exclusive_group(required=True)
args_group.add_argument("-v", "--version", action="store_true",
                        help="Show version, license and exits")
args_group.add_argument("-s", "--service", type=str,
                        help="Shows entries (if any) matching SERVICE")
args_group.add_argument("-w", "--web", type=str,
                        help="Shows entries (if any) matching WEB")
args_group.add_argument("-e", "--email", type=str,
                        help="Shows entries (if any) matching EMAIL")
args_group.add_argument("-u", "--user", type=str,
                        help="Shoes entries (if any) matching USER")
args_group.add_argument("-A", "--all", action="store_true",
                        help="Shows all entries")
args_group.add_argument("-a", "--add", action="store_true",
                        help="Add new entry to database")
args_group.add_argument("-r", "--remove", action="store_true",
                        help="Remove a specific entry from database")
args_group.add_argument("-d", "--delete", action="store_true",
                        help="Delete complete database")
args_group.add_argument("-E", "--export", type=str,
                        help="Export database (in plain text) to EXPORT")
args_group.add_argument("-b", "--backup", type=str,
                        help="Backup database (encoded) to BACKUP")
args_group.add_argument("-i", "--import", type=str, metavar="FILE",
                        help="Import from FILE, Both plain or " +
                             "encoded databases", dest="imprt")
args = parser.parse_args()


if args.version:
    version()
elif args.service:
    site = search("ws")
    show(site, args.service)
elif args.web:
    site = search("lk")
    show(site, args.web)
elif args.email:
    site = search("em")
    show(site, args.email)
elif args.user:
    site = search("usr")
    show(site, args.user)
elif args.all:
    show_all()
elif args.add:
    add()
elif args.remove:
    remove()
elif args.delete:
    delete()
elif args.export:
    export()
elif args.backup:
    export()
elif args.imprt:
    imprt()

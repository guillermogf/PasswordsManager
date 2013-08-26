#!/usr/bin/python
#coding: utf-8
#
# Copyright (C) 2013 Guillermo Gómez Fonfría
#<guillermo.gomezfonfria@gmail.com>
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

version = "0.1"

from sys import argv

def help():
	print("")

def version():
	print("Passwords manager v" + version)
	print("Copyright © 2013 Guillermo Gómez Fonfría")
	print("Licencia GPLv3: GNU GPL version 3")
	print("This is free sotware: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.")
	print("\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.")
	print("\nYou should have received a copy of the GNU General Public License along with this program. If not, see {http://www.gnu.org/license/}.")
	exit()

def main():
	db = open("../passwords.txt")
	passwords = db.read()
	passwords = passwords.split("\n")

	site = []
	for i in passwords:
		i = i.split(" - ")
		site.append(i[0])

	if argv[1] in site:
		index = site.index(argv[1])
		tmp = passwords[index]
		tmp = tmp.split(" - ")
		print("Web service: " + tmp[0])
		print("Link: " + tmp[1])
		print("User: " + tmp[2])
		print("Password: " + tmp[3])

	else:
		print("Password not found on database")

main()

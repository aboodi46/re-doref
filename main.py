#!/usr/bin/env python
# -*- coding: utf-8 -*-

from header import *
from doref.standards.ieee830 import *

#------------------------------------------------------------
# example_modular_project.py
# Smart vacuum cleaner
# A fragmentary project documentation
#------------------------------------------------------------


World("My Smart Home")
cd("./-")
System("Secure Bootloader")
cd("./-")
Project("Bootloader")

cd("/*/Bootloader")
Folder("Protocols")
Folder("Specifications")
cd("./-")

IEEE830SRS("Software Requirements for Secure Bootloader",
           [["Pedro, Meghadoot, Bob", "A-Team", "FH Dortmund"]],
           {'language': 'english', 'paper': 'a4', 'font': '11pt'})

from chapters.chapter1 import *

node("/").dump()
node("/").genPDF()
node("/").genHTML(["doref.ref", "doref.standards.ieee830", "doref.utils.plantuml", "doref.istar"])

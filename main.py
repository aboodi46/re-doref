#!/usr/bin/env python
# -*- coding: utf-8 -*-

from header import *
from doref.standards.ieee830 import *

#------------------------------------------------------------
# example_modular_project.py
# Smart vacuum cleaner
# A fragmentary project documentation
#------------------------------------------------------------


World("Motor vehicle")
cd("./-")
System("Electronic Control Unit")
cd("./-")
Project("Secure Bootloader")

cd("/*/Secure Bootloader")
Folder("Specifications")
cd("./-")

class BLS830(IEEE830SRS):
    chapterStructure = [
        "Introduction", [
            "Purpose",
            "Scope",
            "Definitions, Acronyms, and Abbreviations",
            "References",
            "Overview"
        ],
        "Software requirements", [
            "Bootloader concept",
            "Bootloader states",
            "PBL entering to deafault session",
            "PBL entering to programming session",
            "Exit from programming session",
            "Entering from application to programming session",
            "Entering into application",
            "Functional requirements", [
                "Diagnostic session control requirements",
                "ECU reset requirements",
                "ReadDataByIdentifier service requirements", [
                    "ReadDataByIdentifier service overview",
                    "DataIdentifier",
                    "ECU Delivery Assembly Number",
                    "ECU Core Assembly Number",
                    "Boot Software Identification",
                ],
                "SecurityAccess service requirements",
                "RoutineControl service requirements", [
                    "RoutineInfo - Type and Status",
                    "RoutineIdentifier 0301 Hex (Activate secondary bootloader)",
                    "RoutineIdentifier FF00 hex (EraseMemory)",
                    "RoutineIdentifier FF01 hex (check programming dependencies)",
                    "RoutineIdentifier 0304 hex (check valid application)",
                    "RoutineControl supported NRCs"
                ],
                "RequestDownload service requirements",
                "RequestUpload service requirements",
                "TransferData service requirements",
                "RequestTransferExit service requirements",
                "TesterPresent service requirements"]
        ]
    ]
    def _init_(self, name, authors, properties=None, folder=None):
        IEEE830SRS.init(self, name, authors, properties, folder)


BLS830("Software Requirements for Secure Bootloader",
           [["Pedro, Meghadoot, Bob", "A-Team", "FH Dortmund"]],
           {'language': 'english', 'paper': 'a4', 'font': '11pt'})

from chapters.chapter1 import *
from chapters.chapter2 import *

node("/").dump()
node("/").genPDF()
node("/").genHTML(["doref.ref", "doref.standards.ieee830", "doref.utils.plantuml", "doref.istar"])

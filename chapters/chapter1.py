#!/usr/bin/env python
# -*- coding: utf-8 -*-

from header import *

cd("/*/Introduction")
cd("/*/Purpose")
Inf("""This document is intended to provide guidance and requirements to \
develop Software Download (Boot loader) component. \

The main functionality of the Bootloader software is to flash new versions of \
application software to an ECU. The Boot loader software resides in the ECU \
and interacts with a PC-based flash tool (Ex: Tester Scripts) to support \
downloading of application software over LIN network through Diagnostic \
Services.""")

cd("..")
cd("/*/Scope")
Inf("""The scope of this document is to identify Bootloader software \
requirements and prepare the technical specification. This document forms the \
basis to develop Bootloader component. This document covers the following \
details:

 * Concepts of Bootloader
 * List of  ISO 14429-1 based diagnostic services used for Bootloader
 * Data formats of requests and responses
 * List of Negative Response Code ( NRCs) """)

cd("..")
cd("/*/Definitions, Acronyms, and Abbreviations")
Table("Definitions",
        [
            ["**Term**", "**Definition**"],

            ["Frame", """A complete multiplex "message" consists of one or \
            more frames. Each "frame" contains 8 data bytes, including the \
            Protocol Control Information (PCI). """],

            ["Vehicle main node", """An ECU that is connected to a vehicle main \
            network forms the Vehicle main node."""],

            ["Vehicle main network", """A network for software downloads that \
            is connected to the diagnostic connector."""],

            ["Tester", "An external device used to connect to the vehicle \
            networks through the Diagnostic Link Connector, e.g. workshop \
            electronic tool, manufacturing equipment."],

            ["SuppressPosRspMsgIndicationBit","""TRUE indicates server shall \
            NOT send a positive response message. FALSE indicates server shall \
            send a positive or negative response message"""],

            ["P2Server", """Time between reception of the last frame of a \
            diagnostic request on the LIN bus and the slave node being able \
            to provide data for a response. The maximum value defines the time \
            after which a slave node must receive a slave response header \
            before it discards its response."""],

            ["P2*Server", """Time between sending a NRC 0x78 and the LIN Slave \
            being able to provide data for a response."""],

            ["P4Servermax", """The timing parameter P4Servermax is the maximum \
            time between the reception of a request and the start of \
            transmission of the final response."""],

            ["S3Server", """Time for the server to keep a diagnostic session \
            other than the defaultSession active while not receiving any \
            diagnostic request message. This timer has been referred as S3 \
            throughout this document."""],

            ["LIN Master", """Master always transmits a header and master \
            decides when and which frame shall be transferred on the bus."""],

            ["LIN Slave", """Slave always response when header request from \
            Master. Slave provides the data transported by each frame."""]
        ] )

Table("Acronyms and Abbreviations",
        [
            ["**Abbreviations**", "**Description**"],
            ["ASCII", "American Standard Code For Information Interchange"],
            ["BL", "Bootloader"],
            ["CAN", "Control Area Network"],
            ["CCITT", "Consultative Committee for International Telegraphy and Telephony"],
            ["CNC", "Condition Not Correct"],
            ["CPU", "Central Processing Unit"],
            ["DID", "Data by Identifier"],
            ["DTC", "Diagnostic Trouble Code"],
            ["ECU", "Electronic Control Unit"],
            ["EEPROM", "Electrically Erase Programmable Read Only Memory"],
            ["ENOA", "Exceeded Number Of Attempts"],
            ["EOL", "End Of Line"],
            ["ID", "Identifier"],
            ["ISO", "International Standard Organization"],
            ["Kbps", "Kilobits per second"],
            ["LIN", "Local interconnect network"],
            ["LSB", "Least Significant Bit"],
            ["MSB", "Most Significant Bit"],
            ["msec", "Milliseconds"],
            ["NA", "Not Applicable"],
            ["NAD", "Node Address"],
            ["NRC", "Negative Response Code"],
            ["OEM", "Original Equipment Manufacturer"],
            ["OSI", "Open System Interconnect"],
            ["PBL", "Primary Bootloader"],
            ["PCI", "Protocol Control Information"],
            ["PDU", "Packet Data Unit"],
            ["PID", "Parameter Identifier"],
            ["PLL", "Phase Locked Loop"],
            ["RAM", "Random Access Memory"],
            ["REF", "Reference"],
            ["ROOR", "Request Out Of Range"],
            ["SAD", "Security Access Denied"],
            ["SBL", "Secondary Bootloader"],
            ["SID", "Service Identifier"],
            ["SPRMIB", "Suppress Positive Response Message Indication Bit"],
            ["SRS", "Software Requirement Specification"],
            ["SWDL", "Software Download"],
            ["UDNA", "Upload Download Not Accepted"],
            ["UDS", "Unified Diagnostics Services"]
        ])

cd("..")
cd("/*/References")
Table("References",
        [
            ["No.", "Title", "Version or Date", "Document num."],
            ["1", "LIN Specification Package", "Revision 2.1 24-Nov-2006",
            "NA"],
            ["2","""Road Vehicles - Diagnostic systems - Part1:
            Diagnostic services""", "15-Apr-2007", "ISO 14229-1"],
            ["3", """Road Vehicles - Diagnostic on Control Area Network - \
            Part 2: Network layer services""", "10-Dec-2004", "ISO 15765-2"]
        ])

cd("..")
cd("/*/Overview")
Chapter("System overview", """The Software Download (SWDL) concept provides \
a means for an off-board tester to send multiple bytes of data to an ECU. The \
data transferred may contain configuration or calibration data for the ECU or \
completely new software for the ECU. It also includes uploading of data from \
the ECU to the tester for debugging.

The Software Download concept utilizes the following ISO specifications as a \
base:

* **ISO 15765-2** describes the network layer services.
* **ISO 14229-1** describes the Unified Diagnostic Services used in the
Software Download concept.""")

Chapter("Document overview", """The document overview details are given in \
Table 3 Document overview.""")

cd("/*/Document overview")
Table("Document overview",
        [
            ["**Section 1**", """It describes the introduction, purpose, \
            scope, definitions, acronyms and abbreviations List, references, \
            diagnostic communication requirements, document overview and \
            system overview."""],
            ["**Section 2**", """It describes the concept of bootloader, \
            functional requirements of software download services supported by \
            bootloader and risks involved."""],
            ["**Section 3**", """It describes the requirements of network \
            layer, data link layer, session layer, Transport layer, LIN \
            master, Slave node transmission handler and LIN Diagnostics."""]
        ])

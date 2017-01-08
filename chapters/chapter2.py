#!/usr/bin/env python
# -*- coding: utf-8 -*-

from header import *
from doref.utils.plantuml.plantuml import *

cd("/*/Bootloader concept")
Inf("""The bootloader is divided into two separate and mandatory parts: a \
primary bootloader (PBL) and a secondary bootloader (SBL).The PBL is designed \
to be permanently placed in a protected flash boot sector, which is activated \
from reset. The SBL is intended to be downloaded by the PBL into the CPU \
internal RAM. The SBL can be described as a superset of the PBL, adding \
functions for erase and program of flash memory and EEPROM. """)

Figure("Typical ECU memory map", """images/memory_map.eps""","", {'size':'fit'})

Inf("""

 **PRIMARY BOOTLOADER (PBL)**

The PBL is designed to be permanently placed in a protected flash boot sector. \
The primary bootloader (PBL) has the important task of loading the SBL into the \
CPU internal RAM and transfer the control to secondary boot loader (SBL).
The primary bootloader (PBL) shall have a time window of 20msec (±10%) for \
detection of the DiagnosticSessionControl service. If a \
DiagnosticSessionControl service with diagnosticSessionType equal to \
programmingSession is received during the 20msec time window after power on, \
the ECU shall enter programmingSession.
If not, the ECU shall exit the PBL and jump to the application if valid \
application is present and if application is also not present ,it transits to \
default session.

The code size of the PBL in the target must be very small (so that it can \
easily fit into a boot flash sector). The code must also be correct, since \
after the primary bootloader is programmed into a protected flash boot sector \
there is no chance to update a software error after an ECU is produced. The \
memory area containing the PBL shall be protected from erasure to eliminate \
the possibility of accidentally erasing it. The PBL shall only be capable of \
writing data to RAM due to security and data integrity.
An erase of the flash memory can only occur if the secondary bootloader (SBL) \
is downloaded into RAM. The PBL shall not be able to overwrite or modify any \
of its own memory and the standard SBL shall not be able to overwrite or erase \
the PBL. The PBL shall provide functions to identify the ECU hardware (i.e. \
ECU Delivery Assembly Number, ECU Core Assembly Number and Boot Software \
Identification).When an ECU transitions to the programmingSession, the primary \
bootloader will need to pre-condition all of the ECU's I/O into a state where \
components cannot be damaged and the area is safe for people working on \
the vehicle.

**SECONDARY BOOTLOADER (SBL)**

The SBL includes all routines for flash erase and flash program of data to an \
ECU. The SBL is downloaded with the help of the PBL into RAM. After download \
the SBL is activated from the PBL.
The SBL services are now added (super set to the PBL) and can be used together \
with the PBL services. This means that all PBL services shall be capable of \
being executed after the SBL has been downloaded and activated.

The implementation of SBL also includes all PBL services. This provides two \
advantage and they are:

* If an error is found in the PBL, it is possible to make a workaround \
solution in the SBL.
* No calls are necessary from the SBL to the PBL, which simplify the \
bootloader implementation.

After download and start of execution of the SBL in RAM, it shall not be \
possible to make a new download to RAM (i.e., ECU shall reject request with \
NRC 31 hex). Before a new download to RAM can be performed, an exit from the \
programmingSession shall be required the reason for this is to avoid \
overwriting the SBL.""")

cd("/*/Bootloader states")
Inf("""The Bootloader can be in two different states or sessions, the \
defaultSession or the programmingSession. After power on the PBL shall \
begin an initialization phase where it waits for a DiagnosticSesssionControl \
service for a time period of 20msec called time window for programming session \
entry detection at startup.""")

PlantUML("State diagram of ECU","""

skinparam monochrome true

[*] --> ECUA : Power ON || ECU Reset

state "ECU Application" as ECUA {
  [*] -->   PBL

  state "Primary Bootloader" as PBL {
    state Init
    state "Default Session" as DefSess
    state "Programing Session" as ProgSession

    DefSess --> Init : DiagnosticSessionControl DefaultSession
    DefSess --> ProgSession : DiagnosticSessionControl ProgrammingSession

    ProgSession --> Init : DiagnosticSessionControl DefaultSession || S3 timeout
    ProgSession --> ProgSession : DiagnosticSessionControl ProgrammingSession

    [*] --> Init
    Init --> DefSess : [t >= 20 ms] No Application Detected
    Init --> ProgSession : [t < 20 ms] DiagnosticSessionControl ProgrammingSession

  }

  state "Start Up Mode" as SUP

  Init --> SUP : [t >= 20 ms] Application Detected
  SUP --> ProgSession : [RAMPattern == 0X5A5A5A5A] DiagnosticSessionControl ProgrammingSession
}
""", """The state diagram in the figure shows the states of an ECU. In all \
        the states it shall be possible to force the ECU into program mode \
        with the DiagnosticSession Control service with programmingSession \
        request.""", {'size': 'fit'})

cd("/*/PBL entering to programming session")
Inf("""The PBL enters into defaultSession, when invalid application software \
is present or absence of application software and timeout occurs from the \
initialization phase.

Refer to `/*/RoutineControl service requirements`_ \
for application validity sequence.""")

cd("/*/Exit from programming session")
Inf("""PBL can enter to Programming Session in below ways:

1. The PBL enters into programming session, if it receives the \
DiagnosticSessionControl service with diagnosticSessionType equal to \
programmingSession within the window timer period (20msec) from the \
initialization phase.

2. The PBL enters into 'ProgrammingSession' from default session, whenever it \
receives the DiagnosticSessionControl service with diagnosticSessionType equal \
to programming Session request. When there is no request for programming \
session it stays in default session itself. There is no session timeout in \
'Default' State.
""")

cd("/*/Entering from application to programming session")
Inf("""PBL can exit from Programming Session in below ways:

1. The BL enters into defaultsession when ECUReset service request is \
received from the Tester in the programming session.

2. When bootloader entering into programming session, it shall start the \
S3Server timer. The timeout value for S3Server is 5000msec. If the maximum \
value of S3Server is reached, bootloader make a hard reset and exit from \
the programmingsession and enters into defaultsession.

3. The BL enters into defaultsession when DiagnosticSessionControl control \
service request for Defaultsession is received within the S3Server timeout \
from the Tester in the programming session.""")

cd("/*/Entering into application")
Inf("""In application mode, if it receives the DiagnosticSessionControl \
service with diagnosticSessionType equal to programmingSession the application \
provides a mechanism to enter into programming session of bootloader.

To avoid problems with hardware initialization (i.e., write once registers, \
PLL-setup, memory re-map, interrupt vector table re-map, etc.) the preferred \
solution is that the bootloader always starts executing from reset when the \
application software receives a DiagnosticSessionControl (programmingSession) \
service.

The control will come to the Bootloader from application by sending \
DiagnosticSessionControl (programmingSession as session type) request only \
once. Upon this request, application shall be write the fixed bit pattern in a \
fixed address in RAM and trigger Watchdog reset.

The BL checks for the pattern 0X5A5A5A5A at fixed RAM Location and clear the \
bit pattern, then control will be transferred to the Bootloader. Refer the \
`/*/Application to Bootloader jump`_ and `/*/Bootloader flow diagram`_.

For a faulty programmed ECU or an aborted programming ECU, the "backdoor \
solution" with a 20msec time window for receiving DiagnosticSessionControl \
(programmingSession) after reset can still be used.""")

PlantUML("Application to Bootloader jump","""

skinparam monochrome true

Application -down-> "Diagnostic Session Control (Programming Session)"

--> "Write Pattern 0x5A5A5A5A at specified RAM location"

--> "Trigger Reset"

--> "Programming Session"
""", "", {'size': 'fit'})


PlantUML("Bootloader flow diagram","""

skinparam monochrome true

(*) -down-> Reset

if "Bit pattern == 0x5A5A5A5A at fixed address in RAM?" then
  -right->[true "Warm Start"] "Clear bitpattern at fixed address in RAM"
  --> "Start ProgrammingSession" as StartProgSess
else
  -down->[false "Cold Start"] "Wait for 20 ms"
  if "DiagnosticSessionControl == ProgrammingSession" then
  -right->[true] StartProgSess
  else
    -down->[false] "Check Applications" as CheckApp
    if "Valid application Exists?" then
      -down->[true] "Jump to application SW (Start normal application SW)"
    else
      -right->[false] "Default Session" as DefSess
      if "DiagnosticSessionControl == ProgrammingSession" then
        -up->[true] StartProgSess
      else
        -down->[false] "Default Session" as DefSess
      endif
    endif
  endif
endif
""", "", {'size': 'fit'})

ch(node("/*/Functional requirements"), 'text',
        """This section shall contain the list of functional requirements of \
        the software.""")
cd("/*/Diagnostic session control requirements")
Table("Software download services", [
        ['No.', 'Service', 'SIDs', 'Supported in PBL', 'Supported in SBL'],

        ['1', 'DiagnosticSessionControl', '0x10',
        'DefaultSession State and ProgrammingSession State',
        'ProgrammingSession state'],

        ['2','ECUReset', '0x11',
        'DefaultSession State and ProgrammingSession State',
        'ProgrammingSession state'],

        ['3','SecurityAccess', '0x27',
        'NA',
        'ProgrammingSession state'],

        ['4','ReadDataByIdentifier', '0x22',
        'DefaultSession State and ProgrammingSession State',
        'ProgrammingSession state'],

        ['5','RoutineControl', '0x31',
        'NA',
        'ProgrammingSession state'],

        ['6','RequestDownload', '0x34',
        'NA',
        'ProgrammingSession state'],

        ['7','RequestUpload', '0x35',
        'NA',
        'ProgrammingSession state'],

        ['8','TransferData', '0x36',
        'NA',
        'ProgrammingSession state'],

        ['9','RequestTransferExit', '0x37',
        'NA',
        'ProgrammingSession state'],

        ['10','TesterPresent', '0x3e',
        'ProgrammingSession State',
        'ProgrammingSession state']
        ],
        " The tester supplies an external voltage to perform the SWDL \
        functions. The software download (SWDL) services supported by the \
        bootloader are given in table")

ch(node("/*/Diagnostic session control requirements"), 'text',
        """This DiagnosticSessionControl enables all diagnostic services \
        required to support the memory programming of an ECU.""")

cd("/*/Diagnostic session control requirements")
Req("","""The ECU shall ignore any request other than the \
DiagnosticSessionControl service with diagnosticSessionType equal to \
programmingSession during the 20msec time window after power on.""")
Req("","""The bootloader shall support default session (0x01), programming \
session (0x02). It shall not supported the extendedDiagnosticSession (0x03) \
and safetySystemDiagnosticSession (0x04).""")
Req("", """The BL enters into defaultSession, when invalid application \
software is present or absence of application software and timeout occurs from \
the initialization phase.""")
Req("","""It does not support any diagnostic application timeout handling \
provisions (e.g. no TesterPresent service is necessary to keep the session \
active)""")
Req("","""If the BL in programmingSession, the programmingSession shall only \
be left via an ECUReset (11 hex) service initiated by the tester, a \
DiagnosticSessionControl (10 hex) service with session Type equal to \
defaultSession, or a session layer timeout (5000msec).""")
Req("","""P2 and P2* timer values shall be 50msec & 2000msec in \
defaultSession.""")
Table("DiagnosticSessionControl request message flow", [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'DiagnosticSessionControl request SID', '10'],
        ['2', """DiagnosticSessionType = programmingSession, defaultSession \
                suppressPosRspMsgIndicationBit = TRUE (bit7 = 1) or \
                FALSE (bit7 = 0)""", '02,01'],
        ], 'Message type: request, message direction: tester to ECU')
Table("DiagnosticSessionControl response message flow", [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'DiagnosticSessionControl response SID', '50'],
        ['2', """DiagnosticSessionType = programmingSession or \
        defaultSession)""", '02,01'],
        ['3', """sessionParameterRecord [byte 1] = P2Server_max (high byte)""",
        '00-FF'],
        ['4', """sessionParameterRecord [byte 1] = P2Server_max (low byte)""",
        '00-FF'],
        ['5', """sessionParameterRecord [byte 1] = P2*Server_max (high byte)""",
        '00-FF'],
        ['6', """sessionParameterRecord [byte 1] = P2*Server_max (low byte)""",
        '00-FF']
        ], 'Message type: response, message direction: ECU to tester')
Table("""Software download service and its maximum value of P2Server and \
        P2*Server""", [
            ["Parameter", "DefaultSession", "ProgrammingSession",
            "Description"],

            ["P2Server", "Min - 50 msec, Max - 500 msec",
            "Min - 50 msec, Max - 500 msec",
            """Time between reception of the last frame of a diagnostic \
            request on the LIN bus and the slave node being able to provide \
            data for a response.
            The maximum value defines the time after which a
            slave node must receive a slave response header
            before it discards its response."""],

            ["P2Server", "Min - P2, Max - 2000 msec",
            "Min - P2, Max - 2000 msec",
            """Time between sending a NRC 0x78 and the LIN Slave being able to \
            provide data for a response."""]
        ])
Table("Software download services and its maximum value of P4Server", [
        ['No.', 'Service', 'SIDs', 'Timing'],
        ['1', 'DiagnosticSessionControl', '0x10', 'P2Server_Max'],
        ['2', 'EcuReset', '0x11', '200msec'],
        ['3', 'SecurityAccess', '0x27', 'P2Server_Max'],
        ['4', 'ReadDataByIdentifier', '0x22', 'P2Server_Max'],
        ['5', 'RoutineControl', '0x31', '2400msec'],
        ['6','RequestDownload', '0x34','1000msec'],
        ['7','RequestUpload', '0x35', '1000msec'],
        ['8','TransferData', '0x36','5000msec'],
        ['9','RequestTransferExit', '0x37','6000msec'],
        ['10','TesterPresent', '0x3e','P2Server_Max']
        ])
Table('DiagnosticSessionControl service supported NRCs', [
        ['Hex', 'Description'],
        ['12', """**subFunctionNotSupported**

        Send if the sub-function parameter in the request message is not \
        supported."""],
        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],
        ['22', """**conditionsNotCorrect**

        This code shall be returned if the criteria for the request \
        DiagnosticSessionControl are not met."""]
        ])

ch(node("/*/ECU reset requirements"), 'text',
    """The ECUReset service shall be used to exit the ECU programmingSession \
    by performing a reset. The request message data parameter resetType shall \
    be set to HardReset. The tester may request to suppress the positive \
    response message by setting the suppressPosRspMsgIndicationBit (bit 7 of \
    the sub-function parameter) to TRUE.

    HardReset condition simulates the power-on/start-up sequence typically \
    performed after an ECU has been previously disconnected from its power \
    supply (i.e. battery). The performed action is implementation specific. \
    It might result in the re-initialization of both volatile memory and \
    non-volatile memory locations to predetermined values.""")

cd("/*/ECU reset requirements")
Req('', """ECUReset service shall be supported by the Bootloader in the \
    programmingSession. ECUReset service shall be used to come out from \
    programmingSession in BL.""")
Req('',"""The ECUReset service (11 hex) request shall be supported HardReset \
    with or without suppressPosRspMsgIndicationBit.""")
Req('',"""The ECUReset service shall be requested with sub-function other than \
    0x01/0x81 (HardReset) then BL shall respond NRC with \
    subFunctionNotSupported (0x12).""")
Req('',"""For ECUReset Service, the NRC with ConditionsNotCorrect (0x22) shall \
    not be supported by BL.""")
Req('',"""For ECUReset Service, the NRC with SecurityAccessDenied (SAD–0x33) \
    shall not be supported by the BL.""")
Table('ECUReset request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'EcuReset request SID', '11'],
        ['2', """resetType = HardReset

        suppressPosRspMsgIndicationBit = FALSE or TRUE (bit7 = 0 or 1)""",
        '01 or 81']
        ], 'Message type: request, message direction: tester to ECU')
Table('ECUReset response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'EcuReset response SID', '51'],
        ['2', 'resetType = HardReset', '01']
        ], "Message type: response, message direction: ECU to tester")
Table('ECUReset service supported NRCs', [
        ['Hex', 'Description'],
        ['12', """**subFunctionNotSupported**

        Send if the sub-function parameter in the request message is not \
        supported."""],
        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],
        ['22', """**conditionsNotCorrect**

        This code shall be returned if the criteria for the request \
        DiagnosticSessionControl are not met."""],
        [
            '33', """**SecurityAccessDenied (SAD)**

            This code shall be sent if the requested reset is secured \
            and the server is not in an unlocked state."""]
        ])

ch(node("/*/ReadDataByIdentifier service requirement"), 'text',
        """The ReadDataByIdentifier service shall be used to identify the ECU \
        hardware and software using specific dataIdentifier. The \
        ReadDataByIdentifier service shall supports one dataIdentifier in a \
        single request.""")
cd("/*/ReadDataByIdentifier service overview")
Table("PIDs and DIDs supported for ReadDataByIdentifier service", [
        ['PID/ DID', 'Name', 'Description'],

        ['D100', 'Active Diagnostic Session',
        'To report the active diagnostic session that the bootloader is in.'],

        ['F17E', 'ECU Delivery Assembly Number',
        """ Any variable aspect of the ECU (e.g., its color, associated \
        internal actuators or mechatronic parts). All downloadable software \
        components that are pre-loaded into the ECU."""],

        ['F17F', 'ECU Core Assembly Number',
        """This number shall identify the combination of the ECU hardware \
        (e.g., circuit board, micro-controller, memory, etc.) and any \
        non-replaceable software (primary bootloader and other fixed \
        software). All unused bytes shall be padded with FF hex."""],

        ['F180', 'Boot Software Identification',
        """The Bootloader SW part number (Boot Software Identification) data \
        shall be encoded in ASCII and all unused bytes shall be padded with \
        FF hex."""]
        ])
Req('', """The ReadDataByIdentifier service shall be supported in both \
    programmingSession and defaultSession.""")
Req('', """TesterPresent service is not necessarily required to keep the \
    ReadDataByIdentifier service active.""")
Req('', 'This service shall be supported in both PBL and SBL.')
Req('','For ReadDataByIdentifier, the NRC with conditionsNotCorrect (0x22) '
    'shall be supported by the BL.')
Req('','BL shall respond with NRC SecurityAccessDenied (0x33), if the '
    'dataIdentifier requested in the request message is secured and BL is '
    'not in an unlocked state.')

ch(node("/*/DataIdentifier"), 'text', 'The PBL can be in one of two different '
        'sessions, the defaultSession and the programmingSession. This '
        'dataIdentifier shall be used to report the active diagnostic session '
        'that the bootloader is in. If the ECU has entered the '
        'programmingSession the first byte in the dataRecord shall have the '
        'value of 02 hex (programmingSession). If the ECU is still in the '
        'defaultSession, the first byte in the dataRecord shall have the value '
        'of 01 hex (defaultSession).')
cd("/*/DataIdentifier")
Table(' DID request message flow - D100', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '22'],
        ['2', 'dataIdentifier(MSB)', 'D1'],
        ['3', 'dataIdentifier(LSB)', '00']
        ], 'Message type: request, message direction: tester to ECU')
Table(' DID response message flow - D100', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '62'],
        ['2', 'dataIdentifier(MSB)', 'D1'],
        ['3', 'dataIdentifier(LSB)', '00'],
        ['4', 'dataRecord: defaultSession or programmingSession', '01 or 02']
        ], 'Message type: response, message direction: ECU to tester')
cd("..")

ch(node('/*/ECU Delivery Assembly Number'), 'text', 'This ECU delivery assembly number '
        'shall be written by the ECU supplier while the ECU is being '
        'programmed.')
cd("/*/ECU Delivery Assembly Number")
Table(' PID request message flow - F17E', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '22'],
        ['2', 'dataIdentifier(MSB)', 'F1'],
        ['3', 'dataIdentifier(LSB)', '7E']
        ], 'Message type: request, message direction: tester to ECU')
Table(' PID response message flow - F17E', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '62'],
        ['2', 'dataIdentifier(MSB)', 'D1'],
        ['3', 'dataIdentifier(LSB)', '00'],
        ['4', 'dataRecord[data1]', 'ASCII'],
        ['5', 'dataRecord[data2]', 'ASCII'],
        ['..', '..', '..'],
        ['35', 'dataRecord[data32]', 'ASCII']
        ], 'Message type: response, message direction: ECU to tester')
cd('..')

ch(node('/*/ECU Core Assembly Number'), 'text', 'This ECU core assembly number shall be'
        'written by the OEM while the ECU is being programmed.')
cd("/*/ECU Core Assembly Number")
Table(' PID request message flow - F17F', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '22'],
        ['2', 'dataIdentifier(MSB)', 'F1'],
        ['3', 'dataIdentifier(LSB)', '7F']
        ], 'Message type: request, message direction: tester to ECU')
Table(' PID response message flow - F17F', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '62'],
        ['2', 'dataIdentifier(MSB)', 'D1'],
        ['3', 'dataIdentifier(LSB)', '00'],
        ['4', 'dataRecord[data1]', 'ASCII'],
        ['5', 'dataRecord[data2]', 'ASCII'],
        ['..', '..', '..'],
        ['35', 'dataRecord[data32]', 'ASCII']
        ], 'Message type: response, message direction: ECU to tester')
cd('..')

ch(node('/*/Boot Software Identification'), 'text', 'The boot software identification '
        'value shall be written by the KPIT while delivering the software.')
cd("/*/Boot Software Identification")
Table(' PID request message flow - F180', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '22'],
        ['2', 'dataIdentifier(MSB)', 'F1'],
        ['3', 'dataIdentifier(LSB)', '80']
        ], 'Message type: request, message direction: tester to ECU')
Table(' PID response message flow - F180', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'ReadDataByIdentifier request SID', '62'],
        ['2', 'dataIdentifier(MSB)', 'F1'],
        ['3', 'dataIdentifier(LSB)', '80'],
        ['4', 'numberOfModules', '01'],
        ['5', 'identificationParameterRecord [data_1]', 'ASCII'],
        ['6', 'identificationParameterRecord [data_2]', 'ASCII'],
        ['..', '..', '..'],
        ['36', 'identificationParameterRecord [data_32]', 'ASCII']
        ], 'Message type: response, message direction: ECU to tester')
Table('ReadDataByIdentifier service supported NRCs', [
        ['Hex', 'Description'],
        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],
        ['22', """**conditionsNotCorrect**

        This code shall be returned if the criteria for the request \
        DiagnosticSessionControl are not met."""],

        ['31', """**RequestOutOfRange**

        This code shall be sent if none of the requested dataIdentifier values \
        are supported by the device or the client exceeded the maximum number \
        of dataIdentifiers allowed to be requested at a time."""],

        ['33', """**SecurityAccessDenied (SAD)**

        This code shall be sent if the requested reset is secured \
        and the server is not in an unlocked state."""]
        ])

cd("/*/SecurityAccess service requirements")
Inf("""The SecurityAccess service shall be implemented in all programmable ECUs \
    to restrict access from unapproved tools. The SecurityAccess service \
    shall unlock the ECU for download and upload of data.

    The security access procedure shown below shall be used to "unlock" the \
    ECU and grant security access. Upon acceptance of a valid security seed \
    request, the security seed shall remain valid or "active" in the ECU until \
    the following conditions occur:

    * SecurityAccess (27H) diagnostic request is received (regardless of \
    whether the request is validly formatted, regardless of whether it is a \
    requestSeed or a sendKey request, regardless of whether it is for the same \
    or a different security level, and regardless of whether the security \
    level is supported by the ECU or not).

    Before the ECU is unlocked by the SecurityAccess service the following \
    services shall be blocked:

    * RoutineControl(0x31)
    * RequestDownload(0x34)
    * TransferData(0x36)
    * TransferExit(0x37)
    * RequestUpload(0x35)
    * ReadDataByIdentifier(Optional)"""
)
Req('','This service shall be supported in both PBL and SBL.')
Req('','The Bootloader shall support SecurityAccess service (27 hex) to enable '
    'the ECU unlocks for download and upload of data using security algorithm.')
Req('','The SecurityAccess service (27 hex) request shall only support security '
    'level 01 hex(i.e., requestSeed 01 hex) to protect access to software '
    'download related diagnostic functionality and shall only be supported in '
    'the programmingSession.')
Req('','The requested seed shall remain valid until next SecurityAccess service '
    '(27 hex) request or the change of diagnosticsession.')
Req('','The ECU and the tester shall use a common algorithm to calculate the '
    'security key based on the last seed.')
Table('SecurityAccess request message flow - seed request', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'SecurityAccess request SID', '27'],
        ['2', """securityAccessType = requestSpeed

        suppressPosRspMsgIndicationBit = FALSE (bit7 = 0)""",
        '01']
        ], 'Message type: request, message direction: tester to ECU')
Table('SecurityAccess response message flow - seed response', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'SecurityAccess response SID', '67'],
        ['2', 'securityAccessType = requestSpeed', '01'],
        ['3', 'securitySeed [byte 1]', '01'],
        ['4', 'securitySeed [byte 2]', '01'],
        ['5', 'securitySeed [byte 3]', '01']
        ], "Message type: response, message direction: ECU to tester")
Table('SecurityAccess request message flow - key request', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'SecurityAccess request SID', '27'],
        ['2', 'accessType = sendKey', '02'],
        ['3', 'securityKey [byte 1]', '00-FF'],
        ['4', 'securityKey [byte 2]', '00-FF'],
        ['5', 'securityKey [byte 3]', '00-FF']
        ], "Message type: request, message direction: tester to ECU")
Table('SecurityAccess response message flow - key response', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'SecurityAccess response SID', '67'],
        ['2', 'accessType = sendKey', '02']
        ], 'Message type: response, message direction: ECU to tester')
Table('SecurityAccess service supported NRCs', [
        ['Hex', 'Description'],
        ['12', """**subFunctionNotSupported**

        Send if the sub-function parameter in the request message is not \
        supported"""],

        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],

        ['22', """**conditionsNotCorrect**

        This code shall be returned if the criteria for the request \
        DiagnosticSessionControl are not met."""],

        ['24', """**requestSequenceError**

        Send if the ‘sendKey’ sub-function is received without first \
        receiving a ‘requestSeed’ request message."""],

        ['31', """**RequestOutOfRange**

        This code shall be sent if none of the requested dataIdentifier values \
        are supported by the device or the client exceeded the maximum number \
        of dataIdentifiers allowed to be requested at a time."""],

        ['33', """**SecurityAccessDenied (SAD)**

        This code shall be sent if the requested reset is secured \
        and the server is not in an unlocked state."""],

        ['35', """**invalidKey (IK)**

        Send if an expected “sendKey” sub-function value is received and the \
        value of the key does not match the server's internally \
        stored/calculated key."""],

        ['36', """**exceededNumberOfAttempts (ENOA)**

        Send if the delay timer is active due to exceeding the maximum number \
        of allowed false access attempts."""],

        ['37', """**requiredTimeDelayNotExpired (RTDNE)**

        Send if the delay timer is active and a request is transmitted."""]
        ])


PlantUML("Security access procedure","""

skinparam monochrome true

partition Tester {
(*) --> "Start Security Access"
--> "Request Security Access Seed SID=0x27" as ReqSecSeed
}

partition ECU {
  -right-> if "ECU already unlocked?" then
    -right->[true] "Report Security
Access Seed of 0x000000
to indicate that the ECU
is already unlocked.
Positiv response SID=0x67" as Unlocked
  else
    -down->[false] "Report random
security access seed.
Positiv Response SID=0x67" as RandSeed
  endif
}

partition Tester {
RandSeed -left-> "Calculate 3 byte
key based upon the
3 byte seed received
from the ECU"

-down-> "Submit 3 bytes key to ECU
SID 0x27"
}

partition ECU {
  --> if "Key Correct?" then
    -->[true] "Report security access
granted.
Positive Response SID=0x67" as Granted
  else
    -->[false] "Report Invalid Key.
Negative Response SID=0x7f
Request SID=0x27
responseCode=0x35" as InvalKey
  endif
}

partition Tester {
InvalKey --> "Secutiry Access denied" as SecDen
Granted --> "Security Access Granted" as SecGrand
Unlocked --> SecGrand

SecGrand --> (*)
SecDen --> (*)

}
""","""The security access procedure shown in figure shall be used to \
        "unlock" the ECU and grant security access. Upon receipt of a valid \
        seed request, the ECU shall respond with a randomly chosen security \
        seed. This seed shall remain valid or "active" according to the \
        requirement SFR_BL_SER27_5.On reception of the security key request \
        from the tester the ECU calculates the security key based on the last \
        seed sent with a common algorithm. If ECU calculated Security key and \
        the tester(calculated and sent to ECU) sent Security key matches, only \
        then the security is unlocked, if not it will remain locked.""",
         {'size': 'fit'})

ch(node("/*/RoutineControl service requirements"), 'text',
    """The RoutineControl service shall be used for activating the SBL after \
        download to RAM, erasing flash memory and for calculating checksums. \
        The RoutineControl service is used by the tester to start a routine, \
        stop a routine, and request routine results""")
ch(node("/*/RoutineInfo - Type and Status"), 'text',
    """The RoutineInfo parameter shall always be one byte in length and is \
    always the first data byte reported in the RoutineStatusRecord. \
    RoutineInfo consists of two four bit parameters. The upper nibble \
    (bits 7-4) shall be the RoutineType and the lower nibble (bits 3-0) shall \
    be the RoutineStatus. Valid RoutineType values are defined in Table 27 and \
    valid RoutineStatus values are defined in Table 28.""")
cd("/*/RoutineInfo - Type and Status")
Table("Routine Type", [
    ['Hex', 'Definition'],
    ['1', 'A positive response to sub-function 01H (startRoutine) shall only '
    'be given after the routine has stopped executing. Any Response Additional '
    'Data is returned in the positive response to the startRoutine request.'],
    ['2', 'The routine shall start prior to the positive response to '
    'sub-function 01H (startRoutine). The routine shall complete after it has '
    'run for a finite time (i.e., it is not dependent upon a stopRoutine '
    'request sub-function 02H). Any request for routine results using '
    'sub-function 03H that is received while the routine is executing shall '
    'result in a negative response code of 21H (busyRepeatRequest).'],
    ['3','The routine shall start prior to the positive response to '
    'sub-function 01H (startRoutine). The routine may complete after it has '
    'run for a finite time or it may run until commanded to stop via '
    'sub-function 02H (stopRoutine). Any request for routine results using '
    'sub-function 03H that is received while the routine is executing shall '
    'result in a positive response with the current results. ']
    ],

    'The results from this RoutineType shall remain accessible using '
    'requestRoutineResults so long as the diagnostic session during which the '
    'test was run remains active or until the next control routine is executed.'
    )
Table("Routine Status", [
    ['Hex', 'Definition'],
    ['1','The routine aborted before completion (e.g., all documented fault '
    'monitoring was not executed during selftest because it was blocked by the '
    'presence of an active fault).'],
    ['2','The routine is currently active.']
])
Req('','Routine IDs Erase memory (FF00 hex), Calculate checksum (FF01 hex), '
'Validate Application (0304 hex) and Activate SBL (0301 hex) shall support only '
'routineControlType equal to   startRoutine (01 hex) in the request and response.')
Req('','Routine IDs Erase memory (FF00 hex), Calculate the checksum of an ECU '
'memory block FF01 hex), Validate Application (0304) and Activate SBL '
'(0301 hex) shall contain the first byte routineStatusRecord shall always be '
'10 hex in the positive response indicating RoutineType 1 and RoutineStatus 0.')
Req('','If Routine control service of Routine Type 1 is requested with '
'sub-function other than startRoutine (0x01), stopRoutine (0x02)  and '
'requestRoutineResults (0x03), then BL shall respond with NRC '
'subFunctionNotSupported (0x12).')
Req('','In PBL, Other than RAM download is requested then the BL shall send '
'NRC with conditionsNotCorrect (0x22).')
Req('','If Routine control service of Routine Type 1 is requested with '
'sub-function requestRoutineResults (0x03) before the sub-function '
'StartRoutine (0x01) request then the BL shall send NRC with '
'requestSequenceError (0x24).')
Req('','If Routine control service of Routine Type 1 is requested with '
'sub-function startRoutine (0x01) with sub routine ID other than the Activate '
'SBL(0301), Erase Memory(FF01), Check programming dependencies(FF01) and check '
'valid application(0304) then the BL shall send NRC with requestOutOfRange(0x31).')
Req('','If Routine control service of Routine Type 1 is requested with '
'sub-function startRoutine (0x01) with sub routine ID as Activate SBL (0301) '
'or Erase Memory (FF01) before the security is unlocked then the BL shall send '
'NRC with SecurityAccessDenied (0x33).')
Req('','The BL shall respond NRC with generalProgrammingFailure (0x72), if '
'the BL detects an error when accessing internal memory.')

ch(node("/*/RoutineIdentifier 0301 Hex (Activate secondary bootloader)"),
'text',
'RoutineIdentifier 0301 hex shall be used to activate the SBL after download to RAM.')
cd("/*/RoutineIdentifier 0301 Hex (Activate secondary bootloader)")
Req('','This service is supported in PBL only.')
Req('','SBL shall be downloaded before activating SBL in to RAM.')
Req('','Security should be unlocked before activation of SBL.')
Table('RoutineControl - Activate secondary bootloader request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '31'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', '03'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '01'],
        ['5', 'routineControlOptionRecord = '
        '[memoryAddress (SBL start address, byte 1, MSB)]', '00-FF'],
        ['6', 'memoryAddress (SBL start address, byte 2)', '00-FF'],
        ['7', 'memoryAddress (SBL start address, byte 3)', '00-FF'],
        ['8', 'memoryAddress (SBL start address, byte 4, LSB) ', '00-FF'],
        ], 'Message type: request, message direction: tester to ECU')
Table(' RoutineControl - Activate secondary bootloader response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '71'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', '03'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '01'],
        ['5', 'routineStatusRecord [byte 1]', '10'],
        ], 'Message type: response, message direction: ECU to tester')

ch(node("/*/RoutineIdentifier FF00 hex (EraseMemory)"), 'text',
'If an ECU is delivered with the complete programmable memory already erased, '
'the ECU shall include an internal "already erased" detection in order to '
'reduce the overall software download time. If the complete programmable '
'memory already is erased and all other preconditions are met (e.g., SBL is '
'downloaded and activated), the ECU shall send a positive response to a '
'RoutineControl Erase Memory request within P2server timing. Once the ECU has '
'programmed any bytes within the programmable memory area, the internal '
'"already erased" detection shall be blocked and an erase operation shall '
'always be performed.')
cd("/*/RoutineIdentifier FF00 hex (EraseMemory)")
Req('','This service is supported in SBL only.')
Req('','Security should be unlocked before erase of ECU memory.')
Req('','This service shall erase ECU memory within specified memory '
'address and memory size.')
Table('RoutineControl - EraseMemory request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '31'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', '03'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '01'],
        ['5', 'routineControlOptionRecord = '
        '[memoryAddress (Erase start address, byte 1, MSB)]', '00-FF'],
        ['6', 'memoryAddress (Erase start address, byte 2)', '00-FF'],
        ['7', 'memoryAddress (Erase start address, byte 3)', '00-FF'],
        ['8', 'memoryAddress (Erase start address, byte 4, LSB) ', '00-FF'],
        ['9','memorySize (Erase length, byte 1, MSB)', '00-FF'],
        ['10','memorySize (Erase length, byte 2)', '00-FF'],
        ['11','memorySize (Erase length, byte 3)', '00-FF'],
        ['12','memorySize (Erase length, byte 4, LSB)', '00-FF']
        ], 'Message type: request, message direction: tester to ECU')
Table(' RoutineControl - EraseMemory response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '71'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', 'FF'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '00'],
        ['5', 'routineStatusRecord [byte 1]', '10'],
        ], 'Message type: response, message direction: ECU to tester')

ch(node("/*/RoutineIdentifier FF01 hex (check programming dependencies)"),'text',
'RoutineIdentifier FF01 hex shall be used to initiate a checksum calculation '
'of an ECU memory block. RoutineControl with routine identifier FF01 hex is '
'not used during a normal software download or upload operation, but can be '
'used for debugging. The same checksum algorithm as used by the '
'RequestTransferExit service shall be used.')
cd("/*/RoutineIdentifier FF01 hex (check programming dependencies)")
Req('','This service is supported in both PBL and SBL.')
Req('','16 bit CRC shall be calculated by using this request against '
'downloaded data.')
Req('','This service shall calculate CRC for the specified memory address '
'and the memory size.')
Table('RoutineControl - check programming dependencies request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '31'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', '03'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '01'],
        ['5', 'routineControlOptionRecord = '
        '[memoryAddress (Checksum start address, byte 1, MSB)]', '00-FF'],
        ['6', 'memoryAddress (Checksum start address, byte 2)', '00-FF'],
        ['7', 'memoryAddress (Checksum start address, byte 3)', '00-FF'],
        ['8', 'memoryAddress (Checksum start address, byte 4, LSB) ', '00-FF'],
        ['9','memorySize (Length, byte 1, MSB)', '00-FF'],
        ['10','memorySize (Length, byte 2)', '00-FF'],
        ['11','memorySize (Length, byte 3)', '00-FF'],
        ['12','memorySize (Length, byte 4, LSB)', '00-FF']
        ], 'Message type: request, message direction: tester to ECU')
Table(' RoutineControl - check programming dependencies response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '71'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', 'FF'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '00'],
        ['5', 'routineStatusRecord [byte 1]', '10'],
        ['6', 'routineStatusRecord [byte 2] = Checksum byte 1 (MSB)', '00-FF'],
        ['7', 'routineStatusRecord [byte 2] = Checksum byte 2 (LSB)', '00-FF']
        ], 'Message type: response, message direction: ECU to tester')

cd("/*/RoutineIdentifier 0304 hex (check valid application)")
Inf("""RoutineIdentifier 0304 hex shall be used to detect whether or not the \
ECU has valid application software programmed and report this determination to \
the tester.

The following sequences of checks are carried out for the service “Check \
validate application”:

1. At application start address is not the erase value of controller.

2. Signature pattern at the signature pattern address location.

If all these conditions are satisfied then only the check valid Application \
request will return as valid application is present otherwise it returns \
valid application is not present.""")
Req('','This service shall be supported in both PBL and SBL.')
Req('','The response of service includes the status of application whether '
'it is valid present (0x02) or not valid present (0x01).')
Table('RoutineControl - check valid application request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '31'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', '03'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '04']
        ], 'Message type: request, message direction: tester to ECU')
Table(' RoutineControl - check valid application response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RoutineControl request SID', '71'],
        ['2', 'routineControlType = startRoutine', '01'],
        ['3', 'routineIdentifier [byte 1] (MSB)', '03'],
        ['4', 'routineIdentifier [byte 2] (LSB)', '01'],
        ['5', 'routineStatusRecord [byte 1]', '10'],
        ], 'Message type: response, message direction: ECU to tester')

cd("/*/RoutineControl supported NRCs")
Table('RoutineControl service supported NRCs', [
        ['Hex', 'Description'],
        ['12', """**subFunctionNotSupported**

        Send if the sub-function parameter in the request message is not \
        supported"""],

        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],

        ['22', """**conditionsNotCorrect**

        This code shall be returned if the criteria for the request \
        DiagnosticSessionControl are not met."""],

        ['24', """**requestSequenceError**

        Send if the ‘sendKey’ sub-function is received without first \
        receiving a ‘requestSeed’ request message."""],

        ['31', """**RequestOutOfRange**

        This code shall be sent if none of the requested dataIdentifier values \
        are supported by the device or the client exceeded the maximum number \
        of dataIdentifiers allowed to be requested at a time."""],

        ['33', """**SecurityAccessDenied (SAD)**

        This code shall be sent if the requested reset is secured \
        and the server is not in an unlocked state."""],

        ['72', """**GeneralProgrammingFailure**

        This return code shall be sent if the server detects an error when \
        performing a routine, which accesses server internal memory. An \
        example is when the routine erases or programs a certain memory \
        location in the permanent memory device (e.g. Flash Memory) and the \
        access to that memory location fails."""],
        ])

ch(node("/*/RequestDownload service requirements"), 'text',
"""The requestDownload service is used by the tester to initiate a data \
transfer from the tester to the ECU (download). After the ECU has received \
the requestDownload request message, the ECU shall take all necessary actions \
to receive data before it sends a positive response message.""")

cd("/*/RequestDownload service requirements")

Inf("""The request download service includes the “dataFormatIdentifier” \
parameter of one byte value with each nibble encoded separately. The high \
nibble specifies the “compressionMethod”, and the low nibble specifies the \
“encryptingMethod”. The value 00 hex specifies that neither compressionMethod \
nor encryptingMethod is used.")
Inf("The request download service includes the \
“addressAndLengthFormatIdentifier” parameter of one bye the bit 7 to bit 4 \
specifies the number of bytes allocated to address the memory and the bit 3 to \
bit 0 specifies number of bytes of the information to be written into the \
memory.""")

Inf("""The request download service includes the “memory address” parameter \
indicating the starting address of ECU memory to which data is to be written. \
The number of bytes used for this address is defined by the low nibble (bit 3 \
- 0) of the addressFormatIdentifier parameter. For ex: (0x01F00001 is the \
starting address the byte 3 =01, byte 2= F0, byte 1=00, byte 0=01 with the MSB \
bit of address first).""")

Inf("""The request download service includes the “memorySize \
(unCompressedMemorySize)” parameter used by the ECU to compare the \
uncompressed memory size with the total amount of data transferred during the \
TransferData service. This increases the programming security. The number of \
bytes used for this size is defined by the high nibble (bit 7 - 4) of the \
addressAndLengthFormatIdentifier. For addressAndLengthFormat - 44 hex value is \
used so that the range of memory that can be addressed is (0x00000000 to \
0xFFFFFFFF) and the number of bytes that can be read from the memory ranges \
from 0x00000000 to 0xFFFFFFFF bytes.""")

Req('', 'This service shall be supported for both PBL and SBL.')
Req('', """The bootloader shall support RequestDownload \
service (34 hex) to initiate a data transfer from the tester to the ECU. """)
Req('',"""The positive message response for RequestDownload \
service (34 hex) shall contain lengthFormatIdentifier 20 hex to hold the \
maximum block length which can transmit each download service.""")
Req('',"""The RequestDownload service (34 hex) request shall \
support dataFormatIdentifier 00 hex (uncompressed data) and \
addressAndLengthFormatIdentifier 44 hex.""")
Req('',"""BL shall send NRC with requestOutOfRange (0x31) if \
RequestDownload service is requested with the memory address range that \
doesn’t fall in the supported memory area.""")
Req('',"""If RequestDownload service is requested before the \
security is unlocked then the BL shall send NRC with SecurityAccessDenied \
(0x33).""")

Inf("The NRC uploadDownloadNotAccepted (0x70) shall not supported by BL but \
can be implemented based on customer requirements. The detail on this \
requirement shall be provided in Portspecific SRS under section name Port \
Specific requirements.")

Table('RequestDownload request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RequestDownload request SID', '34'],
        ['2', 'dataFormatIdentifier', '00-FF'],
        ['3', 'addressAndLengthFormatIdentifier', '44'],
        ['4', 'memoryAddress[byte 1] (MSB)', '00-FF'],
        ['5', 'memoryAddress[byte 2]', '00-FF'],
        ['6', 'memoryAddress[byte 3]', '00-FF'],
        ['7', 'memoryAddress[byte 4](LSB)', '00-FF'],
        ['8', 'memorySize[byte 1] (MSB)', '00-FF'],
        ['9', 'memorySize[byte 2]', '00-FF'],
        ['10', 'memorySize[byte 3]', '00-FF'],
        ['11', 'memorySize[byte 4](LSB)', '00-FF']
        ], 'Message type: request, message direction: tester to ECU')
Table('RequestDownload response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RequestDownload response SID', '74'],
        ['2', 'lengthFormatIdentifier', '20'],
        ['3', 'maxNumberofBlockLength [byte 1] (MSB)', '00-0F'],
        ['4', 'maxNumberofBlockLength [byte 2] (LSB)', '00-FF'],
        ], 'Message type: response, message direction: ECU to tester')
Table('RequestDownload service supported NRCs', [
        ['Hex', 'Description'],

        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],

        ['22', """**conditionsNotCorrect**

        This code shall be returned if the criteria for the request \
        DiagnosticSessionControl are not met."""],

        ['31', """**RequestOutOfRange**

        This code shall be sent if none of the requested dataIdentifier values \
        are supported by the device or the client exceeded the maximum number \
        of dataIdentifiers allowed to be requested at a time."""],

        ['33', """**SecurityAccessDenied (SAD)**

        This code shall be sent if the requested reset is secured \
        and the server is not in an unlocked state."""],

        ['70', """**uploadDownloadNotAccepted (UDNA)**

        This response code indicates that an attempt to download to a server's \
        memory cannot be accomplished due to fault conditions."""]
        ])
Inf("""The file download method provides a means for an off-board tester to \
send multiple bytes of data to an ECU. The file download process combines a \
number of bootloader services to achieve this.

The file download sequence is based on the non-volatile server memory \
programming process described in ref. [2]. Only programming step (STP2) and \
post-programming step (STP3) of Programming Phase #1 is used.

All released software files which are downloadable to the ECU shall be capable \
of being downloaded to the ECU individually or in any grouping combination \
independent of order. The only exception to this is that the secondary \
bootloader shall always be required to be downloaded first when supported. \
Any other required grouping or order dependencies shall require explicit\
approval by the responsible authority appointed by the operating company and \
specific agreements with all affected tools from EOL and/or service.

 As an example, if the ECU supports a secondary bootloader (file A), a \
 strategy memory area (file B), and a calibration memory area (file C), then \
 the following download sequences shall be supported:

* Transition to programmingSession, download file A then B
* Transition to programmingSession, download file A then C
* Transition to programmingSession, download file A, B, then C
* Transition to programmingSession, download file A, C, then B""")

#TODO: add diagrams
#Figure("#9-10 Programming sequence")


ch(node("/*/RequestUpload service requirements"), 'text',
"""The RequestUpload service is used by the tester to initiate a data transfer \
from the ECU to the tester (upload).The RequestUpload service shall be \
optional.""")
cd("/*/RequestUpload service requirements")
Inf("""The request upload service includes the “dataFormatIdentifier” \
parameter of one byte value with each nibble encoded separately. The high \
nibble specifies the “compressionMethod”, and the low nibble specifies the \
“encryptingMethod”. The value 00 hex specifies that no compressionMethod nor \
encryptingMethod is used.""")
Inf("""The request upload service includes the \
“addressAndLengthFormatIdentifier” parameter of one bye the bit 7 to bit 4 \
specifies the number of bytes allocated to address the memory and the bit 3 to \
bit 0 specifies number of bytes of the information wanted from the memory.""")
Inf("""The request upload service includes the “memory address” indicates the \
starting address of server memory from which data is to be retrieved. The \
number of bytes used for this address is defined by the low nibble (bit 3 - 0) \
of the addressFormatIdentifier parameter. For ex: (0x01F00001 is the starting \
address the byte 3 =01, byte 2= F0, byte 1=00, byte 0=01 with the MSB bit of \
address first). The use of a memoryIdentifier would be a dual processor server \
with 16-bit addressing and memory address overlap (when a given address is \
valid for either processor but yields a different physical memory device or \
when internal and external flash is used). In this case, an otherwise unused \
byte within the memoryAddress parameter can be specified as a memoryIdentifier \
used to select the desired memory device.""")
Inf("""The request upload service includes the “memorySize \
(unCompressedMemorySize)” used by the server to compare the uncompressed \
memory size with the total amount of data transferred during the TransferData \
service. This increases the programming security. The number of bytes used for \
this size is defined by the high nibble (bit 7 - 4) of the \
addressAndLengthFormatIdentifier.""")

Req('', 'This service shall be supported only in SBL.')
Req('', """The bootloader shall support RequestUpload \
service (35 hex) to initiate a data transfer from the ECU to the tester.""")
Req('',"""The RequestUpload service (35 hex) request shall \
support dataFormatIdentifier 00 hex and addressAndLengthFormatIdentifier 44 \
hex only.""")
Req('',"""The positive message response for RequestUpload \
service (35 hex) shall contain lengthFormatIdentifier 20 hex to hold the 16 \
bit CRC checksum value from the ECU.""")
Req('',"""The conditionsNotCorrect (0x22) shall be issued \
for the upload request while ECU is in PBL programming session or \
RequestUpload service is requested when BL is not completed the previous \
upload request in the current programming session.""")
Req('', """BL shall send NRC with requestOutOfRange (0x31) if RequestUpload \
service is requested with the memory address range that doesn’t fall in the \
supported memory area.""")
Req('',""" If RequestUpload service is requested before the security is \
unlocked then the BL shall send NRC with SecurityAccessDenied (0x33).""")

Inf(""""The NRC uploadDownloadNotAccepted (0x70) is not supported by BL but \
can be implemented based on customer requirements. The detail on this \
requirement shall be provided in Portspecific SRS under section name Port \
Specific requirements.""")

Table('RequestUpload request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RequestUpload request SID', '35'],
        ['2', 'dataFormatIdentifier', '00'],
        ['3', 'addressAndLengthFormatIdentifier', '44'],
        ['4', 'memoryAddress[byte 1] (MSB)', '00-FF'],
        ['5', 'memoryAddress[byte 2]', '00-FF'],
        ['6', 'memoryAddress[byte 3]', '00-FF'],
        ['7', 'memoryAddress[byte 4](LSB)', '00-FF'],
        ['8', 'memorySize[byte 1] (MSB)', '00-FF'],
        ['9', 'memorySize[byte 2]', '00-FF'],
        ['10', 'memorySize[byte 3]', '00-FF'],
        ['11', 'memorySize[byte 4](LSB)', '00-FF']
        ], 'Message type: request, message direction: tester to ECU')
Table('RequestUpload response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RequestUpload response SID', '75'],
        ['2', 'lengthFormatIdentifier', '20'],
        ['3', 'maxNumberofBlockLength [byte 1] (MSB)', '00-0F'],
        ['4', 'maxNumberofBlockLength [byte 2] (LSB)', '00-FF'],
        ], 'Message type: response, message direction: ECU to tester')
Table('RequestUpload service supported NRCs', [
        ['Hex', 'Description'],

        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],

        ['22', """**conditionsNotCorrect**

        This code shall be returned if the criteria for the request \
        DiagnosticSessionControl are not met."""],

        ['31', """**RequestOutOfRange**

        This code shall be sent if none of the requested dataIdentifier values \
        are supported by the device or the client exceeded the maximum number \
        of dataIdentifiers allowed to be requested at a time."""],

        ['33', """**SecurityAccessDenied (SAD)**

        This code shall be sent if the requested reset is secured \
        and the server is not in an unlocked state."""],

        ['70', """**uploadDownloadNotAccepted (UDNA)**

        This response code indicates that an attempt to download to a server's \
        memory cannot be accomplished due to fault conditions."""]
        ])

Inf("""The file upload method provides a means for an ECU to send multiple \
bytes of data to an off-board tester. The file upload process combines a number \
of bootloader services to achieve this.

Message sequencing consists of a means for initiating the upload, transfer \
of messages and exit of the upload operation as detailed in \
`/*/File upload procedure (1 of 5)`_ to `/*/File upload procedure (5 of 5)`_.""")

#TODO: add diagrams
#Figure("#17-21 File upload procedure")
Figure('File upload procedure (1 of 5)', '.png')
Figure('File upload procedure (5 of 5)', '.png')

ch(node("/*/TransferData service requirements"), 'text',
"""The TransferData service is used by the tester to transfer data either from \
the tester to the ECU (download) or from the ECU to the tester (upload).""")
cd("/*/TransferData service requirements")

Inf("The data transfer direction is defined by the preceding RequestDownload \
or RequestUpload service. If the tester initiated a RequestDownload the data \
to be transferred is included in the parameter(s) transferRequestParameter in \
the TransferData request message(s). If the tester initiated a RequestUpload \
the data to be uploaded is included in the parameter(s) \
transferResponseParameter in the TransferData response message(s).")
Inf("""The TransferData service request includes a blockSequenceCounter to \
allow for an improved error handling in case a TransferData service fails \
during a sequence of multiple TransferData requests. The blockSequenceCounter \
shall be handled by the tester and the ECU. It is recommended a tester \
retransmit the transferData service (i.e., with the same blockSequenceCounter \
and data) at least two times if no response is received from the ECU. If an \
ECU receives a transferData request during an active download sequence with \
the same blockSequenceCounter as the last accepted transferData request, it \
shall respond with a positive response without writing the data once again to \
its memory.

The blockSequenceCounter of the ECU shall be initialised to one (1) when \
receiving a RequestDownload (34 hex) or RequestUpload (35 hex) request \
message. This means that the first TransferData (36 hex) request message \
following the RequestDownload (34 hex) or RequestUpload (35 hex) request \
message starts with a blockSequenceCounter of one (1).""")

Req('',"""This service shall be supported in both PBL and SBL.""")
Req('',"""The Bootloader shall support TransferData service (36 hex) to \
transfer data either from the tester to the ECU (download) or from the ECU to \
the tester (upload).""")
Req('',"""f TransferData request to download/upload data is correctly received \
and processed in the Bootloader but the positive response message does not \
reach the tester, then tester would determine an application layer timeout and \
would repeat the same request. Bootloader receives TransferData (0x36) service \
request during an active download or active upload sequence with the same \
blockSequenceCounter as the last accepted TransferData request, then \
Bootloader shall respond with a positive response without writing the data \
once again to its memory.""")
Req('',"""If the TransferData request to download data is not received \
correctly in the ECU, then the ECU would not send a positive response message. \
The tester would determine an application layer timeout and would repeat the \
same request (including the same blockSequenceCounter). The ECU would receive \
the repeated TransferData request and shall determine based on the included \
blockSequenceCounter that this is a new TransferData. The ECU would process \
the service and would send the positive response message.""")
Req('',"""If the TransferData request to upload data is not received correctly \
in the ECU, then the ECU shall not send a positive response message. The \
tester would determine an application layer timeout and would repeat the same \
request (including the same blockSequenceCounter). The ECU shall receive the \
repeated TransferData request and shall determine based on the included \
blockSequenceCounter that this is a new TransferData. The ECU shall process \
the service and would send the positive response message.""")
Req('',"""In TransferData request for download, if Number of bytes transferred \
is not equal to   the length in transfer data request then the BL shall send \
the Negative response code with incorrectMessageLengthOrInvalidFormat \
(0x13).""")
Req('',"""If TransferData request is requested before the RequestDownload or \
RequestUpload security is active then the BL shall send NRC with \
requestSequenceError (0x24).""")
Req('',"""In TransferData request, if requested total transfer data length \
exceeds the length requested in download/upload request then the BL shall send \
NRC with requestOutOfRange (0x31).""")
Req('',"""If the active service is transfer data (0x36) for request upload \
(0x35) AND if number of attempts of starting P2*Server timer exceeds the NRC78 \
max Limit  then the BL shall send NRC with transferDataSuspended(0x71).""")
Req('',"""The BL shall respond NRC with generalProgrammingFailure (0x72), if \
the BL detects an error when accessing internal memory during transfer data \
for request download and transfer data for request upload.""")
Req('',"""In transfer data for request download/upload If block sequence \
counter is NOT same as previous block AND If received block sequence counter \
is NOT EQUAL to  the expected block sequence counter i.e, previous block \
sequence counter + 1 then the BL shall send NRC with \
wrongBlockSequenceCounter(0x73).""")

Table('TransferData request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'TransferData request SID', '36'],
        ['2', 'blockSequenceCounter', '00-FF'],
        ['3', 'transferRequestParameterRecord[transferRequestParameter#1]', '00-FF'],
        ['4', 'transferRequestParameterRecord[transferRequestParameter#2]', '00-FF'],
        ['5', 'transferRequestParameterRecord[transferRequestParameter#3]', '00-FF'],
        ['6', 'transferRequestParameterRecord[transferRequestParameter#4]', '00-FF'],
        ['..','..','..'],
        ['n', 'transferRequestParameterRecord[transferRequestParameter#n]', '00-FF'],
        ], 'Message type: request, message direction: tester to ECU')
Table('TransferData response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'TransferData response SID', '76'],
        ['2', 'blockSequenceCounter', '00-FF']
        ], 'Message type: response, message direction: ECU to tester')
Table('RequestUpload service supported NRCs', [
        ['Hex', 'Description'],

        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],

        ['24', """**RequestSequenceError**

        The RequestDownload or RequestUpload service is not active when a \
        request for this service is received."""],

        ['31', """**RequestOutOfRange**

        This code shall be sent if none of the requested dataIdentifier values \
        are supported by the device or the client exceeded the maximum number \
        of dataIdentifiers allowed to be requested at a time."""],

        ['33', """**SecurityAccessDenied (SAD)**

        This code shall be sent if the requested reset is secured \
        and the server is not in an unlocked state."""],

        ['71', """**transferDataSuspended**

        This response code indicates that a data transfer operation was \
        halted due to some fault."""],

        ['72', """**GeneralProgrammingFailure**

        This return code shall be sent if the server detects an error when \
        performing a routine, which accesses server internal memory. An \
        example is when the routine erases or programs a certain memory \
        location in the permanent memory device (e.g. Flash Memory) and the \
        access to that memory location fails."""],

        ['73', """**WrongBlockSequenceCounter**

        This return code shall be sent if the server detects an error in the \
        sequence of the blockSequenceCounter.

        Note that the repetition of a TransferData request message with a \
        blockSequenceCounter equal to the one included in the previous \
        TransferData request message shall be accepted by the server."""]
        ])

ch(node("/*/RequestTransferExit service requirements"), 'text',
"""This service is used by the tester to terminate a data transfer between \
tester and ECU.""")
cd("/*/RequestTransferExit service requirements")

Req('','This service shall be supported in both PBL and SBL.')
Req('',"""The Bootloader shall support RequestTransferExit service (37 hex) to \
terminate a data transfer either from the tester to the ECU (download) or from \
the Bootloader to the tester (upload).""")
Req('',"""The Bootloader shall return two byte checksum calculated from the \
specified address range in recent request download as positive response for \
RequestTransferExit service (37 hex) request.""")
Req('',"""If Transfer Exit request shall be requested before the \
RequestDownload is active then the BL shall send NRC \
with requestSequenceError(0x24).""")

Table('RequestTransferExit request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RequestTransferExit request SID', '37']
        ], 'Message type: request, message direction: tester to ECU')
Table('RequestTransferExit response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'RequestTransferExit response SID', '77'],
        ['2', 'transferResponseParameterRecord[transferResponseParameter#1 ] \
        =checksum byte 1 (MSB)', '00-FF'],
        ['3', 'transferResponseParameterRecord[transferResponseParameter#2 ] \
        =checksum byte 2 (LSB)', '00-FF'],
        ], 'Message type: response, message direction: ECU to tester')
Table('RequestUpload service supported NRCs', [
        ['Hex', 'Description'],

        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""],

        ['24', """**RequestSequenceError**

        The RequestDownload or RequestUpload service is not active when a \
        request for this service is received."""]])

Inf("""The RequestTransferExit, transferResponseParameterRecord shall include \
a two byte checksum, which is required by the tester to support the transfer \
of data. The two byte checksum shall be calculated including all data bytes \
specified in the latest RequestDownload service (i.e., the data bytes \
following the blockSequenceCounter in each TransferData request). The checksum \
shall be calculated after the data bytes have been programmed into flash memory.

The checksum algorithm to be used shall be the CRC16-CITT:

* Polynomial: x^6+x^2+x^5+1 (1021 hex)

* Initial value: FFFF (hex)

For a fast CRC16-CITT calculation a look-up table implementation is the \
preferred solution. For ECUs with a limited amount of flash memory (or RAM), \
other implementations may be necessary.""")

ch(node("/*/TesterPresent service requirements"),'text',
"""This service is used to indicate to an ECU (or ECUs) that a tester is still \
connected to the vehicle and that certain diagnostic services and/or \
communication that have been previously activated are to remain active.""")
cd("/*/TesterPresent service requirements")
Inf("""This service is used to keep one or multiple servers in a diagnostic \
session other than the defaultSession. This can either be done by transmitting \
the TesterPresent request message periodically or in case of the absence of other \
diagnostic services to prevent the server(s) from automatically returning to \
the defaultSession. The detailed session requirements that apply to the use of \
this service when keeping a single server or multiple servers in a diagnostic \
session other than the defaultSession.""")

Req('','This service shall be supported in both PBL and SBL.')
Req('',"""The Diagnostic module shall support TesterPresent service (3E hex) \
to indicate the ECU that the tester is still connected and that certain \
diagnostic services and/or communications that have been previously activated \
are to remain active.""")

Table('TesterPresent request message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'TesterPresent request SID', '3E'],
        ['2', """zeroSubFunction suppressPosRspMsgIndicationBit = FALSE or \
        TRUE (bit7 = 0 or 1)""", '00 or 80']
        ], 'Message type: request, message direction: tester to ECU')
Table('TesterPresent response message flow', [
        ['Data byte', 'Description', 'Byte Value(Hex)'],
        ['1', 'TesterPresent response SID', '7E'],
        ['2', 'zeroSubFunction', '00']
        ], 'Message type: response, message direction: ECU to tester')
Table('RequestUpload service supported NRCs', [
        ['Hex', 'Description'],

        ['12', """**subFunctionNotSupported**

        Send if the sub-function parameter in the request message is not \
        supported."""],

        ['13', """**incorrectMessageLengthOrInvalidFormat**

        The length of the message is wrong."""]])

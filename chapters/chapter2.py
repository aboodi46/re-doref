#!/usr/bin/env python
# -*- coding: utf-8 -*-

from header import *

cd("/*/Bootloader concept")
Inf("""The bootloader is divided into two separate and mandatory parts: a \
primary bootloader (PBL) and a secondary bootloader (SBL).The PBL is designed \
to be permanently placed in a protected flash boot sector, which is activated \
from reset. The SBL is intended to be downloaded by the PBL into the CPU \
internal RAM. The SBL can be described as a superset of the PBL, adding \
functions for erase and program of flash memory and EEPROM. """)

Figure("Typical ECU memory map", "memory_map.png","", {'size':'fit'})

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

Figure("State diagram of ECU","ecu_state_diagram.png",
        """The state diagram in the figure shows the states of an ECU. In all \
        the states it shall be possible to force the ECU into program mode \
        with the DiagnosticSession Control service with programmingSession \
        request.""", {'size' : 'fit'})

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

Figure("Application to Bootloader jump","app_to_bl_jump.png")

Figure("Bootloader flow diagram","bl_flow_dia.png",
        "", {'size': 'fit'})

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
Figure('Security access procedure','sec_accs_proc.png',
        """The security access procedure shown in figure shall be used to \
        "unlock" the ECU and grant security access. Upon receipt of a valid \
        seed request, the ECU shall respond with a randomly chosen security \
        seed. This seed shall remain valid or "active" according to the \
        requirement SFR_BL_SER27_5.On reception of the security key request \
        from the tester the ECU calculates the security key based on the last \
        seed sent with a common algorithm. If ECU calculated Security key and \
        the tester(calculated and sent to ECU) sent Security key matches, only \
        then the security is unlocked, if not it will remain locked.""",
        {'size':'fit'})

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

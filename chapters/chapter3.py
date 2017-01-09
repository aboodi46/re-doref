from header import *
from doref.utils.plantuml.plantuml import *

ch(node("/*/Network layer requirements"), 'text',
"""Physically addressing (1 to 1 communication) shall be supported for all \
types of network layer messages. Physical addressing is used to address the \
particular ECU.

Functionally addressing message will be sent to group of ECU categorized to \
receive the particular message based on its functionality. Functionally \
addressing (1 to n communication) shall only be supported for single frame \
communication.""")
cd("/*/Network layer requirements")

Req("","""The Network layer shall support both physically and functionally \
addressed requests from the tester.""")
Req('',"""The Network layer shall support multiple frame message transmission \
and reception.""")
Req('',"""The Network layer shall support four different types of network \
layer protocol data units. The network layer protocol data units are called \
Single Frame (SF), First Frame (FF), and Consecutive Frame (CF). """)
Req('',"""The Network layer shall ignore a single frame with data length zero \
or greater than six.""")
Req('',"""The Network layer shall ignore a first frame with data length less \
than seven and message reception shall be aborted.""")
Req('',"""The Network layer shall abort the multiframe message on reception of \
wrong sequence number in consecutive frame.""")
Req('',"""Network layer shall reject multiframe functional requests i.e., \
functionally addressed first frame shall be ignored. """)
Req('',"""N_Cr time is used for reception of next consecutive frame (CF). N_Cr \
timeout value is 1000msec.""")
Req('',"""The Network layer in the middle of receiving a segmented request \
shall, upon receiving a new interleaved single frame request, abort the \
previous reception and process the new request.""")
Req('',"""The Network layer in the middle of transmitting a segmented response \
shall, upon receiving a new interleaved single frame request, ignore the new \
request.""")
Req('',"""The Network layer shall indicate to the Boot main about the \
reception of a complete message.""")
Req('',"""Separation time (STmin) for programming session shall be maximum \
0msec for both tester and ECU side""")
Req('',"""The transport protocol shall send frame by frame to upper layer for \
diagnostic service TransferData 0x36 (optional for all other services). Note \
that this contradicts and shall override normal specified transport layer \
behaviour since normal transport layer behaviour states that the transport \
layer shall only send complete messages to upper layers.""")

cd("/*/Data link layer requirements")
Inf("""Bootloader shall support both physically and functionally addressed \
requests from the tester. Each ECU shall support a total of four (4) \
addressing types.
* 0x3C address is used for Diagnostic request from the master.
* 0x3D address is used for Diagnostic response from the slave.
* 0x7E for functionally addressed requests.
* 0x7F for slave node address broadcast.""")

Req('',"""BL shall be capable of operating at the nominal bus speeds of \
19.2Kbps.""")
Req('',"""Slave shall not send any response until there shall be a request \
from the master.""")
Req('',"""Each frame transmission time must be within the range of \
TFrame_Nominal and TFrame_Maximum. The LIN frame must support a maximum frame \
transmission time of less than TFrame_Maximum.""")
Req('',"""Each inter-byte space shall be between 0 and 8 bit times. The \
response space will be between 0 and 8 bit times. The total transmission time \
is the sum of the header, response space and the response will be between \
TFrame_Minimum and TFrame_Maximum.""")

cd("/*/Session layer requirements")
Inf("""The session layer is responsible for the creation, management and \
termination of sessions between systems. ISO standard shall be followed to \
reduce cost and make implementation easier. The session layer carries out the \
following tasks:
* Starts and ends a session across a network (on request)
* Allows applications to share information.
* Ensures that information is flowing to the right place.""")

Req('','In BL, the minimum time for P2Server in all sessions shall be 50msec.')
Req('','In BL, the maximum time for P2Server in all sessions shall be 500msec.')
Req('','In BL, the minimum time for P2*Server in all sessions shall be P2msec.')
Req('','In BL, the maximum time for P2*Server in all sessions shall be 2000msec.')
Req('',"""S3Server timeout is the time between functionally addressed \
TesterPresent (0x3E) request messages transmitted by the client to keep a \
diagnostic session. S3Server timeout value shall be 5000msec.""")

cd("/*/LIN transport layer requirements")
Inf("""If there are diagnosable and/or re-programmable LIN slaves on a LIN \
network the LIN master shall support the transport protocol specified in LIN \
Specification Package with the restrictions/additions as defined in this \
document.

The LIN protocol does not have a flow control which the LIN slave can use to \
pause a message reception so the size of the LIN slave message buffer shall \
not limit the size of supported diagnostic services.

The LIN slave Receiver message buffer shall be large enough to handle any \
diagnostic request the LIN slave is required to handle. Note that if possible \
the LIN slave may implement a strategy where earlier received data is freed to \
make room for new data and thus lowering the need for buffer.

The LIN slave shall abort the currently received message if the message is \
faulty in regards LIN   TP. The slave node shall abort processing of a \
transport layer message after:
* Reception of a valid master request (except when NAD is the functional NAD)
* Reception of a master request that is valid concerning the LIN protocol, \
but with absurd data, e.g. wrong PCI (except when NAD is the functional NAD).

Prevent the LIN master from timing out TP messages while the enhanced P2Server \
timer runs. The LIN master shall not time out N_Cr transport protocol timer on \
first frames (FF). However N_Cr timer is still applicable for consecutive \
frames (CF).""")

cd("/*/Transport protocol handling in LIN master requirements")
Inf("""The master node and the diagnostic tester are connected via a back-bone \
bus (e.g. LIN). The master node shall receive all diagnostic requests \
addressed to the slave nodes from the back-bone bus, and gateway them to the \
correct LIN cluster(s). Responses from the slave nodes shall be gatewayed back \
to the back-bone bus through the master node.

All diagnostic requests and responses (services) addressed to the slave nodes \
can be routed in the network layer (i.e. no application layer routing), if the \
Diagnostic and Transport Layer Protocol of tester back-bone-bus master node \
fulfills the respective needs. In this case, the master node must implement \
the LIN transport protocol, see Transport Layer Specification, as well as the \
transport protocols used on the backbone busses (e.g. ISO15765-2 on CAN).""")

cd("/*/Slave node transmission handler requirements")
Inf("""Slave nodes are typically electronic devices that are not involved in a \
complex data communication. LIN diagnostics defines 3 classes of diagnostic \
slave nodes detailing the diagnostic communication and performance. The \
diagnostic data is transported by the LIN protocol as specified in the \
Protocol Specification.

Although diagnostics and node configuration services use the same frame IDs, \
i.e. 0x3C (master request frame) and 0x3D (slave response frame), different \
services are used for configuration and diagnostics. Node configuration can be \
performed by the master node independently while diagnostic services are \
always routed on request from an external or internal test tool. Both \
use-cases use the same node address (NAD) and transport protocol with the \
exception that configuration is always performed via Single Frames. Only slave \
nodes have a NAD.
The NAD is also used as the source address in a diagnostic slave response frame.
Transmission handler is to allow for diagnostic communication without frame \
collisions on the cluster. During diagnostics the broadcast NAD is normally \
not used. If this will happen the slave node will process requests with \
broadcast NAD (0x7F) in the same way as if it is the slave node’s own NAD. \
Note the difference between the broadcast NAD (0x7F) and functional NAD (0x7E).
The following states are defined:

* **Idle**. In this state the slave node is neither receiving nor transmitting \
any messages in the cluster. It is consequently available for any incoming \
request from the master node. It shall not respond to slave response frames.

* **Receive physical request**. In this state the slave node is receiving a \
transmission from the master node. It is receiving and processing the \
transport layer frames as received from the master node. The slave node shall \
ignore any interleaved functional addressed transmission from the master node.

* **Transmit physical response**.
In this state a slave node is currently still processing the previously \
received request, is ready to transmit a physical response or is actually \
transmitting the response to the previously received request. A slave node \
shall not receive nor process interleaved functional addressed (NAD 0x7E) \
transmissions from the master node. Physical transmissions shall be received \
and will make the slave node discard the current request data or response \
data. If the request is addressed to the slave node the request shall be \
received and processed.

* **Receive functional request**. In this state a slave node is receiving a \
functional transmission from the master node. The slave node shall not respond \
to any slave response frames. If more than one LIN slave tries to send a \
diagnostic response simultaneously on the same LIN network there will be \
collisions on the network, and all diagnostic responses will be lost. By \
preventing the LIN slaves from sending diagnostic responses on functional \
requests, there shall not be any collision on the LIN network. LIN slaves \
shall process functionally addressed diagnostic requests, but after the \
request has been processed the LIN slave shall discard the functionally \
addressed diagnostic request without sending any response (regardless state \
of SPRMIB bit).Since the LIN slave shall be available for new diagnostic \
requests directly after functionally addressed diagnostic requests, the \
P2Server_max for functionally addressed diagnostic requests shall be less \
than the time it takes to send a frame on LIN. The LIN master shall consider \
a functionally addressed diagnostic request completed as soon as the LIN \
master have sent the request on LIN i.e. the LIN master shall not poll for a \
diagnostic response (send frame identifier 0x3D) for functionally addressed \
requests.""")

PlantUML("", """
skinparam monochrome true

state "Idle" as idle
state "Receive Physical Request" as phy_req
state "Transmit Physical Response" as response
state "Receive Funcional Request" as func_req

[*] --> idle
idle --> phy_req : (1)

phy_req --> idle : (2)
phy_req --> phy_req : (3)

phy_req --> response : (4)
response --> phy_req : (10)

response --> idle : (5)

idle --> idle : (9)

idle --> func_req : (7)
func_req --> idle : (8)
""", "", {'size': 'fit'})

Inf("""Info

1. **Idle → Receive physical request**

 **Condition:** A master request frame has been received with the NAD matching \
 the slave node's own NAD.

 **Action:** Start receiving and processing the physical request according to \
 the transport layer requirements.

2. **Receive physical request → Idle**

**Condition:** A transport layer error has occurred or a master request frame \
with an NAD different from the slave node's own NAD has been received.

**Action:** Stop receiving and processing the physical request. Do not respond \
to slave response frames.

3. **Receive physical request → Receive physical request**

**Condition:** The physical request has not been completely received yet and \
master request frames are received with the NAD set to the slave node's own \
NAD. A functional addressed master request frame shall be ignored.

**Action:** Continue receiving and processing the physical request.

4. **Receive physical request → Transmit physical response**

**Condition:** The physical request has been completely received.

**Action:** Process the diagnostic request. If a new physical request with the \
NAD set to the slave node's own address is received while processing the \
previous request, the slave node shall discard the current request or response \
data and shall start receiving the new request.

5. **Transmit physical response → Transmit physical response**

**Condition:** The physical response has not been completely transmitted yet. \
A functional addressed request shall be ignored.

**Action:** Keep responding to slave response frames according to the \
transport layer requirements.

Note: A slave node will not process a functional addressed request while in \
transmit physical response state. Therefore it must be ensured by the external \
test tool that functionally addressed requests that shall be processed by all \
slave nodes are only transmitted if no further responses from any slave node \
are expected. Otherwise there's no guarantee nor indication for the external \
test tool whether a slave node has processed the functional request.

6. **Transmit physical response → Idle**

**Condition:** The physical response has been completely transmitted, a LIN \
transport layer error occurred or a request with the NAD set to a different \
or the same value as the slave node's own NAD has been received.

**Action:** Discard the request and response data. Stop responding to slave \
response frames.

7. **Idle → Receive functional request**

**Condition:** A master request frame with the NAD parameter set to the \
functional NAD has been received.

**Action:** Receive and process the master request frame according to the \
transport layer. Do not respond to the slave response frame headers.

8. **Receive functional request → Idle**

**Condition:** The functional request was processed.

**Action:** Discard any response data. Stop responding to slave response frames.

9. **Receive functional request → Idle**

 **Condition:** No request is received and no response is pending.

 **Action:** Do not respond to any slave response frames.

10. **Transmit physical response → Receive physical request**

**Condition:** The previous request has been processed and a diagnostic \
master request frame with the NAD parameter set to the slave node's own \
node address has been received.

**Action:** Discard the response data. Start receiving and processing the \
physical request according to the LIN transport protocol requirements.
""")

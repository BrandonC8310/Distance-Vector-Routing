import pickle
import socket
import sys
import threading
import time
from decimal import Decimal

NUMBER_NODES = 10
NODES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
PORT = {
    'A': 6000,
    'B': 6001,
    'C': 6002,
    'D': 6003,
    'E': 6004,
    'F': 6005,
    'G': 6006,
    'H': 6007,
    'I': 6008,
    'J': 6009,
}


def printdict(rt):
    print(
        "\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    print("Current node: {} | SEQ = {}".format(nodeId, sending.seq))
    print(
        "Usage: The table below shows the next hop and least cost on the shortest path from current node to the target node",
        end="")
    print(" i.e. <nextHop>-<leastCost>\n")
    N = [nodeId]
    for ii in NODES:
        N.append(ii)
    print("From \\ To     ", end="")
    for i in N:
        print("{:<13}".format(i), end="")
    print()
    for n in N:
        print("{}         |".format(n), end="")
        for nn in N:
            val1 = rt[n][nn]
            print(" {}-{:<8} |".format(val1[0], val1[1]), end="")
        print(' SEQ = ', rt[n]['SEQ'])
    print(
        "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")


class Packet:
    def __init__(self, pType: bool, data, nodeID, lc):  # True --> DV. False --> link cost change
        self.pType = pType
        self.data = data
        self.nodeID = nodeID
        self.lc = lc
        self.seq = sending.seq


# Thread for the interface -- reading user's inputs and response
class Interface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def printUsage(self):
        print("\nUsage: ")
        print(
            "      link-cost {}                          | display the link-cost between Node {} and its neighbours".format(
                nodeId, nodeId))
        print(
            "      routing-table {}                     | display the routing table stored in Node {} at the moment".format(
                nodeId, nodeId))
        print(
            "      shortest-path {}                      | display the shortest path of Node {} to every other reachable nodes".format(
                nodeId, nodeId))
        print(
            "      modify {} <neighbour Node ID> <value> | modify the link-cost of edge ({}, <Node ID>) to <value>".format(
                nodeId, nodeId))
        print("      disable  {}                           | cause node failure of Node {}".format(nodeId, nodeId))
        print("      usage                                | display the usage")

    def changeLinkCost(self, v, w):
        neighbourCosts[v] = w
        f = open("{}config.txt".format(nodeId), "w")
        f.write(str(len(neighbourCosts.keys())))
        f.write("\n")
        for i in neighbourCosts.keys():
            f.write("{} {} {}\n".format(i, neighbourCosts[i], PORT[i]))
        f.close()
        sending.lc = [v, w]

        for n in NODES:
            minimumCost = Decimal("Infinity")
            nextHop = ' '
            for neighbour, cost in neighbourCosts.items():
                newCost = cost + routingTable[neighbour][n][1]
                if minimumCost > newCost:
                    minimumCost = newCost
                    nextHop = neighbour
            if not (nextHop == routingTable[nodeId][n][0] and minimumCost == routingTable[nodeId][n][1]):
                routingTable[nodeId][n][1] = minimumCost
                routingTable[nodeId][n][0] = nextHop
                receiving.shouldPrint = True
                sending.hasChanged = True

    def disable(self):
        sending.disable = True
        sending.lc = nodeId
        return

    def run(self) -> None:
        self.userInput()

    def userInput(self):
        print("Welcome to the console of Node {}".format(nodeId))
        self.printUsage()
        while True:
            a = input()
            if a == "yes":
                printdict(routingTable)
            elif a == "sp":
                printShortestPath()
            elif a == "link-cost {}".format(nodeId):
                print("-------------")
                for i in neighbourCosts:
                    print("Link-cost of edge ({}, {}) is {}".format(nodeId, i, neighbourCosts[i]))
                print("-------------")
            elif a == "routing-table {}".format(nodeId):
                printdict(routingTable)
            elif a == "shortest-path {}".format(nodeId):
                printShortestPath()
            else:
                ls = a.split(" ")
                if ls[0] == 'modify':
                    self.changeLinkCost(ls[2], Decimal(ls[3]))
                    sending.linkCostChange = True
                elif ls[0] == "disable":
                    self.disable()
                else:
                    self.printUsage()


# Thread for sending updates to its neighbours every 10 seconds
class Sending(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.timer = None
        self.hasChanged = False
        self.linkCostChange = False
        self.disable = False
        self.lc = []
        self.stop = False
        self.neighbourDisable = False
        self.seq = 0

    def run(self):
        # Using a timer -- callback itself after 10 s
        self.timer = threading.Timer(10, self.run)
        self.timer.start()
        self.send()

    def send(self):
        IP = '127.0.0.1'
        # Create a UDP socket
        socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ord(nodeId))

        if self.disable:
            packet = Packet(False, routingTable, nodeId, self.lc)
            # stop the timer when the current node is failed --> so it won't send updates anymore
            # It turns out we cant stop the timer, because UDP cannot guarantee that the packet will be received
            # by the server （neighbour nodes) hence, we need to keep sending this message.
            # However, since the sequence number of the current node will not increase, the neighbours will only receive
            # this packet once.s
            # self.timer.cancel()
            print("one last send")
        elif self.neighbourDisable:
            self.neighbourDisable = False
            packet = Packet(False, routingTable, nodeId, self.lc)
        else:
            if self.hasChanged:
                routingTable[nodeId]['SEQ'] = routingTable[nodeId]['SEQ'] + 1
                self.hasChanged = False
            if self.linkCostChange:
                packet = Packet(True, routingTable, nodeId, self.lc)
            else:
                packet = Packet(True, routingTable, nodeId, None)
        # print("sending...")
        for neighbour, port in neighbourPorts.items():
            addr = (IP, port)
            socketClient.sendto(pickle.dumps(packet), addr)


# Thread for receiving updates from its neighbours and update its routing table
class Receiving(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.shouldPrint = False
        self.socketServer = None
        self.dataReceive = None
        self.adr = None
        self.data = None
        self.routingTable = None
        self.directionTable = None
        self.w = None

    # restart routing algorithm to eliminate the failed node from the network
    def handleDisableAndRestart(self, failNode):
        sending.seq += 1
        NODES.remove(failNode)
        NODES.append(nodeId)
        global routingTable
        routingTable = {}
        for node in NODES:
            routingTable[node] = {}
            routingTable[node]['SEQ'] = 0
            for node_ in NODES:
                routingTable[node][node_] = [' ', Decimal('Infinity')]
        NODES.remove(nodeId)

        global neighbourPorts
        global neighbourCosts
        if failNode in neighbourCosts.keys():
            del neighbourPorts[failNode]
            del neighbourCosts[failNode]

            # if you want to modify config files for a node failure
            # f = open("{}config.txt".format(nodeId), "w")
            # f.write(str(len(neighbourCosts.keys())))
            # f.write("\n")
            # for i in neighbourCosts.keys():
            #     f.write("{} {} {}\n".format(i, neighbourCosts[i], PORT[i]))
            # f.close()

        routingTable[nodeId][nodeId] = [nodeId, 0]
        for i in neighbourCosts.keys():
            routingTable[nodeId][i] = [i, neighbourCosts[i]]
        routingTable[nodeId]['SEQ'] = 1
        sending.neighbourDisable = True
        sending.lc = failNode
        receiving.shouldPrint = True

    def run(self):
        # Receive the client packet along with the address it is coming from
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ord(nodeId))
        self.socketServer.bind(('', self.port))
        while True:
            self.dataReceive, self.adr = self.socketServer.recvfrom(4096)
            packet = pickle.loads(self.dataReceive)  # .decode('utf-8')
            self.routingTable = packet.data
            self.w = packet.nodeID
            newSeq = packet.seq
            if not packet.pType:
                # disable message
                failNode = packet.lc
                if failNode in NODES:
                    # first time receiving this msg
                    print("Received a disable message, Node {} is disable".format(failNode))
                    print("Restarting...")
                    print("Please wait for the network to re-converge...")
                    self.handleDisableAndRestart(failNode)
            else:
                if packet.lc is not None:
                    if nodeId == packet.lc[0]:
                        interface.changeLinkCost(self.w, packet.lc[1])
                        continue
            if sending.seq != newSeq:
                continue
            if self.routingTable != routingTable:
                mutex.acquire()
                try:
                    for n in NODES:
                        minimumCost = Decimal("Infinity")
                        nextHop = " "
                        for neighbour, cost in neighbourCosts.items():
                            if neighbour == self.w:
                                newCost = cost + self.routingTable[neighbour][n][1]
                            else:
                                newCost = cost + routingTable[neighbour][n][1]
                            if minimumCost > newCost:
                                minimumCost = newCost
                                nextHop = neighbour
                        if not (nextHop == routingTable[nodeId][n][0] and minimumCost == routingTable[nodeId][n][1]):
                            routingTable[nodeId][n][1] = minimumCost
                            routingTable[nodeId][n][0] = nextHop
                            receiving.shouldPrint = True
                            sending.hasChanged = True

                        if routingTable[n]['SEQ'] < self.routingTable[n]['SEQ']:
                            routingTable[n] = self.routingTable[n]

                finally:
                    mutex.release()


class OnChange(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = []

    def run(self):
        time.sleep(60)
        while True:
            if receiving.shouldPrint:
                mutex.acquire()
                try:
                    printShortestPath()
                finally:
                    mutex.release()
                    receiving.shouldPrint = False


def printShortestPath():
    print()
    print("I am Node ", nodeId)
    for i in NODES:
        result = findShortestPath(nodeId, i)
        if routingTable[nodeId][i][1] == Decimal('Infinity') or result == -2:
            print("Node {} is unreachable".format(i))
            continue
        if result == -1:
            # routing loop
            print(
                "Encounter a routing loop from {} to {}, current link cost is {}, note that this result is not accurate, please wait...".format(
                    nodeId, i, routingTable[nodeId][i][1]))

        else:
            path = "".join(result)
            print(
                "Least cost path from {} to {}: {}, link cost: {}".format(nodeId, i, path, routingTable[nodeId][i][1]))


def findShortestPath(source, target):
    path = [source]
    routingLoop = False
    counter = 0
    try:
        while True:
            if counter >= 10 or routingTable[routingTable[source][target][0]][target][0] == source:
                routingLoop = True
                break
            if routingTable[source][target][0] == target:
                path.append(target)
                break
            path.append(routingTable[source][target][0])
            source = routingTable[source][target][0]
            counter += 1
    except KeyError as e:
        return -2
    if routingLoop:
        return -1
    return path


# initialising
routingTable = {}  # directionTable[Node1][Node2] --> [next hop from Node1 to Node2 in the shortest path, min_cost]
for node in NODES:
    routingTable[node] = {}
    routingTable[node]['SEQ'] = 0
    for node_ in NODES:
        routingTable[node][node_] = [' ', Decimal('Infinity')]

neighbourPorts = {}
neighbourCosts = {}

# read command line arguments
nodeId = sys.argv[1]
NODES.remove(nodeId)
routingTable[nodeId][nodeId] = [nodeId, 0]
portNo = int(sys.argv[2])
configFile = open(sys.argv[3])
neighbourNum = int(configFile.readline().strip())
for i in range(neighbourNum):
    line = configFile.readline().split()
    cost = Decimal(line[1])
    portNum = int(line[2])
    neighbourPorts[line[0]] = portNum
    neighbourCosts[line[0]] = cost
    routingTable[nodeId][line[0]] = [line[0], cost]
routingTable[nodeId]['SEQ'] = 1
configFile.close()

mutex = threading.Lock()

sending = Sending()
sending.start()

receiving = Receiving(portNo)
receiving.start()

onChange = OnChange()
onChange.start()

interface = Interface()
interface.start()

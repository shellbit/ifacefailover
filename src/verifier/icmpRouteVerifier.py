import random, socket, struct, sys


class IcmpPacket:
    def __init__(self, typeId, code, identifier, sequenceNumber, payload):
        self.typeId = typeId
        self.code = code
        self.identifier = identifier
        self.sequenceNumber = sequenceNumber
        self.payload = payload
    
    def __str__(self):
        return str(self.__dict__)
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class IcmpRouteVerifier:
    ICMP_HEADER_FORAMT = 'bbHHh'
    ICMP_PAYLOAD = ' !"#$%&\'()*+,-./01234567'
    ICMP_REQUEST_TYPE = 8
    ICMP_REQUEST_CODE = 0
    ICMP_REQUEST_SEQUENCE_NUMBER = 1
    ICMP_RESPONSE_TYPE = 0
    ICMP_RESPONSE_CODE = 0
    ICMP_RESPONSE_SEQUENCE_NUMBER = 1
    
    def __str__(self):
        return str(self.__dict__)
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def isRouteAvailable(self, destination, **kwargs):
        timeout = kwargs.get('timeout', 1)
        maxRetry = kwargs.get('maxRetry', 2)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.settimeout(timeout)
        packetId = random.randint(0, sys.maxint) & 0xFFFF
        request = self.createIcmpRequestPacket(packetId)
        attempt = 0
        icmpPacketResponse = None
        while attempt < maxRetry and icmpPacketResponse is None:
            attempt = attempt + 1
            icmpPacketResponse = self.sendAndReceive(s, destination, request)
        s.close()
        if icmpPacketResponse is None:
            return False
        return IcmpPacket(self.ICMP_RESPONSE_TYPE, self.ICMP_RESPONSE_CODE, packetId, self.ICMP_RESPONSE_SEQUENCE_NUMBER, self.ICMP_PAYLOAD) == icmpPacketResponse
    
    def createIcmpRequestPacket(self, packetId):
        packetHeader = struct.pack(self.ICMP_HEADER_FORAMT, self.ICMP_REQUEST_TYPE, self.ICMP_REQUEST_CODE, 0, packetId, self.ICMP_REQUEST_SEQUENCE_NUMBER)
        packetChecksum = self.calculateChecksum(packetHeader + self.ICMP_PAYLOAD)
        return packetHeader[:2] + packetChecksum + packetHeader[4:] + self.ICMP_PAYLOAD
    
    def calculateChecksum(self, msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
            s = self.carryOutAdd(s, w)
        return struct.pack('H', ~s & 0xffff)
    
    def carryOutAdd(self, a, b):
        c = a + b
        return (c & 0xffff) + (c >> 16)
    
    def sendAndReceive(self, s, destination, request):
        while request:
            sent = s.sendto(request, (destination, 1))
            request = request[sent:]
        try:
            response = s.recv(1024)
            return self.parseResponse(response)
        except socket.timeout:
            return None
    
    def parseResponse(self, response):
        header = response[20:28]
        payload = response[28:]
        typeId, code, checksum, identifier, sequenceNumber = struct.unpack(self.ICMP_HEADER_FORAMT, header)
        return IcmpPacket(typeId, code, identifier, sequenceNumber, payload)

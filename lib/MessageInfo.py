from Segment import Segment

class MessageInfo:
    def __init__(self):
        self.ip = None
        self.port = None
        self.segment = Segment()
        
    # Getters
    def getIP(self):
        return self.ip
    
    def getPort(self):
        return self.port
    
    def getSegment(self):
        return self.segment
    
    # Setters
    def setIP(self, ip):
        self.ip = ip
        
    def setPort(self, port):
        self.port = port
        
    def setSegment(self, segment):
        self.segment = segment
    
    def __str__(self):
        return "IP: " + str(self.ip) + ", Port: " + str(self.port) + ", Segment: " + str(self.segment)
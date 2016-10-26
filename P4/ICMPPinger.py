## ICMP Pinger


import socket #changed to work with method calls
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

#For the extra exercises
packetsSent = 0
packetsReceived = 0
minRTT = 100000
maxRTT = 0
totalRTT = 0

def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = ord(str[count+1]) * 256 + ord(str[count])
        csum = csum + thisVal
        csum = csum & 0xffffffffL
        count = count + 2
    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffffL

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            # return "Request timed out."
            #for extra Q#2
            
            size=struct.calcsize("d")
            print ("Reply is " + str(size) + " bytes")
            
            return "Error 0: Destination Network Unreachable"
        timeReceived = time.time()
        
        recPacket, addr = mySocket.recvfrom(1024)

        #Fill in start
        global packetsReceived
        packetsReceived = packetsReceived + 1
        
        #Fetch the ICMP header from the IP packet
        icmpHeader = recPacket[20:28] #8 bytes, starts at 20 bc 0-19 are IC header.
        #get header

        type, code, checksum, packetID, sequence = struct.unpack("bbHHh",icmpHeader)
        
        #check if ID is the one we want.
        if packetID == ID:
            #update time
            packetSize = struct.calcsize("d")
            timeNow = struct.unpack("d", recPacket[28:28 + packetSize])[0]
            rtt = timeReceived - timeNow
            print "RTT: " + str(rtt)
            return rtt
            
        #Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            #            return "Request timed out."
            # for extra Q#2
            return "Error 1: Destination Host Unreachable."

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
    #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")

    #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.org/papers/sock_raw
    #Fill in start
    #Create Socket here

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    mySocket.bind(("",0))
    
    #Fill in end
    myID = os.getpid() & 0xFFFF  #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    global packetsSent
    packetsSent = packetsSent + 1
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def ping(host, timeout=1):
    #timeout=1 means: If one second goes by without a reply from the server,
    #the client assumes that either the client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    print ""
    print "Pinging " + dest + " using Python:"
    #Send ping requests to a server separated by approximately one second
    while 1 :
        delay = doOnePing(dest, timeout)
        
        global totalRTT
        global minRTT
        global maxRTT
        if (isinstance(delay, float)):
            if (delay < minRTT):
                minRTT = delay
            elif (delay > maxRTT):
                maxRTT = delay
            totalRTT = totalRTT + delay
        
        print delay
        time.sleep(1)# one second
        return delay

#ping("127.0.0.1")
#ping("www.google.com")
#host = "www.poly.edu"
host = "127.0.0.1"
#host = "8.8.8.8" #North America
#host = "google.com"

#host = "1.201.102.5" #Asia

#host = "27.124.122.70" #Australian

#host = "86.65.197.135" #EU


for i in range(0, 10):
    ping(host)

print("Report for " + host)
print ("Packets: Sent = "+str(packetsSent))
print ("Packets: Received = "+str(packetsReceived))
print ("Packets: lost =" +str(packetsSent-packetsReceived))
if((packetsSent-packetsReceived)>=0):
    print ("Packets: lost% = "+str(((packetsSent-packetsReceived)/packetsSent)*100))
else:
    print ("Packets: lost% = "+str(0))

print ("Minimum RTT: " + str(minRTT)+" ms")
print("Maximum RTT: " +str(maxRTT)+" ms")
if packetsReceived != 0:
    print("Average RTT: " +str(totalRTT/packetsReceived)+" ms")
else:
    print("Average RTT: 0 ms")







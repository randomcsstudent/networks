# UDPPingerClient.py

from socket import *
import time

def main():
    serverName = 'localhost'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM) #Not SOCK_STREAM anymore

    #Don't need socket.connect anymore, that's TCP
    print 'Begin pinging'

    totalPings = 10
    counter = 0
    
    #variables for additional exercises
    minRTT = 100
    maxRTT = -1
    aveRTT = 0
    packetLossCount = 0
    
#    allTimes = [ for i in range(10)]

    while counter < totalPings:
        message = 'Ping ' + str(counter+1)

        startTime = time.time() #current time for start
        clientSocket.settimeout(1) #time out after 1 second
        clientSocket.sendto(message,(serverName, serverPort)) #
        
        try:
            response = clientSocket.recv(1024) #recv returns string representing data received.
            endTime = time.time()
            totalTime = endTime - startTime
            #Print response message in format:
                #Ping sequence_number time
            print response + ' ' + str(totalTime)
            
            #for additional exercises
            if (totalTime > 0):
                aveRTT += totalTime
            if minRTT > totalTime:
                minRTT = totalTime
            
            if maxRTT < totalTime:
                maxRTT = totalTime
        
        except timeout:
            packetLossCount += 1
            print 'PING ' + str(counter+1)
            print 'Request timed out.'
        

        counter += 1
    
        if counter > 10:
            print 'Closing socket connection'
            clientSocket.close()

    print 'Additional Exercises:'
    print 'Minimum RTT: ' + str(minRTT)
    print 'Maximum RTT: ' + str(maxRTT)
    print 'Average RTT: ' + str(float(aveRTT / (totalPings-packetLossCount)))
    print 'Packet Loss Rate: ' + str(float(packetLossCount / 10.0) * 100.0) + '%'

    print 'Closing socket connection'
    clientSocket.close()

if __name__ == '__main__':
    main()



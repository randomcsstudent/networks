

from socket import *
import sys

if len(sys.argv) <= 1:
    print 'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server'
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpPort = 8888
tcpSerSock.bind(('', tcpPort))
tcpSerSock.listen(5) #max # of queue connections
# Fill in end.

while 1:
    # Start receiving data from the client
    print 'Ready to serve...'
    tcpCliSock, addr = tcpSerSock.accept()
    print 'Received a connection from:', addr
    # Fill in start.
    message = tcpCliSock.recv(1024)
    # Fill in end.
    print "message:", message
    # Extract the filename from the given message
    # print message.split()[1]
    filename = message.split()[1].partition("/")[2]
#    print "Filename: ",filename
    fileExist = "false"
    filetouse = "/" + filename
#    print "filetouse " + filetouse
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
#        print "outputdata: ", outputdata
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        # Fill in start.
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])
        # Fill in end
        print 'Read from cache'
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            # Fill in start.
            print "Creating new socket on proxy server"
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in end.
            hostn = filename.replace("www.","",1)
            print "hostn " + hostn
            try:
                # Connect to the socket to port 80
                # Fill in start.
                cSocketPort = 80
                c.connect((hostn, cSocketPort)) #connect, not bind
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n") ##
                # Read the response into buffer
                # Fill in start.
                buffer = fileobj.readlines()
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                
                # Fill in start.
                for i in range(0, len(buffer)):
                    tmpFile.write(buffer[i])
                    tcpCliSock.send(buffer[i])
        
                tmpFile.close()
                # Fill in end.
                print 'Saved into cache'
            
            except:
                print "Illegal Request"
        else:
                # HTTP response message for file not found
                print "File Not Found"
                # Fill in start.
                tcpCliSock.send("HTTP/1.0 404 Not Found\r\n")
                # Fill in end.
    # Close the client and the server sockets
    tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.









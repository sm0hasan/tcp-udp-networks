from socket import *
import re
import time
from datetime import datetime
serverIP="127.0.0.1"
serverPort = 10000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

def get_current_date():
    now = datetime.now()
    return now.strftime('%a, %d %b %Y %H:%M:%S GMT')

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Received Connection")
   
    requestData = connectionSocket.recv(2048).decode()

    # Split the request into lines
    requestLines = requestData.split('\r\n')
    
    # Get the HTTP method and request path from the first line
    if requestLines:
        firstLine = requestLines[0]
        #use this regex function to get the data we need
        match = re.match(r'(\w+) (.+) HTTP/1\.1', firstLine)
        if match:
            httpMethod, requestPath = match.groups()
        else:
            httpMethod, requestPath = None, None
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    
            connectionSocket.send(response.encode())
            connectionSocket.close()
            continue
            
    
    # Get the header and values for each line
    requestHeaders = {}
    for line in requestLines[1:]:
        parts = line.split(': ')
        if len(parts) == 2:
            headerName, headerValue = parts
            requestHeaders[headerName] = headerValue

    #try to open file at directory specified in request.  If not found, return a 404 error
    try:
        htmlFile = open(requestPath[1:], 'r')
    except:
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
    
        connectionSocket.send(response.encode())
        connectionSocket.close()
        continue
    responseBody = htmlFile.read()

    #setup the response headers
    responseHeaders = [
        'HTTP/1.1 200 OK',
        'Content-Type: text/html',
        'Connection: keep-alive',
        'Date: ' + get_current_date(),
        'Server: TheBestServerInTheClass',
        'Last-Modified: ' + 'Mon, 06 Nov 2023 14:13:34 GMT',
        'Content-Length: ' + str(len(responseBody))
    ]

    #Setup the response based on type of request
    if(httpMethod == 'GET'):
        response = '\r\n'.join(responseHeaders) + "\r\n\r\n" + responseBody
    elif(httpMethod == 'HEAD'):
        response = '\r\n'.join(responseHeaders) + "\r\n\r\n"
    else:
        response = 'HTTP/1.1 405 Method Not Allowed \r\n\r\n'
    
    #send response
    connectionSocket.send(response.encode())
    connectionSocket.close()


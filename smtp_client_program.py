from socket import *
import ssl
import base64
def main():
    msg='I love networking\r\n'
    endmsg='\r\n.\r\n'
    # Choose a mail server (e.g. Google or Yahoo mail server) and call it mailserver
    mailserver = "smtp.mail.yahoo.com"     #I've used yahoo mail server as sender
    port = 465
    username = 'sender@yahoo.com'
    f=open('passFile.txt','r')        #password is read from a text file
    password=f.readline()
    print "password",password
    f.close()

    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    client_ssl_socket = ssl.wrap_socket(clientSocket)
    client_ssl_socket.connect((mailserver, port))

    recvn = client_ssl_socket.recv(1024)
    print "connection msg from server:",recvn
    #Check if server responds properly
    if recvn[:3] != '220':
        print '220 reply not received from server.'

    # Send HELO command and print server response.
    heeloCommand = 'HELO server\r\n'
    client_ssl_socket.send(heeloCommand)
    recvn = client_ssl_socket.recv(1024)
    print "Hello reply:",recvn
    # Check is server responds properly i.e.250
    if recvn[:3] != '250':
        print '250 reply not received from server.'

    authCommand = 'AUTH LOGIN \r\n'
    client_ssl_socket.send(authCommand)
    client_ssl_socket.send(base64.b64encode('sender') + '\r\n')   #username is sent as a base64 encoded string
    client_ssl_socket.send(base64.b64encode(password) + '\r\n')          #password is sent as a base64 encoded string

    # Send MAIL FROM command and print server response.
    mailFromCommand = 'MAIL From: <sender@yahoo.com>\r\n'
    client_ssl_socket.send(mailFromCommand)
    recvn = client_ssl_socket.recv(1024)
    print "Mail From reply:",recvn
    # Check is server responds properly i.e.250
    if recvn[:3] != '250':
        print '250 reply not received from server.'

    # Send RCPT TO command and print server response.
    rcptToCommand = 'RCPT To: <reciever@yahoo.com>\r\n'
    client_ssl_socket.send(rcptToCommand)
    recvn = client_ssl_socket.recv(1024)
    print "Mail To reply:",recvn
    # Check is server responds properly i.e.250
    if recvn[:3] != '250':
        print '250 reply not received from server.'


    # Send DATA command and print server response.
    dataCommand = 'DATA\r\n'
    client_ssl_socket.send(dataCommand)
    recvn = client_ssl_socket.recv(1024)
    print "Data is " + dataCommand
    print "DATA command reply:",recvn

    # Send message data.
    client_ssl_socket.send(msg)

    # Message ends with a single period.
    client_ssl_socket.send(endmsg)

    # Send QUIT command and get server response.
    quitCommand = 'QUIT\r\n'
    client_ssl_socket.send(quitCommand)
    recvn = client_ssl_socket.recv(1024)
    print "QUIT command reply:",recvn

if __name__ == '__main__':
    main()

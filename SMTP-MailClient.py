from socket import *
import ssl
import base64

# ------------------------- SMTP Commands -------------------------------
END_MSG = "\r\n.\r\n"
FORMAT = 'ascii'
QUIT_CMD = 'QUIT\r\n'
HELLO_CMD = 'HELO gmail.com\r\n'
STARTTLS_CMD = 'STARTTLS\r\n'
AUTHORIZATION_CMD = "AUTH LOGIN\r\n"
MAIL_FROM = 'MAIL FROM: <Sender@gmail.com> \r\n'
RCPT_TO = 'RCPT TO: <Receiver@gmail.com> \r\n'
DATA_CMD = 'DATA\r\n'
# ------------------------------------------------------------------------

login_username = 'Example@gmail.com'    # your gmail username (sender gmail.)
login_password = 'blablabla'            # your gmail password
# ------------------------------------------------------------------------

# tuple = server hostname , connection port from server.
mailserver1 = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver1)

recv = clientSocket.recv(1024).decode(FORMAT)

print("\nServer message after connection request: " + recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# ----Send HELO command and print server response.

clientSocket.send(HELLO_CMD.encode())
recv1 = clientSocket.recv(1024).decode(FORMAT)
print('Server response after HELO: ' + recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# ----start TLS
clientSocket.send(STARTTLS_CMD.encode())
recv = clientSocket.recv(1024).decode(FORMAT)
print('Server response after STARTTLS: ' + recv)

if recv[:3] != '220':
    print("220 reply not received from server.")

# ----Secure socket with ssl
sslClientSocket = ssl.wrap_socket(clientSocket)

# ----user authentication part
sslClientSocket.send(AUTHORIZATION_CMD.encode())
recv = sslClientSocket.recv(1024).decode(FORMAT)
print('Server response after AUTH LOGIN: ' + recv)

if recv[:3] != '334':
    print("334 Not received from the server")

# ----sending username for authorization

sslClientSocket.send(
    (base64.b64encode(login_username.encode())) + '\r\n'.encode())
recv = sslClientSocket.recv(1024).decode(FORMAT)
print('Server response after sending username: ' + recv)

# ----sending username for authorization
sslClientSocket.send(
    (base64.b64encode(login_password.encode())) + '\r\n'.encode())
recv = sslClientSocket.recv(1024).decode(FORMAT)
print('Server response after sending password: ' + recv)

if recv[:3] != '235':
    print("235 Not received from the server")


sslClientSocket.send(MAIL_FROM.encode())
recv2 = sslClientSocket.recv(1024).decode(FORMAT)
print("Server response After MAIL FROM command: "+recv2)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# ----Send RCPT TO command and print server response.

sslClientSocket.send(RCPT_TO.encode())
recv3 = sslClientSocket.recv(1024).decode()
print("Server response After RCPT TO command: "+recv3)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# ----Send DATA command and print server response.

sslClientSocket.send(DATA_CMD.encode())
recv4 = sslClientSocket.recv(1024).decode(FORMAT)
print("Server response After DATA command: " + recv4)

if recv4[:3] != '354':
    print('354 reply not received from server.')

# ----Send message data.
subject = "Subject: SMTP mail client testing \r\n\r\n"
sslClientSocket.send(subject.encode())
message = input("\nEnter your message: ")
message = (str(message) + '\r\n').encode()

sslClientSocket.send(message)
sslClientSocket.send(END_MSG.encode())
recv_msg = sslClientSocket.recv(1024)

print("\nServer response after sending message body: " + recv_msg.decode())

if recv1[:3] != '250':
    print('250 reply not received from server.')

# ----Send QUIT command and get server response.
sslClientSocket.send(QUIT_CMD.encode())
message = sslClientSocket.recv(1024)
print('Server response after QUIT: ' + message.decode())

if message[:9] != '221 2.0.0':
    print('221 2.0.0 Not received from the server')

sslClientSocket.close()
print('Email sent successfully :)')

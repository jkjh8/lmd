#!/usr/bin/env python3

import sys, os, socket, platform, time
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide2.QtCore import Qt, Slot, Signal, QThread

class Main(QMainWindow):
    send = Signal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Window')
        self.setGeometry(200,300,500,500)
        self.TcpClient = TcpClient(('127.0.0.1', 10000))
        self.TcpClient.start()

        self.btn = QPushButton('btn1', self)
        self.send.connect(self.TcpClient.send)
        self.btn.clicked.connect(self.click)
        self.show()

    def click(self):
        self.send.emit()

class TcpClient(QThread):
    def __init__(self, addr, parent = None):
        super(TcpClient, self).__init__(parent)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.port = 10000

    def run(self):
        try:
            self.connect()
        except Exception as e:
            print('error', e)
            self.reconnect()
    
    @Slot()
    def send(self):
        try:
            self.socket.send('hello'.encode())
        except Exception as e:
            print('error', e)
            self.reconnect()
            self.socket.send('hello'.encode())

    def connect(self):
        print(self.addr)
        self.socket.connect(self.addr)

    def reconnect(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1)
        self.run()
            

            


# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 65432        # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))

if __name__ == "__main__":
    osPlatform = platform.system()
    print('현제 운영 시스템은 {} 입니다.'.format(osPlatform))
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
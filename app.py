#!/usr/bin/env python3

import sys
import socket
import platform
import time
import sounddevice as sd
import soundfile as sf
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QComboBox
from PySide2.QtCore import Qt, Slot, Signal, QThread


class Main(QMainWindow):
    send = Signal()
    play = Signal(str, int)
    stop = Signal()
    get = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Window')
        self.setGeometry(200, 300, 400, 200)
        # self.TcpClient = TcpClient(('127.0.0.1', 10000))

        # self.TcpClient.start()

        self.qb = QComboBox(self)
        self.qb.resize(250, 28)
        self.qb.move(10, 11)
        self.btnGet = QPushButton('Get', self)
        self.btnGet.move(260, 10)

        self.btnOpen = QPushButton('Open', self)
        self.btnOpen.move(10, 50)
        self.btnPlay = QPushButton('Play', self)
        self.btnPlay.move(110, 50)
        self.btnStop = QPushButton('Stop', self)
        self.btnStop.move(210, 50)

        self.Player = Player()
        self.play.connect(self.Player.play)
        self.stop.connect(self.Player.stop)
        self.btnOpen.clicked.connect(self.showDialog)
        self.btnPlay.clicked.connect(self.playFile)
        self.btnStop.clicked.connect(self.Player.stop)
        self.btnGet.clicked.connect(self.Player.get_devices)

        self.Player.audio_devices.connect(self.updateDevices)
        self.qb.currentIndexChanged.connect(self.changeDevice)
        self.Player.start()
        self.deviceNum = 0
        self.show()

    def showDialog(self):
        self.file = QFileDialog.getOpenFileName(self, 'Open file', './')
        print(self.file[0])

    def changeDevice(self):
        self.deviceNum = self.qb.currentIndex()

    @Slot(list)
    def updateDevices(self, devices):
        print(devices)
        self.qb.clear()
        self.qb.addItems(devices)

    def click(self):
        self.send.emit()

    def playFile(self):
        print('play')
        if self.file:
            self.play.emit(self.file[0], self.deviceNum)


class Player(QThread):
    audio_devices = Signal(list)

    def __init__(self, parent=None):
        super(Player, self).__init__(parent)

    @Slot()
    def get_devices(self):
        self.deviceList = sd.query_devices()
        self.devices = []
        if self.deviceList:
            for device in self.deviceList:
                self.devices.append(device['name'])
        self.audio_devices.emit(self.devices)

    @Slot(str, int)
    def play(self, file, device):
        print(file)
        asio_out = sd.AsioSettings(channel_selectors=[0, 1])
        self.data, self.fs = sf.read(file, dtype='float32')
        sd.play(self.data, self.fs, device=device, extra_settings=asio_out)

    @Slot()
    def stop(self):
        sd.stop()


# class TcpClient(QThread):
#     def __init__(self, addr, parent=None):
#         super(TcpClient, self).__init__(parent)
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.addr = addr
#         self.port = 10000

#     def run(self):
#         try:
#             self.connect()
#         except Exception as e:
#             print('error', e)
#             self.reconnect()

#     @Slot()
#     def send(self):
#         try:
#             self.socket.send('hello'.encode())
#         except Exception as e:
#             print('error', e)
#             self.reconnect()
#             self.socket.send('hello'.encode())

#     def connect(self):
#         print(self.addr)
#         self.socket.connect(self.addr)

#     def reconnect(self):
#         self.socket.close()
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         time.sleep(1)
#         self.run()


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

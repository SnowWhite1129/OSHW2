import os
import cv2
import socket
import numpy as np
from upload import DataProcessor
from detect_opencv import Image


class Client:
    def __init__(self, num, sock):
        self.num = num
        self.sock = sock
        self.fileno = "0" + str(num)

    def recvData(self, count):
        buf = b''
        while count:
            newbuf = self.sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def writeFile(self, frame):
        f = open(self.fileno + "tmp.txt", "w")
        f.close()
        f = open(self.fileno + ".txt", "a")
        for frame_no in frame:
            f.write(str(frame_no) + '\n')
        f.close()

    def LicencePlateDetector(self):
        DP = DataProcessor()
        DP.InitImgDir()
        fileLength = 6
        cvNet = cv2.dnn.readNetFromCaffe("tmp/mssd512_voc.prototxt", "tmp/mssd512_voc.caffemodel")

        with self.sock:
            filename = self.sock.recv(fileLength).decode()  # Demo will always be 6 bytes
            resolution = (1280, 720)
            print("File name: ", filename)
            frameCount = 0
            frameList = []
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video = cv2.VideoWriter(self.fileno + "tmp.mp4", fourcc, 60, resolution)
            while True:
                length = self.sock.recv(16)
                if not length:
                    break
                stringData = self.recvData(int(length))
                if not stringData:
                    break
                data = np.frombuffer(stringData, dtype="uint8")
                decimg = cv2.imdecode(data, 1)
                video.write(decimg)
                Image(decimg, cvNet)
                islic = False
                if frameCount % 10 == 0:
                    islic = Image.detect()
                if islic:
                    print("Success:", end='')
                    print(frameCount)
                    frameList.append(frameCount)
                frameCount += 1
            self.writeFile(frameList)
            DP.UpLoad(self.fileno + ".mp4", self.fileno + "tmp.mp4")
            DP.UpLoad(self.fileno + ".txt", self.fileno + ".txt")


def start():
    client_number = 0
    MAXCLIENT = 5

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 8888))
    print("Sever is binding 127.0.0.1:8888")

    while True:
        if client_number <= MAXCLIENT:
            server.listen(1)
            print("Listening")
            clientsock, clientAddress = server.accept()
            print("Accept")
            client_number += 1
            pid = os.fork()
            if pid == 0:
                server.close()
                client = Client(clientsock, client_number)
                client.LicencePlateDetector()
                os._exit(0)
            clientsock.close()


if __name__ == "__main__":
    start()

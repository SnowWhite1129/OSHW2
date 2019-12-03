import os
import cv2
import time
import socket, threading
import numpy as np
from Extraction import LicencePlateDetector as Detect

MAX_CLIENT = 15


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def LicencePlateDetector(conn):
    with conn:
        file_name = conn.recv(6).decode() # Demo will always be 6 bytes
        print("File name: ",file_name)
        frame_count = 1
        frame_array = []
        while True:
            stime = time.time()
            length = conn.recv(16)
            if not length:
                break
            stringData = recvall(conn, int(length))
            if not stringData:
                break
            data = np.frombuffer(stringData, dtype="uint8")
            decimg = cv2.imdecode(data, 1)
            have_lic = Detect(decimg)
            # have_lic = True
            if(have_lic):
                frame_array.append(frame_count)
                # print("Licence Plate Detected.")
            else:
                pass
                # print("There is no Licence Plate.")
            # print("Time per frame: ", time.time() - stime)
            frame_count += 1
        
        filename = file_name.split(".")[-2]

        while os.path.exists(filename):
            tmp_int = 0
            filename = filename + str(tmp_int)
            tmp_int += 1
    
        f = open(filename+".txt", "w")
        f.close()
        f = open(filename+".txt", "a")
        for frame in frame_array:
            f.write(str(frame)+'\n')
        f.close()

def DataProcessor():
    pass

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddr = clientAddress
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from : ", self.caddr)
        LicencePlateDetector(self.csocket)
        print ("Client at ", self.caddr , " disconnected...")


def main():
    LOCALHOST = "127.0.0.1"
    PORT = 8080
    client_number = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("Server started")
    print("Waiting for client request..")

    while True:
        print("Listening")
        server.listen(1)
        clientsock, clientAddress = server.accept()
        while client_number >= MAX_CLIENT:
            pass
        client_number += 1
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()


if __name__ == "__main__":
    main()
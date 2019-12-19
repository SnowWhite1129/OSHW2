import os
import cv2
import time
import socket
import numpy as np
from TOOLS.server_mod import DataProcessor
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

def write_txt(file_name, frame_no_array):
    filename = file_name.split(".")[-2]
    while os.path.exists(filename):
        tmp_int = 0
        filename = filename + str(tmp_int)
        tmp_int += 1

    f = open(filename+"tmp.txt", "w")
    f.close()
    f = open(filename+".txt", "a")
    for frame_no in frame_no_array:
        f.write(str(frame_no)+'\n')
    f.close()

def LicencePlateDetector(conn):
    DP = DataProcessor()
    DP.InitImgDir()

    with conn:
        file_name = conn.recv(6).decode() #Demo will always be 6 bytes
        print("File name: ", file_name)
        frame_count = 1
        frame_no_array = []
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(file_name.split(".")[-2] +"tmp.mp4", fourcc, 60, (1920,1080))
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
            video.write(decimg)
            # decimg = cv2.resize(decimg, (640, 480))
            if frame_count % 60 == 1:
                have_lic = Detect(decimg)
            if(have_lic):
                frame_no_array.append(frame_count)
            else:
                pass
            # print("Time per frame: ", time.time() - stime)
            frame_count += 1
        write_txt(file_name, frame_no_array)
        DP.UpLoad(file_name.split(".")[-2] + ".mp4",file_name.split(".")[-2] + "tmp.mp4")
        DP.UpLoad(file_name.split(".")[-2] + ".txt",file_name.split(".")[-2] + ".txt")


def main():
    client_number = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", "8888"))
    print("Sever is binding 127.0.0.1:8888")

    while True:
        print("Listening")
        server.listen(1)
        clientsock, clientAddress = server.accept()
        while client_number >= MAX_CLIENT:
            pass
        client_number += 1
        pid = os.fork()
        if pid == 0:
            server.close()

            LicencePlateDetector(clientsock)

            exit(0)
        clientsock.close()

if __name__ == "__main__":
    main()
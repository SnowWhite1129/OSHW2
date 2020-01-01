import os
import json
import time
from hdfs import InsecureClient
from hdfs import util


class DataProcessor:

    def __init__(self, data_path=None):
        if data_path is None:
            self.data_path = r'./config/connect_info.json'
        else:
            assert type(data_path) == str
            self.data_path = data_path
        if not os.path.exists(self.data_path):
            self.data_path = r'./connect_info.json'

        with open(self.data_path) as data_file:
            data = json.load(data_file)
            self.hdfs_client = InsecureClient(url='http://' + data['namenode_url'] + ':' + str(data['port']),
                                              user=data['user'], root=data['root_path'])
            self.img_dir = data['img_dir']

        if self.img_dir[-1] != '/':
            self.img_dir += '/'

        self.file_name = 1

    def InitImgDir(self):
        try:
            list_rslt = self.hdfs_client.list(self.img_dir)
            if len(list_rslt) > 0:
                for name in list_rslt:
                    file_path = self.img_dir + name
                    self.hdfs_client.delete(file_path)

        except util.HdfsError:
            self.hdfs_client.makedirs(self.img_dir)
            print("Mkdir ...")

        return True

    def DataProcess(self, data, append=False, file_name=None):
        assert type(data) == str
        if file_name is None:
            file_name = self.img_dir + str(self.file_name)
        else:
            assert (type(file_name)) == str
        print("start writing...")
        start = time.time()
        self.hdfs_client.write(file_name, data, overwrite=True, replication=1, append=append)
        delta = time.time() - start
        print("writing complete, time delta is " + str(delta))
        return True

    def Upload(self, remote_name, local_path):
        assert os.path.exists(local_path)

        remote_path = self.img_dir + remote_name
        self.hdfs_client.upload(remote_path, local_path)
        return True

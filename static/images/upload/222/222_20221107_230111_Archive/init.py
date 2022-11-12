# coding=gbk

class usr_data:
    def __init__(self, name, dataset):
        self.name = name
        self.dataset = dataset

    def print(self):
        print(self.name)

a = usr_data('peter','ggg')

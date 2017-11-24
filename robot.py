import rpyc

__author__ = 'Xomak'


class Robot:

    def __init__(self, host):
        self.host = host
        self.connection = None
        self.ev3 = None

    def connect(self):
        self.connection = rpyc.classic.connect(self.host)
        self.ev3 = self.connection.modules['ev3dev.ev3']

    def get_ev3(self):
        return self.ev3
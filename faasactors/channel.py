
class Channel(object):
    def __init__(self, actor):
        self.channel_name = actor

    def send(self, msg):
        print("Channel", self.channel_name, "sending ", msg)

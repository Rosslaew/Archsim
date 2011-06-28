from random import seed,choice,shuffle

class arbiter():
    def __init__(self,ndevices=[]):
        self.devices = devices

    def set(self,devices):
        self.devices = devices

    def choose(self, devices):
        """Chooses a device. To implement."""
        pass

    def sorting(self):
        """Returns a function to sort the devices. To implement."""
        pass

    def update(self,item):
        """Updates the arbiter for the next choice. To implement."""
        pass

class randomArbiter(arbiter):
    def __init__(self,ndevices=0):
        seed()
        arbiter.__init__(self, ndevices)

    def choose(self,devices):
        return choice(devices)

    def sorting(self):
        shuffle(self.devices)
        return self.devices.index

class LRUArbiter(arbiter):
    def sorting(self):
        return self.devices.index

    def choose(self,devices):
        item = min(devices, key = self.sorting())
        return item

    def update(self,item):
        self.devices.remove(item)
        self.devices.append(item)

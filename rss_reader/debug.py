class Demo(object):
    def __init__(self, value):
        self.value = value
        if value == 2:
            raise ValueError

    def __del__(self):
        print ('__del__', self.value)


d = Demo(2)  # successfully create an object here
d = 22  # new int object labeled 'd'; old 'd' goes out of scope

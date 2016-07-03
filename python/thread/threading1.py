import threading
mylock = threading.RLock()
num = 0


class MyThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global num
        while True:
            mylock.acquire()
            print '\nThread(%s %d) locked, Number: %d' % (self.name, self.threadID, num)
            num += 1
            print '\nThread(%s %d) released, Number: %d' % (self.name, self.threadID, num)
            mylock.release()
            if num >= 4:
                break


def test():
    thread1 = MyThread(1, 'A')
    thread2 = MyThread(2, 'B')
    thread1.start()
    thread2.start()

if __name__ == '__main__':
    test()

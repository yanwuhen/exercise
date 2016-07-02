import thread
i = 0

def test(t_name):
    global i
    for j in range(10):
        i = i + 1
        print('%s: %d\n' % (t_name,i))
    thread.exit_thread()

if __name__ == '__main__':
    thread.start_new(test, ('a',))
    thread.start_new(test, ('b',))
    #todo:更好的等待方法
    raw_input()
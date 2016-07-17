import random


class Prisoner(object):
    def __init__(self, index, cooperation, life=100):
        # 0:silence 1:betray
        self.index = index
        self.cooperation = cooperation
        self.life = life

    def __str__(self):
        return "index:%d, cooperation:%s, life:%d" % (self.index, 'betay' if self.cooperation == 1 else 'silence', self.life)

    def test(self, another):
        table = {00: (8, 8),
                 01: (10,  -10),
                 10: (-10, 10),
                 11: (-8, -8)}
        test_result = table[self.cooperation * 10 + another.cooperation]
        self.life += test_result[0]
        another.life += test_result[1]

    def is_dead(self):
        return self.life <= 0

    def is_alive(self):
        return not self.is_dead()

    def is_silence(self):
        return self.cooperation == 0

    def is_betray(self):
        return self.cooperation == 1


def start(test_list):
    length = len(test_list)
    test_order = random.sample(range(length),length)
    for one, another in zip(test_order[0::2], test_order[1::2]):
        test_list[one].test(test_list[another])
    return filter(Prisoner.is_alive, test_list)

if __name__ == '__main__':
    sum_prisoner = 10
    test_count = 100
    prisoner_list = []
    dead_list = []
    for i in range(sum_prisoner):
        prisoner_list.append(Prisoner(i, random.choice(range(2))))
    for i in range(test_count):
        prisoner_list = start(prisoner_list)
        #silence=len(filter(Prisoner.is_silence, prisoner_list))
        #print("silence:%d, betray:%d" % (silence, sum_prisoner - silence))
        print i
        for p in prisoner_list:
            print p
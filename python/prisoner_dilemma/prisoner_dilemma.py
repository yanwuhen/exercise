import random


class Prisoner(object):
    type_table = {"silence": 0,
                  "betray": 1,
                  "flexible": 2,
                  "revenge": 3,}

    def __init__(self, index, tactics, life=100):
        self.index = index
        self.tactics = tactics
        self.life = life
        self.cooperation = None
        self.history = [0, 0, 0]
        self.betray_list = []

    def __str__(self):
        return ("index:%d, type:%s, cooperation:%s, life:%d" %
                (self.index, self.type, 'betay' if self.cooperation == 1 else 'silence', self.life))

    def get_cooperation(self, another):
        if self.tactics == "flexible":
            self.cooperation = reduce(lambda x,y: x + y, self.history) / 2
            self.history.pop(0)
            self.history.append(another.cooperation)
        elif self.tactics == "revenge":
            self.cooperation = 1 if another in self.betray_list else 0
        else:
            self.cooperation = Prisoner.type_table[self.tactics]



    def test(self, another):
        # 0:silence 1:betray
        table = {00: (8, 8),
                 01: (10,  -10),
                 10: (-10, 10),
                 11: (-8, -8)}
        self.get_cooperation(another)
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
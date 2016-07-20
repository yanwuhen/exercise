import random


class Prisoner(object):

    def __init__(self, index, tactics, life=100):
        self.index = index
        self.tactics = tactics
        self.life = life
        self.history = [0, 0, 0]
        self.betray_list = []
        if tactics in (0, 1):
            self.cooperation = tactics
        else:
            self.cooperation = 0

    def __str__(self):
        type_table = {0: "silence",
                      1: "betray",
                      2: "flexible",
                      3: "revenge",}
        return ("index:%d, type:%s, cooperation:%s, life:%d" %
                (self.index, type_table[self.tactics], self.cooperation, self.life))

    def get_new_cooperation(self, another):
        if self.tactics == 2:
            #print self.history
            new_cooperation = reduce(lambda x,y: x + y, self.history) / 2
            #print "start:",self.index,self.history
            self.history.pop(0)
            self.history.append(another.cooperation)
            #print another.cooperation
            #print another
            #print "end:", self.index,self.history
        elif self.tactics == 3:
            new_cooperation = 1 if another in self.betray_list else 0
        else:
            new_cooperation = self.tactics
        return new_cooperation


    @staticmethod
    def test(one, another):
        one_new_coop = one.get_new_cooperation(another)
        another_new_coop = another.get_new_cooperation(one)
        one.cooperation = one_new_coop
        another.cooperation = another_new_coop
        # 0:silence 1:betray
        table = {00: (8, 8),
                 01: (10,  -10),
                 10: (-10, 10),
                 11: (-8, -8)}
        test_result = table[one.cooperation * 10 + another.cooperation]
        one.life += test_result[0]
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
        Prisoner.test(test_list[one], test_list[another])
    return filter(Prisoner.is_alive, test_list)

if __name__ == '__main__':
    sum_prisoner = 100
    test_count = 100
    prisoner_list = []
    dead_list = []
    for i in range(sum_prisoner):
        prisoner_list.append(Prisoner(i, random.choice(range(4))))
    for i in range(test_count):
        prisoner_list = start(prisoner_list)
        print i
        #for p in prisoner_list:
        #    print p
        print "sum:"
        print "silence count:",   len(filter(lambda x: x.tactics == 0, prisoner_list))
        print "betray count:",    len(filter(lambda x: x.tactics == 1, prisoner_list))
        print "flexible count:",  len(filter(lambda x: x.tactics == 2, prisoner_list))
        print "revenge count:",   len(filter(lambda x: x.tactics == 3, prisoner_list))
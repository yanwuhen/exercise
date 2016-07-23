import random
from functools import wraps


def print_specific(one, two, type):
    if one.tactics == type or two.tactics == type:
        print one
        print two


def print_prisoner(fun):
    def wrapper(one, another):
        print_specific(one, another, 1)
        result = fun(one, another)
        print_specific(one, another, 1)
        print "======"
        return result
    return wrapper


class Prisoner(object):

    def __init__(self, index, tactics, life=1000):
        self.index = index
        self.tactics = tactics
        self.life = life
        self.history = [0, 1, 0]
        self.betray_list = []
        if tactics in (0, 1):
            self.cooperation = tactics
        else:
            self.cooperation = 1

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
            new_cooperation = 1 if another.index in self.betray_list else 0
        else:
            new_cooperation = self.tactics
        return new_cooperation



    @staticmethod
    def test(one, another):
        one_new_coop = one.get_new_cooperation(another)
        another_new_coop = another.get_new_cooperation(one)
        one.cooperation = one_new_coop
        another.cooperation = another_new_coop

        if another.cooperation == 1 and one.tactics == 3:
            one.betray_list.append(another.index)
        if one.cooperation == 1 and another.tactics == 3:
            another.betray_list.append(one.index)
        # 0:silence 1:betray
        table = {00: (8, 8),
                 01: (-10,  10),
                 10: (10, -10),
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


def get_random_tactics(proportion):
    rand = random.randint(1, 100)
    for i, v in enumerate(proportion):
        if rand > v:
            continue
        return i
    return i


if __name__ == '__main__':
    TEST = False
    def test_random():
        for i in range(100):
            #print get_random_tactics([50, 100])
            #print get_random_tactics([33, 66, 100])
            print get_random_tactics([25, 50, 75, 100])
    if TEST:
        test_random()
        exit()

    sum_prisoner = 250
    test_count = 3000
    proportion = [25, 50, 75, 100]
    prisoner_list = []
    dead_list = []
    for i in range(sum_prisoner):
        prisoner_list.append(Prisoner(i, get_random_tactics(proportion)))
    for i in range(test_count):
        prisoner_list = start(prisoner_list)

        print i
        #for p in prisoner_list:
        #    print p
#
        silence_count  = len(filter(lambda x: x.tactics == 0, prisoner_list))
        betray_count   = len(filter(lambda x: x.tactics == 1, prisoner_list))
        flexible_count = len(filter(lambda x: x.tactics == 2, prisoner_list))
        revenge_count  = len(filter(lambda x: x.tactics == 3, prisoner_list))
        sum_silence_count  = len(filter(lambda x: x.cooperation == 0, prisoner_list))
        sum_betray_count   = len(filter(lambda x: x.cooperation == 1, prisoner_list))
        print "sum:"
        print "silence count:",  silence_count
        print "betray count:",   betray_count
        print "flexible count:", flexible_count
        print "revenge count:",  revenge_count
        print "sum silence count:",  sum_silence_count
        print "sum betray count:",   sum_betray_count
        #if betray_count == 0:
        #   break
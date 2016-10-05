# -*- coding: utf-8 -*-
import copy

num9_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
num9_set = set(num9_list)


def is_int(num):
    return isinstance(num, int)


class sudoku:
    def __init__(self, lists):
        self.data = lists
        self.rst = None
        self.init_data()
        self.changed = False

    # 将各个空格打个可能的标签
    def init_data(self):
        for list in self.data:
            for i in range(len(list)):
                if list[i] not in num9_list and type(list[i]) != type([]):
                    list[i] = num9_list
        #print self.data
        #print('init_end')

    def hang_reduce_possible(self, data):
        for hang in data:
            known = filter(is_int, hang)
            sum_list = []
            for i in range(len(hang)):
                l = hang[i]
                if not is_int(l):
                    hang[i] = list(set(l) - set(known))
                    sum_list += hang[i]
                    if not self.changed and len(set(l) & set(known)) != 0:
                        self.changed = True
            for num in num9_list:
                if sum_list.count(num) == 1:
                    for i in range(len(hang)):
                        if not is_int(hang[i]) and num in hang[i]:
                            hang[i] = num
                            self.changed = True




    def small_reduce_possible(self, data):
        #print data
        all_num = set([])
        sum_list = []
        for x in range(3):
            for y in range(3):
                if isinstance(data[x][y], int):
                    all_num.add(data[x][y])
        for x in range(3):
            for y in range(3):
                if not isinstance(data[x][y], int):
                    if not self.changed and len(set(data[x][y]) & all_num) != 0:
                        self.changed = True
                    data[x][y] = list(set(data[x][y]) - all_num)
                    sum_list += data[x][y]
        for num in num9_list:
            if sum_list.count(num) == 1:
                for x in range(3):
                    for y in range(3):
                        if not is_int(data[x][y]) and num in data[x][y]:
                            data[x][y] = num
                            self.changed = True

    # 排除不可能的标签，如果本轮有减掉标签，返回True，否则返回False
    def reduce_possible(self):
        #print self.data
        #self.print_data(self.data)
        self.changed = False
        # 横
        #print('start reduce')
        self.hang_reduce_possible(self.data)
        #print('横删减：')
        #self.print_data(self.data)
        # 竖
        new_data = [list(i) for i in zip(*self.data)]
        self.hang_reduce_possible(new_data)
        self.data = [list(i) for i in zip(*new_data)]
        #print('竖删减：')
        #self.print_data(self.data)

        # 小格
        new_data = [[[] for x in range(3)] for y in range(3)]
        for x in range(0, 3):
            for y in range(0, 3):
                #print new_data[x][y]
                new_data[x][y] = [self.data[i][y * 3:y * 3 + 3] for i in range(x * 3, x * 3 + 3)]
                #print new_data[x][y]
                self.small_reduce_possible(new_data[x][y])
        for i in range(9):
            x = i / 3
            z = i % 3
            self.data[i] = new_data[x][0][z] + new_data[x][1][z] + new_data[x][2][z]
        #print('小格删减：')
        #self.print_data(self.data)
        #print self.data

        #print('end reduce')
        return self.changed

    def guest(self):
        for x in range(9):
            for y in range(9):
                if self.data[x][y] not in num9_list:
                    for num in self.data[x][y]:
                        new_data = copy.deepcopy(self.data)
                        new_data[x][y] = num
                        yield new_data

    # 解题
    def solove(self):
        while self.reduce_possible():
            pass
        if self.is_soloved():
            self.rst = copy.deepcopy(self.data)
            return self.rst
        # 假设其中之一,迭代解题
        for new_data in self.guest():
            new_sudoku = sudoku(new_data)
            rst = new_sudoku.solove()
            if rst is not None:
                self.rst = copy.deepcopy(rst)
                return rst
        return None

    # 是否已经解题成功
    def is_soloved(self):
        for list in self.data:
            for l in list:
                if not is_int(l):
                    return False
            if sum(list) != 45:
                return False
        for column in zip(*self.data):
            if sum(column) != 45:
                return False
        return True

    @staticmethod
    def print_data(data):
        for list in data:
            if type(list) != type([]):
                raise Exception("unknown list type:%s", type(i))

            str = ''
            for i in list:
                if i in num9_list:
                    str = '%s%d ' % (str,  i)
                elif type(i) != type([]):
                    raise Exception("unknown type:%s", type(i))
                else:
                    str = str + 'x '
            print str
        print("=================")


if __name__ == '__main__':
    x = -1
    _data = [
        [x, x, 6, x, x, 8, x, 9, 2],
        [x, x, x, x, 2, x, x, x, x],
        [x, x, 4, x, x, x, 3, x, 1],
        [x, x, 2, x, 5, x, x, 1, x],
        [7, 8, x, x, x, 9, x, x, x],
        [1, 4, x, x, x, 2, x, x, 6],
        [4, 7, x, x, 6, x, 1, x, 8],
        [2, 6, 1, x, x, x, 5, 7, x],
        [x, 3, 8, x, x, x, x, x, x],
    ]
    # _data = [
    #     [x, 8, 6, 7, x, x, x, x, x],
    #     [x, x, x, x, x, x, x, x, 9],
    #     [x, x, 7, 3, x, x, 5, x, x],
    #     [x, x, x, 4, x, x, 2, 6, 1],
    #     [x, 7, x, x, 6, 9, x, 5, x],
    #     [4, x, 2, x, 1, 3, 9, x, 8],
    #     [6, 3, 5, 9, 8, 4, x, x, 7],
    #     [x, 1, 4, 6, 3, 2, 8, x, 5],
    #     [9, 2, 8, 1, x, 7, x, 4, 3],
    # ]
    s = sudoku(_data)
    s.solove()
    s.print_data(s.rst)

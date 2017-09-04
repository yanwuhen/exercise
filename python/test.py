class A(object):
    def __init__(self, **kwargs):
        super().__init__()
        print('a1')
        print('a', kwargs)
        print('a2')


class B(object):
    def __init__(self, **kwargs):
        super().__init__()
        print('b1')
        print('b', kwargs)
        print('b2')


class C(A, B):
    def __init__(self, **kwargs):
        print('c1')
#        super(C, self).__init__()
        super().__init__()
        print('c2')


if __name__ == '__main__':
    c = C()

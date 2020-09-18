class a():
    def __index__(self):
        return 12

    def __add__(self, other):
        return 1

    def __radd__(self, other):
        return self.__add__(other)

    def __len__(self):
        return 10

    def __contains__(self, item):
        return True

    def __call__(self, a):
        print(123)

    def __call__(self):
        print(12341421)
    def __b__d(self):
        print('__b')

    def __c__(self):
        print('__c__')

class b(a):
    pass

aa = a()

print(1 + aa)
aa += 1
print([1,2,3][aa])
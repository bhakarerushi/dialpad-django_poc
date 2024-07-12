

TEST_VAR = 'VAR'

class Test:

    def __init__(self,a) -> None:
        self.a = a

class Child(Test):

    def __init__(self, a,b) -> None:
        super().__init__(a)
        self.b = b

    def show(self):
        print(self.b)
        print(self.a)




if __name__ == '__main__':

    c = Child(4,5)
    c.show()
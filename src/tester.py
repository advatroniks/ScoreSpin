class A:
    a: int = 4
    b: int = 10

    @property
    def c(self):
        return 10


a = A()

print(dir(A))
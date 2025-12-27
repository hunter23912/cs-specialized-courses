class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, n):
        r = Vector()
        r.x = self.x + n.x
        r.y = self.y + n.y
        r.z = self.z + n.z
        return r
    
    def __sub__(self, n):
        r = Vector()
        r.x = self.x - n.x
        r.y = self.y - n.y
        r.z = self.z - n.z
        return r
    
    def __mul__(self, n):
        r = Vector()
        r.x = self.x * n.x
        r.y = self.y * n.y
        r.z = self.z * n.z
        return r
    
    def __truediv__(self, n):
        r = Vector()
        r.x = self.x / n.x
        r.y = self.y / n.y
        r.z = self.z / n.z
        return r
    
    def __floordiv__(self, n):
        r = Vector()
        r.x = self.x // n.x
        r.y = self.y // n.y
        r.z = self.z // n.z
        return r
    
    def show(self):
        print(f'({self.x},{self.y},{self.z})')

v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
v3 = v1 + v2
v3.show()
v4 = v1 - v2
v4.show()
v5 = v1 * v2
v5.show()
v6 = v1 / v2
v6.show()
v7 = v1 // v2
v7.show()
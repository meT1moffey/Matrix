class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, oth):
        return Vector(self.x + oth.x, self.y + oth.y)
    def __sub__(self, oth):
        return Vector(self.x - oth.x, self.y - oth.y)
    def __mul__(self, oth):
        return Vector(self.x * oth, self.y * oth)
    def __truediv__(self, oth):
        return Vector(self.x / oth, self.y / oth)
    def __rmul__(self, oth):
        return Vector(oth * self.x, oth * self.y)
    
    def __iadd__(self, oth):
        self.x += oth.x
        self.y += oth.y
        return self
    def __isub__(self, oth):
        self.x -= oth.x
        self.y -= oth.y
        return self
    def __imul__(self, oth):
        self.x *= oth
        self.y *= oth
        return self
    def __itruediv__(self, oth):
        self.x /= oth
        self.y /= oth
        return self
    
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
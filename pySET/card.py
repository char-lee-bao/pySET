class Card(object):
    
    def __init__(self, number, shape, shading, color, index):
        self.number = number
        self.shape = shape
        self.shading = shading
        self.color = color
        self.index = index

    def __repr__(self):
        return f"{self.number} {self.shading} {self.color} {self.shape}"

    def get_number(self):
        return self.number

    def get_shape(self):
        return self.shape

    def get_shading(self):
        return self.shading

    def get_color(self):
        return self.color

    def get_index(self):
        return self.index
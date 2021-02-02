class Location(object):
    def __init__(self, name=''):
        self.name = str(name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

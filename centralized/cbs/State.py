class State(object):
    def __init__(self, time, location):
        self.time = time
        self.location = location

    def __eq__(self, other):
        return self.time == other.time and self.location == other.location

    def __hash__(self):
        try:
            hashVal = hash(str(self.time)+str(self.location.x) + str(self.location.y))
        except Exception:
            hashVal = hash(str(self.time) + str(self.location.name))
        return hashVal

    def is_equal_except_time(self, state):
        return self.location == state.location

    def __str__(self):
        try:
            return str((self.time, self.location.x, self.location.y))
        except Exception:
            return str((self.time, self.location.name))

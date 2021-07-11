class t:
    def __init__(self):
        self.a = None
        self.b = None

    def set(self, user, num):
        if num == 1:
            self.a = user
        else:
            self.b = user

    def compare(self):
        return self.a.id == self.b.id

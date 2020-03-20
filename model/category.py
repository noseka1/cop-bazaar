class Category(object):

    all = []

    def __init__(self, title):
        self.title = title
        self.repositories = []
        self.all.append(self)

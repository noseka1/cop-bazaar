class Category(object):

    all = []

    def __init__(self, title, desc):
        self.title = title
        self.desc = desc
        self.repositories = []
        self.all.append(self)

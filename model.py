__author__ = 'papaloizouc'


class Model:
    def __init__(self):
        self.questions = []


class Question:
    def __init__(self, id, title, user, link, votes, answers, views, tags):
        self.id = id
        self.user = user
        self.title = title
        self.link = link
        self.votes = votes
        self.answers = answers
        self.views = views
        self.tags = tags

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__()


class User:
    def __init__(self, name, reputation):
        self.name = name
        self.reputation = reputation

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__()
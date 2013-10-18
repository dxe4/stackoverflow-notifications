__author__ = 'papaloizouc'


class Model:
    def __init__(self):
        self.questions = []


class Question:
    def __init__(self, title, user, link, votes, answers, views):
        self.title = title
        self.user = user


class User:
    def __init__(self, name, reputation):
        self.name = name
        self.reputation = reputation
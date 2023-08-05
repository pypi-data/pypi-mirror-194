import textwrap


class Lesson:
    def __init__(self):
        self.group = None
        self.name = None
        self.room = None
        self.teacher = None

    def __str__(self):
        return ', '.join([self.name, self.teacher, self.room])

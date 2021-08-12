import json


class Habit():
    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description
        self.preconditions = []
        self.place = None
        self.time = None

    def __str__(self):
        return self.__representation_pattern()

    def set_place(self, place: str):
        self.place = place

    def set_time(self, time: str):
        # 8.30 in the morning
        self.time = time

    def set_schedule(self, **kwargs):
        # everyday / choose days of the week ...
        # TODO: how to manage schedule
        print(kwargs)

    def set_precondition(self, precondition: str):
        # text description about what should be before habit
        self.preconditions.append(precondition)

    def __representation_pattern(self):
        pattern = {
            'name': self.name,
            'description': self.description,
            'place': self.place,
            'time': self.time,
            'preconditions': self.preconditions
        }
        return json.dumps(pattern)


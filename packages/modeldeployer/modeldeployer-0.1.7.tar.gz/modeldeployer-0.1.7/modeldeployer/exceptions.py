

class IsNotList(Exception):
    def __init__(self, message="object type is not List"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class IsNotFunction(Exception):
    def __init__(self, message="object type is not Function"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

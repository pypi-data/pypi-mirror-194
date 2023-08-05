class Node:

    def __init__(self, name: str, context: str, extension: str, priority: int=1) -> None:
        self.name = name
        self.context = context
        self.extension = extension
        self.priority = priority
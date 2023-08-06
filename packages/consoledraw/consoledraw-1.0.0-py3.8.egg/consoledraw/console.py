class Console:
    def __init__(self, hideCursor: bool = True) -> None:
        self.text = ""

        if hideCursor:
            print("\x1b[?25l")
    
    def write(self, text: str) -> None:
        self.text += text

    def print(self, *args, **kwargs) -> None:
        if "file" in kwargs:
            kwargs.pop("file")
        print(end="\033[0;0f")
        print(*args, **kwargs, file=self)
    
    def clear(self) -> None:
        self.text = ""

    def update(self) -> None:
        print(self.text, end="")

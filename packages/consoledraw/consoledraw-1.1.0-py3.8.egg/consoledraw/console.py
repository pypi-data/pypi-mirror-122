import os


class Console:
    def __init__(self, hideCursor: bool = True) -> None:
        self.text = ""

        if hideCursor:
            print("\x1b[?25l")
        
        self.update()
    
    def write(self, text: str) -> None:
        self.text += text

    def print(self, *args, **kwargs) -> None:
        if "file" in kwargs:
            kwargs.pop("file")
        print(*args, **kwargs, file=self)
    
    def clear(self) -> None:
        self.lastText = self.text.rstrip()
        self.text = ""
        print(end="\033[0;0f")

    def update(self) -> None:
        self.text = self.text.rstrip()

        grid = []
        size = os.get_terminal_size()
        for _ in range(size.lines - 1):
            row = []
            for _ in range(size.columns):
                row.append(" ")
            grid.append(row)

        x, y = 0, 0
        for char in self.text:
            if char == "\n":
                x = 0
                y += 1
            else:
                grid[y][x] = char
                if (x := x + 1) == size.columns:
                    x = 0
                    y += 1

        print("".join(["".join(row) for row in grid]), end="")

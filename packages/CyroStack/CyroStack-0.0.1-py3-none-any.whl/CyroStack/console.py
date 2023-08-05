import os
import sys
import logging

class Console:
    def __init__(self, app, block_printing=True):
        self.app = app
        self.block_printing = block_printing
        self.refresh()
        self.console_history = []
        self.log_history = []

    def refresh(self, console_width=os.get_terminal_size().columns, console_height=os.get_terminal_size().lines):
        os.system('cls')
        self.title = "CyroStack"
        self.title_width = len(self.title)
        self.title_padding = (console_width - self.title_width) // 2
        self.title = " " * self.title_padding + self.title + " " * self.title_padding

        self.version = "v0.1.0"
        self.version_width = len(self.version)
        self.version_padding = (console_width - self.version_width) // 2

        self.version = " " * self.version_padding + self.version + " " * self.version_padding

        self.line = "-" * console_width
        sys.stdout = sys.__stdout__
        print(self.title)
        print(self.version)
        print(self.line)
        sys.stdout = open(os.devnull, 'w') if self.block_printing else sys.__stdout__
        
    def getRemainingLines(self):
        return os.get_terminal_size().lines - 4

    def printHorizontal(self, l1, l2):
        l1 = self.wrap(l1, (os.get_terminal_size().columns - 3) // 2)[-self.getRemainingLines():]
        l2 = self.wrap(l2, (os.get_terminal_size().columns - 3) // 2)[-self.getRemainingLines():]
        for i in range(self.getRemainingLines()):
            sys.stdout = sys.__stdout__
            print(f"{l1[i] if i < len(l1) else ' ' * ((os.get_terminal_size().columns - 3) // 2)}{' ' * (((os.get_terminal_size().columns - 3) // 2) - len(l1[i])) if i < len(l1) else ''}|{l2[i] if i < len(l2) else ' ' * ((os.get_terminal_size().columns - 3) // 2)}{' ' * (((os.get_terminal_size().columns - 3) // 2) - len(l2[i])) if i < len(l2) else ''}")
            sys.stdout = open(os.devnull, 'w') if self.block_printing else sys.__stdout__

    def wrap(self, lines, width):
        wrapped_lines = []
        for line in lines:
            l = ''
            for word in line.split(' '):
                if len(l + word) > width:
                    wrapped_lines.append(l)
                    l = ''
                l += word + ' '
            wrapped_lines.append(l)
        return wrapped_lines

    def run(self):
        while True:
            console_width = os.get_terminal_size().columns
            console_height = os.get_terminal_size().lines

            if os.get_terminal_size().columns != console_width or os.get_terminal_size().lines != console_height:
                console_width = os.get_terminal_size().columns
                console_height = os.get_terminal_size().lines
                self.refresh(os.get_terminal_size().columns, os.get_terminal_size().lines)
            self.clear()

            sys.stdout = sys.__stdout__
            command = input(">>> ")
            sys.stdout = open(os.devnull, 'w') if self.block_printing else sys.__stdout__
            self.console(command)
            
    def log(self, text):
        self.log_history.append(text)
        self.clear()

    def console(self, text):
        self.console_history.append(f'>>> {text}')
        if text == "clear":
            self.console_history = []
            self.log_history = []
            self.clear()
        elif text == "start":
            self.app.controlQueue.put("start")
        elif text == "resize":
            self.refresh()
        elif text == "stop":
            self.app.controlQueue.put("stop")
        elif text == "exit":
            self.app.controlQueue.put("exit")
        elif text == "help":
            self.console_history.append("help: Displays this message")
            self.console_history.append("clear: Clears the console")
            self.console_history.append("resize: Resizes the console")
            self.console_history.append("stop: Stops the server")
        else:
            self.console_history.append("Unknown command")
        self.clear()

    def clear(self):
        self.refresh()
        self.printHorizontal(self.console_history, self.log_history)
                
class Logger(logging.Logger):
    def __init__(self, console):
        super().__init__("CyroStack")
        self.console = console
        self.setLevel(logging.DEBUG)
        self.addHandler(LogHandler(self.console))

class LogHandler(logging.StreamHandler):
    def __init__(self, console):
        super().__init__()
        self.console = console
        self.file = open("CyroStack.log", "a")

    def emit(self, record):
        if record.levelno == logging.DEBUG:
            level = "🔵"
        elif record.levelno == logging.INFO:
            level = "🟢"
        elif record.levelno == logging.WARNING:
            level = "🟡"
        elif record.levelno == logging.ERROR:
            level = "🔴"
        elif record.levelno == logging.CRITICAL:
            level = "💥"
        else:
            level = "🤷"
        
        self.console.log(f'{level} {self.format(record)}')
        self.file.write(f'{self.format(record)}\r')
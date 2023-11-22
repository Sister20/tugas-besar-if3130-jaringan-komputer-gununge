class Logger:
    WARNING = "\033[91m"
    ALERT = "\033[93m"
    SUCCESS = "\033[92m"
    DEFAULT = "\033[0m"

    def __init__(self, name):
        self.name = name

    def success_log(self, msg):
        print(f"{self.SUCCESS}[{self.name}]{self.DEFAULT} {msg}")

    def alert_log(self, msg):
        print(f"{self.ALERT}[{self.name}]{self.DEFAULT} {msg}")

    def warning_log(self, msg):
        print(f"{self.WARNING}[{self.name}]{self.DEFAULT} {msg}")

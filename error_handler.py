import sys

class ErrorHandler:
    current_line_num = 0
    def __init__(self) -> None:
        pass
    def ThrowError(self, message):
        print("ERROR (line ", ErrorHandler.current_line_num, "): ", message, sep="")
        sys.exit()
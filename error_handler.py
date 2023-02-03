import sys

class ErrorHandler:
    current_line_num = 0
    has_done_error = False
    def __init__(self) -> None:
        pass
    def ThrowError(self, message):
        print("ERROR (line ", ErrorHandler.current_line_num, "): ", message, sep="")
        ErrorHandler.has_done_error = True
        sys.exit()
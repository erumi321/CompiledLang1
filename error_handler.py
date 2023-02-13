import sys

class ErrorHandler:
    current_line_num = 0
    current_line = ""
    has_done_error = False
    def __init__(self) -> None:
        pass
    def ThrowError(self, *message, sep=""):
        print("ERROR (line ", ErrorHandler.current_line_num, "): ", sep.join(str(e) for e in message), sep="")
        ErrorHandler.has_done_error = True
        sys.exit()
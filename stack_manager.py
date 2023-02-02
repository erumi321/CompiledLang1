from error_handler import ErrorHandler

class StackManager:
    stacks = {}
    errorHandler = ErrorHandler
    def __init__(self, errorHandler) -> None:
        self.stacks = {}
        self.errorHandler = errorHandler
        pass

    def process_stack_val(self, val):
        if isinstance(val, str):
            try:
                return int(val)
            except ValueError:
                self.errorHandler.ThrowError("Invalid Stack Val")
                return 0
        elif isinstance(val, int):
            return val
        else:
            self.errorHandler.ThrowError("Invalid Stack Val")
            return 0

    def check_stack_created(self, val):
        if not val in self.stacks:
            self.stacks[val] = []

    def clear_stack(self, stack_val):
        s_v = self.process_stack_val(stack_val)
        self.check_stack_created(s_v)
        self.stacks[s_v] = []
    
    def push_stack(self, stack_val, val):
        s_v = self.process_stack_val(stack_val)
        self.check_stack_created(s_v)
        self.stacks[s_v].insert(0, val)
    
    def pop_stack(self, stack_val):
        s_v = self.process_stack_val(stack_val)
        self.check_stack_created(s_v)
        self.stacks[s_v].pop(0)
    
    def stack_length(self, stack_val):
        s_v = self.process_stack_val(stack_val)
        self.check_stack_created(s_v)
        return len(self.stacks[s_v])
    
    def get_stack_val(self, stack_val):
        s_v = self.process_stack_val(stack_val)
        self.check_stack_created(s_v)

        if len(self.stacks[s_v]) == 0:
            self.errorHandler.ThrowError("Refrencing Stack Value from an Empty Stack")
            return -1

        return self.stacks[s_v][0]
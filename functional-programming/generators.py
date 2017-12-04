# Imperative version
def get_log_lines(log_file):
    line = read_line(log_file)
    while True:
        try:
            if complex_condition(line):
                yield line
            line = read_line(log_file)
        except StopIteration:
            raise

log_lines = get_log_lines(huge_log_file)

# Generator version
log_lines = (line for line in read_line(huge_log_file) 
                if complex_condition(line))

# Class version

class get_log_lines(object):
    def __init__(self,log_file):
        self.log_file = log_file
        self.line = None
    def __iter__(self):
        return self
    def __next__(self):
        if self.line is None:
            self.line = read_line(self.log_file)
        while not complex_condition(self.line):
            self.line = read_line(self.log_file)
        return self.line

log_lines = get_log_lines(huge_log_file)



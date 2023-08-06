class ShowUpper:
    # constructor
    def __init__(self, name):
        self.name = name
    # String to upper
    def str_upper(self):
        self.name += self.name.upper()
    def str_lower(self):
        self.name += self.name.lower()
    # show
    def show(self):
        print(self.name)


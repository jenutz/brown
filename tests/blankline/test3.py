import os

# Top level comment
@decorator
# Gap between decorator and class (E304)

class ComplexEntity:
    """Docstring for the class"""
    # Comment touching the docstring (E301)
    def __init__(self, value):
        self.value = value
        # Comment with huge gap above it (E303)


        # Another comment
        self.setup()

    def setup(self):
        # A comment inside a method
        pass
# Comment touching the end of a class (E305)
def global_func():
    # Comment before a nested function (E306)
    def nested():
        pass
    
    
    # 3 blank lines above this comment (E303)
    
    return True



# 4 blank lines before the final call (E303)



global_func()
"""
    Module which declares auxiliary classes for specs execution
"""

# Use models.py Method class instead
# class Method:
#     """ Method object """

#     def __init__(self):
#         self.method_id = ""
#         self.method_name = ""
#         self.class_name = ""
#         self.class_path = ""

#     def __str__(self):
#         print("METHOD:")
#         print("\t\t\t name: " + self.method_name)
#         print("\t\t\t classe: " + self.class_name)
#         print("\t\t\t path: " + self.class_path)
#         return ''


# Ver a necessidade de utilizar a modelo de Describe tb.. acho que não precisa.
# class Describe:
#     def __init__(self):
#         self.description = ""
#         self.line = None


class It:
    """ It object """

    def __init__(self, project="", key="", file="", description="", line=None, executed_methods=[],
                result=""):
        self.project = project
        self.key = key
        self.file = file
        self.description = description
        self.line = line
        self.executed_methods = executed_methods
        self.result = result

    def __str__(self):
        return self.description

    def obj_dict(self):
        """ Return a dictionary or other mapping object. """
        return self.__dict__

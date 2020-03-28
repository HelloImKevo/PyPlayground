students = []

# -------------------------------------------------------------------


class Student:

    school_name = "Springfield Elementary"

    _name: str = None
    _student_id = None

    def __init__(self, name: str, student_id=332):
        self._name = name
        self._student_id = student_id
        students.append(self)

    def __str__(self):
        return "Student" + self._name

    def get_name_capitalize(self):
        return self._name.capitalize()

    def get_school_name(self):
        return self.school_name


class HighSchoolStudent(Student):

    school_name = "Springfield High School"

    def get_school_name(self):
        return "This is a High School Student"

    def get_name_capitalize(self):
        original_value = super().get_name_capitalize()
        return original_value + "-HS"


# mark = Student("Mark")
# print(mark)
# print(Student.school_name)

james = HighSchoolStudent("james")
print(james.get_name_capitalize())

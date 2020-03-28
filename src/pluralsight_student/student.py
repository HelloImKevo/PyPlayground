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

    def add_student(self, name, student_id=332):
        """
        Adds the student to the student list.
        :param name: string - student name
        :param student_id: integer - optional student ID
        :return: None
        """
        pass

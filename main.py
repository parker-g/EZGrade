import datetime
import pandas as pd
from results import write_results

# future features 
# Front end GUI
# Python web framework ie. flask / django
# ability to input picture of student's assignment
# DONE - ability to view gradebook in graph or excel format
# DONE - want each student to easily store multiple assignments (might not have to make adjustments for this.) - changed to pandas for data instead of dictionaries

class Student:
    def __init__(self, name, age=None, birthday=None, readLevel=None):
        self.name = name
        self.age = age
        self.birthday = birthday
        self.readLevel = readLevel
        self.grades = {}
    def __repr__(self): # works
        if self.readLevel == None:
            return f'Student {self.name} was born on {self.birthday}. A collection of their current grades looks like this: {self.grades}'
        return f'Student {self.name} was born on {self.birthday}. {self.name} reads at a {self.readLevel} grade level. A collection of their current grades looks like this: {self.grades}'
    def add_grade(self, assignment, grade): # works
        self.grades[assignment] = grade

class SpedStudent(Student):
    def __init__(self, name, age=None, birthday=None, readLevel=None): 
        super().__init__(name, age, birthday, readLevel) # works
        self.accomodations = []
    def __repr__(self):
        return f'{self.name} is a special student. This student requires special accomodations in order to learn.'
    def add_accomodations(self, *accomodations): # works
        for accomodation in accomodations:
            self.accomodations.append(accomodation)
    def accomodations(self): # works
        accomodations = (str(self.accomodations))
        print(f"{self.name} has the following accomodations listed: {accomodations}")

jefferey = SpedStudent('Jefferey', 22, readLevel=9)
jefferey.add_accomodations('Needs a blanket', 'Prefers to listen to music with headphones while working')

jessica =Student('Jessica', age=7, birthday=datetime.date(2015, 4, 21))
jessica.add_grade('Project one', 85)
parker = Student('Parker', 21, datetime.date(2000, 9, 9), 12)
parker.add_grade('Coding Assingment 1', 100)

# self.gradebook is a dataframe table with names as y-axis values and assignment names as x-axis values. 
class Gradebook: # kinda want to accept dictionaries too. idk how practical that would be tho in real world
    def __init__(self, grades_info):
        if type(grades_info) == str:
            df = pd.read_csv(grades_info)
            self.gradebook = df
        else:
            raise TypeError('Gradebook objects\'s __init__ takes a csv file path as an argument.')
        # elif type(grades_info) == dict:
        #     self.gradebook = grades_info

    def __repr__(self):
        return str(self.gradebook.head(15))

    def add_student(self, student): # adds a student to df with 0's for every assignment
        if type(student) == str:    
            names_list = self.gradebook['Name'].tolist()
            if student in names_list:
                print(f'{student} is already in the gradebook.')
            else:
                columns = len(self.gradebook.columns)
                finale = []
                for i in range(0, columns):
                    i+= 1 
                    finale.append(0)
                finale[0] = student
                print(f'Adding student {student} to gradebook.')
                self.gradebook.loc[len(self.gradebook.index)] = finale
                self.gradebook.to_csv('testing.csv', index=False, sep=',')
        elif type(student) == Student: # wanna modify this so if a Student object has a dictionary of assignment:grade pairs, 
            # they will be automatically added to gradebook. 
            names_list = self.gradebook['Name'].tolist()
            if student.name in names_list:
                print(f'{student.name} is already in the gradebook.')
            else:
                columns = len(self.gradebook.columns)
                finale = []
                for i in range(0, columns):
                    i+= 1 
                    finale.append(0)
                finale[0] = student.name
                print(f'Adding student {student.name} to gradebook.')
                self.gradebook.loc[len(self.gradebook.index)] = finale
                self.gradebook.to_csv('testing.csv', index=False, sep=',')

    def remove_student(self, student): # unsure if it works after adding type statements
        if type(student) == str:
            student_index = self.gradebook.index[self.gradebook['Name'] == student].tolist()
        elif type(student) == Student:
            student_index = self.gradebook.index[self.gradebook['Name'] == student.name].tolist()
        self.gradebook.drop(
                labels = student_index, 
                axis = 0, #0 for rows, 1 for columns,
                inplace=True # determines whether u directly alter the dataframe or create a new one
            )
        self.gradebook.to_csv('testing.csv', sep=',', index=False)

# can definitely refactor this a bit
    def add_grade(self, student, assignment:str, grade:int): # works with dataframe. string or Student object for student input
        if type(student) == str:
            student_index = self.gradebook.index[self.gradebook['Name'] == student].tolist()
            short_index = student_index[0]
            self.gradebook.at[short_index, assignment] = grade
            self.gradebook.to_csv('testing.csv', sep=',', index=False)
            print(f'{student}\'s grade for {assignment} is now {grade}.')
            print(self.gradebook[self.gradebook.Name == student])
        elif type(student) == Student:
            student_index = self.gradebook.index[self.gradebook['Name'] == student.name].tolist()
            short_index = student_index[0]
            self.gradebook.at[short_index, assignment] = grade
            self.gradebook.to_csv('testing.csv', sep=',', index=False)
            print(f'{student.name}\'s grade for {assignment} is now {grade}.')
            print(self.gradebook[self.gradebook.Name == student.name])



#control+D to select next occurence of a highlighted word/number/character(s)

pandas_test = Gradebook('testing.csv')
# pandas_test.add_grade('Garrett', 'Project 2', 85)
jocelyn = Student('Jocelyn', 20, readLevel=12)


def main(gradebook:Gradebook):
    a = input('What would you like to do? View gradebook, view student grades, add student, or add grades?: ')
    if a == 'view gradebook':
        print(gradebook)
    elif a == 'view student grades' or a == 'view student grade' or a == 'view student':
        b = input('Which student\'s grades would you like to view?: ')
        print(gradebook.gradebook.loc[gradebook.gradebook['Name'] == b])
    elif a == 'add student':
        name = input('Now I will collect some information about your new student. First, what\'s your student\'s name?: ')
        name = name.capitalize()
        if name in gradebook.gradebook['Name'].values:
            print(f'{name} is already in gradebook.')
            return
        age = int(input(f'How old is {name}?: '))
        lvl = int(input(f'What grade is {name}\'s reading level?: '))
        new_student = Student(name, age, readLevel = lvl)
        gradebook.add_student(new_student)
    elif a =='add grades':
        name = input('Which student would you like to add grades for?: ')
        assignment = input(f'Which one of {name}\'s assignments are you inputting?: ')
        grade = int(input(f'What grade did {name} recieve on that assignment?: '))
        gradebook.add_grade(name, assignment, grade)
        print('Perfect, your grade has been added.')
        print(gradebook.gradebook)
    else:
        print('You did not enter a valid input. Please try again.')
main(pandas_test)

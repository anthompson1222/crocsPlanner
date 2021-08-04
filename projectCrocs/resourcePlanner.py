import sys
sys.path.append("/Users/anthompson/Desktop/Python Stuff/projectCrocs")
from fileReader import read_file, write_file

class employee:

    def __init__ (self, name, department, skillset): #skill set should be 
        self.name = name                             #in the format (skill, proficiency)
        self.department = department
        self.skillset = skillset
        self.hours = 40 #default hours is 40
        self.projects = []

        
    def printSkills(self):
        skills = ""
        for x in self.skillset:
            skills += x[0]
            skills += ", "
            skills += str(x[1])
            skills += " | "
        return skills

    def adjustHours(self, hours):
        self.hours = hours

    def insertProject(self, project):
        self.projects.append(project)

    def calculateHours(self):
        self.hours = 40
        for x in self.projects:
            self.hours -= int(x.hours)

        return self.hours

    def calculateUtilization(self):
        return str(((40 - self.hours) / 40) * 100) + "%"


skills = ["N/A", "Computers", "Programming", "Scripting"]

######################### Below is the matrix for Employers ####################
 
class raciMatrix:


    def __init__ (self, name, employees):
        self.name = name
        self.employees = employees
        self.names = ["N/A"]
        for x in employees:
            self.names.append(x.name)
        self.raci = [["Skills/Names", "Computers", "Programming", "Scripting"]]
        for x in employees:
            self.raci.append([x.name] + [0 for x in range(len(skills)-1)])


    def populateMatrix(self):
        for x in self.employees:
            for y in x.skillset:
                self.raci[self.names.index(x.name)][skills.index(y[0])] = y[1]

    def addEmployee(self, newEmployee):
        self.raci.append([newEmployee.name, 0, 0, 0])
        self.names.append(newEmployee.name)
        self.employees.append(newEmployee)
        for x in newEmployee.skillset:
            self.raci[len(self.names) - 1][skills.index(x[0])] = x[1]

    def printUtilizations(self):
        for x in self.employees:
            x.calculateHours()
            print("Name: " + x.name + ", Utilization: " + x.calculateUtilization())

def createEmployeeObjects(employees):
    employeeList = [] #List of employee objects
    for x in employees:
        if len(x) == 2:
            employeeList.append(employee(x[0],x[1],[]))
            #The below code is confusing, basically it takes the first two elements
            #since they are always going to be name and department and puts them into
            #the employee object, then it zips up the rest of the employees stats into tuples
            #as they always follow the same format and through this length doesnt matter
        else:
            employeeList.append(employee(x[0], x[1], [*zip((x[2:])[::2], (x[2:])[1::2])]))
    return employeeList
    
def createMatrixFromFile(filename):
    listEmploy = read_file(filename)
    r = raciMatrix("test", createEmployeeObjects(listEmploy))
    r.populateMatrix()
    return r

def saveEmployeesToFile(employees):
    listToBeSaved = []
    for x in employees:
        listToBeSaved.append([x.name, x.department] + [i for y in x.skillset for i in y])
    write_file(listToBeSaved)

def totalUtil(employees):
    totalHours = len(employees) * 40
    takenHours = 0
    for x in employees:
        takenHours += (40 - x.calculateHours())

    return takenHours / totalHours
        
    

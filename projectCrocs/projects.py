import resourcePlanner as rp
from fileReader import save_projects, read_projects

class project:

    def __init__ (self, name, employees, hours): #Project hours is a per
        self.hours = hours                       #person average
        self.name = name
        self.employees = employees
        self.tasks = []
        for x in employees:
            x.insertProject(self)

    def printEmployees(self):
        print(self.name + "\n" + "Employees:")
        for x in self.employees:
            print("Name: " + x.name + ", Skillset: " + x.printSkills())

    def addEmployee(self, employee):
        self.employees.append(employee)
        employee.insertProject(self)

    def printUtilizations(self):
        for x in self.employees:
            x.calculateHours()
            print("Name: " + x.name + ", Utilization: " + x.calculateUtilization())

    def addTask(self, task):
        self.tasks.append(task)

    def adjustProject(self, name, hours):
        self.name = name
        self.hours = hours
        
def saveProjectsToFile(projects):
    projectsToBeSaved = []
    for x in projects:
        projectsToBeSaved.append([x.name, x.hours] + [y.name for y in x.employees])
    save_projects(projectsToBeSaved)


test = rp.employee("Mark", "IT", [])
test2 = rp.employee("Alex", "IT", [])
testProject = project("TEST", [test, test2], 20)
testProject2 = project("lol", [test], 100)
#testProject.printUtilizations()

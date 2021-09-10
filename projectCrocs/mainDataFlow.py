import fileReader as fr
import resourcePlanner as rp
import projects as p
import tasks as t

#Need employee flow first, then project flow in order for projects to work
#Projects must reference employee list in order to create objects

def checkNames(string, employees): #taking in a string as a name and
    for x in employees:            #a list of employees
        if string == x.name:
            return x

def createProjects(projects, employees):
    teamProjects = []
    if len(projects) == 0:
        return []
    for x in projects:
        teamProjects.append(p.project(x[0], [checkNames(y,employees) for y in
                                           x[2:]], int(x[1])))

    return teamProjects

def createTasks(tasks, projects):
    for x in tasks:

        #i = 0
        #while x[1] != projects[i].name:
            #i+=1

        #i+=1
        for y in projects:
            if y.name == x[1]:
                y.addTask(t.tasks(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))

def reverseTasks(projects):
    tempList = []
    retList = []

    for x in projects:
        for y in x.tasks:
            retList.append([y.name, y.project, y.taskType, y.priority, y.assignee, y.reporter, y.description])
            
    return retList

###################Both of the above could go into projects.py##################
    
def load_saveFile():
    listEmploy = fr.read_file2("saveFile.txt")
    employees = rp.createEmployeeObjects(listEmploy[0])
    listProjects = fr.read_projects("projects.txt")
    projects = createProjects(listProjects, employees)
    createTasks(fr.read_tasks("tasks.txt"), projects)
    
    return [employees, projects, listEmploy[1]] #x[0] is employees, x[1] is projects

def write_saveFile(employees, projects, skills):
    p.saveProjectsToFile(projects)
    rp.saveEmployeesToFile(employees, skills)
    fr.write_tasks(reverseTasks(projects))
    

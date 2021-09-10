import csv
import os

def read_file(filename):
    employeeStats = []
    indEmployee = []
    with open(filename,newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            if row != []:
                for x in row:
                    indEmployee.append(x)

                employeeStats.append(indEmployee)
                indEmployee = []

    return employeeStats

def read_file2(filename): #Made to read the xcel stuff
    employeeStats = []
    indEmployee = []
    skillz = []
    skips = 0
    noNeedCats = ['ID', 'Start time', 'Completion time', 'Email', 'Name']
    with open(filename,newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for index, row in enumerate(csv_reader):
            if index == 0:
                for x in row:
                    if x in noNeedCats:
                        skips += 1
                    else:
                        skillz.append(x)
            else:
                for x in range(skips, len(row)):
                    indEmployee.append(row[x])

                employeeStats.append(indEmployee)
                indEmployee = []
    if skillz == []:
        skillz.append("Import Employees")
    else:
        skillz[0] = "Skills/Names"
    return [employeeStats, skillz]
                        


def write_file(employees): #writes to csv file in folder named saveFile.txt
    filename = "saveFile.txt" #Needs to be run through saveMatrixToFile

    with open(filename, 'w', newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        for x in employees:
            csvwriter.writerow(x)

def save_projects(projects): #Needs to be run through convertProjects
    filename = "projects.txt"

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for x in projects:
            csvwriter.writerow(x)

def read_projects(filename):
    projectStats = []
    indProject = []
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            if row != []:
                for x in row:
                    indProject.append(x)

                projectStats.append(indProject)
                indProject = []

    return projectStats

def read_tasks(filename):
    tasksTotal = []
    indTask = []
    with open(filename,newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            if row != []:
                for x in row:
                    indTask.append(x)

                tasksTotal.append(indTask)
                indTask = []

    return tasksTotal

def write_tasks(tasks):
    with open("tasks.txt", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for x in tasks:
            csvwriter.writerow(x)
    
            

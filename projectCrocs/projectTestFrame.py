import tkinter as tk
import tkinter.messagebox as tkms
import mainDataFlow as mdf
import resourcePlanner as rp
import projects as p
from functools import partial


employer = mdf.load_saveFile()
projectsList = ["None"] + [x.name for x in employer[1]]

def findEmployeeObjects(employees, employerList): #Just like check names but for a list
    foundList = []
    for x in employees:                           #TO DO Needs to be made more effiecient
        foundList.append(mdf.checkNames(x, employerList))

    return foundList

top = tk.Tk()

top.title("Projects")
top.geometry("400x400")


variable = tk.StringVar(top) #variable relating to current project selected
variable.set(projectsList[0])
f1 = tk.Frame(top, height = 400, width = 100, bg = "green")
f1.pack(side = "right", expand = "true", fill = "both")
f11 = tk.Frame(f1, height = 45, width = 100, bg = "#dbdbd3")
f12 = tk.Frame(f1, height = 355, width = 100, bg = "#dbdbd3")
f11.pack(side = "top", expand = "true", fill = "both")
f12.pack(side = "bottom", expand = "true", fill = "both")
f2 = tk.Frame(top,height = 400, width = 300)
f2.pack(side = "left", expand = "true", fill = "both")
f21 = tk.Frame(f2,height = 75,width = 300, bg = "#dbdbd3")
f21.pack(side = "top", expand = "true", fill = "both")
f21.grid_propagate(False)
f22 = tk.Frame(f2, height = 250, width = 300, bg = "red")
f22.pack(expand = "true", fill = "both")
f23 = tk.Frame(f2, height = 75, width = 300, bg = "#dbdbd3")
f23.pack(side = "bottom", expand = "true", fill = "both")
tskslbl = tk.Label(f11, text = "Tasks", bg = "#dbdbd3")
tskslbl.pack(fill = "both", expand = "true")
#################################Tasks Frame####################################
canvas_container=tk.Canvas(f12, height=355,width=100, highlightbackground="gray", bg = "#dbdbd3")
myscrollbar=tk.Scrollbar(f12,orient="vertical",command=canvas_container.yview)

def create_TaskBar():
    canvas_container.delete("all")
    frame2=tk.Frame(canvas_container)
    
    canvas_container.create_window((0,0),window=frame2,anchor='nw')

    def createTaskWindow(name):
        if variable.get() != "None":   
            currentProject = employer[1][(projectsList.index(variable.get()))-1]
            tasks = currentProject.tasks
            for x in tasks:
                if x.name == name:
                    popout = tk.Tk()
                    tk.Label(popout, text = x.name).pack()
                    tk.Label(popout, text = x.description).pack()
                    popout.mainloop()
    if variable.get() != "None": 
        mylist = [x.name for x in employer[1][(projectsList.index(variable.get()))-1].tasks]
        for item in mylist:
            button = tk.Button(frame2,text=item,
                               width = 15,height = 4,
                               command= lambda item=item: createTaskWindow(item),
                               wraplength=80,justify="left")
            button.pack(expand = "true", fill = "both")

    frame2.update() # update frame2 height so it's no longer 0 ( height is 0 when it has just been created )
    canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height()) # the scrollregion mustbe the size of the frame inside it,                                                                                                           #in this case "x=0 y=0 width=0 height=frame2height"                                                                                                           #width 0 because we only scroll verticaly so don't mind about the width
    canvas_container.pack(side="left", expand ="true", fill = "both")
    myscrollbar.pack(side="right", fill = "y")

create_TaskBar()
#############################Skill Extrapolation Below##########################
skillCanvas = tk.Canvas(f22, height = 250, width = 300, bg = "#dbdbd3", highlightthickness=0)
xbar=tk.Scrollbar(f22,orient="horizontal",command=skillCanvas.xview)
def createGraphs():
    skillCap = [0,0,0]
    if variable.get() != "None":
        tempEmpList = employer[1][(projectsList.index(variable.get()))-1].employees
        for x in tempEmpList:
            for y,z in enumerate(x.skillset):
                skillCap[y] += int(z[1])

        maximum = max(skillCap)

        def giveGraphColor(string):
            num = int(string)
            if num > 66:
                return "green"
            elif num > 33:
                return "yellow"
            else:
                return "red"
    
        x_initial = 35
        x_gap = 30
        x_width = 45


        for x in range(len(skillCap)):
            skillCanvas.create_rectangle(x_initial, 25,
                                         x_initial+x_width,
                                         225, fill = "white")
            skillCanvas.create_rectangle(x_initial, 225,
                                         x_initial+x_width,
                                         225 - (200 * ( skillCap[x] / (10 * len(tempEmpList)))),
                                         fill = giveGraphColor(100 * ( skillCap[x] / (10 * len(tempEmpList)))))
            x_initial += x_gap + x_width

    else:
        x_initial = 35
        x_gap = 30
        x_width = 45


        for x in range(len(skillCap)):
            skillCanvas.create_rectangle(x_initial, 25,
                                         x_initial+x_width,
                                         225, fill = "white")
            x_initial += x_gap + x_width

    x_initial += 15

    skillCanvas.configure(xscrollcommand=xbar.set, scrollregion=(0,0,x_initial,f22.winfo_height()))
    skillCanvas.pack(expand = "true", fill = "both")
    xbar.pack(side="bottom", fill = "x")

createGraphs()

def loadButton():
    createGraphs()
    create_TaskBar()

#################################TOP FRAME BELOW################################
title = tk.Label(f21, bg = "#dbdbd3", text = "Projects View \n Choose Project and Load It")
title.grid(row = 0, columnspan = 2)
w = tk.OptionMenu(f21, variable, *projectsList)
w["highlightthickness"]=0
w.grid(row = 1, column = 0, pady = 2,sticky = "NSEW")

def newButton():
    proWindow = tk.Tk()
    name = tk.Entry(proWindow)
    name.grid(row = 0, column = 1)
    name1 = tk.Label(proWindow,text = "Name").grid(row = 0, column = 0)
    hours = tk.Entry(proWindow)
    hours.grid(row = 1, column = 1)
    hours1 = tk.Label(proWindow,text = "Hours").grid(row = 1, column = 0)
    employees = tk.Entry(proWindow)
    employees.grid(row = 2, column = 1)
    employees1 = tk.Label(proWindow,text = "Employees").grid(row = 2, column = 0)


    def newProject():
        newProject = p.project(name.get(), findEmployeeObjects(employees.get().split(','),employer[0]), hours.get())
        employer[1].append(newProject)
        projectsList.append(name.get())
        mdf.write_saveFile(employer[0], employer[1])
        proWindow.destroy()
    

    butt = tk.Button(proWindow, text = "Create New Project",
                 command = newProject).grid(row = 3, column = 1)

    proWindow.mainloop()

submit = tk.Button(f21,text = "Load Project", command = loadButton)
submit.grid(row = 2, column = 0, pady = 2, sticky = "NSEW")
newPro = tk.Button(f21, text = "Create Project", command = newButton)
newPro.grid(row = 1, column = 1, pady = 2, sticky = "NSEW")
exportPro = tk.Button(f21, text = "Export Project")
exportPro.grid(row = 2, column = 1, pady = 2, sticky = "NSEW")
f21.rowconfigure(0, weight = 1)
f21.rowconfigure(1, weight = 1)
f21.rowconfigure(2, weight = 1)
f21.columnconfigure(0, weight = 1)
f21.columnconfigure(1, weight = 1)

### Bottom Frame
empList = tk.Button(f23, text = "Employees")
empList.grid(row = 0, column = 0, pady = 1, padx = 1, sticky = "NSEW")
utilButton = tk.Button(f23, text = "Utilization")
utilButton.grid(row = 1, column = 0, pady = 1, padx = 1, sticky = "NSEW")
addEmp = tk.Button(f23, text = "Add Employee")
addEmp.grid(row = 0, column = 1, pady = 1, padx = 1, sticky = "NSEW")
removeEmp = tk.Button(f23, text = "Remove Employee")
removeEmp.grid(row=1,column=1, pady = 1, padx = 1,sticky="NSEW")
addTask = tk.Button(f23,text = "Add Task")
addTask.grid(row = 0, column = 2, pady = 1, padx = 1, sticky = "NSEW")
removeTask = tk.Button(f23,text = "Remove Task")
removeTask.grid(row = 1, column = 2, pady = 1, padx = 1, sticky = "NSEW")

f23.rowconfigure(0, weight = 1)
f23.columnconfigure(1, weight = 1)
f23.columnconfigure(2, weight = 1)

top.mainloop()


import tkinter as tk
import tkinter.messagebox as tkms
import mainDataFlow as mdf
import resourcePlanner as rp
import projects as p
import tasks as t
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
            for y,x in enumerate(tasks):
                if x.name == name:
                    popout = tk.Tk()
                    popout.title("Task Creation")
                    popout.resizable(0,0)
                    tsktype = tk.StringVar(popout)
                    tsktype.set(x.taskType)
                    prio = tk.StringVar(popout)
                    prio.set(x.priority)
                    tk.Label(popout,text = "Name").grid(row = 0, column = 0)
                    e1 = tk.Entry(popout)
                    e1.insert(0, x.name)
                    e1.grid(row = 0,column = 1)
                    tk.Label(popout,text = "Task Type").grid(row = 1, column =0)
                    ttList = ["To Do", "Bug", "Story", "Epic", "New Feature", "Decision", "Question"]
                    tk.OptionMenu(popout, tsktype, *ttList).grid(row = 1, column = 1)
                    prioList = ["Lowest", "Low", "Medium", "High", "Highest"]
                    tk.Label(popout,text = "Priority").grid(row = 2, column = 0)
                    tk.OptionMenu(popout, prio, *prioList).grid(row = 2, column = 1)
                    tk.Label(popout, text = "Assignee").grid(row = 3, column = 0)
                    e3 = tk.Entry(popout)
                    e3.insert(0, x.assignee)
                    e3.grid(row=3, column = 1)
                    tk.Label(popout, text = "Reporter").grid(row = 4, column = 0)
                    e4 = tk.Entry(popout)
                    e4.insert(0, x.reporter)
                    e4.grid(row = 4, column = 1)
                    tk.Label(popout,text = "Description").grid(row=5, column = 0, columnspan = 2)
                    box = tk.Text(popout, height = 5, width = 23, font = ("TkDefaultFont", 9))
                    box.insert(tk.END, x.description)
                    box.grid(row=6, column = 0, columnspan = 2)
                    
                    def confirmChange():
                        
                        employer[1][(projectsList.index(variable.get()))-1].tasks[y].changeFullTask(
                            e1.get(), variable.get(), tsktype.get(), prio.get(), e3.get(),e4.get(),box.get("1.0","end"))
                        loadButton()
                        mdf.write_saveFile(employer[0],employer[1])
                        popout.destroy()
            
                    tk.Button(popout,text = "Confirm Changes", command = confirmChange).grid(row = 10, column = 0, columnspan = 2)
                    
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
                return "#90de47"
            elif num > 33:
                return "#faf393"
            else:
                return "#fa8787"
    
        x_initial = 35
        x_gap = 30
        x_width = 45
        skillCanvas.create_text(55,18,text = "Computers")
        skillCanvas.create_text(133,18,text = "Programming")
        skillCanvas.create_text(208,18,text = "Scripting")

        if tempEmpList == []:
            for x in range(len(skillCap)):
                skillCanvas.create_rectangle(x_initial, 25,
                                             x_initial+x_width,
                                             225, fill = "white")
                x_initial += x_gap + x_width
        else:
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

def refresh(new_choices, name):
    variable.set(name)
    w['menu'].delete(0, 'end')
    for x in new_choices:
        w['menu'].add_command(label=x, command=tk._setit(variable, x))

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
        if employees.get() == "":
            newProject = p.project(name.get(),[],hours.get())
            employer[1].append(newProject)
            projectsList.append(name.get())
            refresh(["None"] + [x.name for x in employer[1]], newProject.name)
            loadButton()

        else:
            newProject = p.project(name.get(), findEmployeeObjects(employees.get().split(','),employer[0]), hours.get())
            employer[1].append(newProject)
            projectsList.append(name.get())
            refresh(["None"] + [x.name for x in employer[1]], newProject.name)
            loadButton()

        mdf.write_saveFile(employer[0], employer[1])
        proWindow.destroy()
    

    butt = tk.Button(proWindow, text = "Create New Project",
                 command = newProject).grid(row = 3, column = 1)

    proWindow.mainloop()

def delProject():
    if variable.get() != "None":
        popout = tkms.askyesno(title="Confirm Delete", message="Are you sure you want to delete " + variable.get() + "?")
        if popout == True:
            employer[1].pop((projectsList.index(variable.get()))-1)
            projectsList.pop(projectsList.index(variable.get())-1)                                                    
            mdf.write_saveFile(employer[0], employer[1])
            refresh(["None"] + [x.name for x in employer[1]], "None")
            loadButton()

            
submit = tk.Button(f21,text = "Load Project", command = loadButton)
submit.grid(row = 2, column = 0, pady = 2, sticky = "NSEW")
newPro = tk.Button(f21, text = "Create Project", command = newButton)
newPro.grid(row = 1, column = 1, pady = 2, sticky = "NSEW")
exportPro = tk.Button(f21, text = "Delete Project", command = delProject)
exportPro.grid(row = 2, column = 1, pady = 2, sticky = "NSEW")
f21.rowconfigure(0, weight = 1)
f21.rowconfigure(1, weight = 1)
f21.rowconfigure(2, weight = 1)
f21.columnconfigure(0, weight = 1)
f21.columnconfigure(1, weight = 1)

### Bottom Frame

#Functions That Buttons Use
def listOEmp():
    if variable.get() != "None":
        popout = tk.Tk()
        emps = employer[1][(projectsList.index(variable.get()))-1].employees
        tk.Label(popout, text = "List of Employees").pack()
        for x in emps:
            tk.Label(popout, text = x.name).pack()
        popout.mainloop()

def addEmp2():
    if variable.get() != "None":
        
        currentProject = employer[1][(projectsList.index(variable.get()))-1]
        employeeList = []
        nameList = []
        for x in employer[0]:
            if x not in currentProject.employees:
                employeeList.append(x)
                nameList.append(x.name)

        if nameList == []:
            tkms.showerror(title="Error!", message = "No Employees left to add!")
        else:
            popout = tk.Tk()
            tk.Label(popout, text = "Select Employee to Add").pack(side = "top")
            empName = tk.StringVar(popout)
            empName.set(nameList[0])
            drop = tk.OptionMenu(popout, empName, *nameList).pack(side = "left")
            def submit():
                employer[1][employer[1].index(currentProject)].employees.append(employeeList[nameList.index(empName.get())])
                loadButton()
                mdf.write_saveFile(employer[0],employer[1])
                popout.destroy()

            tk.Button(popout, text = "Submit", command = submit).pack(side = "right")
            popout.mainloop()

def removeEmp2():
    if variable.get() != "None":

        currentProject = employer[1][(projectsList.index(variable.get()))-1]
        employeeList = currentProject.employees
        if employeeList == []:
            tkms.showerror(title="Error!", message = "No employees exist in this project.")
        else:
            popout = tk.Tk()
            nameList = []
            for x in employeeList:
                nameList.append(x.name)

            tk.Label(popout, text = "Select Employee to Remove").pack(side = "top")
            empName = tk.StringVar(popout)
            empName.set(nameList[0])
            drop = tk.OptionMenu(popout, empName, *nameList).pack(side = "left")
            def submit():
                employer[1][(projectsList.index(variable.get()))-1].employees.pop(nameList.index(empName.get()))
                loadButton()
                mdf.write_saveFile(employer[0],employer[1])
                popout.destroy()

            tk.Button(popout,text = "Submit", command = submit).pack(side = "right")
            popout.rowconfigure(0, weight = 1)
            popout.columnconfigure(0, weight = 1)
            popout.mainloop()
        
def util():
    if variable.get() != "None":
        popout = tk.Tk()
        currentProject = employer[1][(projectsList.index(variable.get()))-1]
        can = tk.Canvas(popout,width = 300, height = 240)
        xbar=tk.Scrollbar(popout,orient="horizontal",command=can.xview)
        x_initial = 40
        x_gap = 40
        x_width = 40

        for x in currentProject.employees:
            x.calculateHours()
            can.create_rectangle(x_initial, 220, x_initial + x_width, 20, fill = "white")
            can.create_rectangle(x_initial, 220, x_initial + x_width, 220 - (220 * ((40 - x.hours)/40))+20, fill = "yellow")
            can.create_rectangle(x_initial, 220, x_initial + x_width, 220 - (220 * (currentProject.hours/40))+20, fill = "blue")
            x_initial = x_initial + x_gap + x_width


        can.configure(xscrollcommand=xbar.set, scrollregion=(0,0,x_initial,f22.winfo_height()))
        can.pack(expand = "true", fill = "both")
        xbar.pack(expand = "true", fill = "x")
        popout.mainloop()

def addTask2():
    if variable.get() != "None":
        popout = tk.Tk()
        popout.title("Task Creation")
        popout.resizable(0,0)
        tsktype = tk.StringVar(popout)
        prio = tk.StringVar(popout)
        tk.Label(popout,text = "Name").grid(row = 0, column = 0)
        e1 = tk.Entry(popout)
        e1.grid(row = 0,column = 1)
        tk.Label(popout,text = "Project").grid(row = 1, column = 0)
        e2 = tk.Entry(popout)
        e2.insert(0, employer[1][(projectsList.index(variable.get()))-1].name)
        e2.grid(row = 1,column = 1)
        tk.Label(popout,text = "Task Type").grid(row = 2, column =0)
        ttList = ["To Do", "Bug", "Story", "Epic", "New Feature", "Decision", "Question"]
        tsktype.set(ttList[0])
        tk.OptionMenu(popout, tsktype, *ttList).grid(row = 2, column = 1)
        prioList = ["Lowest", "Low", "Medium", "High", "Highest"]
        tk.Label(popout,text = "Priority").grid(row = 3, column = 0)
        prio.set(prioList[0])
        tk.OptionMenu(popout, prio, *prioList).grid(row = 3, column = 1)
        tk.Label(popout, text = "Assignee").grid(row = 4, column = 0)
        e3 = tk.Entry(popout)
        e3.grid(row=4, column = 1)
        tk.Label(popout, text = "Reporter").grid(row = 5, column = 0)
        e4 = tk.Entry(popout)
        e4.grid(row = 5, column = 1)
        tk.Label(popout,text = "Description").grid(row=6, column = 0, columnspan = 2)
        box = tk.Text(popout, height = 5, width = 23, font = ("TkDefaultFont", 9))
        box.grid(row=7, column = 0, columnspan = 2)

        def subi():
            tempTask = t.tasks(e1.get(), e2.get(), tsktype.get(), prio.get(), e3.get(),e4.get(),box.get("1.0","end"))
            employer[1][(projectsList.index(variable.get()))-1].tasks.append(tempTask)
            loadButton()
            mdf.write_saveFile(employer[0],employer[1])
            popout.destroy()
            
        tk.Button(popout,text = "Submit", command = subi).grid(row = 10, column = 0, columnspan = 2)
        popout.mainloop()

def removeTask():
    if variable.get != "None":
        currentProjectTasks = employer[1][(projectsList.index(variable.get()))-1].tasks
        cTNames = [x.name for x in currentProjectTasks]
        if currentProjectTasks == []:
            tkms.showerror(title="Error!", message = "No Tasks Exist in the Project!")
        else:
            popout = tk.Tk()
            popout.title("Remove Task")
            tk.Label(popout, text = "Select Task To Remove").pack(side = "top")
            taskName = tk.StringVar(popout)
            taskName.set(cTNames[0])
            tk.OptionMenu(popout, taskName, *cTNames).pack(side = "left")

            def subi():
                tsk_idx = cTNames.index(taskName.get())
                employer[1][(projectsList.index(variable.get()))-1].tasks.pop(tsk_idx)
                loadButton()
                mdf.write_saveFile(employer[0],employer[1])
                popout.destroy()

            tk.Button(popout,text = "Submit", command = subi).pack(side = "right")
            popout.mainloop()
    


empList = tk.Button(f23, text = "Employees", command = listOEmp) #done/make better popout
empList.grid(row = 0, column = 0, pady = 1, padx = 1, sticky = "NSEW")
utilButton = tk.Button(f23, text = "Utilization", command=util)
utilButton.grid(row = 1, column = 0, pady = 1, padx = 1, sticky = "NSEW")
addEmp = tk.Button(f23, text = "Add Employee", command=addEmp2) #done/make better popout
addEmp.grid(row = 0, column = 1, pady = 1, padx = 1, sticky = "NSEW")
removeEmp = tk.Button(f23, text = "Remove Employee", command = removeEmp2) #done/make better popout
removeEmp.grid(row=1,column=1, pady = 1, padx = 1,sticky="NSEW")
addTask = tk.Button(f23,text = "Add Task",command=addTask2)
addTask.grid(row = 0, column = 2, pady = 1, padx = 1, sticky = "NSEW")
removeTask = tk.Button(f23,text = "Remove Task", command = removeTask)
removeTask.grid(row = 1, column = 2, pady = 1, padx = 1, sticky = "NSEW")

f23.rowconfigure(0, weight = 1)
f23.columnconfigure(1, weight = 1)
f23.columnconfigure(2, weight = 1)

top.mainloop()


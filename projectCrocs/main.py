import tkinter as tk
import tkinter.messagebox as tkms
from tkinter import ttk
import mainDataFlow as mdf
import resourcePlanner as rp
from fileReader import read_file2
import projects as p
import tasks as t
from functools import partial
import os


#employer = mdf.load_saveFile()

main = tk.Tk()
main.geometry("400x420")
f1 = tk.Frame(main, height = 20, width = 400, bg = "#dbdbd3")
f1.pack(side = "top", fill = "both", expand = "true")
f2 = tk.Frame(main, height = 400, width = 400)
f2.pack(side = "bottom")


def switchFrame(frame):
    
    for x in f2.winfo_children():
        
        x.destroy()
    new_frame = frame(f2)

tk.Button(f1, text = "Employees", command = lambda: switchFrame(employeeFrame)).pack(side = "left")
tk.Button(f1, text = "Projects", command = lambda: switchFrame(projectFrame)).pack(side = "left")

class projectFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

                
        employer = mdf.load_saveFile()
        projectsList = ["None"] + [x.name for x in employer[1]]

        def findEmployeeObjects(employees, employerList): #Just like check names but for a list
            foundList = []
            for x in employees:                           #TO DO Needs to be made more effiecient
                foundList.append(mdf.checkNames(x, employerList))

            return foundList


        variable = tk.StringVar(parent) #variable relating to current project selected
        variable.set(projectsList[0])


        f1 = tk.Frame(parent, height = 400, width = 100, bg = "green")
        f1.pack(side = "right", expand = "true", fill = "both")
        f11 = tk.Frame(f1, height = 45, width = 100, bg = "#dbdbd3")
        f12 = tk.Frame(f1, height = 355, width = 100, bg = "#dbdbd3")
        f11.pack(side = "top", expand = "true", fill = "both")
        f12.pack(side = "bottom", expand = "true", fill = "both")
        f2 = tk.Frame(parent,height = 400, width = 300)
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
                                mdf.write_saveFile(employer[0],employer[1], employer[2])
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
                        skillCap[y] += int(z)

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

                mdf.write_saveFile(employer[0], employer[1], employer[2])
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
                    mdf.write_saveFile(employer[0], employer[1], employer[2])
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
                        mdf.write_saveFile(employer[0],employer[1], employer[2])
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
                        mdf.write_saveFile(employer[0],employer[1], employer[2])
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
                    can.create_rectangle(x_initial, 220, x_initial + x_width, 220 - (220 * ((40 - x.hours)/40))+20, fill = "black")
                    can.create_rectangle(x_initial, 220, x_initial + x_width, 220 - (220 * (currentProject.hours/40))+20, fill = "red")
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
                    mdf.write_saveFile(employer[0],employer[1], employer[2])
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
                        mdf.write_saveFile(employer[0],employer[1], employer[2])
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

        def buttonDisable(*args):
            if variable.get() == "None":
                empList["state"] = "disabled"
                utilButton["state"] = "disabled"
                removeEmp["state"] = "disabled"
                addTask["state"] = "disabled"
                removeTask["state"] = "disabled"
                addEmp["state"] = "disabled"
                submit["state"] = "disabled"
                exportPro["state"] = "disabled"

            else:
                empList["state"] = "normal"
                utilButton["state"] = "normal"
                removeEmp["state"] = "normal"
                addTask["state"] = "normal"
                removeTask["state"] = "normal"
                addEmp["state"] = "normal"
                submit["state"] = "normal"
                exportPro["state"] = "normal"

        variable.trace("w", buttonDisable)
        f23.rowconfigure(0, weight = 1)
        f23.columnconfigure(1, weight = 1)
        f23.columnconfigure(2, weight = 1)

        if variable.get() == "None":
                empList["state"] = "disabled"
                utilButton["state"] = "disabled"
                removeEmp["state"] = "disabled"
                addTask["state"] = "disabled"
                removeTask["state"] = "disabled"
                addEmp["state"] = "disabled"
                submit["state"] = "disabled"
                exportPro["state"] = "disabled"


class employeeFrame(ttk.Frame):
    def __init__(self, parent):
        #THIS GUI IS FOR SHOWING OFF CODE NICELY
        employer = mdf.load_saveFile()


        def giveColor(string):
            if string.isnumeric():
                x = int(string)
                if x < 3:
                    return "#fa8787"
                elif x < 7:
                    return "#faf393"
                else:
                    return "#90de47"
                
            else:
                return "white"

        #Window/Frame design


        f1 = tk.Frame(parent, height = 300, width = 400)
        f1.pack(side = "top")
        f12 = tk.Frame(f1, height = 300, width = 300)
        f12.pack(side = "right")
        f12.grid_propagate(False)
        f11 = tk.Frame(f1, height = 300, width = 100, bg = "#dbdbd3")
        f11.pack(side ="left")
        f11.grid_propagate(False)
        f2 = tk.Frame(parent, height = 100, width = 400, bg = "green")
        f2.pack(side = "bottom")


        
        def makeRaci(employees):

            test = rp.raciMatrix("test", employees,employer[2])
            test.populateMatrix()
            #Visualising the matrix

            for i in range(len(test.raci)):
                for j in range(len(test.raci[0])):
                        e = tk.Label(f12, text = str(test.raci[i][j]),
                            bg = giveColor(str(test.raci[i][j])), relief="sunken")
                        e.grid(row=i, column=j, sticky = "NSEW")
                        f12.columnconfigure(j, weight = 1)
                f12.rowconfigure(i, weight = 1)


        makeRaci(employer[0])

        #Button Commands
        def addEmploy(): #Current Column Entry for skills should go Skill,Proficiency,Skill,Proficiency
            popout = tk.Tk()
            popout.resizable(False,False)
            popout.configure(bg="#dbdbd3")
            popout.title("Add Employee")
            nam = tk.Label(popout, text = "Name",bg="#dbdbd3")
            nam.grid(row = 0, column = 0)
            name = tk.Entry(popout,highlightbackground = "#dbdbd3")
            name.grid(row = 0, column = 1,sticky = "NSEW")
            dep = tk.Label(popout, text = "Department",bg="#dbdbd3")
            dep.grid(row = 1, column = 0)
            depart = tk.Entry(popout,highlightbackground = "#dbdbd3")
            depart.grid(row = 1, column = 1)
            skil = tk.Label(popout, text = "Skills",bg="#dbdbd3")
            skil.grid(row = 2, column = 0)
            skills = tk.Entry(popout,highlightbackground = "#dbdbd3")
            skills.grid(row = 2, column = 1)
            def subi():
                if len(name.get()) == 0:
                    tkms.showerror(title ="No Name", message = "Must input a name!")
                    
                elif len(depart.get()) == 0:
                    tkms.showerror(title ="No Department", message = "Must input a department!")
                else:
                    x = skills.get().split(',')
                    #newEmp = rp.employee(name.get(), depart.get(), [*zip(x[::2], x[1::2])])
                    newEmp = rp.employee(name.get(), depart.get(), x)
                    employer[0].append(newEmp)
                    mdf.write_saveFile(employer[0],employer[1], employer[2])
                    makeRaci(employer[0])
                    createUtilBar(employer[0])
                    popout.destroy()
                    
            submit = tk.Button(popout, text = "Submit",highlightbackground = "#dbdbd3", command=subi)
            submit.grid(row = 3, column = 1)
            
            popout.mainloop()

        def loadSkillSheet(): #Needs .txt file in csv format
            popout = tk.Tk()
            popout.title("Load Skills")
            instruct = tk.Label(popout, text = "Enter File Name: Format: filename.txt \n Must be in a txt file (Can convert using notepad++)") 
            instruct.pack()
            field = tk.Entry(popout)
            field.pack()
            

            def subi():
                if employer[0] == []:
                    file = read_file2(field.get())
                    employer[0] = rp.createEmployeeObjects(file[0])
                    employer[2] = file[1]
                    mdf.write_saveFile(employer[0],employer[1], employer[2])
                    switchFrame(employeeFrame)
                    makeRaci(employer[0])
                    createUtilBar(employer[0])
                    popout.destroy()

                else:
                    file = read_file2(field.get())
                    empObj = rp.createEmployeeObjects(file[0])
                    empNames = [x.name for x in employer[0]]
                    for x in empObj:
                        if x.name in empNames:
                            idx = empNames.index(x.name)
                            employer[0][idx].skillset = x.skillset
                        else:
                            employer[0].append(x)

                    mdf.write_saveFile(employer[0],employer[1], employer[2])
                    switchFrame(employeeFrame)
                    makeRaci(employer[0])
                    createUtilBar(employer[0])
                    popout.destroy()
            


            tk.Button(popout,text = "Submit", command = subi).pack()
            popout.mainloop()

        def removeEmploy(): #Just needs a name 
            popout = tk.Tk()
            popout.title("Remove Employee")
            instruct = tk.Label(popout, text = "Enter Employee Name")
            name = tk.Entry(popout,highlightbackground = "#dbdbd3")
            def subi():
                for x,y in enumerate(employer[0]):
                    if name.get() == y.name:
                        employer[0].pop(x)
                        for z in f12.winfo_children():
                            z.destroy()

                        
                        mdf.write_saveFile(employer[0],employer[1], employer[2])
                        switchFrame(employeeFrame)
                        makeRaci(employer[0])
                        createUtilBar(employer[0])
                        popout.destroy()
                        
            butt = tk.Button(popout,text = "Submit",command=subi)
            instruct.pack()
            name.pack()
            butt.pack()
            popout.mainloop()

        def expandRa():
            popout = tk.Tk()
            
            def makeRa(employees):

                test = rp.raciMatrix("test", employees,employer[2])
                test.populateMatrix()
                #Visualising the matrix

                for i in range(len(test.raci)):
                    for j in range(len(test.raci[0])):
                            e = tk.Label(popout, text = str(test.raci[i][j]),
                                bg = giveColor(str(test.raci[i][j])), relief="sunken")
                            e.grid(row=i, column=j, sticky = "NSEW")
                            popout.columnconfigure(j, weight = 1)
                    popout.rowconfigure(i, weight = 1)

            makeRa(employer[0])
            

        #All the Buttons on the left hand side
        addEmp = tk.Button(f11, text = "Add Employee", command = addEmploy,
                           highlightbackground = "#dbdbd3")
        loadSkills = tk.Button(f11, text = "Load Skills",command = loadSkillSheet,
                               highlightbackground = "#dbdbd3")
        removeEmp = tk.Button(f11, text = "Remove Employee", command = removeEmploy,
                              highlightbackground = "#dbdbd3")
        expandRaci = tk.Button(f11, text = "Expand Raci", command = expandRa,
                               highlightbackground = "#dbdbd3")
        addEmp.grid(row = 0, column = 0, pady = 20, sticky = "EW")
        loadSkills.grid(row = 1, column = 0, pady = 20, sticky = "EW")
        removeEmp.grid(row = 2, column = 0, pady = 20, sticky = "EW")
        expandRaci.grid(row = 3, column = 0, pady = 20, sticky = "EW")
        f11.columnconfigure(0, weight = 1)
        for x in range(0,2):
            f11.rowconfigure(x, weight = 1)

        #The bar at the bottom
        canvas = tk.Canvas(f2, width = 400, height = 100, bd = 0, highlightthickness=0,bg = "#dbdbd3")
        canvas.pack()
        def createUtilBar(employees):
            canvas.delete("all")
            totalUtil = rp.totalUtil(employees)
            canvas.create_rectangle(35,25,365,75, fill = "white")
            canvas.create_rectangle(35,25,int(330 * totalUtil + 35), 75, fill = "#faf393")
            canvas.create_text(35,25,anchor=tk.SW,text ="Total Utilization")
            canvas.create_text(int(330 * totalUtil + 35) + 5, 82, text = str(round(totalUtil*100)) + "%")
        createUtilBar(employer[0])





ef = employeeFrame(f2)

































"""
#utiliziation
c_width = 500
c_height = 500
c = tk.Canvas(main, width = c_width, height = c_height, bg = "white",scrollregion=(0,0,main.winfo_screenwidth(),500))
hbar=tk.Scrollbar(main, orient = "horizontal")
hbar.pack(side = "bottom", fill = "x")
hbar.config(command=c.xview)
c.config(xscrollcommand=hbar.set)
c.pack(fill = "both", expand = True,side = "left")

y_stretch = 5
y_gap = 20
x_stretch = 40
x_width = 40
x_gap = 15

for x in employer[0]:
    x.calculateHours()


for x, y in enumerate(employer[0]):
    x0 = x * x_stretch + x * x_width + x_gap
    y0 = c_height - ((((40 - y.hours) / 40) * 100) * y_stretch + y_gap)
    x1 = x * x_stretch + x * x_width + x_width + x_gap
    y1 = c_height - y_gap + 2
    c.create_rectangle(x0, y0, x1, y1, fill = giveColor(str((40 - y.hours) // 4)))
    c.create_text(x0+2, y0, anchor=tk.SW, text = str(((40 - y.hours) / 40) * 100) + "%")
    c.create_text(x0, y1 + 15, anchor=tk.SW, text = y.name)


"""

main.mainloop()

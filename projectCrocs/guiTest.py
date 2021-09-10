import tkinter as tk
import tkinter.messagebox as tkms
import sys
import os
sys.path.append("/Users/anthompson/Desktop/Python Stuff/projectCrocs")
import resourcePlanner as rp
import projects as p
import mainDataFlow as mdf

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
top = tk.Tk()


top.title("Mark's Resource Planner")
top.geometry("400x400")
top.resizable(False, False)
f1 = tk.Frame(top, height = 300, width = 400)
f1.pack(side = "top")
f12 = tk.Frame(f1, height = 300, width = 300)
f12.pack(side = "right")
f12.grid_propagate(False)
f11 = tk.Frame(f1, height = 300, width = 100, bg = "#dbdbd3")
f11.pack(side ="left")
f11.grid_propagate(False)
f2 = tk.Frame(top, height = 100, width = 400, bg = "green")
f2.pack(side = "bottom")


def makeRaci(employees):

    test = rp.raciMatrix("test", employees)
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
            print("nope") #add error message
        elif len(depart.get()) == 0:
            print("no") #add error message
        else:
            x = skills.get().split(',')
            newEmp = rp.employee(name.get(), depart.get(), [*zip(x[::2], x[1::2])])
            employer[0].append(newEmp)
            mdf.write_saveFile(employer[0],employer[1])
            makeRaci(employer[0])
            createUtilBar(employer[0])
            popout.destroy()
            
    submit = tk.Button(popout, text = "Submit",highlightbackground = "#dbdbd3", command=subi)
    submit.grid(row = 3, column = 1)
    
    popout.mainloop()

def loadSkillSheet(): #Needs .txt file in csv format
    popout = tk.Tk()
    popout.title("Load Skills")
    instruct = tk.Label(popout, text = "Enter File Name: Format: filename.txt")
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
                for x in f12.winfo_children():
                    x.destroy()

                makeRaci(employer[0])
                createUtilBar(employer[0])
                popout.destroy()
                
    butt = tk.Button(popout,text = "Submit",command=subi)
    instruct.pack()
    name.pack()
    butt.pack()
    popout.mainloop()

#All the Buttons on the left hand side
addEmp = tk.Button(f11, text = "Add Employee", command = addEmploy,
                   highlightbackground = "#dbdbd3")
loadSkills = tk.Button(f11, text = "Load Skills",command = loadSkillSheet,
                       highlightbackground = "#dbdbd3")
removeEmp = tk.Button(f11, text = "Remove Employee", command = removeEmploy,
                      highlightbackground = "#dbdbd3")
addEmp.grid(row = 0, column = 0, pady = 40, sticky = "EW")
loadSkills.grid(row = 1, column = 0, pady = 40, sticky = "EW")
removeEmp.grid(row = 2, column = 0, pady = 40, sticky = "EW")
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

print(employer[1][0].tasks[1].name)

top.mainloop()

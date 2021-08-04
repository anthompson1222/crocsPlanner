import tkinter as tk
import tkinter.messagebox as tkms
import sys
sys.path.append("/Users/anthompson/Desktop/Python Stuff/projectCrocs")
import mainDataFlow as mdf
import resourcePlanner as rp

employer = mdf.load_saveFile()

def giveColor(string):
    if string.isnumeric():
        x = int(string)
        if x < 3:
            return "red"
        elif x < 7:
            return "yellow"
        else:
            return "green"
        
    else:
        return "white"

employerMatrix = rp.raciMatrix("EmployerMatrix", employer[0])
employerMatrix.populateMatrix()

main = tk.Tk()
main.title("Bar Graph")
"""
f2 = tk.Frame(main, width = 400, height = 200)
f2.pack(side = "top", expand = "yes", fill = "both")
f3 = tk.Frame(f2)
f3.pack(side = "left", expand = "yes", fill = "both")
f4 = tk.Frame(f2)
f4.pack(side = "right", expand = "yes", fill = "both")
f1 = tk.Frame(main, width = 400, height = 200)
f1.pack(side = "bottom", expand = "yes", fill = "both")
"""

"""
#employees
for i in range(len(employerMatrix.raci)):
    for j in range(len(employerMatrix.raci[0])):
        e = tk.Label(f3, text = str(employerMatrix.raci[i][j]),
                     width = 200 // (len(employerMatrix.raci[0]) * 100),
                     height = 200 // (len(employerMatrix.raci) * 100),
                     bg = giveColor(str(employerMatrix.raci[i][j])), relief="sunken")
        e.grid(row=i, column=j, sticky = "NSEW")
        main.grid_columnconfigure(j,weight=1)
    main.grid_rowconfigure(i,weight=1)
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
#project section
projectsList = ["None"] + [x.name for x in employer[1]]
mf = tk.Frame(f4)
mf.pack()
sf = tk.Frame(f4)

variable = tk.StringVar(mf)
variable.set(projectsList[0])
w = tk.OptionMenu(mf, variable, *projectsList)
w.pack()

def ok():
    for child in sf.winfo_children():
        child.destroy()
    
    sf.pack()
    if variable.get() != "None":
        currentProject = employer[1][projectsList.index(variable.get())-1]
        label1 = tk.Label(sf, text = currentProject.name).pack()
        label2 = tk.Label(sf, text = str(currentProject.hours) + " hours").pack()
        label3 = tk.Label(sf, text = "Employee Utilization").pack()
        c_width = 500
        c_height = 500
        c = tk.Canvas(sf, width = c_width, height = c_height, bg = "white",scrollregion=(0,0,main.winfo_screenwidth(),500))
        hbar=tk.Scrollbar(sf, orient = "horizontal")
        hbar.pack(side = "bottom", fill = "x")
        hbar.config(command=c.xview)
        c.config(xscrollcommand=hbar.set)
        c.pack(fill = "both", expand = True,side = "left")

        y_stretch = 5
        y_gap = 20
        x_stretch = 40
        x_width = 40
        x_gap = 15

        for x in currentProject.employees:
            x.calculateHours()
        #some inneficiency here i think

        for x, y in enumerate(currentProject.employees):
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - ((((40 - y.hours) / 40) * 100) * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap + 2
            c.create_rectangle(x0, y0, x1, y1, fill = "black")
            c.create_text(x0+2, y0, anchor=tk.SW, text = str(((40 - y.hours) / 40) * 100) + "%")
            c.create_text(x0, y1 + 15, anchor=tk.SW, text = y.name)
            
submit = tk.Button(mf, text = "Submit", command = ok)
submit.pack()
"""


main.mainloop()

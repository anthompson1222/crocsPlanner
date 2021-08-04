import fileReader as fr

class tasks:

    def __init__ (self, name, project, taskType, priority, assignee, reporter, description):
        self.name = name
        self.project = project
        self.taskType = taskType
        self.priority = priority
        self.assignee = assignee
        self.reporter = reporter
        self.description = description


    def changeTaskName(self, name):
        self.name = name

    def changeTaskType(self, taskType):
        self.taskType = taskType


l = fr.read_tasks("tasks.txt")
#print(l)
fr.write_tasks(l)

        
        

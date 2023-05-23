import tkinter as tk
from tkinter import ttk
import sqlite3
import os

#Basewindow is the class I use for the windows
class BaseWindow():
    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.widgets = []
        self.tempWidgets = []
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.admin = False

    def Run(self):
        self.root.mainloop()
    
    def ClearScreen(self):
        for widget in self.widgets:
            widget.destroy()
        for widget in self.tempWidgets:
            widget.destroy()
        self.widgets = []
    
    def destroy(self):
        self.root.destroy()
        
#This class holds the label widget and important functions for it. 
class LabelWidget(BaseWindow):
    def __init__(self, root, text, size, x, y, width=None, height=None, bg=None, fg=None):
        self.label = tk.Label(root, text=text, font=("Arial", size), width=width, height=height, bg=bg, fg=fg)
        self.label.place(x=x, y=y)
        
    def destroy(self):
        self.label.destroy()

#This class holds the button widget and important functions for it. 
class ButtonWidget(BaseWindow):
    def __init__(self, root, text, x, y, executedFunction, height, width, textSize):
        self.button = tk.Button(root, text=text, command=executedFunction, height=height, width=width,
                                font=("Arial", textSize))
        self.button.place(x=x, y=y)
        
    def destroy(self):
        self.button.destroy()

#This class holds the option widget and important functions for it. 
class OptionMenu(BaseWindow):
    def __init__(self, root, values, x, y):
        self.variable = tk.StringVar()
        self.variable.set(values[0])
        self.dropdown = ttk.Combobox(root, values=values, state="readonly")
        self.dropdown.place(x=x, y=y)
        
    def destroy(self):
        self.dropdown.destroy()

#This class holds the entry widget and important functions for it. 
class Entry(BaseWindow):
    def __init__(self, root, text, x, y, width, height):
        self.Entry = tk.Entry(root, width=width)
        self.Entry.insert(0, text)
        self.Entry.place(x=x, y=y, height=height)
        
    def destroy(self):
        self.button.destroy()

#This class holds the text widget and important functions for it. 
class Text(BaseWindow):
    def __init__(self, root, text, x, y, width, height):
        self.Text = tk.Text(root, width=width)
        self.Text.insert("0.0", text)
        self.Text.place(x=x, y=y, height=height)
        
    def destroy(self):
        self.Text.destroy()

#This class holds the scrollable window widget and important functions for it. 
class ScrollableWindow(BaseWindow):
    def __init__(self, root, width, height, x, y):
        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.place(x=x, y=y)
        
        self.scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(x=x + width, y=y, height=height)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        
        self.scrollable_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
    def destroy(self):
        self.canvas.destroy()
        


#This class is a subclass of the basewindow, with more functions relevant to its usecase such as instantiating the
#previously made widget classes
class Windows(BaseWindow):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        
    def AddLabel(self, passedText, size, x, y, isTemporary, width=None, height=None, bg=None, fg=None):
        label = LabelWidget(self.root, passedText, size, x, y, width, height, bg, fg)
        if isTemporary:
            self.tempWidgets.append(label.label)
        else: 
            self.widgets.append(label.label)
    
    def AddButton(self, text, x, y, executedFunction, height, width, textSize, isTemporary):
        button = ButtonWidget(self.root, text, x, y, executedFunction, height, width, textSize)
        if isTemporary:
            self.tempWidgets.append(button.button)  
        else:
            self.widgets.append(button.button)
        
    def AddEntry(self, text, x, y, width, height):
        textBox = Entry(self.root, text, x, y, width, height)
        self.widgets.append(textBox.Entry)
        
    def AddMultiEntry(self, text, x, y, width, height):
        textBox = Text(self.root, text, x, y, width, height)
        self.widgets.append(textBox.Text)
    
    def AddOptionMenu(self, values, x, y):
        optionMenu = OptionMenu(self.root, values, x, y)
        self.widgets.append(optionMenu.dropdown)
    
    def AddScrollableWindow(self, width, height, x, y, isTemporary):
        scrollable = ScrollableWindow(self.root, width, height, x, y)
        if isTemporary:
            self.tempWidgets.append(scrollable)
            self.tempWidgets.append(scrollable.scrollable_frame)
            self.tempWidgets.append(scrollable.scrollbar)          
        else:
            self.widgets.append(scrollable)
            self.widgets.append(scrollable.scrollable_frame)
            self.widgets.append(scrollable.scrollbar)
        
    def destroy(self):
        try:
            self.widgets.destroy()
        except:
            pass
        super().destroy()
  
import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, parameters=None):
        cursor = self.connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()

    def delete_person(self, person_id):
        query = "DELETE FROM Employees WHERE ID = ?"
        self.execute_query(query, (person_id,))

    def delete_project(self, project_id):
        query = "DELETE FROM Projects WHERE ID = ?"
        self.execute_query(query, (project_id,))
        
    def delete_task(self, task_id):
        query = "DELETE FROM Tasks WHERE ID == ?"
        self.execute_query(query, (task_id,))

    def update_project(self, project_id, project_name, start_date, end_date, budget, owner):
        query = 'UPDATE Projects SET "NAME" = ?, "Start Date" = ?, "End Date" = ?, "Budget" = ?, "Owner" = ? WHERE "ID" = ?'
        self.execute_query(query, (project_name, start_date, end_date, budget, owner, project_id))
        
    def update_person(self, person_id, forename, surname, age, expertise, comments):
        query = "UPDATE Employees SET Forename = ?, Surname = ?, Age = ?, Expertise = ?, Comments = ? WHERE ID = ?"
        self.execute_query(query, (forename, surname, age, expertise, comments, person_id))
        
    def update_task(self, id, taskName, startDate, endDate, comments):
        query = "UPDATE Tasks SET Description = ?, StartDate = ?, EndDate = ?, Comments = ? WHERE ID == ?"
        self.execute_query(query, (taskName, startDate, endDate, comments, id))

    def get_projects(self):
        query = "SELECT * FROM Projects"
        return self.execute_query(query)

    def get_employees(self):
        query = "SELECT * FROM Employees"
        return self.execute_query(query)
    
    def get_tasks(self, data):
        query = "SELECT * FROM Tasks WHERE ProjectID = ?"
        return self.execute_query(query, (data,))
    
    def add_task(self, id, project_id, start_date, end_date, leader_id, task_name, comments):
        query = "INSERT INTO Tasks VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.execute_query(query, (id, project_id, start_date, end_date, leader_id, task_name, comments))
        
    def add_person(self, newID, forename, surname, age, expertise, comments):
        query = "INSERT INTO Employees VALUES (?, ?, ?, ?, ?, ?)"
        self.execute_query(query, (newID, forename, surname, age, expertise, comments))
        
    def add_project(self, newID, projectName, startDate, endDate, budget, leader):
        query = "INSERT INTO Projects VALUES (?, ?, ?, ?, ?, ?)"
        self.execute_query(query, (newID, projectName, startDate, endDate, budget, leader))
 
class databaseController:
    def __init__(self):
        pass

    #Executes data deletion to the database when the button was pressed
    
    def GetTasks(data):
        db = Database('Database.db')
        db.connect()
        tasks = db.get_tasks(data)
        db.disconnect()
        return tasks
    
    def DeletePerson(data):
        db = Database('Database.db')
        db.connect()
        db.delete_person(data)
        db.disconnect()
        
    def DeleteProject(data):
        db = Database('Database.db')
        db.connect()
        db.delete_project(data)
        db.disconnect()
        
    def DeleteCurrentTaskRecord(data, detailWindow):
        db = Database('Database.db')
        db.connect()
        db.delete_task(data[0])
        db.disconnect()
        detailWindow.destroy()
    
    #Executes data changes to the database when the button was pressed
    def SubmitPersonChanges(detailWindow, id, foreName, surName, age, expertise, comments):
        db = Database('Database.db')
        db.connect()
        db.update_person(id, foreName, surName, age, expertise, comments)
        db.disconnect()
        detailWindow.destroy()

    #Busted for some reason now??
    def SubmitProjectChanges(detailWindow, ID, projectName, startDate, endDate, budget, leader):
        db = Database('Database.db')
        db.connect()
        leader = leader.split(" ", 2)
        forename = leader[0]
        surname = leader[1]
        leader = db.execute_query("SELECT ID FROM Employees WHERE Forename == ? AND Surname == ?", (forename, surname))
        leader = leader[0][0]
        db.update_project(ID, projectName, startDate, endDate, budget, leader)
        db.disconnect()
        detailWindow.destroy()    

    def SubmitTaskChanges(detailWindow, id, taskName, startDate, endDate, comments):
        db = Database('Database.db')
        db.connect()
        db.update_task(id, taskName, startDate, endDate, comments)
        db.disconnect()
        detailWindow.destroy()
        
    def SubmitNewTask(detailWindow, taskName, startDate, leader, endDate, comments, projectID):
        db = Database('Database.db')
        db.connect()
        newID = db.execute_query("SELECT MAX(ID) FROM Tasks")
        newID = int(newID[0][0]) + 1
        leader = leader.split(" ", 2)
        forename = leader[0]
        surname = leader[1]
        leader = db.execute_query("SELECT ID FROM Employees WHERE Forename == ? AND Surname == ?", (forename, surname))
        db.add_task(newID, projectID, startDate, endDate, leader[0][0], taskName, comments)
        db.disconnect()
        detailWindow.destroy()

    def SubmitNewPerson(detailWindow, forename, surname, age, expertise, comments):
        db = Database('Database.db')
        db.connect()
        newID = db.execute_query("SELECT MAX(ID) FROM Employees")
        newID = int(newID[0][0]) + 1
        db.add_person(newID, forename, surname, age, expertise, comments)
        db.disconnect()
        detailWindow.destroy()
        
    def SubmitNewProject(detailWindow, projectName, startDate, leader, endDate, budget):
        db = Database('Database.db')
        db.connect()
        newID = db.execute_query("SELECT MAX(ID) FROM Projects")
        newID = int(newID[0][0]) + 1
        leader = leader.split(" ", 2)
        forename = leader[0]
        surname = leader[1]
        leader = db.execute_query("SELECT ID FROM Employees WHERE Forename == ? AND Surname == ?", (forename, surname))
        db.add_project(newID, projectName, startDate, endDate, budget, leader[0][0])
        db.disconnect()
        detailWindow.destroy()
    
#Brings up the home window
def ShowHomeWindow(mainWindow=None, admin=False):
    if mainWindow is None:
        mainWindow = Windows("Title Screen", 1280, 720)
        global databasecontroller
        databasecontroller = databaseController
        if admin == False:
            mainWindow.admin = False
        else:
            mainWindow.admin = True
    mainWindow.ClearScreen()
    mainWindow.AddLabel("Project Management Software", 35, 305, 100, False)
    mainWindow.AddButton("Projects", 200, 350, lambda: ShowProjectWindow(mainWindow), 5, 20, 20, False)
    mainWindow.AddButton("People", 750, 350, lambda: ShowPeopleWindow(mainWindow), 5, 20, 20, False)
    mainWindow.Run()
    
#Opens the window to edit people
def EditCurrentPerson(data):
    detailWindow = Windows("Details", 600, 300)
    detailWindow.AddLabel("Forename:", 15, 10, 10, False)
    detailWindow.AddEntry(str(data[1]), 15, 40, 30, 20)
    foreName = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Surname:", 15, 10, 60, False)
    detailWindow.AddEntry(str(data[2]), 15, 90, 30, 20)
    surName = detailWindow.widgets[-1]

    detailWindow.AddLabel("Age:", 15, 10, 110, False)
    detailWindow.AddEntry(str(data[3]), 15, 140, 30, 20)
    age = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Expertise:", 15, 350, 10, False)
    detailWindow.AddEntry(str(data[4]), 350, 40, 30, 20)
    expertise = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Comments:", 15, 10, 160, False)
    detailWindow.AddMultiEntry(str(data[5]), 15, 190, 60, 300)
    comments = detailWindow.widgets[-1]
    
    detailWindow.AddButton("Submit", 450, 250, lambda: databasecontroller.SubmitPersonChanges(detailWindow, data[0], foreName.get(), surName.get(), age.get(), expertise.get(), comments.get()), 2, 10, 10, False)

#Opens the window to show people
def ShowPeopleData(mainWindow, data):
    for widget in mainWindow.tempWidgets:
        widget.destroy()
    mainWindow.AddLabel(data[1], 35, 300, 100, True)
    mainWindow.AddLabel(data[2], 35, 500, 100, True)
    mainWindow.AddLabel("Age: " + str(data[3]), 25, 300, 170, True)
    mainWindow.AddLabel("Expertise: " + data[4], 25, 300, 220, True)
    mainWindow.AddLabel("Comments: " + data[5], 15, 300, 280, True)
    if mainWindow.admin == True:
        mainWindow.AddButton("Delete Person", 1035, 9, lambda: databasecontroller.DeletePerson(data[0]), 2, 12, 11, True)
        mainWindow.AddButton("Edit Person", 915, 9, lambda: EditCurrentPerson(data), 2, 12, 11, True)

#Executes the SQL statement to add a new project and close the window

def AddNewTask(projectID):
    detailWindow = Windows("Details", 600, 600)
    detailWindow.AddLabel("Task Name:", 15, 10, 10, False)
    detailWindow.AddEntry("", 15, 40, 30, 20)
    taskName = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Start Date:", 15, 10, 60, False)
    detailWindow.AddEntry("", 15, 90, 30, 20)
    startDate = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Task Leader:", 15, 300, 10, False)
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT Forename, Surname FROM Employees")
    IDs = c.fetchall()
    conn.commit()
    conn.close()
    detailWindow.AddOptionMenu(IDs, 300, 40)
    leader = detailWindow.widgets[-1]

    detailWindow.AddLabel("End Date:", 15, 10, 110, False)
    detailWindow.AddEntry("", 15, 140, 30, 20)
    endDate = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Comments:", 15, 10, 160, False)
    detailWindow.AddMultiEntry("", 15, 190, 60, 300)
    comments = detailWindow.widgets[-1]
    
    detailWindow.AddButton("Submit", 250, 525, lambda: databasecontroller.SubmitNewTask(detailWindow, taskName.get(), startDate.get(), leader.get(), endDate.get(), comments.get("0.0", tk.END), projectID), 2, 10, 10, False)
    
def EditCurrentProject(data):
    detailWindow = Windows("Details", 600, 300)
    detailWindow.AddLabel("Project Name:", 15, 10, 10, False)
    detailWindow.AddEntry(str(data[1]), 15, 40, 30, 20)
    projectName = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Start Date:", 15, 10, 60, False)
    detailWindow.AddEntry(str(data[2]), 15, 90, 30, 20)
    startDate = detailWindow.widgets[-1]

    detailWindow.AddLabel("End Date:", 15, 10, 110, False)
    detailWindow.AddEntry(str(data[3]), 15, 140, 30, 20)
    endDate = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Budget:", 15, 350, 10, False)
    detailWindow.AddEntry(str(data[4]), 350, 40, 30, 20)
    budget = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Project Lead:", 15, 350, 60, False)
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT Forename, Surname FROM Employees")
    IDs = c.fetchall()
    conn.commit()
    conn.close()
    detailWindow.AddOptionMenu(IDs, 350, 90)
    projectLead = detailWindow.widgets[-1] 
    
    detailWindow.AddButton("Submit", 450, 250, lambda: databasecontroller.SubmitProjectChanges(detailWindow, data[0], projectName.get(), startDate.get(), endDate.get(), budget.get(), projectLead.get()), 2, 10, 10, False)

def ShowProjectData(mainWindow, data):
    for widget in mainWindow.tempWidgets:
        widget.destroy()
    mainWindow.AddLabel("Project id: " + str(data[0]), 10, 295, 80, True)
    mainWindow.AddLabel("Project Title: ", 18, 295, 110, True)
    mainWindow.AddLabel(str(data[1]), 15, 295, 140, True)
    mainWindow.AddLabel("Start Date: ", 10, 295, 180, True)
    mainWindow.AddLabel(str(data[2]), 15, 295, 200, True)
    mainWindow.AddLabel("End Date: ", 10, 295, 250, True)
    mainWindow.AddLabel(str(data[3]), 15, 295, 270, True)
    mainWindow.AddLabel("Budget: ", 10, 295, 320, True)
    mainWindow.AddLabel("£" + str(data[4]), 15, 295, 340, True)
    mainWindow.AddLabel("Project Lead: ", 10, 295, 390, True)
    if mainWindow.admin == True:
        mainWindow.AddButton("Add New Task", 1155, 9, lambda: AddNewTask(data[0]), 2, 12, 11, True)
        mainWindow.AddButton("Delete Project", 1035, 9, lambda: databasecontroller.DeleteProject(data[0]), 2, 12, 11, True)
        mainWindow.AddButton("Edit Project", 915, 9, lambda: EditCurrentProject(data), 2, 12, 11, True)
        
    newData = databaseController.GetTasks(data[0])
    
    mainWindow.AddScrollableWindow(733, 635, 522, 75, True)

    scrollable_frame2 = mainWindow.tempWidgets[-2]

    for i, newData in enumerate(newData):
        
        box = tk.Label(scrollable_frame2, text=newData[5], bg="white", relief="solid", bd=1, width=103)
        box.pack()

        # Bind the click event to a function to show text on a different canvas
        box.bind("<Button-1>", lambda event, data=newData: ShowTaskData(data, mainWindow))

        mainWindow.widgets.append(box)
    
def EditCurrentTaskRecord(data, detailWindow):
    detailWindow.ClearScreen()
    detailWindow.AddLabel("Task Name:", 15, 10, 10, False)
    detailWindow.AddEntry(str(data[5]), 15, 40, 30, 20)
    taskName = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Start Date:", 15, 10, 60, False)
    detailWindow.AddEntry(str(data[2]), 15, 90, 30, 20)
    startDate = detailWindow.widgets[-1]

    detailWindow.AddLabel("End Date:", 15, 10, 110, False)
    detailWindow.AddEntry(str(data[3]), 15, 140, 30, 20)
    endDate = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Comments:", 15, 10, 160, False)
    detailWindow.AddMultiEntry(str(data[6]), 15, 190, 60, 300)
    comments = detailWindow.widgets[-1]
    
    detailWindow.AddButton("Submit", 250, 525, lambda: databasecontroller.SubmitTaskChanges(detailWindow, data[0], taskName.get(), startDate.get(), endDate.get(), comments.get("0.0", tk.END)), 2, 10, 10, False)
    
def ShowTaskData(data, mainWindow):
    detailWindow = Windows("Details", 600, 600)
    detailWindow.AddLabel("", 0, 0, 0, False, width=detailWindow.width, height=3, bg="gray")
    detailWindow.AddLabel(str(data[5]), 20, 10, 20, False)
    detailWindow.AddLabel("Start Date: ", 10, 5, 80, False)
    detailWindow.AddLabel(str(data[2]), 15, 5, 100, False)
    detailWindow.AddLabel("End Date: ", 10, 200, 80, False)
    detailWindow.AddLabel(str(data[3]), 15, 200, 100, False)
    detailWindow.AddLabel("Comments: ", 15, 5, 140, False)
    detailWindow.AddLabel(str(data[6]), 10, 5, 170, False)
    detailWindow.AddLabel("Task Leader: ", 10, 400, 80, False)
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT Forename FROM Employees WHERE ID == ?", (data[4],))
    name = c.fetchall()
    name = str(name).strip("[(,')]")
    detailWindow.AddLabel(name, 15, 400, 100, False)
    if mainWindow.admin == True:
        detailWindow.AddButton("Delete Record", 470, 10, lambda: databasecontroller.DeleteCurrentTaskRecord(data, detailWindow), 2, 12, 12, False)
    detailWindow.AddButton("Edit Record", 330, 10, lambda: EditCurrentTaskRecord(data, detailWindow), 2, 12, 12, False)
    
def AddNewPerson():
    detailWindow = Windows("Details", 600, 600)
    detailWindow.AddLabel("Forename:", 15, 10, 10, False)
    detailWindow.AddEntry("", 15, 40, 30, 20)
    name = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Surname:", 15, 10, 60, False)
    detailWindow.AddEntry("", 15, 90, 30, 20)
    name2 = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Age:", 15, 300, 10, False)
    detailWindow.AddEntry("", 300, 40, 5, 20)
    age = detailWindow.widgets[-1]

    detailWindow.AddLabel("Expertise:", 15, 10, 110, False)
    detailWindow.AddEntry("", 15, 140, 30, 20)
    expertise = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Comments:", 15, 10, 160, False)
    detailWindow.AddMultiEntry("", 15, 190, 60, 300)
    comments = detailWindow.widgets[-1]
    
    detailWindow.AddButton("Submit", 250, 525, lambda: databasecontroller.SubmitNewPerson(detailWindow, name.get(), name2.get(), age.get(), expertise.get(), comments.get("0.0", tk.END)), 2, 10, 10, False) 

def ShowPeopleWindow(mainWindow):
    mainWindow.ClearScreen()

    mainWindow.AddLabel("", 0, 0, 0, False, width=mainWindow.width, height=3, bg="gray")
    mainWindow.AddLabel("", 0, 0, 60, False, width=mainWindow.width, height=40, bg="lightgray")
    mainWindow.AddLabel("", 0, 285, 70, False, width=109, height=35, bg="white")

    mainWindow.AddLabel("People", 20, 590, 10, False, bg="gray", fg="white")
    mainWindow.AddButton("Back", 10, 10, lambda: ShowHomeWindow(mainWindow), 2, 10, 10, False)
    
    if mainWindow.admin == True:
        mainWindow.AddButton("Add New Person", 1155, 9, lambda: AddNewPerson(), 2, 12, 11, False)
 
    mainWindow.AddScrollableWindow(250, 635, 10, 70, False)
 
    scrollable_frame = mainWindow.widgets[-2]
    
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT Forename FROM Employees")
    names = c.fetchall()
    c.execute("SELECT * FROM Employees")
    allData = c.fetchall()
    conn.close()

    for i, name in enumerate(names):
        box = tk.Label(scrollable_frame, text=name, bg="white", relief="solid", bd=1, width=34)
        box.pack()

        # Bind the click event to a function to show text on a different canvas
        box.bind("<Button-1>", lambda event, data=allData[i]: ShowPeopleData(mainWindow, data))

        mainWindow.widgets.append(box)

def AddNewProject():
    detailWindow = Windows("Details", 600, 235)
    detailWindow.AddLabel("Project Name:", 15, 10, 10, False)
    detailWindow.AddEntry("", 15, 40, 30, 20)
    projectName = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Start Date:", 15, 10, 60, False)
    detailWindow.AddEntry("", 15, 90, 30, 20)
    startDate = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Task Leader:", 15, 300, 10, False)
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT Forename, Surname FROM Employees")
    IDs = c.fetchall()
    conn.commit()
    conn.close()
    detailWindow.AddOptionMenu(IDs, 300, 40)
    leader = detailWindow.widgets[-1]  

    detailWindow.AddLabel("End Date:", 15, 10, 110, False)
    detailWindow.AddEntry("", 15, 140, 30, 20)
    endDate = detailWindow.widgets[-1]
    
    detailWindow.AddLabel("Budget:", 15, 10, 160, False)
    detailWindow.AddMultiEntry("", 15, 190, 30, 20)
    budget = detailWindow.widgets[-1]
    
    detailWindow.AddButton("Submit", 450, 175, lambda: databasecontroller.SubmitNewProject(detailWindow, projectName.get(), startDate.get(), leader.get(), endDate.get(), budget.get("0.0", tk.END)), 2, 10, 10, False)
        
def ShowProjectWindow(mainWindow):
    mainWindow.ClearScreen()

    mainWindow.AddLabel("", 0, 0, 0, False, width=mainWindow.width, height=3, bg="gray")
    mainWindow.AddLabel("", 0, 0, 60, False, width=mainWindow.width, height=40, bg="lightgray")
    mainWindow.AddLabel("", 0, 285, 70, False, width=109, height=35, bg="white")
    mainWindow.AddLabel("", 0, 500, 70, False, width=1, height=35, bg="lightgray")
    
    if mainWindow.admin == True:
        mainWindow.AddButton("Add New Project", 120, 10, lambda: AddNewProject(), 2, 13, 10, False)
        
    mainWindow.AddButton("Back", 10, 10, lambda: ShowHomeWindow(mainWindow), 2, 12, 10, False)
 
    mainWindow.AddScrollableWindow(250, 635, 10, 70, False)
 
    scrollable_frame = mainWindow.widgets[-2]
    
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("SELECT Name FROM Projects")
    names = c.fetchall()
    c.execute("SELECT * FROM Projects")
    allData = c.fetchall()
    conn.close()

    for i, name in enumerate(names):
        box = tk.Label(scrollable_frame, text=name, bg="white", relief="solid", bd=1, width=34)
        box.pack()

        # Bind the click event to a function to show text on a different canvas
        box.bind("<Button-1>", lambda event, data=allData[i]: ShowProjectData(mainWindow, data))

        mainWindow.widgets.append(box)
    
def LoginCheck(loginWindow, password):
    if password == "admin":
        verification = True
    else:
        verification = False
    loginWindow.destroy()
    ShowHomeWindow(None, verification)

if __name__ == '__main__':
    loginWindow = Windows("Details", 600, 235)
    loginWindow.AddLabel("Login Page", 25, 220, 10, False)
    loginWindow.AddLabel("Admin Password: (Optional)", 10, 80, 110, False)
    loginWindow.AddEntry("", 45, 150, 40, 20)
    password = loginWindow.widgets[-1]
    loginWindow.AddButton("Log In", 400, 115, lambda: ShowHomeWindow(LoginCheck(loginWindow, password.get())), 2, 12, 10, False)
    loginWindow.Run()
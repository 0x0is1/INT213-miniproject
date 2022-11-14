from tkinter import LabelFrame, Label, Button, Checkbutton, Entry, StringVar, IntVar, messagebox
from utils.constants.constant import BUTTONCOLOR
from utils.mysqlHandler import DBManager
import mysql
import json
from hashlib import md5

class Embedder:

    def __init__(self, root):
        self.root = root
        self.nameVar = StringVar(self.root)
        self.regVar = StringVar(self.root)
        self.specVar = StringVar(self.root)
        self.mobVar = StringVar(self.root)
        self.emailVar = StringVar(self.root)
        self.passVar = StringVar(self.root)
        self.usernameVar = StringVar(self.root)
        self.loginpassVar = StringVar(self.root)
        self.sessionToken = None
        with open('./openHours.json', 'r') as fp:
            self.openHoursData = json.load(fp)
        self.dbmanager = DBManager()
        self.stateApprContainer = []

        query = 'create table if not exists student_users(reg bigint primary key, name varchar(100), specs varchar(100), contact bigint, email varchar(100), passhash varchar(100));'
        self.dbmanager.executeCommand(query)
        query = 'create table if not exists supervisor_users(reg bigint primary key, name varchar(100), specs varchar(100), contact bigint, email varchar(100), passhash varchar(100));'
        self.dbmanager.executeCommand(query)
        query = 'create table if not exists capstone_allocation_requests(reg int, title varchar(200), desp varchar(1000), approved int);'
        self.dbmanager.executeCommand(query)

    def clearFrame(self):
        # destroy all widgets from frame
        for widget in self.root.winfo_children():
            widget.destroy()
        Button(self.root, text="Home", bg=BUTTONCOLOR, font=("Arial", 12), command=self.studentPanel)\
            .grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def setApproval(self, code):
        query = 'select reg from capstone_allocation_requests;'
        regs = self.dbmanager.executeCommand(query)
        try:
            for idx, i in enumerate(self.stateApprContainer):
                if i.get() == 1:
                    query = f'update capstone_allocation_requests set approved={code} where reg="{regs[idx][0]}"'
                    self.dbmanager.executeCommand(query)
            messagebox.showinfo("Successful", "Action completed successfully.")
        except Exception as e:
            messagebox.error("Failed", e)
            
    def studentPanel(self):
        self.clearFrame()
        studentPanelFrame = LabelFrame(self.root, text="Student", font=("Arial", 12, "bold"))
        Button(studentPanelFrame, text="Login", bg=BUTTONCOLOR, font=("Arial", 12), command=self.loginPanel)\
            .grid(row=0, column=0, padx=50, pady=10, sticky="ew")
        Button(studentPanelFrame, text="New user", bg=BUTTONCOLOR, font=("Arial", 12), command=self.newStudentPanel)\
            .grid(row=0, column=1, padx=50, pady=10, sticky="ew")
        Button(studentPanelFrame, text="Request for Supervisor", bg=BUTTONCOLOR, font=("Arial", 12), command=self.requestSupervisorPanel)\
            .grid(row=0, column=2, padx=50, pady=10, sticky="ew")
        studentPanelFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def newStudentPanel(self):
        self.clearFrame()
        
        newStudentFrame = LabelFrame(self.root, text="New user student", font=("Arial", 12, "bold"))
        Label(newStudentFrame, text="Name", font=("Arial", 12), anchor="w")\
            .grid(row=0, column=0, padx=50, pady=10, sticky="ew")

        Entry(newStudentFrame, textvariable=self.nameVar)\
            .grid(row=0, column=1, padx=50, pady=10, sticky="ew")

        Label(newStudentFrame, text="Reg. No", font=("Arial", 12), anchor="w")\
            .grid(row=1, column=0, padx=50, pady=10, sticky="ew")

        Entry(newStudentFrame, textvariable=self.regVar)\
            .grid(row=1, column=1, padx=50, pady=10, sticky="ew")

        Label(newStudentFrame, text="Specialization", font=("Arial", 12), anchor="w")\
            .grid(row=2, column=0, padx=50, pady=10, sticky="ew")

        Entry(newStudentFrame, textvariable=self.specVar)\
            .grid(row=2, column=1, padx=50, pady=10, sticky="ew")

        Label(newStudentFrame, text="Mobile no", font=("Arial", 12), anchor="w")\
            .grid(row=3, column=0, padx=50, pady=10, sticky="ew") 

        Entry(newStudentFrame, textvariable=self.mobVar)\
            .grid(row=3, column=1, padx=50, pady=10, sticky="ew")

        Label(newStudentFrame, text="Email Id", font=("Arial", 12), anchor="w")\
            .grid(row=4, column=0, padx=50, pady=10, sticky="ew")

        Entry(newStudentFrame, textvariable=self.emailVar)\
            .grid(row=4, column=1, padx=50, pady=10, sticky="ew")

        Label(newStudentFrame, text="Password", font=("Arial", 12), anchor="w")\
            .grid(row=5, column=0, padx=50, pady=10, sticky="ew")

        Entry(newStudentFrame, textvariable=self.passVar, show='●')\
            .grid(row=5, column=1, padx=50, pady=10, sticky="ew")

        Button(newStudentFrame, text="Register", bg=BUTTONCOLOR, font=("Arial", 12), command=self.onRegisterd)\
            .grid(row=6, column=2, padx=50, pady=20, sticky="ew")
        
        newStudentFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def loginPanel(self):
        self.clearFrame()
        loginFrame = LabelFrame(self.root, text="Login Page", font=("Arial", 12, "bold"))
        Label(loginFrame, text="Username", font=("Arial", 12), anchor="w")\
            .grid(row=0, column=0, padx=50, pady=20, sticky="ew")

        Entry(loginFrame, textvariable=self.usernameVar)\
            .grid(row=0, column=1, padx=50, pady=20, sticky="ew")

        Label(loginFrame, text="Password", font=("Arial", 12), anchor="w")\
            .grid(row=1, column=0, padx=50, pady=20, sticky="ew")

        Entry(loginFrame, textvariable=self.loginpassVar, show='●')\
            .grid(row=1, column=1, padx=50, pady=20, sticky="ew")

        Button(loginFrame, text="Login", bg=BUTTONCOLOR, font=("Arial", 12), command=self.onLogin)\
            .grid(row=2, column=1, padx=50, pady=20, sticky="ew")

        Button(loginFrame, text="New User", bg=BUTTONCOLOR, font=("Arial", 12), command=self.newStudentPanel)\
            .grid(row=2, column=2, padx=50, pady=20, sticky="ew")

        loginFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def loginSuperPanel(self):
        self.clearFrame()
        loginSuperFrame = LabelFrame(self.root, text="Supervisor Login Page", font=("Arial", 12, "bold"))
        Label(loginSuperFrame, text="Username", font=("Arial", 12), anchor="w")\
            .grid(row=0, column=0, padx=50, pady=20, sticky="ew")

        Entry(loginSuperFrame, textvariable=self.usernameVar)\
            .grid(row=0, column=1, padx=50, pady=20, sticky="ew")

        Label(loginSuperFrame, text="Password", font=("Arial", 12), anchor="w")\
            .grid(row=1, column=0, padx=50, pady=20, sticky="ew")

        Entry(loginSuperFrame, textvariable=self.loginpassVar, show='●')\
            .grid(row=1, column=1, padx=50, pady=20, sticky="ew")

        Button(loginSuperFrame, text="Login", bg=BUTTONCOLOR, font=("Arial", 12), command=self.onSuperLogin)\
            .grid(row=2, column=1, padx=50, pady=20, sticky="ew")

        Button(loginSuperFrame, text="New User", bg=BUTTONCOLOR, font=("Arial", 12), command=self.newSuperPanel)\
            .grid(row=2, column=2, padx=50, pady=20, sticky="ew")

        loginSuperFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
    def requestSupervisorPanel(self):
        self.clearFrame()
        supervisorPanelFrame = LabelFrame(self.root, text="Supervisor", font=("Arial", 12, "bold"))
        Button(supervisorPanelFrame, text="Login", bg=BUTTONCOLOR, font=("Arial", 12), command=self.loginSuperPanel)\
            .grid(row=0, column=0, padx=100, pady=30, sticky="ew")
        Button(supervisorPanelFrame, text="New user", bg=BUTTONCOLOR, font=("Arial", 12), command=self.newSuperPanel)\
            .grid(row=0, column=1, padx=100, pady=30, sticky="ew")
        Button(supervisorPanelFrame, text="Open Hours", bg=BUTTONCOLOR, font=("Arial", 12), command=self.openHours)\
            .grid(row=1, column=0, padx=100, pady=30, sticky="ew")
        Button(supervisorPanelFrame, text="Select Students", bg=BUTTONCOLOR, font=("Arial", 12), command=self.selectStudents)\
            .grid(row=1, column=1, padx=100, pady=30, sticky="ew", ipadx=20)
        supervisorPanelFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def newSuperPanel(self):
        self.clearFrame()
        
        newSupervisorFrame = LabelFrame(self.root, text="New user supervisor", font=("Arial", 12, "bold"))
        Label(newSupervisorFrame, text="Name", font=("Arial", 12), anchor="w")\
            .grid(row=0, column=0, padx=50, pady=10, sticky="ew")

        Entry(newSupervisorFrame, textvariable=self.nameVar)\
            .grid(row=0, column=1, padx=50, pady=10, sticky="ew")

        Label(newSupervisorFrame, text="Reg. No", font=("Arial", 12), anchor="w")\
            .grid(row=1, column=0, padx=50, pady=10, sticky="ew")

        Entry(newSupervisorFrame, textvariable=self.regVar)\
            .grid(row=1, column=1, padx=50, pady=10, sticky="ew")

        Label(newSupervisorFrame, text="Specialization", font=("Arial", 12), anchor="w")\
            .grid(row=2, column=0, padx=50, pady=10, sticky="ew")

        Entry(newSupervisorFrame, textvariable=self.specVar)\
            .grid(row=2, column=1, padx=50, pady=10, sticky="ew")

        Label(newSupervisorFrame, text="Mobile no", font=("Arial", 12), anchor="w")\
            .grid(row=3, column=0, padx=50, pady=10, sticky="ew") 

        Entry(newSupervisorFrame, textvariable=self.mobVar)\
            .grid(row=3, column=1, padx=50, pady=10, sticky="ew")

        Label(newSupervisorFrame, text="Email Id", font=("Arial", 12), anchor="w")\
            .grid(row=4, column=0, padx=50, pady=10, sticky="ew")

        Entry(newSupervisorFrame, textvariable=self.emailVar)\
            .grid(row=4, column=1, padx=50, pady=10, sticky="ew")

        Label(newSupervisorFrame, text="password", font=("Arial", 12), anchor="w")\
            .grid(row=5, column=0, padx=50, pady=10, sticky="ew")

        Entry(newSupervisorFrame, textvariable=self.passVar, show='●')\
            .grid(row=5, column=1, padx=50, pady=10, sticky="ew")

        Button(newSupervisorFrame, text="Register", bg=BUTTONCOLOR, font=("Arial", 12), command=self.onSuperRegisterd)\
            .grid(row=6, column=2, padx=50, pady=10, sticky="ew")
        
        newSupervisorFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def openHours(self):
        self.clearFrame()
        openHoursFrame = LabelFrame(self.root, text="Portal Open Hours", font=("Arial", 18))
        Label(openHoursFrame, text="Day", font=("Arial", 14, "bold"), borderwidth=3, bg=BUTTONCOLOR, anchor="n")\
            .grid(row=0, column=0, sticky="ew", ipadx=140)
        Label(openHoursFrame, text="Time", font=("Arial", 14, "bold"), borderwidth=3, bg="grey", anchor="n")\
            .grid(row=0, column=1, sticky="ew", ipadx=140)
        for idx, i in enumerate(self.openHoursData):
            Label(openHoursFrame, text=i, font=("Arial", 14), borderwidth=3, anchor="w")\
                .grid(row=idx, column=0, sticky="ew", ipadx=90)
            Label(openHoursFrame, text=f"{self.openHoursData[i][0]} - {self.openHoursData[i][1]}", font=("Arial", 14),  anchor="w")\
                .grid(row=idx, column=1, sticky="ew", ipadx=90)
        openHoursFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew", ipadx=10, ipady=10)

    def selectStudents(self):
        if self.sessionToken != None:
            query = f'select * from supervisor_users where reg={self.usernameVar.get()} and passhash="{self.sessionToken}";'
            data = self.dbmanager.executeCommand(query)
            if len(data) != 0:
                messagebox.showinfo("Info", f"Welcome back {data[0][1]}!")
                self.clearFrame()
                selectStudentsFrame = LabelFrame(self.root, text="Select Students", font=("Arial", 12))
                query = f'select * from capstone_allocation_requests;'
                requests_data = self.dbmanager.executeCommand(query)
                if len(requests_data) < 1:
                    Label(selectStudentsFrame, text="No request data available.", foreground="gray")\
                        .grid(row=0, column=1, padx=30, pady=10, sticky='ew')
                else:
                    self.stateApprContainer.clear()
                    Label(selectStudentsFrame, text="Select", font=("Arial", 12), bg=BUTTONCOLOR)\
                        .grid(row=0, column=0, pady=5, padx=1, ipadx=5)
                    Label(selectStudentsFrame, text="Registration No.", font=("Arial", 12), bg=BUTTONCOLOR)\
                        .grid(row=0, column=1, pady=5, padx=1, ipadx=5)
                    Label(selectStudentsFrame, text="Title", font=("Arial", 12), bg=BUTTONCOLOR)\
                        .grid(row=0, column=2, pady=5, padx=1, ipadx=50)
                    Label(selectStudentsFrame, text="Description", font=("Arial", 12), bg=BUTTONCOLOR)\
                        .grid(row=0, column=3, pady=5, padx=1, ipadx=50)
                    Label(selectStudentsFrame, text="Approval status", font=("Arial", 12), bg=BUTTONCOLOR)\
                        .grid(row=0, column=4, pady=5, padx=1, ipadx=5)
                    for idx, i in enumerate(requests_data):
                        statusVar = IntVar(self.root)
                        self.stateApprContainer.append(statusVar)
                        Checkbutton(selectStudentsFrame, variable=statusVar).grid(row=idx+1, column=0, pady=5)
                        Label(selectStudentsFrame, text=i[0], wraplength=100, borderwidth=1, relief="solid").grid(row=idx+1, column=1, pady=5, sticky="nsew")
                        Label(selectStudentsFrame, text=i[1], wraplength=100, borderwidth=1, relief="solid").grid(row=idx+1, column=2, pady=5, sticky="nsew")
                        Label(selectStudentsFrame, text=i[2], wraplength=200, borderwidth=1, relief="solid").grid(row=idx+1, column=3, pady=5, sticky="nsew")
                        Label(selectStudentsFrame, text=["Pending", "Approved", "Rejected"][i[3]], borderwidth=1, relief="solid").grid(row=idx+1, column=4, pady=5, sticky="nsew")
                    Button(selectStudentsFrame, text="Approve", bg="#98c379", fg="white", font=("Arial"), command=lambda:self.setApproval(1))\
                        .grid(row=idx+2, column=4, padx=10, pady=10)
                    Button(selectStudentsFrame, text="Delete", bg="#cd656e", fg="white", font=("Arial"), command=lambda:self.setApproval(2))\
                        .grid(row=idx+2, column=1, padx=10, pady=10)
                    Button(selectStudentsFrame, text="Default", bg="#abb2bf", font=("Arial"), command=lambda:self.setApproval(0))\
                        .grid(row=idx+2, column=3, padx=10, pady=10)
                selectStudentsFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
                return
            messagebox.showerror("Authentication failed", "You have to be logged in as a supervisor before using this.")
            return
        messagebox.showerror("Authentication failed", "You have to be logged in before using this.")

    def studentRequestPanel(self):
        if self.sessionToken != None:
            query = f'select * from student_users where reg={self.usernameVar.get()} and passhash="{self.sessionToken}";'
            data = self.dbmanager.executeCommand(query)
            if len(data) != 0:
                messagebox.showinfo("Info", f"Welcome back {data[0][1]}!")
                self.clearFrame()
                studentRequestFrame = LabelFrame(self.root, text="Student Request Panel", font=("Arial", 12), width=100)
                Button(studentRequestFrame, text="Log Request", bg=BUTTONCOLOR, font=("Arial", 10), command=self.logRequest)\
                    .grid(row=0, column=0, padx=80, pady=20, ipadx=140)
                Button(studentRequestFrame, text="Check Request Status", bg=BUTTONCOLOR, font=("Arial", 10), command=self.requestStatus)\
                    .grid(row=1, column=0, padx=80, pady=20, ipadx=140)
                studentRequestFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
                return
            messagebox.showerror("Authentication failed", "You have to be logged in as a student before using this.")
            return
        messagebox.showerror("Authentication failed", "You have to be logged in before using this.")

    def logRequest(self):
        requestTitleVar = StringVar(self.root)
        requestDescVar = StringVar(self.root)
        
        def submitRequest():
            regquery = f'select reg from student_users where passhash="{self.sessionToken}";'
            reg = self.dbmanager.executeCommand(regquery)[0][0]
            query = 'create table if not exists capstone_allocation_requests(reg int, title varchar(200), desp varchar(1000), approved int);'
            self.dbmanager.executeCommand(query)
            query = f'insert into capstone_allocation_requests values({reg}, "{requestTitleVar.get()}", "{requestDescVar.get()}", 0);'
            try:
                self.dbmanager.executeCommand(query)
                messagebox.showinfo("Log successful", "Request logged successfully")
            except Exception as e:
                messagebox.showerror("Request logging failed", e)
        
        self.clearFrame()
        logRequestFrame = LabelFrame(self.root, text="Log Request", font=("Arial", 12))
        Label(logRequestFrame, text="Title", font=("Arial", 10))\
            .grid(row=0, column=0, padx=10, pady=10)
        Entry(logRequestFrame, textvariable=requestTitleVar).grid(row=0, column=1, padx=50, pady=10, sticky="ew")
        Label(logRequestFrame, text="Description", font=("Arial", 10))\
            .grid(row=1, column=0, padx=10, pady=10)
        Entry(logRequestFrame, textvariable=requestDescVar, width=50)\
            .grid(row=1, column=1, padx=50, pady=30, sticky="ew")
        Button(logRequestFrame, text="Submit", command=submitRequest, font=("Arial", 12), bg=BUTTONCOLOR)\
            .grid(row=2, column=1, padx=50, pady=30, sticky="ew")
        logRequestFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
    def requestStatus(self):
        self.clearFrame()
        regquery = f'select reg from student_users where passhash="{self.sessionToken}";'
        reg = self.dbmanager.executeCommand(regquery)[0][0]
        requestStatusFrame = LabelFrame(self.root, text="Request Status", font=("Arial", 12))
        query = f'select * from capstone_allocation_requests where reg={reg};'
        statusData = self.dbmanager.executeCommand(query)
        if len(statusData) < 1:
            Label(requestStatusFrame, text="No request data available.", foreground="gray")\
                .grid(row=0, column=1, padx=30, pady=10, ipadx=150, sticky='news')
        else:
            Label(requestStatusFrame, text="Title", font=("Arial", 12), bg=BUTTONCOLOR)\
                .grid(row=0, column=0, pady=5, padx=1, ipadx=75)
            Label(requestStatusFrame, text="Description", font=("Arial", 12), bg=BUTTONCOLOR)\
                .grid(row=0, column=1, pady=5, padx=1, ipadx=75)
            Label(requestStatusFrame, text="Approval status", font=("Arial", 12), bg=BUTTONCOLOR)\
                .grid(row=0, column=2, pady=5, padx=1, ipadx=10)
            for idx, i in enumerate(statusData):
                Label(requestStatusFrame, text=i[1], wraplength=100, borderwidth=1, relief="solid").grid(row=idx+1, column=0, pady=5, sticky="nsew")
                Label(requestStatusFrame, text=i[2], wraplength=300, borderwidth=1, relief="solid").grid(row=idx+1, column=1, pady=5, sticky="nsew")
                Label(requestStatusFrame, text=["Pending", "Approved", "Rejected"][i[3]], borderwidth=1, relief="solid").grid(row=idx+1, column=2, pady=5, sticky="nsew")
        requestStatusFrame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def onRegisterd(self):
        query = 'create table if not exists student_users(reg bigint primary key, name varchar(100), specs varchar(100), contact bigint, email varchar(100), passhash varchar(100));'
        print(self.dbmanager.executeCommand(query))
        try:
            passhash = md5(f"{self.regVar.get()}{self.passVar.get()}".encode('utf-8')).hexdigest()
            print(passhash)
            query = f'insert into student_users values({self.regVar.get()}, "{self.nameVar.get()}", "{self.specVar.get()}", {self.mobVar.get()}, "{self.emailVar.get()}", "{passhash}");'
            print(self.dbmanager.executeCommand(query))
            query = f'select * from student_users;'
            print(self.dbmanager.executeCommand(query))
            messagebox.showinfo("Info", "You have registered successfully.")
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Error", e)
        except mysql.connector.errors.ProgrammingError as e:
            messagebox.showerror("Error", e)

    def onSuperRegisterd(self):
        query = f'create table if not exists supervisor_users(reg bigint primary key, name varchar(100), specs varchar(100), contact bigint, email varchar(100), passhash varchar(100));'
        print(self.dbmanager.executeCommand(query))
        try:
            passhash = md5(f"{self.regVar.get()}{self.passVar.get()}".encode('utf-8')).hexdigest()
            query = f'insert into supervisor_users values({self.regVar.get()}, "{self.nameVar.get()}", "{self.specVar.get()}", {self.mobVar.get()}, "{self.emailVar.get()}", "{passhash}");'
            print(self.dbmanager.executeCommand(query))
            query = f'select * from supervisor_users;'
            print(self.dbmanager.executeCommand(query))
            messagebox.showinfo("Info", "You have registered successfully.")
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Error", e)
        except mysql.connector.errors.ProgrammingError as e:
            messagebox.showerror("Error", e)

    def onLogin(self):
        self.sessionToken = None
        passhash = md5(f"{self.usernameVar.get()}{self.loginpassVar.get()}".encode('utf-8')).hexdigest()
        query = f'select * from student_users where reg={self.usernameVar.get()} and passhash="{passhash}";'
        try:
            data = self.dbmanager.executeCommand(query)
            if len(data) != 0:
                messagebox.showinfo("Info", "You have logged in successfully.")
                self.sessionToken = passhash
                self.studentRequestPanel()
                return
            messagebox.showerror("Authentication failed", "Username or password is incorrect.")
        except Exception:
            messagebox.showerror("Registration Error", "Looks like you have not registered yet. Try registering first.")       

    def onSuperLogin(self):
        self.sessionToken = None
        passhash = md5(f"{self.usernameVar.get()}{self.loginpassVar.get()}".encode('utf-8')).hexdigest()
        query = f'select * from supervisor_users where reg={self.usernameVar.get()} and passhash="{passhash}";'
        data = self.dbmanager.executeCommand(query)
        try:
            if len(data) != 0:
                messagebox.showinfo("Info", "You have logged in successfully.")
                self.sessionToken = passhash
                return
            messagebox.showerror("Authentication failed", "Username or password is incorrect.")
        except Exception:
            messagebox.showerror("Registration Error", "Looks like you have not registered yet. Try registering first.")       

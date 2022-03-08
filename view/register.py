from tkinter import *
from view.abstract_page_view import AbstractPageView
from model.views import Views
from server.database_client import REGISTER_RESULT, REGISTER_RESULT_MESSAGE

class Register(AbstractPageView):
    def __init__(self, root, on_register, on_login, on_home):
        super().__init__(root, Views.REGISTER)
        self.on_login = on_login
        self.on_home = on_home
        self.on_register = on_register
        self.username = StringVar()
        self.password = StringVar()
        self.error = None
    
    def display(self):
        self.root.geometry('350x500')

        j = 0
        k = 10
        for i in range(100):
            c = str(222222 + k)
            f1 = Frame(self.root, width=10, height=500, bg="#" + c)
            f1.place(x=j, y=0)
            self.widgets.append(f1)
            j = j + 10
            k += 1

        t = ('Consolas', 13)



        f2 = Frame(self.root, width=250, height=400, bg='white')
        f2.place(x=50, y=50)


        l4 = Label(self.root, text='Username', fg='gray', bg='white', font='Helvetica 15 bold')
        l4.place(x = 80, y = 200)

        e4 = Entry(self.root, width=20, border=0, textvariable=self.username, fg="black", bg="white", highlightbackground="white")
        e4.config(font= t)
        e4.place(x=80, y=230)
        e4.bind('<Return>', lambda x: self.click_register())

        # We'll add this once we add emails
        # l1 = Label(self.root, text='email-id', bg='white', font='Helvetica 15 bold')
        # l1.place(x=80, y=200)

        # e1 = Entry(self.root, width=20, border=0)
        # e1.config(font= t)
        # e1.place(x=80, y=230)

        e2 = Entry(self.root, width=20, border=0, show='*', textvariable=self.password, fg="black", bg="white", highlightbackground="white")
        e2.config(font=t)
        e2.place(x=80, y=310)
        e2.bind('<Return>', lambda x: self.click_register())

        l2 = Label(self.root, text='Password', font = 'Helvetica 15 bold', fg="gray", bg="white", highlightbackground="white")
        l2.place(x=80, y=280)

        self.widgets.extend([f2, l4, e4, e2, l2])

        f3 = Frame(self.root, width=180, height=2, bg='#141414')
        f3.place(x=80, y=332)
        f4 = Frame(self.root, width=180, height=2, bg='#141414')
        f4.place(x=80, y=252)
        self.widgets.extend([f3, f4])
        
        self.bttn(100, 375, 'Register', 'gray', '#994422', self.click_register)

        b2 = Button(self.root, text = "Log in", bg='white', fg = 'blue', font = 'Helvetica 10', command=self.on_login, highlightbackground="white")
        b2.place(x = 68, y = 422)
        self.widgets.append(b2)
    
    def close(self):
        self.destroy_widgets()
        self.root.geometry("")

    def click_register(self):
        result = self.on_register(self.username.get(), self.password.get())
        if result == REGISTER_RESULT.SUCCESS:
            self.close()
            self.on_home()
        else:
            self.display_error(result)
    
    def display_error(self, result):
        l = Label(self.root, text=REGISTER_RESULT_MESSAGE[result], bg='white', fg='red', font = 'Helvetica 12')
        l.place(x=80, y=342)
        if self.error is not None:
            self.error.destroy()
        self.error = l
        self.widgets.append(l)

    def bttn(self, x, y, text, ecolor, lcolor, on_click=None):
        def on_entera(e):
            myButton1['background'] = ecolor  
            myButton1['foreground'] = lcolor  

        def on_leavea(e):
            myButton1['background'] = lcolor
            myButton1['foreground'] = ecolor

        myButton1 = Button(self.root, text=text,width=20,height=2,fg=ecolor, bg=lcolor,activeforeground=lcolor,activebackground=ecolor, highlightbackground="white", command=on_click)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x-35, y=y)
        self.widgets.append(myButton1)


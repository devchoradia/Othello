from tkinter import *
from view.abstract_page_view import AbstractPageView, ROW_HEIGHT
from model.views import Views
from server.database_client import LOGIN_RESULT, LOGIN_RESULT_MESSAGE, REGISTER_RESULT, REGISTER_RESULT_MESSAGE
import math
from abc import abstractmethod
from PIL import Image, ImageTk

LOGO_LENGTH = 130

class AccountInfoView(AbstractPageView):
    '''
    Renders a page where a user inputs their username and password
    '''
    def __init__(self, root, on_submit, on_switch_view, on_home, view=Views.LOGIN, \
        submit_results = LOGIN_RESULT, result_messages = LOGIN_RESULT_MESSAGE, \
        submit_label="LOGIN", switch_view_label="Register account"):
        super().__init__(root, view, on_home=on_home)
        self.on_submit = on_submit
        self.on_home = on_home
        self.on_switch_view = on_switch_view
        self.username = StringVar()
        self.password = StringVar()
        self.error = None
        self.submit_results = submit_results
        self.result_messages = result_messages
        self.submit_label = submit_label
        self.switch_view_label = switch_view_label
        logo = Image.open("logo.png").resize((LOGO_LENGTH, LOGO_LENGTH), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(logo)

    
    def display(self):
        self.root.geometry('350x500')
        main_frame = Frame(self.root, width=250, height=420, bg='white')
        self.main_frame = main_frame
        font = ('Consolas', 13)
        self.add_title()
        main_frame.place(anchor='center', relx=0.5, rely=0.5)

        self.add_logo()

        entry_frame = self.make_frame(0.5, 0.6)

        # Username label
        self.add_label('Username', entry_frame=entry_frame)

        # Username entry
        username_entry = Entry(entry_frame, width=20, border=0, textvariable=self.username, insertbackground="black", fg="black", bg="white", highlightbackground="white")
        username_entry.config(font=font)
        username_entry.pack()
        username_entry.focus()
        username_entry.bind('<Return>', lambda x: self.click_login())

        # Border
        f3 = Frame(entry_frame, width=180, height=2, bg='#141414')
        f3.pack()

        # Password label
        self.add_label('Password', (10,0), entry_frame)

        e2 = Entry(entry_frame, width=20, border=0, show='*', textvariable=self.password, insertbackground="black", fg="black", bg="white", highlightbackground="white")
        e2.config(font=font)
        e2.pack()
        e2.bind('<Return>', lambda x: self.click_login())

        # Border
        f4 = Frame(entry_frame, width=180, height=2, bg='#141414')
        f4.pack()

        # Frame for login/register buttons
        self.add_buttons()

    def make_frame(self, relx=0.5, rely=0.5, width=None, height=None, parent=None):
        if parent is None:
            parent = self.main_frame
        frame = Frame(parent, width=width, height=height, bg="white", highlightbackground="white")
        frame.pack()
        frame.place(anchor='center', relx=relx, rely=rely)
        return frame

    def add_buttons(self):
        e_color = 'gray'
        l_color = '#994422'
        button_frame = Frame(self.main_frame, bg="white")
        button_frame.pack()
        button_frame.place(anchor='center', relx=0.5, rely=0.89)

        submit_button = Button(button_frame, text=self.submit_label,width=20,height=2,fg=e_color, bg=l_color,activeforeground=l_color,activebackground=e_color, highlightbackground="white", command=self.click_login)

        def on_hover(e):
            submit_button['background'] = e_color  
            submit_button['foreground'] = l_color  

        def on_leave(e):
            submit_button['background'] = l_color
            submit_button['foreground'] = e_color

        submit_button.bind("<Enter>", on_hover)
        submit_button.bind("<Leave>", on_leave)

        submit_button.pack()

        switch_view_button = Button(button_frame, text=self.switch_view_label, bg='white', fg = 'blue', font = 'Helvetica 10', borderwidth=3, highlightbackground="white", command=self.switch_view)
        switch_view_button.pack(side=TOP, pady=5)

    def add_label(self, label, pady=None, entry_frame=None):
        l1 = Label(entry_frame, text=label, fg='gray', bg='white', font='Helvetica 15 bold')
        l1.pack(anchor='w', pady=pady)

    def add_title(self):
        title_frame = Frame(self.main_frame, bg="white")
        title_frame.pack()
        title_frame.place(anchor='n', relx=0.5)
        label = Label(title_frame, relief=RAISED, borderwidth=1, width=self.main_frame.cget("width"), height=ROW_HEIGHT, font=("Arial", 25), text=self.title, bg="white", fg="black")
        label.pack(expand=True)
    
    def add_logo(self):
        img_frame = self.make_frame(0.5, 0.3, LOGO_LENGTH, LOGO_LENGTH)
        label = Label(img_frame, image = self.logo, bg="white")
        label.pack()

    def close(self):
        super().close()
        self.root.geometry("")

    def switch_view(self):
        self.close()
        self.on_switch_view()

    def click_login(self):
        result = self.on_submit(self.username.get(), self.password.get())
        if result == self.submit_results.SUCCESS:
            self.close()
            self.on_home()
        else:
            self.display_error(result)
    
    def display_error(self, result):
        l = Label(self.root, text=self.result_messages[result], bg='white', fg='red', font = 'Helvetica 11')
        l.place(x=79, y=348)
        if self.error is not None:
            self.error.destroy()
        self.error = l


from tkinter import *

from PIL import Image, ImageTk

from model.views import Views
from server.database_client import LOGIN_RESULT, LOGIN_RESULT_MESSAGE
from view.abstract_page_view import PageView, ROW_HEIGHT, TEXT_FONT, APP_COLOR

LOGO_LENGTH = 200


class AccountInfoView(PageView):
    '''
    Renders a page where a user inputs their username and password
    '''

    def __init__(self, master, on_submit, on_switch_view, on_home, view=Views.LOGIN, \
                 submit_results=LOGIN_RESULT, result_messages=LOGIN_RESULT_MESSAGE, \
                 submit_label="LOGIN", switch_view_label="Register account"):
        super().__init__(master, view, on_home=on_home, width=500, height=600, bg='white')
        master.geometry('600x800')
        master['background'] = APP_COLOR
        self.on_submit = on_submit
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
        font = TEXT_FONT
        self.add_title()
        self.place(anchor='center', relx=0.5, rely=0.5)

        self.add_logo()

        entry_frame = self.make_frame(0.5, 0.6)

        # Username label
        self.add_label('Username', entry_frame=entry_frame)

        # Username entry
        username_entry = Entry(entry_frame, width=30, border=0, textvariable=self.username, insertbackground="black",
                               fg="black", bg="white", highlightbackground="white")
        username_entry.config(font=font)
        username_entry.pack()
        username_entry.focus()
        username_entry.bind('<Return>', lambda x: self.click_login())

        # Border
        f3 = Frame(entry_frame, width=265, height=2, bg='#141414')
        f3.pack()

        # Password label
        self.add_label('Password', (10, 0), entry_frame)

        e2 = Entry(entry_frame, width=30, border=0, show='*', textvariable=self.password, insertbackground="black",
                   fg="black", bg="white", highlightbackground="white")
        e2.config(font=font)
        e2.pack()
        e2.bind('<Return>', lambda x: self.click_login())

        # Border
        f4 = Frame(entry_frame, width=265, height=2, bg='#141414')
        f4.pack()

        # Frame for login/register buttons
        self.add_buttons()

    def make_frame(self, relx=0.5, rely=0.5, width=None, height=None):
        frame = Frame(self, width=width, height=height, bg="white", highlightbackground="white")
        frame.pack()
        frame.place(anchor='center', relx=relx, rely=rely)
        return frame

    def add_buttons(self):
        e_color = 'gray'
        l_color = '#994422'
        button_frame = Frame(self, bg="white")
        button_frame.pack()
        button_frame.place(anchor='center', relx=0.5, rely=0.85)

        submit_button = Button(button_frame, text=self.submit_label, width=20, height=2, fg=e_color, bg=l_color,
                               activeforeground=l_color, activebackground=e_color, highlightbackground="white",
                               command=self.click_login)

        def on_hover(e):
            submit_button['background'] = e_color
            submit_button['foreground'] = l_color

        def on_leave(e):
            submit_button['background'] = l_color
            submit_button['foreground'] = e_color

        submit_button.bind("<Enter>", on_hover)
        submit_button.bind("<Leave>", on_leave)

        submit_button.pack()

        switch_view_button = Button(button_frame, text=self.switch_view_label, bg='white', fg = 'blue', font = 'Helvetica 12', borderwidth=3, highlightbackground="white", command=self.on_switch_view)
        switch_view_button.pack(side=TOP, pady=5)

        login_as_guest_button = Button(button_frame, text="Log in as guest", bg='white', fg='blue', font='Helvetica 12',
                                       borderwidth=3, highlightbackground="white", command=self.on_home)
        login_as_guest_button.pack(side=TOP, pady=2)

    def add_label(self, label, pady=None, entry_frame=None):
        l1 = Label(entry_frame, text=label, fg='gray', bg='white', font='Helvetica 15 bold')
        l1.pack(anchor='w', pady=pady)

    def add_logo(self):
        img_frame = self.make_frame(0.5, 0.3, LOGO_LENGTH, LOGO_LENGTH)
        label = Label(img_frame, image=self.logo, bg="white")
        label.pack()

    def click_login(self):
        result = self.on_submit(self.username.get(), self.password.get())

    def login_result(self, result):
        if result == self.submit_results.SUCCESS:
            self.on_home()
        else:
            self.display_error(result)

    def display_error(self, result):
        l = Label(self, text=self.result_messages[result], bg='white', fg='red', font='Helvetica 14')
        l.place(relx=0.5, rely=0.73, anchor=CENTER)
        if self.error is not None:
            self.error.destroy()
        self.error = l

    def add_title(self):
        title_frame = Frame(self, bg="white")
        title_frame.pack()
        title_frame.place(anchor='n', relx=0.5)
        label = Label(title_frame, relief=RAISED, borderwidth=1, width=self.cget("width"), height=ROW_HEIGHT,
                      font=("Palatino", 40), text=self.title, bg="white", fg="black")
        label.pack(expand=True)

from tkinter import *

class login:
    def __init__(self):

        root = Tk()
        root.geometry('350x500')
        root.title(' LOGIN ')
        root.resizable(0, 0)

        j = 0
        k = 10
        for i in range(100):
            c = str(222222 + k)
            Frame(root, width=10, height=500, bg="#" + c).place(x=j, y=0)
            j = j + 10
            k += 1




        Frame(root, width=250, height=400, bg='white').place(x=50, y=50)





        l1 = Label(root, text='Username', bg='white', font='Helvetica 15 bold')
        t = ('Consolas', 13)
        l1.place(x=80, y=200)

        e1 = Entry(root, width=20, border=0)
        e1.config(font= t)
        e1.place(x=80, y=230)

        e2 = Entry(root, width=20, border=0, show='*')
        e2.config(font=t)
        e2.place(x=80, y=310)

        l2 = Label(root, text='Password', bg='white', font = 'Helvetica 15 bold')
        l2.place(x=80, y=280)


        Frame(root, width=180, height=2, bg='#141414').place(x=80, y=332)
        Frame(root, width=180, height=2, bg='#141414').place(x=80, y=252)




        def bttn(x, y, text, ecolor, lcolor):
            def on_entera(e):
                myButton1['background'] = ecolor  
                myButton1['foreground'] = lcolor  

            def on_leavea(e):
                myButton1['background'] = lcolor
                myButton1['foreground'] = ecolor

            myButton1 = Button(root, text=text,width=20,height=2,fg=ecolor, bg=lcolor,activeforeground=lcolor,activebackground=ecolor,)

            myButton1.bind("<Enter>", on_entera)
            myButton1.bind("<Leave>", on_leavea)

            myButton1.place(x=x-35, y=y)

        bttn(100, 375, 'LOGIN', 'white', '#994422')
        
        
        b2 = Button(root, text = "Haven't registered here? Click here", bg='white', fg = 'blue', font = 'Helvetica 10')
        b2.place(x = 68, y = 422)

        
        
        root.mainloop()

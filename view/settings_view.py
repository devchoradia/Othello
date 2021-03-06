import tkinter as tk

from model.settings import Settings, Setting
from model.views import Views
from view.abstract_page_view import GridPageView, STICKY, ROW_HEIGHT, BUTTON_FONT

COLUMNS = ["Setting", "Value"]
COLUMN_WIDTHS = [15, 15]


class SettingsView(GridPageView):
    def __init__(self, master, on_home):
        super().__init__(master, Views.SETTINGS, len(COLUMNS), on_home=on_home)
        board_color = tk.StringVar()
        board_color.set(Settings().get_board_color())
        board_size = tk.IntVar()
        board_size.set(Settings().get_board_size())
        game_mode = tk.Variable()
        game_mode.set(Settings().get_game_mode())
        self.saved = tk.BooleanVar()
        self.setting_inputs = {
            Setting.BOARD_SIZE: board_size,
            Setting.BOARD_COLOR: board_color,
            Setting.GAME_MODE: game_mode
        }
        self.saved.set(False)

    def display(self):
        # Configure rows and columns
        for row in range(len(Setting) + 4):
            self.rowconfigure(row, weight=1, minsize=50)
        for col in range(len(COLUMNS)):
            self.columnconfigure(col, weight=1)

        self.add_title()  # row 0
        self.add_column_labels(1)  # row 1
        self.add_settings(2)  # beginning at row 2
        self.add_save(5)  # row 5
        self.add_navigator(6)  # row 6

        self.pack(expand=True, fill=tk.BOTH)

    def add_settings(self, start_row):
        for index, setting in enumerate(Setting):
            row = start_row + index
            # Setting name
            label_frame = tk.Frame(self, padx=5, pady=5, relief=tk.RAISED, borderwidth=1, bg='white')
            label_frame.grid(row=row, column=0, sticky=STICKY)
            tile = tk.Label(label_frame, borderwidth=1, font=("Palatino", 20), width=COLUMN_WIDTHS[0],
                            height=ROW_HEIGHT, text=Settings().get_setting_label(setting), bg="white", fg="black")
            tile.pack(ipadx=1, ipady=1, expand=True)
            # Setting value
            options_frame = tk.Frame(self, padx=5, pady=5, relief=tk.RAISED, borderwidth=1, bg='white')
            options_frame.grid(row=row, column=1, sticky=STICKY)
            option = tk.OptionMenu(options_frame, self.setting_inputs[setting],
                                   *Settings().get_setting_options(setting))
            option.config(bg="white", fg="black")
            option.pack(ipadx=1, ipady=1, expand=True)

    def add_save(self, row):
        frame = tk.Frame(self, padx=5, pady=5, relief=tk.RAISED, borderwidth=2, bg='white')
        frame.grid(row=row, columnspan=self.columnspan, sticky=STICKY)
        save = tk.Button(frame, text="Save", command=self.save, background="white", bg="white",
                         highlightbackground="white")
        save.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def add_column_labels(self, row):
        for index, column in enumerate(COLUMNS):
            frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1, bg='gray')
            frame.grid(row=row, column=index, sticky=STICKY)
            tile = tk.Label(frame, font=BUTTON_FONT, borderwidth=1, width=COLUMN_WIDTHS[0], height=ROW_HEIGHT,
                            text=column, bg="gray")
            tile.pack(expand=True)

    def save(self):
        self.saved.set(True)
        self.close()

    def close(self):
        if (self.saved.get()):
            settings = {k: v.get() for k, v in self.setting_inputs.items()}
            Settings().save_settings(settings)
        self.on_home()

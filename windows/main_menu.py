from tkinter import Tk, SOLID

from app_strings.app_strings import main_menu_title, main_menu_size, checksum_window_title, diff_window_title, \
    diff_window_size
from windows.crc_sum import CRCSum
from windows.difference import Diff
from frames.frames import MainMenuFrame


class MainMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title(main_menu_title)
        self.geometry(main_menu_size)
        self.resizable(False, False)
        self.make_frame()

    def make_frame(self):
        self.frame = MainMenuFrame(master=self, padding=[10, 10], height=100, width=450,
                                borderwidth=1, relief=SOLID)
        self.frame.pack(expand=True, padx=20, pady=20, fill='both')

    def get_hash(self):
        self.withdraw()
        self.hash_window = CRCSum(self, checksum_window_title, main_menu_size)

    def get_diff(self):
        self.withdraw()
        self.diff_window = Diff(self, diff_window_title, diff_window_size)

    def start(self):
        self.mainloop()

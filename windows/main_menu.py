from tkinter import Tk, SOLID

from windows.crc_sum import CRCSum
from windows.difference import Diff
from frames.frames import MainMenuFrame


class MainMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title('CRC sum')
        self.geometry('500x440+500+200')
        self.resizable(False, False)
        self.make_frame()

    def make_frame(self):
        self.frame = MainMenuFrame(master=self, padding=[10, 10], height=100, width=450,
                                borderwidth=1, relief=SOLID)
        self.frame.pack(expand=True, padx=20, pady=20, fill='both')

    def get_hash(self):
        self.withdraw()
        self.hash_window = CRCSum(self, 'CRC Amount', '500x440+500+200')

    def get_diff(self):
        self.withdraw()
        self.diff_window = Diff(self, 'CRC difference', '500x500+500+100')

    def start(self):
        self.mainloop()

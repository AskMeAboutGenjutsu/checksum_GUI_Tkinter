from tkinter import SOLID, filedialog, ACTIVE
from tkinter.messagebox import showwarning, showinfo

from app_strings.app_strings import showwarning_title, \
    successful_message_save_format, showinfo_save_title
from frames.frames import FileFrame, HashFrame, InfoFrame
from functional.work_with_csv import CSVSaver
from windows.base_toplevel import BaseToplevel
from windows.custom_exception import EmptyFilepathError


class CRCSum(BaseToplevel):
    def make_file_frame(self):
        self.file_frame = FileFrame(master=self, padding=[10, 10], height=150, width=480,
                                borderwidth=1, relief=SOLID)
        self.file_frame.place(x=10, y=10)

    def make_hash_frame(self):
        self.hash_frame = HashFrame(master=self, padding=[10, 10], height=70, width=480,
                                borderwidth=1, relief=SOLID)
        self.hash_frame.place(x=10, y=170)

    def make_info_frame(self):
        self.info_frame = InfoFrame(master=self)
        self.info_frame.place(x=10, y=250)

    def save_hash(self):
        try:
            filepath = filedialog.asksaveasfilename(defaultextension='.csv',
                                                    filetypes=(('.csv', '*.csv'),))
            if self.is_not_empty_filepath(filepath):
                info = self.hash.get_hash()
                csv = CSVSaver(filepath, info)
                csv.save()
                showinfo(title=showinfo_save_title,
                         message=self.successful_message.format(successful_message_save_format))
        except EmptyFilepathError:
            showwarning(title=showwarning_title,
                        message=self.filepath_warning_massage)

    def show_file_system(self):
        super().show_file_system()
        if self.flag:
            self.hash_frame.hash_button['state'] = ACTIVE

from tkinter import SOLID, filedialog, END, DISABLED, ACTIVE
from tkinter.messagebox import showwarning

from frames.frames import FileDiffFrame, HashFrame, InfoFrame
from functional.work_with_csv import CSVParser
from windows.base_toplevel import BaseToplevel
from windows.custom_exception import EmptyFilepathError


class Diff(BaseToplevel):
    def make_file_frame(self):
        self.file_frame = FileDiffFrame(master=self, padding=[10, 10], height=210, width=480,
                                borderwidth=1, relief=SOLID)
        self.file_frame.place(x=10, y=10)
        self.flag = False
        self.flag_csv = False

    def make_hash_frame(self):
        self.hash_frame = HashFrame(master=self, padding=[10, 10], height=70, width=480,
                                    borderwidth=1, relief=SOLID)
        self.hash_frame.place(x=10, y=230)

    def make_info_frame(self):
        self.info_frame = InfoFrame(master=self)
        self.info_frame.place(x=10, y=310)

    def show_file_system(self):
        super().show_file_system()
        if self.flag and self.flag_csv:
            self.hash_frame.hash_button['state'] = ACTIVE

    def show_file_system_csv(self):
        self.file_frame.entry_filepath_csv.delete(0, END)
        try:
            self.path_csv = filedialog.askopenfilename(defaultextension='.csv',
                                                    filetypes=(('.csv', '*.csv'),))
            if self.is_not_empty_filepath(self.path_csv):
                self.file_frame.entry_filepath_csv.insert(0, self.path_csv)
                self.flag_csv = True
                if self.flag and self.flag_csv:
                    self.hash_frame.hash_button['state'] = ACTIVE
        except EmptyFilepathError:
            showwarning(title="Предупреждение",
                        message=self.filepath_warning_massage)

    def change_state(self, state):
        super().change_state(state)
        self.file_frame.select_button_csv['state'] = ACTIVE if state else DISABLED

    def get_info(self):
        parser = CSVParser(self.path_csv)
        parser.parse()
        info_csv = parser.get_hash()
        new_info = self.hash.get_hash()
        self.info = self.update_info(info_csv, new_info)
        if len(info_csv) != len(new_info):
            showwarning(title="Предупреждение",
                    message='Разное количество файлов')
        self.change_state(True)
        
    def update_info(self, info_csv, new_info):
        info = {}
        for key, val in info_csv.items():
            if key in new_info:
                info[key] = [val, new_info[key]]
            else:
                info[key] = [val, 'Пусто']
        for key, val in new_info.items():
            if key not in info:
                info[key] = ['Пусто', val]
        return info


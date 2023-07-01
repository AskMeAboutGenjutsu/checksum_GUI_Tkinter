from tkinter import Label, CENTER, Entry, DISABLED, Text
from tkinter.constants import BOTTOM, X, RIGHT, Y, LEFT, BOTH, END
from tkinter.ttk import Combobox, Button, Frame, Scrollbar, Style


class BaseFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = kwargs['master']
        self.widgets_font = 'helvetica 10'
        self.button_style = Style(self).configure('My.TButton',
                                              font=self.widgets_font,
                                              foreground='black',
                                              justify=CENTER)
        self.make_widgets()

    def make_widgets(self):
        pass


class MainMenuFrame(BaseFrame):
    def make_widgets(self):
        self.button_calc_hash = Button(self,
                                       style='My.TButton',
                                       text='Вычислить HASH файла/\nдиректории',
                                       command=self.master.get_hash)
        self.button_calc_diff = Button(self,
                                       style='My.TButton',
                                       text='Вычислить разницу файлов/\nдиректорий',
                                       command=self.master.get_diff)
        self.button_calc_hash.pack(anchor='center', pady=90)
        self.button_calc_diff.pack(anchor='center', )


class FileFrame(BaseFrame):
    def make_widgets(self):
        self.label_choice = Label(self,
                                  text='Выберите с чего будет снята контрольная сумма:',
                                  font=self.widgets_font)
        self.label_choice.place(x=5, y=27)
        self.combobox = Combobox(self, values=['Файл', 'Директория'],
                                 justify=CENTER, font=self.widgets_font, width=18)
        self.combobox.place(x=310, y=28)
        self.label_filepath = Label(self, text='Путь до файла/директории:',
                                    font=self.widgets_font)
        self.label_filepath.place(x=5, y=63)
        self.entry_filepath = Entry(self, width=47, font=self.widgets_font,
                                    justify=CENTER)
        self.entry_filepath.place(x=5, y=90)
        self.select_button = Button(self,
                                    style='My.TButton',
                                    text='Выберите файл/\nдиректорию',
                                    command=self.master.show_file_system)
        self.select_button.place(x=350, y=80)


class HashFrame(BaseFrame):
    def make_widgets(self):
        self.hash_button = Button(self,
                                  style='My.TButton',
                                  text='Вычислить контрольную\nсумму',
                                  command=self.master.start_calc_hash,
                                  state=DISABLED)
        self.save_button = Button(self,
                                  style='My.TButton',
                                  text='Сохранить',
                                  command=self.master.save_hash,
                                  state=DISABLED)
        self.save_button.place(x=360, y=10)
        self.hash_button.place(x=5, y=5)


class InfoFrame(BaseFrame):
    def make_widgets(self):
        self.vbar = Scrollbar(self)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar = Scrollbar(self, orient='horizontal')
        self.hbar.pack(side=BOTTOM, fill=X)
        self.info_text = Text(self,
                              wrap='none',
                              height=10, width=66,
                              font=self.widgets_font,
                              xscrollcommand=self.hbar.set,
                              yscrollcommand=self.vbar.set)
        self.info_text.bind('<<Modified>>', self.show_info_end)
        self.info_text.pack(side=LEFT, fill=BOTH, expand=True)
        self.vbar['command'] = self.info_text.yview
        self.hbar['command'] = self.info_text.xview

    def show_info_end(self, event):
        self.info_text.see(END)
        self.info_text.edit_modified(False)


class FileDiffFrame(FileFrame):
    def make_widgets(self):
        super().make_widgets()
        self.select_button.place(x=350, y=80)
        self.label_filepath_csv = Label(self, text='Путь до csv файла',
                                    font=self.widgets_font)
        self.label_filepath_csv.place(x=5, y=113)
        self.entry_filepath_csv = Entry(self, width=47, font=self.widgets_font,
                                     justify=CENTER)
        self.entry_filepath_csv.place(x=5, y=140)
        self.select_button_csv = Button(self,
                                     style='My.TButton',
                                     text='Выберите csv\nфайл',
                                     command=self.master.show_file_system_csv)
        self.select_button_csv.place(x=358, y=130)
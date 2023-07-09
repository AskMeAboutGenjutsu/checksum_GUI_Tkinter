from tkinter import Label, CENTER, Entry, DISABLED, Text
from tkinter.constants import BOTTOM, X, RIGHT, Y, LEFT, BOTH, END
from tkinter.ttk import Combobox, Button, Frame, Scrollbar, Style

from app_strings.app_strings import widgets_font, style_name, foreground_color, button_calc_hash_text, \
    button_calc_diff_text, label_choice_text, combobox_values, label_filepath_text, select_button_text, \
    hash_button_text, save_button_text, label_filepath_csv_text, select_button_csv_text


class BaseFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = kwargs['master']
        self.widgets_font = widgets_font
        self.button_style = Style(self).configure(style_name,
                                                  font=self.widgets_font,
                                                  foreground=foreground_color,
                                                  justify=CENTER)
        self.make_widgets()

    def make_widgets(self):
        pass


class MainMenuFrame(BaseFrame):
    def make_widgets(self):
        self.button_calc_hash = Button(self,
                                       style=style_name,
                                       text=button_calc_hash_text,
                                       command=self.master.get_hash)
        self.button_calc_diff = Button(self,
                                       style='My.TButton',
                                       text=button_calc_diff_text,
                                       command=self.master.get_diff)
        self.button_calc_hash.pack(anchor='center', pady=90)
        self.button_calc_diff.pack(anchor='center', )


class FileFrame(BaseFrame):
    def make_widgets(self):
        self.label_choice = Label(self,
                                  text=label_choice_text,
                                  font=self.widgets_font)
        self.label_choice.place(x=5, y=27)
        self.combobox = Combobox(self, values=combobox_values,
                                 justify=CENTER, font=self.widgets_font, width=18)
        self.combobox.place(x=310, y=28)
        self.label_filepath = Label(self, text=label_filepath_text,
                                    font=self.widgets_font)
        self.label_filepath.place(x=5, y=63)
        self.entry_filepath = Entry(self, width=47, font=self.widgets_font,
                                    justify=CENTER)
        self.entry_filepath.place(x=5, y=90)
        self.select_button = Button(self,
                                    style=style_name,
                                    text=select_button_text,
                                    command=self.master.show_file_system)
        self.select_button.place(x=350, y=80)


class HashFrame(BaseFrame):
    def make_widgets(self):
        self.hash_button = Button(self,
                                  style=style_name,
                                  text=hash_button_text,
                                  command=self.master.start_calc_hash,
                                  state=DISABLED)
        self.save_button = Button(self,
                                  style=style_name,
                                  text=save_button_text,
                                  command=self.master.save_hash,
                                  state=DISABLED)
        self.save_button.place(x=360, y=5)
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
        self.label_filepath_csv = Label(self, text=label_filepath_csv_text,
                                        font=self.widgets_font)
        self.label_filepath_csv.place(x=5, y=113)
        self.entry_filepath_csv = Entry(self, width=47, font=self.widgets_font,
                                        justify=CENTER)
        self.entry_filepath_csv.place(x=5, y=140)
        self.select_button_csv = Button(self,
                                        style=style_name,
                                        text=select_button_csv_text,
                                        command=self.master.show_file_system_csv)
        self.select_button_csv.place(x=357, y=130)

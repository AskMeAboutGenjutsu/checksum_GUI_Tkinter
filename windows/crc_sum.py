import threading
from tkinter import SOLID, filedialog, END, DISABLED, ACTIVE, INSERT
from tkinter.messagebox import showwarning, showinfo

from functional.calc_hash import Hash
from frames.frames import FileFrame, HashFrame, InfoFrame
from functional.work_with_csv import CSVSaver
from windows.base_toplevel import BaseToplevel
from windows.custom_exception import EmptyFilepathError, ComboboxError


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
                showinfo(title='Успешное сохранение',
                         message=self.successful_message.format('сохранена'))
        except EmptyFilepathError:
            showwarning(title="Предупреждение",
                        message=self.filepath_warning_massage)

    def show_file_system(self):
        self.file_frame.entry_filepath.delete(0, END)
        try:
            if self.is_file(self.file_frame.combobox):
                self.path = filedialog.askopenfilename()
            else:
                self.path = filedialog.askdirectory()
            if self.is_not_empty_filepath(self.path):
                self.file_frame.entry_filepath.insert(0, self.path)
                self.hash_frame.hash_button['state'] = ACTIVE
        except ComboboxError:
            showwarning(title="Предупреждение",
                        message=self.combo_warning_massage)
        except EmptyFilepathError:
            showwarning(title="Предупреждение",
                        message=self.filepath_warning_massage)

    def start_calc_hash(self):
        self.change_state(False)
        self.info_frame.info_text.delete('0.0', END)
        self.hash = Hash(self.path, self.queue_update)
        self.thread = threading.Thread(target=self.hash.calc_hash)
        self.thread.start()
        self.poll_queue()

    def change_state(self, state):
        self.file_frame.combobox['state'] = ACTIVE if state else DISABLED
        self.file_frame.select_button['state'] = ACTIVE if state else DISABLED
        self.hash_frame.hash_button['state'] = ACTIVE if state else DISABLED
        self.hash_frame.save_button['state'] = ACTIVE if state else DISABLED

    def poll_queue(self):
        if not self.queue.empty() or self.thread.is_alive():
            info = self.queue.get()
            self.info_frame.info_text.insert(INSERT, info)
            self.after(self.ms_refresh, self.poll_queue)
        else:
            self.thread.join()
            showinfo(title='Успешное завершение',
                     message=self.successful_message.format('снята'))
            self.change_state(True)


# if __name__ == '__main__':
#     app = CRCSum()
#     app.mainloop()

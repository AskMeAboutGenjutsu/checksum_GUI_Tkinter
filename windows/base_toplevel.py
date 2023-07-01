import threading
from queue import Queue
from tkinter import ACTIVE, DISABLED, END, INSERT, Toplevel, filedialog
from tkinter.messagebox import showinfo, showwarning

from app_strings.app_strings import successful_message, combo_warning_massage, filepath_warning_massage, \
    showwarning_title, showinfo_save_title, successful_message_save_format, file_str, showinfo_end_title, \
    successful_message_end_format
from functional.calc_hash import Hash
from functional.work_with_csv import CSVSaver

from windows.custom_exception import EmptyFilepathError, ComboboxError


class BaseToplevel(Toplevel):
    def __init__(self, master, title, size):
        super().__init__(master)
        self.queue = Queue()
        self.ms_refresh = 15
        self.title(title)
        self.geometry(size)
        self.resizable(False, False)
        self.successful_message = successful_message
        self.combo_warning_massage = combo_warning_massage
        self.filepath_warning_massage = filepath_warning_massage
        self.flag = False
        self.info = ''
        self.make_file_frame()
        self.make_hash_frame()
        self.make_info_frame()
        self.wm_protocol('WM_DELETE_WINDOW', self.on_close)

    def show_file_system(self):
        self.file_frame.entry_filepath.delete(0, END)
        try:
            if self.is_file(self.file_frame.combobox):
                self.path = filedialog.askopenfilename()
            else:
                self.path = filedialog.askdirectory()
            if self.is_not_empty_filepath(self.path):
                self.file_frame.entry_filepath.insert(0, self.path)
                self.flag = True
        except ComboboxError:
            showwarning(title=showwarning_title,
                        message=self.combo_warning_massage)
        except EmptyFilepathError:
            showwarning(title=showwarning_title,
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

    def save_hash(self):
        try:
            filepath = filedialog.asksaveasfilename(defaultextension='.csv',
                                                    filetypes=(('.csv', '*.csv'),))
            if self.is_not_empty_filepath(filepath):
                saver = CSVSaver(filepath, self.info)
                saver.save()
                showinfo(title=showinfo_save_title,
                         message=self.successful_message.format(successful_message_save_format))
        except EmptyFilepathError:
            showwarning(title=showwarning_title,
                        message=self.filepath_warning_massage)

    def on_close(self):
        self.destroy()
        self.master.destroy()

    def is_file(self, combobox):
        if file := combobox.get():
            if file == file_str:
                return True
            return False
        raise ComboboxError

    def is_not_empty_filepath(self, path):
        if path:
            return True
        raise EmptyFilepathError

    def queue_update(self, info):
        self.queue.put(info)

    def poll_queue(self):
        if not self.queue.empty() or self.thread.is_alive():
            info = self.queue.get()
            self.info_frame.info_text.insert(INSERT, info)
            self.after(self.ms_refresh, self.poll_queue)
        else:
            self.thread.join()
            showinfo(title=showinfo_end_title,
                     message=self.successful_message.format(successful_message_end_format))
            self.change_state(True)
            self.get_info()

    def get_info(self):
        pass

    def make_file_frame(self):
        pass

    def make_hash_frame(self):
        pass

    def make_info_frame(self):
        pass

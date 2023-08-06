"""
This a good library to write an IDE.
It need tkinter and tcl (version >= 8.5)
You also need install chardet:
pip install chardet
I changed https://www.cnblogs.com/shuangzikun/p/python_tao_tao_tkinter_ide.html and
https://www.sohu.com/a/406318628_797291
"""

import json
import os
import string
import pickle
import builtins
import keyword
import tkinter as tk
import tkinter.messagebox as mbox
import tkinter.filedialog as fbox

try:
    import chardet
except (ImportError, ModuleNotFoundError):
    raise SystemExit('must install chardet')

from idegui import ResultBox

if tk.TkVersion < 8.5 or tk.TclVersion < 8.5:
    raise SystemExit('It need tkinter and tcl (version >= 8.5)')


__all__ = ['IDEConfig', 'IDEWindow']


def _get_encoding(file):
    with open(file, 'rb') as content:
        encoding = chardet.detect(content.read()).get('encoding', 'utf-8')
    return encoding


def _read(file, **kwargs):
    encoding = _get_encoding(file)
    try:
        with open(file, 'r', encoding=encoding, **kwargs) as f:
            result = f.read()
    except (Exception, SystemExit):
        with open(file, 'r', encoding='utf-8', **kwargs) as f:
            result = f.read()
            encoding = 'utf-8'
    return result, encoding


class IDEConfig(object):
    def __init__(self, configs: dict):
        self.configs = configs
    
    def __str__(self):
        return str(self.configs)
    
    def get(self, key, default=None):
        return self.configs.get(key, default)
    
    def set(self, key, value):
        self.configs[key] = value
    
    def from_dict(self, dictionary: dict):
        self.configs = dictionary.copy()
    
    def from_json(self, json_path: str, encoding='utf-8', *args, **kwargs):
        with open(json_path, 'r', encoding=encoding) as fp:
            self.configs = json.load(fp, *args, **kwargs)
    
    def from_object(self, obj: object):
        dictionary = {}
        for attr in dir(obj):
            if not attr.startswith('_'):
                dictionary.setdefault(attr, getattr(obj, attr))
        self.configs = dictionary.copy()
    
    def from_pickle(self, pickle_path, *args, **kwargs):
        with open(pickle_path, 'rb') as f:
            dictionary = pickle.load(f, *args, **kwargs)
        self.configs = dictionary.copy()
    
    def write_to_object(self, obj: object):
        for key, value in self.configs.items():
            setattr(obj, key, value)
    
    def write_to_pickle(self, pickle_path, *args, **kwargs):
        with open(pickle_path, 'wb') as f:
            pickle.dump(self.configs, f, *args, **kwargs)
    
    def write_to_json(self, json_path, encoding='utf-8', *args, **kwargs):
        with open(json_path, 'w+', encoding=encoding) as f:
            json.dump(self.configs, f, *args, **kwargs)


class IDEWindow(object):
    def __init__(self, name, **kwargs):
        self._init_config = {
            'app': name, 'status': 0, 'title': 'idegui', 'resizeable': False,
            'bifs': dir(builtins) + ['...'], 'kws': keyword.kwlist + ['self'],
            'author': 'stripe-python', 'minsize': (1000, 600),
            'themes': {
                'Default': '#000000.#FFFFFF',
                'Greygarious': '#83406A.#D1D4D1',
                'Aquamarine': '#5B8340.#D1E7E0',
                'Bold Beige': '#4B4620.#FFF0E1',
                'Cobalt Blue': '#ffffBB.#3333aa',
                'Olive Green': '#D1E7E0.#5B8340',
                'Night Mode': '#FFFFFF.#000000'
            }, 'default_theme': 'Default', 'welcome': 'Welcome to idegui!',
            'indent': ':', 'indent_length': 4, 'render_string': True,
            'annotation': '#', 'filetypes': [('Python Files', ['*.py', '*.pyw'])],
            'favicon': None, 'delete_indent': self._pass, 'render_number': True
        }
        self.config = IDEConfig(self._init_config)
        self.window = tk.Tk(**kwargs)
        self.file_name = None
        self.file_encoding = 'utf-8'
    
    def __str__(self):
        return '<IDEWindow in idegui config=%s>' % str(self.config)
    
    def _pass(self, *args, **kwargs):
        return self, args, kwargs
    
    def is_number(self, s: str):
        self._pass()
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def config_update(self, **configs):
        for key, value in configs.items():
            self.config.set(key, value)
    
    def change_theme(self):
        selected_theme = self.themes_choices.get()
        self.config.set('default_theme', selected_theme)
        fg_bg = self.config.get('themes').get(selected_theme)
        foreground, background = fg_bg.split('.')
        self.content_text.config(background=background, fg=foreground)
    
    def clear_code(self):
        self.content_text.delete(1.0, tk.END)
    
    def remove_tag(self, tag_name):
        self.content_text.tag_remove(tag_name, 1.0, tk.END)
    
    def cut(self):
        self.content_text.event_generate('<<Cut>>')
    
    def copy(self):
        self.content_text.event_generate('<<Copy>>')
    
    def paste(self):
        self.content_text.event_generate('<<Paste>>')
    
    def undo(self, event=None):
        self.event_handler(event)
        self.content_text.event_generate('<<Undo>>')
        return 'break'
    
    def redo(self, event=None):
        self.event_handler(event)
        self.content_text.event_generate('<<Redo>>')
        return 'break'
    
    def select_all(self, event=None):
        self.event_handler(event)
        self.content_text.tag_add('sel', '1.0', 'end')
        return 'break'
    
    def exit_text(self):
        if mbox.askyesnocancel('Quit?', 'Really quit?'):
            self.destroy()
    
    def event_handler(self, event):
        return self, event
    
    def find_text(self, event=None):
        self.event_handler(event)
        search_window = tk.Toplevel(self.window)
        search_window.title('Find Text')
        search_window.transient(self.window)
        search_window.resizable(False, False)
        find_text = tk.Label(search_window, text='Find All:', font=('Consoles', 12))
        find_text.grid(row=0, column=0, sticky='e')
        search_entry = tk.Entry(search_window, width=25)
        search_entry.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry.focus_set()
        ignore_case_value = tk.IntVar()
        ignore_case = tk.Checkbutton(search_window,
                                     text='Ignore Case',
                                     variable=ignore_case_value,
                                     font=('Consoles', 12))
        ignore_case.grid(row=1, column=1, sticky='e', padx=2, pady=2)
        find_all = tk.Button(search_window, text='Find All', underline=0,
                             command=lambda: self.search_output(
                                 search_entry.get(),
                                 ignore_case_value.get(),
                                 search_window,
                                 search_entry
                             ))
        find_all.grid(row=0, column=2, sticky=tk.EW, padx=2, pady=2)
        
        def close_search_window():
            self.content_text.tag_remove('match', '1.0', tk.END)
            search_window.destroy()
            return 'break'
        
        search_window.protocol('WM_DELETE_WINDOW', close_search_window)
    
    def search_output(self, needle, if_ignore_case,
                      search_window, search_box):
        self.content_text.tag_remove('match', '1.0', tk.END)
        matches_found = 0
        if needle:
            start_pos = '1.0'
            while True:
                start_pos = self.content_text.search(needle, start_pos,
                                                     nocase=if_ignore_case,
                                                     stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = '{}+{}c'.format(start_pos, len(needle))
                self.content_text.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
                self.content_text.tag_config('match', foreground='red',
                                             background='yellow')
                search_box.focus_set()
                search_window.title('{} matches found'.format(matches_found))
    
    def render_code(self, event=None):
        self.event_handler(event)
        self.content_text.tag_config('bif', foreground='purple')
        self.content_text.tag_config('kw', foreground='orange')
        self.content_text.tag_config('comment', foreground='red')
        self.content_text.tag_config('string', foreground='green')
        current_line_number, current_col_number = \
            map(int, self.content_text.index(tk.INSERT).split('.'))
        if event.keycode == 13 and self.config.get('indent'):  # press Enter
            last_line_number = current_line_number - 1
            last_line = self.content_text.get('%d.0' % last_line_number,
                                              tk.INSERT).rstrip()
            n = len(last_line) - len(last_line.lstrip())
            if (
                    last_line.endswith(self.config.get('indent')) or
                    (
                            (self.config.get('indent') in last_line) and
                            last_line.split(self.config.get('indent'))[-1]
                            .strip().startswith(self.config.get('annotation'))
                    )
            ):
                n += self.config.get('indent_length')
            elif self.config.get('delete_indent')(last_line.strip()):
                n -= self.config.get('indent_length')
            current_col_number += n
            self.content_text.insert(tk.INSERT, ' ' * n)
        
        elif event.keysym == 'BackSpace':
            current_line = self.content_text.get(
                '%d.0' % current_line_number,
                '%d.%d' % (current_line_number, current_col_number)
            )
            n = len(current_line) - len(current_line.rstrip())
            n = min(self.config.get('indent_length') - 1, n)
            if n > 1:
                self.content_text.delete(
                    '%d.%d' % (current_line_number, current_col_number - n),
                    '%d.%d' % (current_line_number, current_col_number)
                )
        
        else:
            lines = (self.content_text.get('0.0', tk.END).
                     rstrip('\n').splitlines(keepends=True))
            self.content_text.delete('0.0', tk.END)
            start = 0
            bifs = self.config.get('bifs')
            kws = self.config.get('kws')
            for line in lines:
                flag1 = flag2 = flag3 = False
                for index, char in enumerate(line):
                    if char == "'" and not flag2 and self.config.get('render_string'):
                        flag3 = not flag3
                        self.content_text.insert(tk.INSERT, char, 'string')
                    elif char == '"' and not flag3 and self.config.get('render_string'):
                        flag2 = not flag2
                        self.content_text.insert(tk.INSERT, char, 'string')
                    elif flag2 or flag3:
                        if self.config.get('render_string'):
                            self.content_text.insert(tk.INSERT, char, 'string')
                    else:
                        if char not in (string.ascii_letters + string.digits):
                            if flag1:
                                flag1 = False
                                word = line[start: index]
                                if word in bifs:
                                    self.content_text.insert(tk.INSERT, word, 'bif')
                                elif word in kws:
                                    self.content_text.insert(tk.INSERT, word, 'kw')
                                else:
                                    self.content_text.insert(tk.INSERT, word)
                            if char == self.config.get('annotation'):
                                self.content_text.insert(tk.INSERT,
                                                         line[index:], 'comment')
                                break
                            else:
                                self.content_text.insert(tk.INSERT, char)
                        else:
                            if not flag1:
                                flag1 = True
                                start = index
                if flag1:
                    word = line[start:]
                    if word in bifs:
                        self.content_text.insert(tk.INSERT, word, 'bif')
                    elif word in kws:
                        self.content_text.insert(tk.INSERT, word, 'kw')
                    else:
                        self.content_text.insert(tk.INSERT, word)
        
        self.content_text.mark_set(tk.INSERT, '%d.%d' %
                                   (current_line_number, current_col_number))
    
    def get_line_numbers(self):
        result = ''
        if self.show_line_number.get():
            row, col = self.content_text.index(tk.END).split('.')
            for n in range(1, int(row)):
                result += str(n)
                result += '\n'
        return result
    
    def update_line_numbers(self):
        line_numbers = self.get_line_numbers()
        self.line_number_bar.config(state='normal')
        self.line_number_bar.delete('0.0', tk.END)
        self.line_number_bar.insert('0.0', line_numbers)
        self.line_number_bar.config(state='disabled')
    
    def open_file(self, event=None):
        self.event_handler(event)
        if self.file_name:
            self.save()
        file_path = fbox.askopenfilename(title='Choose a File',
                                         filetypes=self.config.get('filetypes'))
        if file_path:
            try:
                code, encoding = _read(file_path)
            except (Exception, Warning):
                mbox.showerror('Error', 'File cannot read')
                return
            self.file_name = file_path
            self.file_encoding = encoding
            self.content_text.insert(1.0, code)
            self.window.title('%s - %s' % (os.path.basename(self.file_name),
                                           self.config.get('title')))
        self.update_line_numbers()
    
    def save(self, event=None):
        self.event_handler(event)
        try:
            if self.file_name:
                self.write_to_file(self.file_name)
            else:
                self.save_as()
        except (Exception, Warning):
            mbox.showerror('Error', 'File cannot write')
            return
        return 'break'
    
    def save_as(self, event=None):
        self.event_handler(event)
        input_file_name = fbox.asksaveasfilename(title='Choose Save File',
                                                 defaultextension='.txt',
                                                 filetypes=self.config.get('filetypes'))
        if input_file_name:
            self.file_name = input_file_name
            self.write_to_file(self.file_name)
            self.window.title('%s - %s' % (os.path.basename(self.file_name),
                                           self.config.get('title')))
        return 'break'
    
    def write_to_file(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf-8') as the_file:
                the_file.write(self.content_text.get('0.0', tk.END))
            self.file_encoding = 'utf-8'
        except IOError:
            pass
    
    def new_file(self, event=None):
        self.event_handler(event)
        self.window.title('Untitled')
        self.file_name = None
        self.clear_code()
    
    def run_code(self, event=None):
        self.event_handler(event)
        self.save(event)
        if self.file_name:
            result = os.popen('python %s' % self.file_name)
            result = result.read()
            ResultBox(self.window, result).show()
    
    def update_cursor_info_bar(self):
        row, col = self.content_text.index(tk.INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col) + 1)
        info_text = 'Line: %s | Column: %s | Encoding: %s' % \
                    (line_num, col_num, self.file_encoding)
        self.cursor_info_bar.config(text=info_text)
        
    def add_word(self, event=None):
        if not self.show_candidate_words.get():
            return
        self.event_handler(event)
        choose_index = self.auto_code_bar.curselection()
        choose_word = self.auto_code_bar.get(choose_index)
        
        current_line_number, current_col_number = \
            map(int, self.content_text.index(tk.INSERT).split('.'))
        current_line = self.content_text.get('%d.0' % current_line_number,
                                             tk.INSERT).strip()
        current_word = current_line.split(' ')[-1]
        self.content_text.delete('%d.%d' % (current_line_number,
                                            current_col_number - len(current_word)),
                                 tk.END)
        
        self.content_text.insert(tk.INSERT, choose_word)
        
    def auto_code(self):
        self.auto_code_bar.delete(0, tk.END)
        if not self.show_candidate_words.get():
            return
        
        current_line_number, current_col_number = \
            map(int, self.content_text.index(tk.INSERT).split('.'))
        current_line = self.content_text.get('%d.0' % current_line_number,
                                             tk.INSERT).strip()
        words = self.config.get('bifs') + self.config.get('kws')
        current_word = current_line.split(' ')[-1]
        if current_word in words:
            return
        candidate_words = []
        for w in words:
            if w.startswith(current_word):
                candidate_words.append(w)
        if not candidate_words:
            return
        
        self.auto_code_bar.insert(tk.END, *candidate_words)
    
    def on_content_changed(self, event=None):
        self.event_handler(event)
        self.update_line_numbers()
        self.update_cursor_info_bar()
        self.auto_code()
    
    def highlight_line(self, interval=100):
        self.remove_tag('active_line')
        self.content_text.tag_add('active_line', 'insert linestart',
                                  'insert lineend+1c')
        self.content_text.after(interval, self.toggle_highlight)
    
    def undo_highlight(self):
        self.remove_tag('active_line')
    
    def toggle_highlight(self):
        if self.to_highlight_line.get():
            self.highlight_line()
        else:
            self.undo_highlight()
    
    def force_close(self):
        if mbox.askyesnocancel('Force Close',
                               'Force Close not save your file, Really close?',
                               icon=mbox.WARNING):
            self.window.destroy()
    
    def show_cursor_info_bar(self):
        show_cursor_info_checked = self.show_cursor_info.get()
        if show_cursor_info_checked:
            self.cursor_info_bar.pack(expand=tk.NO, fill=None, side=tk.RIGHT, anchor=tk.SE)
        else:
            self.cursor_info_bar.pack_forget()
    
    def show_popup_menu(self, event=None):
        self.event_handler(event)
        self.popup_menu.tk_popup(event.x_root, event.y_root)
    
    def text_bind(self):
        self.content_text.bind('<Control-y>', self.redo)  # handling Ctrl + small-case y
        self.content_text.bind('<Control-Y>', self.redo)  # handling Ctrl + upper-case Y
        self.content_text.bind('<Control-a>', self.select_all)  # handling Ctrl + upper-case a
        self.content_text.bind('<Control-A>', self.select_all)  # handling Ctrl + upper-case A
        self.content_text.bind('<Control-f>', self.find_text)  # ctrl + f
        self.content_text.bind('<Control-F>', self.find_text)  # ctrl + F
        self.content_text.bind('<Control-N>', self.new_file)  # ctrl + N
        self.content_text.bind('<Control-n>', self.new_file)  # ctrl + n
        self.content_text.bind('<Control-O>', self.open_file)  # ctrl + O
        self.content_text.bind('<Control-o>', self.open_file)  # ctrl + o
        self.content_text.bind('<Control-S>', self.save)  # ctrl + S
        self.content_text.bind('<Control-s>', self.save)  # ctrl + s
        self.content_text.bind('<Control-Shift-S>', self.save_as)  # ctrl + shift + S
        self.content_text.bind('<Control-Shift-s>', self.save_as)  # ctrl + shift + s
        self.content_text.bind('<KeyPress-F1>', self.show_help)
        self.content_text.bind('<Any-KeyPress>', self.on_content_changed)
        self.content_text.bind('<KeyRelease>', self.render_code)
        self.content_text.bind('<Button-1>', self.on_content_changed)
        self.content_text.tag_configure('active_line', background='ivory2')
        
        self.popup_menu = tk.Menu(self.content_text, tearoff=0)
        self.popup_menu.add_command(label='Cut', compound='left', command=self.cut)
        self.popup_menu.add_command(label='Copy', compound='left', command=self.copy)
        self.popup_menu.add_command(label='Paste', compound='left', command=self.paste)
        self.popup_menu.add_command(label='Undo', compound='left', command=self.undo)
        self.popup_menu.add_command(label='Redo', compound='left', command=self.redo)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='Select All', command=self.select_all,
                                    underline=7)
        
        self.content_text.bind('<Button-3>', self.show_popup_menu)
        
        self.auto_code_bar.bind('<Double-Button-1>', self.add_word)
    
    def create_menu(self):
        self.menu_bar = tk.Menu(self.window)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.themes_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)
        self.menu_bar.add_cascade(label='View', menu=self.view_menu)
        self.menu_bar.add_cascade(label='About', menu=self.about_menu)
        self.menu_bar.add_cascade(label='Run', menu=self.run_menu)
    
    def create_frames(self):
        self.welcome_bar = tk.Frame(self.window, height=25, background='light seagreen')
        self.welcome_bar.pack(expand='no', fill='x')
        
        self.welcome_text = tk.Label(self.welcome_bar, text=self.config.get('welcome'),
                                     background='light seagreen', font=('consoles', 10))
        self.welcome_text.pack()
        
        self.auto_code_bar = tk.Listbox(self.window, background='light grey',
                                        font=('consoles', 13))
        self.auto_code_bar.pack(side=tk.RIGHT, expand=tk.NO, anchor=tk.E, fill=tk.BOTH)
        
        self.auto_code_y_scroll_bar = tk.Scrollbar(self.auto_code_bar)
        self.auto_code_bar.config(yscrollcommand=self.auto_code_y_scroll_bar.set)
        self.auto_code_y_scroll_bar.config(command=self.auto_code_bar.yview)
        self.auto_code_y_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.line_number_bar = tk.Text(self.window, width=4, padx=3, takefocus=0,
                                       border=0, background='khaki', state='disabled',
                                       wrap='none', font=('consoles', 13))
        self.line_number_bar.pack(side='left', fill='y')
        
        self.content_text = tk.Text(self.window, wrap='word', undo=True,
                                    font=('consoles', 13))
        self.text_bind()
        self.content_text.pack(expand=tk.YES, fill=tk.BOTH)
        
        self.text_scroll_bar = tk.Scrollbar(self.content_text)
        self.content_text.config(yscrollcommand=self.text_scroll_bar.set)
        self.text_scroll_bar.config(command=self.content_text.yview)
        self.text_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cursor_info_bar = tk.Label(self.auto_code_bar,
                                        text='Line: 1 | Column: 1 | Encoding: %s'
                                             % self.file_encoding)
        self.cursor_info_bar.pack(expand=tk.NO, fill=None, side=tk.RIGHT, anchor=tk.SE)
    
    def render_menu(self):
        self.file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left',
                                   command=self.new_file)
        self.file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                                   command=self.open_file)
        self.file_menu.add_command(label='Save', accelerator='Ctrl+S', compound='left',
                                   command=self.save)
        self.file_menu.add_command(label='Save as', accelerator='Ctrl+Shift+S',
                                   compound='left', command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', accelerator='Alt+F4', compound='left',
                                   command=self.exit_text)
        self.file_menu.add_command(label='Force Close', compound='left',
                                   command=self.force_close)
        
        self.edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound='left',
                                   command=self.undo)
        self.edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left',
                                   command=self.redo)
        self.edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left',
                                   command=self.cut)
        self.edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left',
                                   command=self.copy)
        self.edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left',
                                   command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound='left',
                                   command=self.find_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Select All', accelerator='Ctrl+A',
                                   compound='left', command=self.select_all)
        
        self.about_menu.add_command(label='About', compound='left', command=self.show_about)
        self.about_menu.add_command(label='Help', compound='left', command=self.show_help)
        
        self.show_line_number = tk.IntVar()
        self.show_line_number.set(1)
        self.view_menu.add_checkbutton(label='Show Line Number',
                                       variable=self.show_line_number,
                                       command=self.update_line_numbers)
        
        self.show_cursor_info = tk.IntVar()
        self.show_cursor_info.set(1)
        self.view_menu.add_checkbutton(label='Show Cursor Location at Bottom',
                                       variable=self.show_cursor_info,
                                       command=self.show_cursor_info_bar)
        
        self.to_highlight_line = tk.BooleanVar()
        self.to_highlight_line.set(1)
        self.view_menu.add_checkbutton(label='Highlight Current Line',
                                       variable=self.to_highlight_line,
                                       command=self.toggle_highlight)
        self.toggle_highlight()
        
        self.show_candidate_words = tk.IntVar()
        self.show_candidate_words.set(1)
        self.view_menu.add_checkbutton(label='Show Candidate Words',
                                       variable=self.show_candidate_words)
        
        self.view_menu.add_cascade(label='Themes', menu=self.themes_menu)
        self.themes_choices = tk.StringVar()
        self.themes_choices.set(self.config.get('default_theme'))
        
        for k, theme in self.config.get('themes').items():
            self.themes_menu.add_radiobutton(label=k, variable=self.themes_choices,
                                             command=self.change_theme, value=k)
        
        self.run_menu.add_command(label='Run Code', command=self.run_code,
                                  compound='left')
    
    def on_window_closing(self):
        self.exit_text()
    
    def config_window(self):
        self.window.title(self.config.get('title'))
        if not self.config.get('resizeable'):
            self.window.resizable(False, False)
        self.window.minsize(*self.config.get('minsize'))
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_closing)
        self.window.config(menu=self.menu_bar)
        self.window.geometry(
            '%dx%d+%d+%d' % (
                self.config.get('minsize')[0],
                self.config.get('minsize')[1],
                (self.window.winfo_screenwidth() - self.config.get('minsize')[0]) / 2,
                (self.window.winfo_screenheight() - self.config.get('minsize')[1]) / 2,
            )
        )
        if self.config.get('favicon'):
            self.window.iconbitmap(self.config.get('favicon'))
    
    def init(self):
        self.create_menu()
        self.create_frames()
        self.render_menu()
        self.config_window()
        
        self.change_theme()
    
    def destroy(self):
        self.window.destroy()
    
    def withdraw(self):
        self.window.withdraw()
    
    def show_about(self):
        mbox.showinfo(self.config.get('app'), 'about')
    
    def show_help(self):
        mbox.showinfo(self.config.get('app'), 'help')
    
    def show(self):
        self.window.mainloop(self.config.get('status'))

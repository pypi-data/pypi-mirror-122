import tkinter as tk
import tkinter.messagebox as mbox


class ResultBox(object):
    def __init__(self, root, info: str):
        self.window = tk.Toplevel()
        self.window.transient(root)
        self.window.title('Result')
        
        self.result_show = tk.Text(self.window, font=('consoles', 12),
                                   width=30, height=4)
        self.result_show.insert('0.0', info)
        
        self.scroll_bar = tk.Scrollbar(self.result_show)
        self.result_show.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.configure(command=self.result_show.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_show.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_closing)
        
    def show(self):
        self.window.mainloop()
        
    def on_window_closing(self):
        if mbox.askyesnocancel('Quit', 'Really quit?'):
            self.window.destroy()

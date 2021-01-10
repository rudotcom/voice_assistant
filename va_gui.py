import threading
import tkinter as tk


class VAGui(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        # self.root.geometry("+250+250")

        # self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "gray")
        self.root.attributes("-topmost", True)

        head = 'Historical-Barbarian-Female-icon'
        self.root.image = tk.PhotoImage(file=''.join(['static/img/', head, '.png']))
        self.label = tk.Label(self.root, image=self.root.image, bg='gray')
        # self.txt_label = tk.Label(master=self.root, text="")
        self.text_box = tk.Text(width=32, height=8)
        self.label.pack()
        # self.txt_label.pack()
        self.text_box.pack()

        self.root.mainloop()

    def dress_up_as(self, dress):
        self.root.image = tk.PhotoImage(file=''.join(['static/img/', dress, '.png']))
        self.label['image'] = self.root.image

    def type(self, text):
        self.text_box.insert("1.0", text + '\r\n\r\n')


girl = VAGui()

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
        self.root.geometry("-150+150")

        # self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "gray")
        self.root.attributes("-topmost", True)

        head = 'Historical-Barbarian-Female-icon'
        self.root.image = tk.PhotoImage(file=''.join(['static/img/', head, '.png']))
        self.label = tk.Label(self.root, image=self.root.image, bg='gray')
        vsb = tk.Scrollbar()

        self.text_box = tk.Text(width=30, height=9, yscrollcommand=vsb.set, wrap="word", font="{Tahoma} 9")

        self.text_box.tag_configure("voice_in", background="#E3FFBE")
        self.text_box.tag_configure("voice_out", background="#FDFFBE")

        self.label.pack()
        # self.vsb.pack(side="right", fill="y")
        self.text_box.pack(side="left", fill="both", expand=True)
        vsb.pack(side='right', fill='y')

        self.root.mainloop()

    def dress_up_as(self, dress):
        self.root.image = tk.PhotoImage(file=''.join(['static/img/', dress, '.png']))
        self.label['image'] = self.root.image

    def type(self, text, tag="voice_out"):
        self.text_box.insert(tk.END, text + '\r\n', tag)
        self.text_box.see("end")


girl = VAGui()

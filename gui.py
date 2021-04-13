import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

class DisplayImage(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)

        self.btn_zoom_in = tk.Button(self)
        self.btn_zoom_in["text"] = "Zoom In"
        self.btn_zoom_in["command"] = self.zoom_in
        self.btn_zoom_in.pack(side="top")

        self.btn_zoom_out = tk.Button(self)
        self.btn_zoom_out["text"] = "Zoom Out"
        self.btn_zoom_out["command"] = self.zoom_out
        self.btn_zoom_out.pack(side="top")

        self.canvas = tk.Canvas(self, width=500, height=700, bg="black", relief="sunken", highlightthickness=0)

        self.scrollbar1 = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar2 = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.scrollbar1.set)
        self.canvas.config(xscrollcommand=self.scrollbar2.set)

        self.scrollbar1.pack(side = "right", fill = "y")
        self.scrollbar2.pack(side = "bottom", fill="x")
        self.canvas.pack(side="left", expand="YES", fill="both")
    
    def open_img(self, path):
        self.title(path)

        load = Image.open(path)
        width, height = load.size

        self.canvas.config(scrollregion = (0,0,width,height))

        self.canvas.image = ImageTk.PhotoImage(load)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)

    def zoom_in(self):
        print("hey1")

    def zoom_out(self):
        print("hey2")

class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_img = tk.Button(self)
        self.select_img["text"] = "Abrir Imagem"
        self.select_img["command"] = self.select_file
        self.select_img.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def select_file(self):
        filename = askopenfilename(parent=self.master, title="Selecione uma Imagem", filetypes=[(".png .tiff", ".png .tiff")])
        
        if filename:
            new = DisplayImage(self.master)
            new.open_img(filename)
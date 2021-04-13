import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

class DisplayImage(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)

        self.zoom_ratio = 1.0

        self.btn_zoom_in = tk.Button(self)
        self.btn_zoom_in["text"] = "Zoom In"
        self.btn_zoom_in["command"] = self.zoom_in
        self.btn_zoom_in.pack(side="top")

        self.btn_zoom_out = tk.Button(self)
        self.btn_zoom_out["text"] = "Zoom Out"
        self.btn_zoom_out["command"] = self.zoom_out
        self.btn_zoom_out.pack(side="top")
          
    
    def open_img(self, path):
        self.title(path)

        self.loaded_img = Image.open(path)
        self.base_width, self.base_height = self.loaded_img.size


        self.config_canvas()

        self.canvas.config(scrollregion = (0,0,self.base_width,self.base_height))

        self.canvas.image = ImageTk.PhotoImage(self.loaded_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)

    def config_canvas(self):
        self.canvas = tk.Canvas(self, width = self.base_width, height = self.base_height, bg="black", relief="sunken", highlightthickness=0)

        self.scrollbar1 = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar2 = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.scrollbar1.set)
        self.canvas.config(xscrollcommand=self.scrollbar2.set)
        self.canvas.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.callback)

        self.scrollbar1.pack(side = "right", fill = "y")
        self.scrollbar2.pack(side = "bottom", fill="x")
        self.canvas.pack(side="left", expand="NO", fill="both")

    def zoom_in(self):
        self.zoom_ratio = self.zoom_ratio + 0.1

        new_width = int(self.base_width * self.zoom_ratio)
        new_height = int(self.base_height * self.zoom_ratio)

        new_img = self.loaded_img.resize((new_width, new_height))

        self.canvas.config(width = new_width, height = new_height)
        self.canvas.config(scrollregion = (0,0, new_width, new_height))
        self.canvas.image = ImageTk.PhotoImage(new_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)

    def zoom_out(self):
        self.zoom_ratio = self.zoom_ratio - 0.1

        new_width = int(self.base_width * self.zoom_ratio)
        new_height = int(self.base_height * self.zoom_ratio)

        new_img = self.loaded_img.resize((new_width, new_height))
        self.canvas.config(width = new_width, height = new_height)
        self.canvas.config(scrollregion = (0,0, new_width,new_height))
        self.canvas.image = ImageTk.PhotoImage(new_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)


    def key(self, event):
        print(f"pressed {event.char}")

    def callback(self, event):
        print(f"clicked at {event.x} {event.y}")




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
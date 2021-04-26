import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageOps
# import cv2

class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.loaded_img = None
        self.create_menu()


    def create_menu(self):
        self.menu_frame = tk.Frame(self)
        self.btn_select_img = tk.Button(self.menu_frame, text="Abrir Imagem", command=self.select_file, fg="white", bd=5, bg="green")
        self.btn_select_img.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_zoom_in = tk.Button(self.menu_frame, text="Zoom In", command=self.zoom_in, state="disabled", bd=5)
        self.btn_zoom_in.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_zoom_out = tk.Button(self.menu_frame, text="Zoom Out", command=self.zoom_out, state="disabled", bd=5)
        self.btn_zoom_out.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_region = tk.Button(self.menu_frame, text="Selecionar Região", command=self.select_region, fg="blue", state="disabled", bd=5)
        self.btn_region.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_exibir_selecao = tk.Button(self.menu_frame, text="Exibir Seleção 128x128", command=self.exibir_selecao, state="disabled", bd=5)
        self.btn_exibir_selecao.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_res64 = tk.Button(self.menu_frame, text="Reduzir Resolução para 64x64", command=self.res64, state="disabled", bd=5)
        self.btn_res64.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_res32 = tk.Button(self.menu_frame, text="Reduzir Resolução para 32x32", command=self.res32, state="disabled", bd=5)
        self.btn_res32.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_quant256 = tk.Button(self.menu_frame, text="Reduzir Quantização para 256x256", command=self.quant256, state="disabled", bd=5)
        self.btn_quant256.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_quant32 = tk.Button(self.menu_frame, text="Reduzir Quantização para 32x32", command=self.quant32, state="disabled", bd=5)
        self.btn_quant32.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_quant16 = tk.Button(self.menu_frame, text="Reduzir Quantização para 16x16", command=self.quant16, state="disabled", bd=5)
        self.btn_quant16.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_equalize = tk.Button(self.menu_frame, text="Equalizar Região", command=self.equalize, state="disabled", bd=5)
        self.btn_equalize.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_quit = tk.Button(self.menu_frame, text="SAIR", fg="red",
                              command=self.master.destroy, bd=5)
        self.btn_quit.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)
        
        self.menu_frame.pack(side="left", padx = 10, pady = 10)


    def enable_btn_group1(self):
        self.btn_zoom_in.config(state="active")
        self.btn_zoom_out.config(state="active")
        self.btn_region.config(state="active")

    def enable_btn_group2(self):
        self.btn_exibir_selecao.config(state="active")
        self.btn_res64.config(state="active")
        self.btn_res32.config(state="active")
        self.btn_quant256.config(state="active")
        self.btn_quant32.config(state="active")
        self.btn_quant16.config(state="active")
        self.btn_equalize.config(state="active")

    def disable_btn_group1(self):
        self.btn_zoom_in.config(state="disabled")
        self.btn_zoom_out.config(state="disabled")
        self.btn_region.config(state="disabled")

    def disable_btn_group2(self):
        self.btn_exibir_selecao.config(state="disabled")
        self.btn_res64.config(state="disabled")
        self.btn_res32.config(state="disabled")
        self.btn_quant256.config(state="disabled")
        self.btn_quant32.config(state="disabled")
        self.btn_quant16.config(state="disabled")
        self.btn_equalize.config(state="disabled")


    def show_img(self, path):
        self.zoom_ratio = 1.0
        self.current_rectangle = None

        self.loaded_img = Image.open(path)
        self.base_width, self.base_height = self.loaded_img.size

        self.img_frame = tk.Frame(self)

        self.canvas = tk.Canvas(self.img_frame, width = 450, height = 700, bg="green", relief="sunken", highlightthickness=0)
        self.scrollbar1 = tk.Scrollbar(self.img_frame, orient="vertical", command= self.canvas.yview)
        self.scrollbar2 = tk.Scrollbar(self.img_frame, orient="horizontal", command= self.canvas.xview)

        self.canvas.config(yscrollcommand= self.scrollbar1.set)
        self.canvas.config(xscrollcommand= self.scrollbar2.set)
        self.canvas.config(scrollregion = (0, 0, self.base_width, self.base_height))

        self.scrollbar1.pack(side = "right", fill = "y")
        self.scrollbar2.pack(side = "bottom", fill="x")
        self.canvas.pack(side="top", expand="NO", fill="both")

        self.img_frame.pack(side="right")

        self.canvas.image = ImageTk.PhotoImage(self.loaded_img)
        self.image_on_canvas = self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)

        self.enable_btn_group1()
        self.disable_btn_group2()


    def zoom_in(self):
        self.zoom_ratio = self.zoom_ratio + 0.1

        new_width = int(self.base_width * self.zoom_ratio)
        new_height = int(self.base_height * self.zoom_ratio)

        new_img = self.loaded_img.resize((new_width, new_height))

        self.canvas.config(scrollregion = (0,0, new_width, new_height))
        self.canvas.image = ImageTk.PhotoImage(new_img)
        self.canvas.create_image(0,0, anchor="nw", image= self.canvas.image)

        if self.current_rectangle != None:
            self.current_rectangle = self.canvas.create_rectangle((self.x_real - 64) * self.zoom_ratio, (self.y_real - 64) * self.zoom_ratio, (self.x_real + 64) * self.zoom_ratio, (self.y_real + 64) * self.zoom_ratio, width="2", outline="blue")

    def zoom_out(self):
        self.zoom_ratio = self.zoom_ratio - 0.1

        new_width = int(self.base_width * self.zoom_ratio)
        new_height = int(self.base_height * self.zoom_ratio)

        new_img = self.loaded_img.resize((new_width, new_height))

        self.canvas.config(scrollregion = (0,0, new_width, new_height))
        self.canvas.image = ImageTk.PhotoImage(new_img)
        self.canvas.create_image(0,0, anchor="nw", image= self.canvas.image)

        if self.current_rectangle != None:
            self.current_rectangle = self.canvas.create_rectangle((self.x_real - 64) * self.zoom_ratio, (self.y_real - 64) * self.zoom_ratio, (self.x_real + 64) * self.zoom_ratio, (self.y_real + 64) * self.zoom_ratio, width="2", outline="blue")


    def draw_rect(self, event):
        perc_x = event.x / self.canvas.winfo_width()
        perc_y = event.y / self.canvas.winfo_height()

        height_real_start = self.scrollbar1.get()[0] * self.base_height
        height_real_final = self.scrollbar1.get()[1] * self.base_height
        width_real_start = self.scrollbar2.get()[0] * self.base_width
        width_real_final = self.scrollbar2.get()[1] * self.base_width

        self.x_real = round((width_real_final - width_real_start) * perc_x + width_real_start)
        self.y_real = round((height_real_final - height_real_start) * perc_y + height_real_start)

        if self.current_rectangle != None:
            self.canvas.delete(self.current_rectangle)

        self.current_rectangle = self.canvas.create_rectangle((self.x_real - 64) * self.zoom_ratio, (self.y_real - 64) * self.zoom_ratio, (self.x_real + 64) * self.zoom_ratio, (self.y_real + 64) * self.zoom_ratio, width="2", outline="blue")
        self.cropped_img = self.loaded_img.crop((self.x_real - 64, self.y_real - 64, self.x_real + 64, self.y_real + 64))
        self.canvas.unbind("<Button-1>")
        self.btn_region.config(relief="raised")
        self.enable_btn_group2()


    def select_region(self):
        self.btn_region.config(relief="sunken")
        self.canvas.bind("<Button-1>", self.draw_rect)


    def exibir_selecao(self):
        self.canvas.delete('all')
        self.cropped_img = self.cropped_img.resize((128,128))
        self.canvas.image = ImageTk.PhotoImage(self.cropped_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)
        self.canvas.config(width=128, height = 128)
        self.canvas.config(scrollregion = (0,0, 128, 128))
        self.disable_btn_group1()


    def res64(self):
        self.canvas.delete('all')
        self.cropped_img = self.cropped_img.resize((64,64))
        self.canvas.image = ImageTk.PhotoImage(self.cropped_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)
        self.canvas.config(width=128, height = 128)
        self.canvas.config(scrollregion = (0,0, 128, 128))
        self.disable_btn_group1()


    def res32(self):
        self.canvas.delete('all')
        self.cropped_img = self.cropped_img.resize((32,32))
        self.canvas.image = ImageTk.PhotoImage(self.cropped_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)
        self.canvas.config(width=128, height = 128)
        self.canvas.config(scrollregion = (0,0, 128, 128))
        self.disable_btn_group1()


    def quant256(self):
        self.canvas.delete('all')
        quant_img = self.cropped_img.quantize(256)
        self.canvas.image = ImageTk.PhotoImage(quant_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)
        self.canvas.config(width=128, height = 128)
        self.canvas.config(scrollregion = (0,0, 128, 128))
        self.disable_btn_group1()


    def quant32(self):
        self.canvas.delete('all')
        quant_img = self.cropped_img.quantize(32)
        self.canvas.image = ImageTk.PhotoImage(quant_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)
        self.canvas.config(width=128, height = 128)
        self.canvas.config(scrollregion = (0,0, 128, 128))
        self.disable_btn_group1()


    def quant16(self):
        self.canvas.delete('all')
        quant_img = self.cropped_img.quantize(16)
        self.canvas.image = ImageTk.PhotoImage(quant_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)
        self.canvas.config(width=128, height = 128)
        self.canvas.config(scrollregion = (0,0, 128, 128))
        self.disable_btn_group1()

    def equalize(self):
        self.canvas.delete('all')
        equalized_img = ImageOps.equalize(self.cropped_img)
        self.canvas.image = ImageTk.PhotoImage(equalized_img)
        self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)
        self.canvas.config(width=128, height = 128)
        self.canvas.config(scrollregion = (0,0, 128, 128))
        self.disable_btn_group1()


    def select_file(self):
        filename = askopenfilename(parent=self.master, title="Selecione uma Imagem", filetypes=[(".png .tiff", ".png .tiff")])
        
        if filename:
            if self.loaded_img == None:
                self.show_img(path = filename)
            else:
                self.img_frame.destroy()
                self.show_img(path = filename)
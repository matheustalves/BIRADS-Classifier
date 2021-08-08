import tkinter as tk
import math
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageOps
from processing import classify

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

    def create_menu2(self):
        self.menu_frame2 = tk.Frame(self)
        self.menu_frame3 = tk.Frame(self)

        self.label_haralick = tk.Label(self.menu_frame2, text="Descritores", bd=5)
        self.label_haralick.pack(fill=tk.X, padx = 5, pady=2, ipadx = 5, ipady = 2)

        self.btn_homogeneity = tk.Button(self.menu_frame2, text="Homogeneidade", command=self.handle_btn_homogeneity, state="disabled", bd=5)
        self.btn_homogeneity.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_entropy = tk.Button(self.menu_frame2, text="Entropia", command=self.handle_btn_entropy, state="disabled", bd=5)
        self.btn_entropy.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_contrast = tk.Button(self.menu_frame2, text="Contraste", command=self.handle_btn_contrast, state="disabled", bd=5)
        self.btn_contrast.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.label_distance = tk.Label(self.menu_frame2, text="Raios", bd=5)
        self.label_distance.pack(fill=tk.X, padx = 5, pady=2, ipadx = 5, ipady = 2)

        self.btn_distance1 = tk.Button(self.menu_frame2, text="1", command=self.handle_btn_distance1, state="disabled", bd=5)
        self.btn_distance1.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_distance2 = tk.Button(self.menu_frame2, text="2", command=self.handle_btn_distance2, state="disabled", bd=5)
        self.btn_distance2.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_distance4 = tk.Button(self.menu_frame2, text="4", command=self.handle_btn_distance4, state="disabled", bd=5)
        self.btn_distance4.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_distance8 = tk.Button(self.menu_frame2, text="8", command=self.handle_btn_distance8, state="disabled", bd=5)
        self.btn_distance8.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_distance16 = tk.Button(self.menu_frame2, text="16", command=self.handle_btn_distance16, state="disabled", bd=5)
        self.btn_distance16.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.label_angles = tk.Label(self.menu_frame2, text="Ângulos", bd=5)
        self.label_angles.pack(fill=tk.X, padx = 5, pady=2, ipadx = 5, ipady = 2)

        self.btn_angle0 = tk.Button(self.menu_frame2, text="0°", command=self.handle_btn_angle0, state="disabled", bd=5)
        self.btn_angle0.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_angle45 = tk.Button(self.menu_frame2, text="45°", command=self.handle_btn_angle45, state="disabled", bd=5)
        self.btn_angle45.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_angle90 = tk.Button(self.menu_frame2, text="90°", command=self.handle_btn_angle90, state="disabled", bd=5)
        self.btn_angle90.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_angle135 = tk.Button(self.menu_frame2, text="135°", command=self.handle_btn_angle135, state="disabled", bd=5)
        self.btn_angle135.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.label_opts = tk.Label(self.menu_frame3, text="Classificação", bd=5)
        self.label_opts.pack(fill=tk.X, padx = 5, pady=2, ipadx = 5, ipady = 2)

        self.btn_hres128 = tk.Button(self.menu_frame3, text="Utilizar 128x128", command=self.handle_btn_hres128, state="disabled", bd=5)
        self.btn_hres128.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_hres64 = tk.Button(self.menu_frame3, text="Utilizar 64x64", command=self.handle_btn_hres64, state="disabled", bd=5)
        self.btn_hres64.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_hres32 = tk.Button(self.menu_frame3, text="Utilizar 32x32", command=self.handle_btn_hres32, state="disabled", bd=5)
        self.btn_hres32.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_hquant32 = tk.Button(self.menu_frame3, text="Utilizar Quant. 32x32", command=self.handle_btn_hquant32, state="disabled", bd=5)
        self.btn_hquant32.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_hquant16 = tk.Button(self.menu_frame3, text="Utilizar Quant. 16x16", command=self.handle_btn_hquant16, state="disabled", bd=5)
        self.btn_hquant16.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_calcHaralick_full = tk.Button(self.menu_frame3, text="Caracterizar Imagem", command=self.calcHaralick_full, state="disabled", fg="black", bd=5, bg="yellow")
        self.btn_calcHaralick_full.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)

        self.btn_calcHaralick_crop = tk.Button(self.menu_frame3, text="Caracterizar Recorte", command=self.calcHaralick_crop, state="disabled", fg="white", bd=5, bg="blue")
        self.btn_calcHaralick_crop.pack(fill=tk.X, padx = 5, pady=5, ipadx = 5, ipady = 5)
        
        self.menu_frame3.pack(side="right", padx = 10, pady = 10)
        self.menu_frame2.pack(side="right", padx = 10, pady = 10)


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

    def enable_btn_group3(self):
        self.btn_homogeneity.config(state="active")
        self.btn_entropy.config(state="active")
        self.btn_contrast.config(state="active")
        self.btn_distance1.config(state="active")
        self.btn_distance2.config(state="active")
        self.btn_distance4.config(state="active")
        self.btn_distance8.config(state="active")
        self.btn_distance16.config(state="active")
        self.btn_angle0.config(state="active")
        self.btn_angle45.config(state="active")
        self.btn_angle90.config(state="active")
        self.btn_angle135.config(state="active")
        self.btn_calcHaralick_full.config(state="active")
        self.btn_hres128.config(state="active")
        self.btn_hres64.config(state="active")
        self.btn_hres32.config(state="active")
        self.btn_hquant32.config(state="active")
        self.btn_hquant16.config(state="active")


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
        self.haralick_descriptors = []
        self.haralick_distances = []
        self.haralick_angles = []
        self.haralick_resolutions = []
        self.haralick_quants = []

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

        self.create_menu2()
        self.img_frame.pack(side="right")

        self.canvas.image = ImageTk.PhotoImage(self.loaded_img)
        self.image_on_canvas = self.canvas.create_image(0,0, anchor="nw", image=self.canvas.image)

        self.enable_btn_group1()
        self.enable_btn_group3()
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
        self.btn_calcHaralick_crop.config(state="active")


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


    def handle_btn_homogeneity(self):
        if self.btn_homogeneity.cget("relief") == "raised":
            self.btn_homogeneity.config(relief="sunken")
            self.haralick_descriptors.append('homogeneity')
            self.haralick_descriptors.sort()
        else:
            self.btn_homogeneity.config(relief="raised")
            self.haralick_descriptors.remove('homogeneity')
            

    def handle_btn_entropy(self):
        if self.btn_entropy.cget("relief") == "raised":
            self.btn_entropy.config(relief="sunken")
            self.haralick_descriptors.append('correlation')
            self.haralick_descriptors.sort()
        else:
            self.btn_entropy.config(relief="raised")
            self.haralick_descriptors.remove('correlation')
            

    def handle_btn_contrast(self):
        if self.btn_contrast.cget("relief") == "raised":
            self.btn_contrast.config(relief="sunken")
            self.haralick_descriptors.append('contrast')
            self.haralick_descriptors.sort()
        else:
            self.btn_contrast.config(relief="raised")
            self.haralick_descriptors.remove('contrast')
            


    def handle_btn_distance1(self):
        if self.btn_distance1.cget("relief") == "raised":
            self.btn_distance1.config(relief="sunken")
            self.haralick_distances.append(1)
            self.haralick_distances.sort()
        else:
            self.btn_distance1.config(relief="raised")
            self.haralick_distances.remove(1)

    def handle_btn_distance2(self):
        if self.btn_distance2.cget("relief") == "raised":
            self.btn_distance2.config(relief="sunken")
            self.haralick_distances.append(2)
            self.haralick_distances.sort()
        else:
            self.btn_distance2.config(relief="raised")
            self.haralick_distances.remove(2)

    def handle_btn_distance4(self):
        if self.btn_distance4.cget("relief") == "raised":
            self.btn_distance4.config(relief="sunken")
            self.haralick_distances.append(4)
            self.haralick_distances.sort()
        else:
            self.btn_distance4.config(relief="raised")
            self.haralick_distances.remove(4)

    def handle_btn_distance8(self):
        if self.btn_distance8.cget("relief") == "raised":
            self.btn_distance8.config(relief="sunken")
            self.haralick_distances.append(8)
            self.haralick_distances.sort()
        else:
            self.btn_distance8.config(relief="raised")
            self.haralick_distances.remove(8)

    def handle_btn_distance16(self):
        if self.btn_distance16.cget("relief") == "raised":
            self.btn_distance16.config(relief="sunken")
            self.haralick_distances.append(16)
            self.haralick_distances.sort()
        else:
            self.btn_distance16.config(relief="raised")
            self.haralick_distances.remove(16)

    def handle_btn_angle0(self):
        if self.btn_angle0.cget("relief") == "raised":
            self.btn_angle0.config(relief="sunken")
            self.haralick_angles.append(0)
            self.haralick_angles.sort()
        else:
            self.btn_angle0.config(relief="raised")
            self.haralick_angles.remove(0)

    def handle_btn_angle45(self):
        if self.btn_angle45.cget("relief") == "raised":
            self.btn_angle45.config(relief="sunken")
            self.haralick_angles.append(45)
            self.haralick_angles.sort()
        else:
            self.btn_angle45.config(relief="raised")
            self.haralick_angles.remove(45)

    def handle_btn_angle90(self):
        if self.btn_angle90.cget("relief") == "raised":
            self.btn_angle90.config(relief="sunken")
            self.haralick_angles.append(90)
            self.haralick_angles.sort()
        else:
            self.btn_angle90.config(relief="raised")
            self.haralick_angles.remove(90)

    def handle_btn_angle135(self):
        if self.btn_angle135.cget("relief") == "raised":
            self.btn_angle135.config(relief="sunken")
            self.haralick_angles.append(135)
            self.haralick_angles.sort()
        else:
            self.btn_angle135.config(relief="raised")
            self.haralick_angles.remove(135)

    def handle_btn_hres128(self):
        if self.btn_hres128.cget("relief") == "raised":
            self.btn_hres128.config(relief="sunken")
            self.haralick_resolutions.append(128)
            self.haralick_resolutions.sort()
        else:
            self.btn_hres128.config(relief="raised")
            self.haralick_resolutions.remove(128)

    def handle_btn_hres64(self):
        if self.btn_hres64.cget("relief") == "raised":
            self.btn_hres64.config(relief="sunken")
            self.haralick_resolutions.append(64)
            self.haralick_resolutions.sort()
        else:
            self.btn_hres64.config(relief="raised")
            self.haralick_resolutions.remove(64)

    def handle_btn_hres32(self):
        if self.btn_hres32.cget("relief") == "raised":
            self.btn_hres32.config(relief="sunken")
            self.haralick_resolutions.append(32)
            self.haralick_resolutions.sort()
        else:
            self.btn_hres32.config(relief="raised")
            self.haralick_resolutions.remove(32)

    def handle_btn_hquant32(self):
        if self.btn_hquant32.cget("relief") == "raised":
            self.btn_hquant32.config(relief="sunken")
            self.haralick_quants.append(32)
            self.haralick_quants.sort()
        else:
            self.btn_hquant32.config(relief="raised")
            self.haralick_quants.remove(32)

    def handle_btn_hquant16(self):
        if self.btn_hquant16.cget("relief") == "raised":
            self.btn_hquant16.config(relief="sunken")
            self.haralick_quants.append(16)
            self.haralick_quants.sort()
        else:
            self.btn_hquant16.config(relief="raised")
            self.haralick_quants.remove(16)


    def calcHaralick_full(self):
        if len(self.haralick_descriptors) >= 1 and len(self.haralick_distances) >= 1 and len(self.haralick_angles) >= 1 and len(self.haralick_resolutions) >= 1 and len(self.haralick_quants) >= 1:

            rad_angles = [math.radians(angle) for angle in self.haralick_angles]

            classify(self.haralick_descriptors, self.haralick_distances, rad_angles, self.haralick_resolutions, self.haralick_quants, self.loaded_img)
        else:
            print("Selecione pelo menos 1 descritor, 1 distância, 1 ângulo, 1 resolução e 1 quantização.")

    def calcHaralick_crop(self):
        if len(self.haralick_descriptors) >= 1 and len(self.haralick_distances) >= 1 and len(self.haralick_angles) >= 1 and len(self.haralick_resolutions) >= 1 and len(self.haralick_quants) >= 1:

            rad_angles = [math.radians(angle) for angle in self.haralick_angles]

            classify(self.haralick_descriptors, self.haralick_distances, rad_angles, self.haralick_resolutions, self.haralick_quants, self.cropped_img)
        else:
            print("Selecione pelo menos 1 descritor, 1 distância, 1 ângulo, 1 resolução e 1 quantização.")


    def select_file(self):
        filename = askopenfilename(parent=self.master, title="Selecione uma Imagem", filetypes=[(".png .tiff", ".png .tiff")])
        
        if filename:
            if self.loaded_img == None:
                self.show_img(path = filename)
            else:
                self.img_frame.destroy()
                self.menu_frame2.destroy()
                self.menu_frame3.destroy()
                self.show_img(path = filename)

"""
 _______________________________________________________________________
| ######  #     # #    #    ###   ######   #####    #     #   ###       | 
| #     #  #   #  #   #      #    #     # #         #     #    #        |
| #     #   # #   #  #       #    #     # #         #     #    #        |
| ######     #    ###        #    #     # #    ###  #     #    #        |
| #          #    #  #       #    #     # #      #  #     #    #        |
| #          #    #   #      #    #     # #      #  #     #    #        |
| #          #    #    #    ###   ######   #####    #####     ###       |
|_______________________________________________________________________|

"""

version  = '2.0.0'
author = 'github@RonanBasto'

import tkinter as tk
from tkinter import *



class Gui(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        self.widgets = {}
        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
    def add_menu(self, menu_name, menu_items):
        # Cria um novo menu
        new_menu = tk.Menu(self.menu_bar, tearoff=0)
        # Adiciona cada item ao novo menu
        for item in menu_items:
            # Verifica se o item é um separador
            if item == "-":
                new_menu.add_separator()
            else:
                # Extrai o nome e a ação do item
                item_name, item_action = item
                # Adiciona o item ao menu com a ação associada
                new_menu.add_command(label=item_name, command=item_action)
        # Adiciona o novo menu à barra de menu
        self.menu_bar.add_cascade(label=menu_name, menu=new_menu)
        
    def add_image(self, img_path, **kwargs):
        img = tk.PhotoImage(file=img_path)
        img_label = ImageLabel(self, image=img, **kwargs)
        img_label.image = img
        img_label.pack()
        return img_label
    def add_scrollbar(self):
        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        return scrollbar
    
    def update_image_position(self):
        self.place(x=self.x, y=self.y)
        
    def open_file_dialog(self, file_types):
                        file = filedialog.askopenfile(mode="r", filetypes=file_types)
                        if file:
                            return file.name
        
    def add_spinbox(self, label, from_, to, callback):
        var = tk.StringVar()
        spinbox = tk.Spinbox(self, from_=from_, to=to, textvariable=var, command=callback)
        spinbox.pack()
        label_widget = tk.Label(self, text=label)
        label_widget.pack()

    def add_checkbox(self, text, callback):
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(self, text=text, variable=var, command=lambda: callback(var.get()))
        checkbox.pack()
        
    def add_text(self, text_name, prompt=""):
        text_var = tk.StringVar()
        new_text = tk.Entry(self, textvariable=text_var)
        new_text.pack()
        self.widgets[text_name] = new_text, text_var
        return text_var

    def add_button(self, button_name, on_click, text=""):
        new_button = tk.Button(self, text=text, command=lambda: self.new_on_click(button_name, on_click))
        new_button.pack()
        self.widgets[button_name] = new_button


    def add_listbox(self, listbox_name, items):
        new_listbox = tk.Listbox(self)
        for item in items:
            new_listbox.insert(tk.END, item)
        new_listbox.pack()
        self.widgets[listbox_name] = new_listbox

    def add_text_area(self, text_area_name):
        text_area = tk.Text(self)
        text_area.pack()
        self.widgets[text_area_name] = text_area
        return text_area
        
    def add_canvas(self, canvas_name, width, height):
        new_canvas = tk.Canvas(self, width=width, height=height)
        new_canvas.pack()
        self.widgets[canvas_name] = new_canvas
        return new_canvas

    def add_canvas_items(self, canvas_name, maps):
        canvas = self.widgets[canvas_name]
        for m in maps:
            shape = m['shape']
            coords = m['coords']
            fill = m.get('fill', '')
            outline = m.get('outline', '')
            width = m.get('width', 1)
            tags = m.get('tags', '')
            if shape == 'rectangle':
                canvas.create_rectangle(coords, fill=fill, outline=outline, width=width, tags=tags)
            elif shape == 'oval':
                canvas.create_oval(coords, fill=fill, outline=outline, width=width, tags=tags)
            elif shape == 'line':
                canvas.create_line(coords, fill=fill, width=width, tags=tags)
            elif shape == 'polygon':
                canvas.create_polygon(coords, fill=fill, outline=outline, width=width, tags=tags)

    def update_canvas_items(self, canvas_name, maps):
        canvas = self.widgets[canvas_name]
        canvas.delete('all')
        self.add_canvas_items(canvas_name, maps)

    def clear_canvas(self, canvas_name):
        canvas = self.widgets[canvas_name]
        canvas.delete('all')

    def new_on_click(self, button_name, on_click):
        if isinstance(self.widgets[button_name], tuple):
            _, text_var = self.widgets[button_name]
            on_click(text_var.get())
        elif isinstance(self.widgets[button_name], tk.Listbox):
            selected_index = self.widgets[button_name].curselection()
            on_click(selected_index)
        else:
            on_click()
            
    def add_entry(self, entry_name):
        entry = tk.Entry(self)
        entry.pack()
        return entry
        
    def get_entry_value(self, entry):
        return entry.get()

    def add_label(self, text):
        label = Label(self.frame, text=text)
        label.pack()
    
class Canvas_Map(tk.Canvas):
    def __init__(self, master, map_data, cell_size=50):
        super().__init__(master, width=len(map_data[0]) * cell_size, height=len(map_data) * cell_size)
        self.map_data = map_data
        self.cell_size = cell_size
        self.cells = []
        self.draw_map()

    def draw_map(self):
        for y, row in enumerate(self.map_data):
            for x, value in enumerate(row):
                x1, y1 = x * self.cell_size, y * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                cell = self.create_rectangle(x1, y1, x2, y2, fill=value)
                self.cells.append(cell)


class GUI_FRAME:
    def __init__(self, title, geometry):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.frames = {}

    def add_frame(self, frame_name, **kwargs):
        frame = tk.Frame(self.root, **kwargs)
        self.frames[frame_name] = frame
        frame.pack()

    def run(self):
        self.root.mainloop()

class ImageLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.image = None
        self.x = 0
        self.y = 0

    def set_image(self, img_path):
        self.image = tk.PhotoImage(file=img_path)
        self.config(image=self.image)

    def update_position(self):
        self.place(x=self.x, y=self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_position()

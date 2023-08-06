from pykidgui import *



map_data = [
    ["#333", "#333", "#333", "#333", "#333", "#333", "#333", "#333", "#333", "#333"],
    ["#333", "#FFF", "#FFF", "#FFF", "#333", "#333", "#333", "#333", "#333", "#333"],
    ["#333", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#333"],
    ["#333", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#333"],
    ["#333", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#FFF", "#333"],
    ["#333", "#333", "#333", "#333", "#333", "#333", "#333", "#333", "#333", "#333"],
]

root = tk.Tk()
canvas_map = Canvas_Map(root, map_data)
canvas_map.pack()
root.mainloop()


# onclick ex
'''
def hello_world():
    print("Hello, World!")

my_gui = Gui("Janela","500x500")

# Adiciona um botão à janela principal
my_gui.add_button("hello_button", hello_world, text="Say Hello!")
'''


# entry ex
my_gui = Gui("Janela","500x500")
my_entry = my_gui.add_entry("entry1")

def on_click():
    entry_value = my_gui.get_entry_value(my_entry)
    print(f"Valor digitado: {entry_value}")
    
my_gui.add_button("button1",on_click, "Clique aqui")
my_gui.mainloop()


#listbox


my_gui = Gui("Janela","500x500")
my_gui.add_listbox("opcoes", ["opção 1", "opção 2", "opção 3"])


selected_index = my_gui.widgets["opcoes"].curselection()
if selected_index:
    selected_option = my_gui.widgets["opcoes"].get(selected_index)
    print(selected_option)
else:
    print("Nenhuma opção selecionada.")


my_gui.mainloop()

# area de texto

my_gui = Gui("Janela","500x500")
my_gui.add_text_area("texto1")
my_gui.mainloop()

#processer Bar


from pykidgui import *

my_gui = Gui("Janela","500x500")

# Adicionar um canvas com uma largura e altura definidas
canvas = my_gui.add_canvas("canvas", width=500, height=500)

# Criar um mapa para uma linha que começa na posição (50, 50) e termina na posição (250, 250)
line_map = {'shape': 'line', 'coords': [50, 50, 250, 250], 'fill': 'black', 'width': 2}
line_map1 = {'shape': 'line', 'coords': [100,150, 250, 250], 'fill': 'red', 'width': 2}
# Adicionar a linha ao canvas
my_gui.add_canvas_items("canvas", [line_map])
my_gui.add_canvas_items("canvas", [line_map1])

# Executar o loop principal da GUI
my_gui.mainloop()


def on_checkbox_clicked(checked):
    print("Checkbox marcado" if checked else "Checkbox desmarcado")

my_gui = Gui("Exemplo de Checkbox", "300x200")
my_gui.add_checkbox("Marque aqui", on_checkbox_clicked)
my_gui.add_checkbox("Marque aqui", on_checkbox_clicked)
my_gui.mainloop()

checkbox_values = []

my_gui = Gui("Exemplo de Checkbox", "300x200")

def on_checkbox_clicked(value):
    checkbox_values.append(value)
    print(checkbox_values)

my_gui.add_checkbox("Checkbox 1", on_checkbox_clicked)
my_gui.add_checkbox("Checkbox 2", on_checkbox_clicked)
my_gui.add_checkbox("Checkbox 3", on_checkbox_clicked)

my_gui.mainloop()


def minha_funcao_callback(value):
 
    print(value)
    
gui = Gui("Minha janela", "400x300")
gui.add_spinbox("Idade", 0, 100,minha_funcao_callback)
gui.mainloop()



def minha_funcao1():
 
    print("novo arquivo")

def minha_funcao2():
 
    print("abrir arquivo")

def minha_funcao3():
 
    print("sair")
            
gui = Gui("Minha janela", "400x400")
gui.add_menu("Arquivo", [("Novo", minha_funcao1), ("Abrir", minha_funcao2), "-", ("Sair", minha_funcao3)])
gui.add_menu("Arquivo2", [("Novo2", minha_funcao1), ("Abrir2", minha_funcao2), "-", ("Sair2", minha_funcao3)])
gui.mainloop()

gui = Gui("Minha janela", "500x500")
img1 = gui.add_image("test.png")
img1.set_position(15,100)
gui.mainloop()

gui = Gui("Minha janela", "500x500")
gui.add_label("Hello, world!")
scrollbar = gui.add_scrollbar()
gui.mainloop()


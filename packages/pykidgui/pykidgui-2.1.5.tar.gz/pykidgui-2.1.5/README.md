```
______________________________________________________________________
| ######  #     # #    #    ###   ######   #####    #     #   ###       | 
| #     #  #   #  #   #      #    #     # #         #     #    #        |
| #     #   # #   #  #       #    #     # #         #     #    #        |
| ######     #    ###        #    #     # #    ###  #     #    #        |
| #          #    #  #       #    #     # #      #  #     #    #        |
| #          #    #   #      #    #     # #      #  #     #    #        |
| #          #    #    #    ###   ######   #####    #####     ###       |
|_______________________________________________________________________|

```
''

PyKidGUI é uma biblioteca Python que visa facilitar a criação de interfaces gráficas de usuário (GUIs) para aplicações desktop simples. Seu foco é em aplicações para crianças e iniciantes em programação, proporcionando uma API simples e intuitiva que permite a criação de janelas, botões, caixas de texto, imagens e outros elementos visuais de forma fácil e rápida.

## Instalação

Para instalar a biblioteca, basta executar o seguinte comando:

bash:

<pre><code> pip install pykidgui</code></pre>


## Como Usar

Para começar a usar a PyKidGUI, importe a classe Gui do módulo pykidgui e crie uma instância da classe:


<pre><code>
from pykidgui import *


my_gui = Gui("Janela","500x500")

Em seguida, use os métodos da classe para adicionar elementos visuais à janela:
</code></pre>

<pre><code>
my_gui.add_label("Olá, mundo!")
my_gui.add_button("hello_button", hello_world, text="Say Hello!")


</code></pre>
Você também pode adicionar imagens à janela usando o método add_image:


<pre><code>
gui = Gui("Minha janela", "500x500")
img1 = gui.add_image("test.png")
img1.set_position(15,100)
gui.mainloop()

</code></pre>

E utilizar o método add_scrollbar para adicionar uma barra de rolagem a um frame:
Para adicionar um botão na janela, podemos utilizar o método add_button da classe Gui. Esse método recebe um texto que será exibido no botão e uma função que será executada quando o botão for clicado

<pre><code>
from pykidgui import *


def click_button():
    print("Botão clicado!")

my_gui = Gui("Minha janela", "500x500")
my_gui.add_button("hello_button", click_button, text="Say Hello!")
</code></pre>

<pre><code>
from pykidgui import *

checkbox_values = []

my_gui = Gui("Exemplo de Checkbox", "300x200")

def on_checkbox_clicked(value):
    checkbox_values.append(value)
    print(checkbox_values)

my_gui.add_checkbox("Checkbox 1", on_checkbox_clicked)
my_gui.add_checkbox("Checkbox 2", on_checkbox_clicked)
my_gui.add_checkbox("Checkbox 3", on_checkbox_clicked)

my_gui.mainloop()

from pykidgui import *

gui = Gui("Minha janela", "400x400")
gui.add_menu("Arquivo", [("Novo", minha_funcao1), ("Abrir", minha_funcao2), "-", ("Sair", minha_funcao3)])
gui.add_menu("Arquivo2", [("Novo2", minha_funcao1), ("Abrir2", minha_funcao2), "-", ("Sair2", minha_funcao3)])
gui.mainloop()



</code></pre>
```

## Documentação

Para mais informações sobre os métodos e parâmetros disponíveis na PyKidGUI, consulte a documentação.


## Contribuição

Contribuições para a biblioteca são sempre bem-vindas! Caso queira contribuir, abra uma issue para discutir o que você deseja adicionar ou consertar na biblioteca, e submeta um pull request com suas alterações.

## Licença

PyKidGUI é distribuída sob a licença MIT. Veja o arquivo LICENSE para mais informações.

## ✒️ Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

* **Um desenvolvedor** - *Trabalho Inicial* - [umdesenvolvedor](https://gist.github.com/ronanbastos)
* **help codificação*** - *Trabalho segundario* [umdesenvolvedor](https://chat.openai.com)

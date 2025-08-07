from flet import Page, TextField, ElevatedButton, Column, Text, TextStyle, Container, Colors, Dropdown, dropdown, Row, app
import requests
from chuck import chuck_norris
from countries import rest_countries
from ip import get_ip_info

    
def main(page: Page):
    page.title = "Chatbot Multiuso"
    page.bgcolor = Colors.BLUE_GREY_900
    page.theme_mode = "dark"

    input_box = TextField(
        label="Escribe tu mensaje",
        border_color=Colors.BLUE_200,
        focused_border_color=Colors.BLUE_400,
        text_style=TextStyle(color=Colors.WHITE),
        expand=True
    )

    def mostrar_bienvenida():
        chat_area.controls.clear()  # Limpia mensajes anteriores

        if mode_dropdown.value == "countries":
            mensaje = "🌐 CountryBot: ¡Salut! Dime un país y te diré todo sobre él."
        elif mode_dropdown.value == "chuck":
            categories = requests.get("https://api.chucknorris.io/jokes/categories").json()
            mensaje = f"🤣 ChuckBot: ¿Listo para reír? Aquí vienen los chistes de Chuck Norris. Si lo quieres de una categoría específica, ingresa una de las siguientes: {", ".join(category for category in categories)}"

        chat_area.controls.append(Text(mensaje, color=Colors.BLUE_200))
        page.update()

    mode_dropdown = Dropdown(
        options=[
            dropdown.Option("countries", "Datos sobre países"),
            dropdown.Option("chuck", "Chistes de Chuck Norris")
        ],
        value="countries",
        label="Modo",
        border_color=Colors.BLUE_200,
        color=Colors.WHITE,
        on_change=lambda e: mostrar_bienvenida()
    )

    chat_area = Column(scroll='auto', expand=True)
 
    mostrar_bienvenida()

    def send_message(e):
        user_message = input_box.value
        if not user_message:
            return
        
        # Mostrar mensaje del usuario
        chat_area.controls.append(Text(f"Tú: {user_message}", color= Colors.WHITE))
        
        # Procesar según el modo seleccionado
        if mode_dropdown.value == "chuck":
            response = chuck_norris(user_message)
        elif mode_dropdown.value == "countries":
            response = rest_countries(user_message)
        
        # Mostrar respuesta
        if mode_dropdown.value == "chuck":
            chat_area.controls.append(Text(f"ChuckBot: {response}", color=Colors.BLUE_200))
        elif mode_dropdown.value == "countries":
            chat_area.controls.append(Text(f"CountryBot: {response}", color=Colors.BLUE_200))

        # Limpiar input y actualizar UI
        input_box.value = ""
        page.update()

    send_button = ElevatedButton(
        text="Enviar",
        on_click=send_message,
        bgcolor=Colors.BLUE_700,
        color=Colors.WHITE
    )

    chat_container = Container(
        content=chat_area,
        bgcolor=Colors.BLUE_GREY_800,
        padding=10,
        border_radius=10,
        expand=True
    )

    input_container = Container(
        content=Row(
            controls=[
                mode_dropdown,
                input_box,
                send_button
            ],
            spacing=10
        )
    )

    page.add(chat_container, input_container)

    page.window.width = 800
    page.window.height = 600
    page.update()


if __name__ == "__main__":
    app(target=main)
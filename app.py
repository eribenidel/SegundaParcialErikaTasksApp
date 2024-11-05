from flet import * #Luego de haber instalado el módulo Flet, se importa aquí. Esta importación permite utilizar todos sus recursos (*).
import flet as ft #Importa de Flet...

#Comando para ejecutar en la terminal y que el proyecto se actualice en tiempo real: flet -r app.py

#Función principal que abordará la página.
def main(page: Page): #Función llamada 'main' con parámetro de tipo 'Page' que es una nube del módulo Flet. Esto se necesita para iniciar la aplicación.
    
    #Definir ancho y altura de la ventana
    page.window_width = 450  #Ancho de la ventana
    page.window_height = 880  #Altura de la ventana
    page.title = "Lista de Tareas"  #Título de la ventana

    #Se crean varibles para asignar los valores de colores.
    BG = '#041955' #Color de fondo a utilizar.
    FWG = '#97b4ff' #Primer plano.
    FG = '#3450a1' #Ni idea.
    PINK = '#eb06ff' #Linea rosa.

    #Estilos aplicados para la foto de perfil.
    circle = Stack(
    controls=[
      Container(
        width=100,
        height=100,
        border_radius=50,
        bgcolor='white12'
        ),
      Container(
                  gradient=SweepGradient(
                      center=alignment.center,
                      start_angle=0.0,
                      end_angle=3,
                      stops=[0.5,0.5],
                  colors=['#00000000', PINK],
                  ),
                  width=100,
                  height=100,
                  border_radius=50,
                  content=Row(alignment='center',
                      controls=[
                        Container(padding=padding.all(5),
                          bgcolor=BG,
                          width=90,height=90,
                          border_radius=50,
                          content=Container(bgcolor=FG,
                            height=80,width=80,
                            border_radius=40,
                          content=CircleAvatar(opacity=0.8,
                foreground_image_url="https://images.unsplash.com/photo-1545912452-8aea7e25a3d3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80")
                          )
                          )
                      ],
                  ),
              ),
      
    ]
  )


    #Función de encogimiento/reducción.
    def shrink(e):
        page_2.controls[0].width = 120 #Se selecciona al contenedor que sería el primer elemento de la lista porque es el que tiene peso.
        page_2.controls[0].scale = transform.Scale(0.8, alignment=alignment.center_right) #También se puede escalar de esta manera.
        page_2.controls[0].border_radius=border_radius.only( #Estilos que tendrá la página 2 al encogerse.
            top_left=35,
            top_right=0,
            bottom_left=35,
            bottom_right=0
        )
        page_2.update() #Al actualizar se reduce la página.

    #Función de restauración.
    def restore(e):
        page_2.controls[0].width = 400 #Se vuelve a poner el valor inicial del ancho de contenedor que era 400.
        page_2.controls[0].border_radius=35 #Para que el borde se mantenga redondeado.
        page_2.controls[0].scale = transform.Scale(1, alignment=alignment.center_right) #También se restaura la escala inicial que era 1.
        page_2.update() #Al actualizar se restaura la página.

    #Variable que será para las tarjetas de categoria.
    categories_card = Row( #Serán las tarjetas horizontales que se deslizan.
        scroll='auto' #Para que se deslice la tarjeta de categoría de manera automática.
    )
    categories = ['Business', 'Family', 'Friends']
    for i, category in enumerate(categories): #Se realiza un ciclo por cada categoría para rellenar la barra de progreso.
        categories_card.controls.append( #Se pone así porque no puede agregar como cadena.
            Container( #Valores que tendrá el contenedor deslizante.
                border_radius=20, #Intensidad del borde redondeado.
                bgcolor=BG, #Color de fondo de las tarjetas deslizantes.
                width=170, #Ancho de cada tarjeta.
                height=110, #Altura de cada tarjeta.
                padding=15, #Espacio dentro de cada tarjeta.
                content=Column(
                    controls=[ #Donde se debe especificar los parámetros. Es decir, indicar qué elemento contendrá la tarjeta.
                        Text('40 Tasks'),
                        Text(category),
                        Container( #La barra de progreso debe ir dentro de un contenedor.
                            #Valores de la barra de progreso.
                            width=160,
                            height=5,
                            bgcolor='white12', #Color de la barra de progreso
                            border_radius=20,
                            padding=padding.only(right=i*30), #Esto especifica que tan completo debe estar la barra de progreso. Se multiplica con i porque deberá hacer un ciclo.
                            content=Container( #Se crea otro contenedor para rellenar la barra de progreso.
                                bgcolor=PINK #Color del relleno de la barra de progreso.
                            )
                        )
                    ]
                )
            )
        )


    # Función para añadir
    def agregar_opc(e):
        if new_task.value != "":  # Verifica que el campo de texto no esté vacío
            task = opciones_tarea(new_task.value)  # Crea una nueva tarea
            task_list.controls.append(task)  # Agrega la nueva tarea a `task_list`
            new_task.value = ""  # Limpia el campo de texto
            new_task.focus()  # Enfoca nuevamente en el campo de texto
            task_list.update()  # Actualiza solo `task_list` para mostrar la nueva tarea
            page_2.update()


    #Función editar
    def guardar_editado(e, task_checkbox, edit_textbox, task_view, edit_view):
        # Actualiza el texto del checkbox con el nuevo valor
        task_checkbox.label = edit_textbox.value
        task_checkbox.update()  # Actualiza la vista del checkbox

        # Cambia la visibilidad entre la vista de tarea y la de edición
        task_view.visible = True  # Muestra la vista normal de la tarea
        edit_view.visible = False  # Oculta la vista de edición
        
        # Actualiza ambas vistas para que se refleje el cambio
        task_view.update()
        edit_view.update()


    #Función para eliminar
    def eliminar_tarea(e, task_card):
        task_list.controls.remove(task_card)  #Elimina la opción de la lista de tareas
        page_2.update()

    #Crear opciones de tareas con botones de editar y eliminar
    def opciones_tarea(task_text):
        task_checkbox = ft.Checkbox(label=task_text)

        #Vista para mostrar la tarea
        task_view = ft.Row([
            task_checkbox,
            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: mostrar_vista_edit(task_view, edit_view)), #icono de editar
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: eliminar_tarea(e, task_card)) #icono de eliminar
        ])

        #Vista para editar la tarea
        edit_textbox = ft.TextField(value=task_text)
        edit_view = ft.Row([
            edit_textbox,
            ft.IconButton(icon=ft.icons.SAVE, on_click=lambda e: guardar_editado(e, task_checkbox, edit_textbox, task_view, edit_view)) #icono de modificar cambios
        ], visible=False)

        #Alterna las vistas de tarea y edición
        def mostrar_vista_edit(task_view, edit_view):
            task_view.visible = False  # Oculta la vista de tarea
            edit_view.visible = True  # Muestra la vista de edición
            task_view.update()
            edit_view.update()


        #Contenedor que agrupa ambas vistas (tarea y edición)
        task_card = ft.Column([task_view, edit_view]) #Coloca en columna las vistas
        return task_card
    
    #Lista donde se agregarán las tareas
    task_list = ft.Column()
    
    new_task = ft.TextField(hint_text="New task", width=300, border_radius=15, border_color="white")

    #Variable que se utilizará para el contenido de la primera página.
    first_page_contents = Container(
    content=Column(
        controls=[
            Row(
                alignment='spaceBetween',
                controls=[
                    Container(
                        on_click=lambda e: shrink(e),
                        content=Icon(icons.MENU)
                    ),
                    Row(
                        controls=[
                            Icon(icons.SEARCH),
                            Icon(icons.NOTIFICATIONS_OUTLINED)
                        ]
                    )
                ]
            ),
            Container(height=20),
            Text(value='Welcome, Erika!', size=26, weight="bold"),
            Text(value='CATEGORIES'),
            Container(
                padding=padding.only(top=10, bottom=20),
                content=categories_card
            ),
            Text("TODAY'S TASKS"),
            Container(
                bgcolor=BG,
                height=450,
                width=400,
                border_radius=25,
                padding=10,
                content=Column([
                    new_task,
                    ft.ElevatedButton("ADD TASK", color= "White", width=200, height=35 , bgcolor=PINK , on_click=agregar_opc),  # Botón para agregar tareas
                    task_list  # Aquí se muestra la lista de tareas
                ],
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
        ]
    )
)


    #Se crean variables de las páginas que tendrá la aplicación.
    page_1 = Container( #Página que aparecerá al achicarse la página principal (page_2).
        width=400,
        height=850,
        bgcolor=BG,
        border_radius=35,
        padding=padding.only(left=50, top=60, right=200), #Ubicación que tendrá el ícono '<' dentro del contenedor.
        
        content = Column( #Se crea una columna dentro del contenedor porque solo queremos utilizar una columna para la parte de perfil del usuario.
            controls=[
                Row(
                    controls=[
                        Container( #Se añade un contenedor dentro de la columna para manejar mejor los espacios.
                    
                            #Estilos aplicado al ícono '<'.
                            border_radius=25,
                            padding=padding.only(top=13, left=13),
                            height=50,
                            width=50,
                            border=border.all(color='white', width=1),
                            on_click=lambda e: restore(e), #Función que hará al 
                            content=Text('<') #Será el ícono a utilizar para retroceder.
                        )
                    ]
                ),
                Container(height=20),
                circle,
                Text('Erika\nBenítez', size=32, weight='bold'),
                Container(height=20),
                Row( #Bloque del favorito.
                    controls=[
                        Icon(icons.FAVORITE_BORDER_SHARP, color='white60'), #Ícono de corazón y el color asignado a este.
                        Text('Favorites', size=15, weight=FontWeight.W_300, color='white', font_family='poppins'), #Texto qu acompaña al ícono de corazón.
                    ]
                ),
                Container(height=5), #Espacio entre los bloques.
                Row( #Bloque de la categoría.
                    controls=[
                        Icon(icons.CARD_TRAVEL, color='white60'), #Ícono de la categoría y el color asignado a este.
                        Text('Categories', size=15, weight=FontWeight.W_300, color='white', font_family='poppins'), #Texto qu acompaña al ícono de la categoría.
                    ]
                ),
                Container(height=5), #Espacio entre los bloques.
                Row( #Bloque del análisis.
                    controls=[
                        Icon(icons.CALCULATE_OUTLINED, color='white60'), #Ícono del análisis y el color asignado a este.
                        Text('Analytics', size=15, weight=FontWeight.W_300, color='white', font_family='poppins'), #Texto qu acompaña al ícono del análisis.
                    ]
                ),
                Image( #Imagen del gráfico.
                    src="img/1.png",
                    width=300,
                    height=200
                ),
                Text('Good', color=FG, font_family='poppins'), #Texto pequeño de abajo.
                Text('Consistency', size=22) #Texto grande de abajo.
            ]
        ) 
    )
    page_2 = Row( #Se define así porque se utilizarán animaciones y el widget de fila da la alineación que se desea.
        alignment='end', #Alinea hacia la derecha al achicarse.
        controls=[ #Se utilizarán parámetros de controles.
            Container(
                width=400,
                height=850,
                bgcolor=FG,
                border_radius=35,
                animate=animation.Animation(600, AnimationCurve.DECELERATE), #Asigna una animación que durará 600s y tendrá un estilo desacelerado.
                animate_scale=animation.Animation(400, curve='decelerate'), #Otra manera de animar.
                padding=padding.only(
                    top=50, left=20,
                    right=20, bottom=5 
                ),
                content=Column( #Se crea el contenido como una columna para que vayan los widgets horizontales allí.
                    controls=[
                        first_page_contents
                    ]
                )
            )
        ]
    )

    container = Container( #Se crea un contenedor para luego agregar dentro de la página.
        #Se establecen los valores que tendrá el contenedor (ancho, altura y color de fondo).
        width=400, #Ancho
        height=815, #Altura (850 según el tutorial pero no me entró en la pantalla)
        bgcolor=BG, #Color de fondo.
        border_radius=35,
        content=Stack( #contenido que irá dentro del contenedor y se convertirá en un widget
            #Widget de pila que contendrá muchos widgets más.
            controls=[ #Al contenido de la pila de widgets se lo llama controls.
                page_1,
                page_2
            ]
        )
    )

    #Diccionario de vistas.
    pages = {
        '/':View( #Página 1: Diccionario /
            "/", #Cuando se llame a la página de esta manera...
            [   #Tendrá que hacer todo lo que está en este bloque []
                container
            ],
        ),
        '/create_task': View( #Página 2: Diccionario /create_task
            "/create_task", #Cuando se llame a la página de esta manera...
            [ #Tendrá que hacer todo lo que está en este bloque []
                
            ]
        )
    }
    
    #Se crea la función que cambiará de ruta cuando se presione el botón flotante.
    def route_change(route):
        page.views.clear() #Esto hace que se borre la vista actual. Cada que se llame a la función, se volverá a crear una vista nueva.
        page.views.append( #Se agrega una vista particular.
            pages[page.route] #Se llama al diccionario de vistas.
        )

    page.add(container) #Aquí se agrega el contenedor a la página.

    page.on_route_change = route_change #Hace que cambie la ruta por la que se definió en la variable route_change. Crea la ruta aquí y la activa, una vez hecho esto pasa a la función definida con ese nombre.
    page.go(page.route) #Es lo que hará que inicie otra página.

ft.app(target=main, assets_dir='img')
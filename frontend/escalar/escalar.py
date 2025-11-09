import reflex as rx
from escalar.pages.index import index
from escalar.pages.documentos import documentos_page
from escalar.pages.subir_documento import subir_documento_page


app = rx.App()
app.add_page(index, route="/")
app.add_page(documentos_page, route="/documentos")
app.add_page(subir_documento_page, route="/subir_documento")





import reflex as rx
from ..state import DocumentoState


def documentos_page() -> rx.Component:
    return rx.vstack(
        rx.heading("📂 Lista de Documentos", size="8", margin_bottom="1em"),
        rx.button(
            "🔄 Actualizar lista",
            on_click=DocumentoState.cargar_documentos,
            color_scheme="blue",
        ),
        rx.divider(margin_y="1em"),

        # ───────────── LISTA DE DOCUMENTOS ─────────────
        rx.foreach(
            DocumentoState.documentos,
            lambda doc: rx.box(
                rx.hstack(
                    rx.text(f"📄 {doc['title']} — {doc['area']} ({doc['fecha']})"),
                    rx.spacer(),
                    rx.button(
                        "✏️ Editar",
                        size="2",
                        color_scheme="blue",
                        on_click=lambda: DocumentoState.editar_documento(doc),
                    ),
                    rx.button(
                        "🗑️ Eliminar",
                        size="2",
                        color_scheme="red",
                        on_click=lambda: DocumentoState.confirmar_eliminacion(doc["id"]),
                    ),
                ),
                border="1px solid #ddd",
                border_radius="8px",
                padding="10px",
                margin_bottom="8px",
                width="100%",
            ),
        ),


        # ───────────── MODAL DE EDICIÓN ─────────────
        rx.cond(
            DocumentoState.editando,
            rx.dialog.root(
                rx.dialog.trigger(rx.box()),
                rx.dialog.content(
                    rx.heading("Editar Documento", size="6", margin_bottom="1em"),
                    rx.input(
                        value=DocumentoState.titulo_edit,
                        placeholder="Título",
                        on_change=DocumentoState.set_titulo,
                    ),
                    rx.input(
                        value=DocumentoState.area_edit,
                        placeholder="Área",
                        on_change=DocumentoState.set_area,
                    ),
                    rx.input(
                        value=DocumentoState.clasificacion_edit,
                        placeholder="Clasificación",
                        on_change=DocumentoState.set_clasificacion,
                    ),
                    rx.hstack(
                        rx.button(
                            "Guardar",
                            color_scheme="green",
                            on_click=DocumentoState.guardar_edicion,
                        ),
                        rx.button(
                            "Cancelar",
                            color_scheme="gray",
                            on_click=DocumentoState.cancelar_edicion,
                        ),
                    ),
                ),
            ),
        ),

        # ───────────── MODAL DE CONFIRMACIÓN DE ELIMINAR ─────────────
        rx.cond(
            DocumentoState.confirm_delete_id,
            rx.dialog.root(
                rx.dialog.trigger(rx.box()),
                rx.dialog.content(
                    rx.heading("Confirmar eliminación", size="6"),
                    rx.text(
                        "¿Desea eliminar este documento? Esta acción no se puede deshacer."
                    ),
                    rx.hstack(
                        rx.button(
                            "Eliminar",
                            color_scheme="red",
                            on_click=DocumentoState.eliminar_documento,
                        ),
                        rx.button(
                            "Cancelar",
                            color_scheme="gray",
                            on_click=DocumentoState.cancelar_eliminacion,
                        ),
                    ),
                ),
            ),
        ),

        spacing="3",
        padding="2em",
    )







import reflex as rx

def index() -> rx.Component:
    """Página principal de la app."""
    return rx.center(
        rx.vstack(
            rx.heading("Gestión de Documentos", size="9"),
            rx.text("Frontend conectado a la API FastAPI."),
        ),
        min_h="100vh",
    )


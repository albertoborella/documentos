import os
import reflex as rx


class SubirDocumentoState(rx.State):
    # Campos del formulario
    title: str = ""
    fecha: str = ""
    tipo: str = "externo"
    area: str = ""
    clasificacion: str = ""
    mensaje: str = ""
    archivo_subido: bool = False

    # --- Métodos setters ---
    def set_title(self, value):
        self.title = value

    def set_fecha(self, value):
        self.fecha = value

    def set_tipo(self, value):
        self.tipo = value

    def set_area(self, value):
        self.area = value

    def set_clasificacion(self, value):
        self.clasificacion = value

    # --- Manejo de subida de archivos ---
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Guarda el archivo seleccionado localmente."""
        if not files:
            self.mensaje = "❌ No se seleccionó ningún archivo."
            return

        file = files[0]
        os.makedirs("uploads", exist_ok=True)

        file_path = os.path.join("uploads", file.filename)
        contenido = await file.read()

        with open(file_path, "wb") as f:
            f.write(contenido)

        self.archivo_subido = True
        self.mensaje = f"✅ Archivo '{file.filename}' subido correctamente."


# --- Página principal ---
def subir_documento_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("📎 Subir Documento", size="7"),
                rx.text("Completá los campos y subí tu archivo.", size="4"),

                # --- Campos del formulario ---
                rx.input(
                    placeholder="Título del documento",
                    value=SubirDocumentoState.title,
                    on_change=SubirDocumentoState.set_title,
                ),
                rx.input(
                    type="date",
                    value=SubirDocumentoState.fecha,
                    on_change=SubirDocumentoState.set_fecha,
                ),
                rx.select(
                    ["externo", "interno"],
                    value=SubirDocumentoState.tipo,
                    on_change=SubirDocumentoState.set_tipo,
                ),
                rx.input(
                    placeholder="Área",
                    value=SubirDocumentoState.area,
                    on_change=SubirDocumentoState.set_area,
                ),
                rx.input(
                    placeholder="Clasificación",
                    value=SubirDocumentoState.clasificacion,
                    on_change=SubirDocumentoState.set_clasificacion,
                ),

                # --- Subida de archivo ---
                rx.upload(
                    rx.button("📤 Seleccionar archivo"),
                    accept=[".pdf", ".xlsx", ".docx", ".txt", ".csv"],
                ),
                rx.button(
                    "Subir archivo",
                    color_scheme="green",
                    on_click=lambda: SubirDocumentoState.handle_upload(
                        rx.upload_files()
                    ),
                ),

                # --- Mensaje de estado ---
                rx.text(SubirDocumentoState.mensaje, size="4"),

                spacing="4",
                width="100%",
                align="center",
            ),
            padding="6",
            width="480px",
            shadow="md",
        ),
        height="100vh",
    )


# --- Registrar la página ---
# app = rx.App()
# app.add_page(subir_documento_page, route="/subir_documento")









import reflex as rx
import requests

API_URL = "http://localhost:8000/documentos/"

class DocumentoState(rx.State):
    """Maneja el estado y las acciones de la lista de documentos."""
    documentos: list[dict] = []
    editando: dict | None = None
    titulo_edit: str = ""
    area_edit: str = ""
    clasificacion_edit: str = ""
    confirm_delete_id: int | None = None  # para mostrar diálogo de confirmación

    # ──────────────────────────────── AUXILIARES ────────────────────────────────
    @rx.event
    def cancelar_edicion(self):
        """Cierra el diálogo de edición."""
        self.editando = None
        self.titulo_edit = ""
        self.area_edit = ""
        self.clasificacion_edit = ""

    @rx.event
    def confirmar_eliminacion(self, doc_id: int):
        """Muestra el diálogo de confirmación para eliminar."""
        self.confirm_delete_id = doc_id

    @rx.event
    def cancelar_eliminacion(self):
        """Cierra el diálogo sin eliminar."""
        self.confirm_delete_id = None

    # ──────────────────────────────── CRUD ────────────────────────────────
    async def cargar_documentos(self):
        """Obtiene la lista de documentos desde la API."""
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                self.documentos = response.json()
            else:
                print(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print("Error al conectar con la API:", e)

    async def eliminar_documento(self):
        """Elimina el documento confirmado."""
        if not self.confirm_delete_id:
            return
        try:
            response = requests.delete(f"{API_URL}{self.confirm_delete_id}")
            if response.status_code == 200:
                self.documentos = [
                    d for d in self.documentos if d["id"] != self.confirm_delete_id
                ]
            else:
                print(f"Error al eliminar: {response.status_code}")
        except Exception as e:
            print("Error al conectar con la API:", e)
        finally:
            self.confirm_delete_id = None

    @rx.event
    def editar_documento(self, doc: dict):
        """Carga los datos del documento a editar."""
        self.editando = doc
        self.titulo_edit = doc["title"]
        self.area_edit = doc["area"]
        self.clasificacion_edit = doc["clasificacion"]

    async def guardar_edicion(self):
        """Actualiza los datos del documento en el backend."""
        if not self.editando:
            return

        doc_id = self.editando["id"]
        datos_actualizados = {
            "title": self.titulo_edit,
            "area": self.area_edit,
            "clasificacion": self.clasificacion_edit,
            "activo": True,
        }

        try:
            response = requests.put(f"{API_URL}{doc_id}", json=datos_actualizados)
            if response.status_code == 200:
                actualizado = response.json()
                self.documentos = [
                    actualizado if d["id"] == doc_id else d for d in self.documentos
                ]
                self.cancelar_edicion()
            else:
                print(f"Error al actualizar: {response.status_code}")
        except Exception as e:
            print("Error al conectar con la API:", e)

    # ──────────────────────────────── EVENTOS DE FORMULARIO ────────────────────────────────
    @rx.event
    def set_titulo(self, value: str):
        self.titulo_edit = value

    @rx.event
    def set_area(self, value: str):
        self.area_edit = value

    @rx.event
    def set_clasificacion(self, value: str):
        self.clasificacion_edit = value

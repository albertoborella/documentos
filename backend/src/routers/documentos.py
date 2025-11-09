from datetime import date, datetime
import os
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from sqlmodel import select
from src.db.database import sessionDep
from src.models.documentos import Documento, DocumentoCrear, DocumentoModificar, DocumentoMostrar, TipoEnum


documentos_router = APIRouter(prefix='/documentos', tags=['Documentos'])

# Mostrar documentos
@documentos_router.get("/", response_model=list[DocumentoMostrar])
async def documentos(session: sessionDep):
    doc = select(Documento)
    documentos = session.exec(doc).all()
    return documentos

@documentos_router.get("/{documento_id}", response_model=DocumentoMostrar)
async def obtener_documento(documento_id: int, session: sessionDep):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento

# Ruta base para guardar los documentos
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
UPLOAD_DIR = os.path.join(BASE_DIR, "archivos")
os.makedirs(UPLOAD_DIR, exist_ok=True)

FECHAS_FORMATOS = ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"]

@documentos_router.post("/subir", response_model=DocumentoMostrar)
async def subir_documento(
    title: str = Form(...),
    fecha: str = Form(...),
    tipo: TipoEnum = Form(...),
    area: str = Form(...),
    clasificacion: str = Form(...),
    archivo: UploadFile = File(...),
    session: sessionDep = None,
):
    # Convertir la fecha con varios formatos posibles
    for fmt in FECHAS_FORMATOS:
        try:
            fecha_obj = datetime.strptime(fecha.strip(), fmt).date()
            break
        except ValueError:
            continue
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de fecha inválido ({fecha}). Usa DD-MM-YYYY, YYYY-MM-DD o DD/MM/YYYY.",
        )

    # Guardar el archivo en disco
    nombre_archivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{archivo.filename}"
    ruta_absoluta = os.path.join(UPLOAD_DIR, nombre_archivo)
    with open(ruta_absoluta, "wb") as f:
        f.write(await archivo.read())

    ruta_relativa = f"/archivos/{nombre_archivo}"

    # Crear el diccionario primero
    datos_doc = {
        "title": title,
        "fecha": fecha_obj,
        "tipo": tipo,
        "area": area,
        "clasificacion": clasificacion,
        "texto": ruta_relativa,
        "activo": True,
    }

    # Crear y guardar el documento
    nuevo_doc = Documento(**datos_doc)

    session.add(nuevo_doc)
    session.commit()
    session.refresh(nuevo_doc)

    return nuevo_doc

# @documentos_router.post("/subir", response_model=DocumentoMostrar)
# async def subir_documento(
#     title: str = Form(...),
#     fecha: str = Form(...),
#     tipo: TipoEnum = Form(...),
#     area: str = Form(...),
#     clasificacion: str = Form(...),
#     archivo: UploadFile = File(...),
#     session: sessionDep = None,
# ):
#     # Convertir la fecha
#     try:
#         fecha_obj = datetime.strptime(fecha.strip(), "%d-%m-%Y").date()
#     except ValueError:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Formato de fecha inválido ({fecha}). Usa el formato DD-MM-YYYY.",
#         )

#     # Guardar el archivo en disco
#     nombre_archivo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{archivo.filename}"
#     ruta_absoluta = os.path.join(UPLOAD_DIR, nombre_archivo)
#     with open(ruta_absoluta, "wb") as f:
#         f.write(await archivo.read())

#     ruta_relativa = f"/archivos/{nombre_archivo}"

#     # Crear el diccionario primero, no el modelo directamente
#     datos_doc = {
#         "title": title,
#         "fecha": fecha_obj,  # 👈 aseguramos que es un datetime.date
#         "tipo": tipo,
#         "area": area,
#         "clasificacion": clasificacion,
#         "texto": ruta_relativa,
#         "activo": True,
#     }

#     # Crear y guardar el documento
#     nuevo_doc = Documento(**datos_doc)

#     # Confirmar que la fecha es date
#     if not isinstance(nuevo_doc.fecha, date):
#         raise HTTPException(
#             status_code=500,
#             detail=f"Fecha no es del tipo date: {type(nuevo_doc.fecha)} -> {nuevo_doc.fecha}",
#         )

#     session.add(nuevo_doc)
#     session.commit()
#     session.refresh(nuevo_doc)

#     return nuevo_doc

@documentos_router.put("/{documento_id}", response_model=DocumentoMostrar)
async def actualizar_documento(
    documento_id: int,
    doc_modif: DocumentoModificar,
    session: sessionDep,
):
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # Actualizar solo los campos enviados
    doc_data = doc_modif.model_dump(exclude_unset=True)
    for key, value in doc_data.items():
        setattr(documento, key, value)

    session.add(documento)
    session.commit()
    session.refresh(documento)
    return documento

# @documentos_router.delete("/{documento_id}")
# async def eliminar_documento(documento_id: int, session: sessionDep):
#     documento = session.get(Documento, documento_id)
#     if not documento:
#         raise HTTPException(status_code=404, detail="Documento no encontrado")

#     # Eliminar archivo físico si existe
#     if documento.texto:
#         archivo_path = os.path.join(BASE_DIR, documento.texto.strip("/"))
#         if os.path.exists(archivo_path):
#             os.remove(archivo_path)

#     session.delete(documento)
#     session.commit()
#     return {"mensaje": f"Documento {documento_id} eliminado correctamente"}

@documentos_router.delete("/documento/{documento_id}", response_model=DocumentoMostrar)
def eliminar_documento_logico(
    documento_id: int,
    session: sessionDep,
):
    # Buscar el documento
    documento = session.get(Documento, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Eliminación lógica
    documento.activo = False
    session.add(documento)
    session.commit()
    session.refresh(documento)

    return documento



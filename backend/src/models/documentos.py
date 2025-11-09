from datetime import date, datetime
from enum import Enum
from sqlmodel import SQLModel, Field  

class TipoEnum(str, Enum):
    interno = "interno"
    externo = "externo"


class DocumentoBase(SQLModel):
    title: str
    fecha: date | None = None
    tipo: TipoEnum = Field(default=TipoEnum.externo)
    area: str
    clasificacion: str
    texto: str
    

class Documento(DocumentoBase, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    created_at: datetime = Field(default_factory=datetime.now)
    activo: bool = Field(default=True)

class DocumentoCrear(DocumentoBase):
    pass

class DocumentoMostrar(DocumentoBase):
    id: int

class DocumentoModificar(DocumentoBase):
    title: str | None = None
    fecha: date | None = None
    area: str| None = None
    clasificacion: str | None = None
    texto: str | None = None
    activo: bool | None = None




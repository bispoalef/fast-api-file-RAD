from fastapi import APIRouter, Path, UploadFile, File

from domain.file_processor import FileProcessor

router = APIRouter()


@router.post("/file/create_file")
async def create_file():
    return FileProcessor().create_file()


@router.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    return await FileProcessor().upload_file(file)


@router.post("/file/add_data")
async def add_data():
    return {"message": "Dado adicionado com sucesso"}


@router.delete("/file/delete_data")
async def delete_data():
    return {"message": "Dado removido com sucesso"}


@router.get("/list_files/{file_name}")
def list_files(file_name: str = Path(..., example="seu_file.csv", description="Nome do arquivo a ser listado")):
    return FileProcessor().list_files(file_name)

import csv
import os

from fastapi import HTTPException, status, UploadFile


class FileProcessor:
    """ Manager of files and folders processor."""

    def __init__(self):
        self.file_path = 'data/seu_file.csv'
        self.directory = 'data'

    def create_file(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['conta', 'agencia', 'texto', 'valor'])
                return {"mensagem": f"Arquivo {self.file_path} craido com suscesso."}
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Arquivo já existe")

    async def upload_file(self, file: UploadFile):
        """
        Upload a file to read and print data
        :param file: uploaded file
        :return: success or error
        """
        if file.filename.endswith('.csv'):
            try:
                # Decodifica o arquivo para string
                contents = await file.read()
                decoded_file = contents.decode('utf-8').splitlines()

                # Cria o CSV reader a partir do conteúdo decodificado
                csv_reader = csv.DictReader(decoded_file)

                for row in csv_reader:
                    data = {
                        "conta": row['conta'],  # Usa o nome correto da coluna no CSV
                        "agencia": row['agencia'],
                        "texto": row['texto'],
                        "valor": float(row['valor'])
                    }
                    print(data)

                return {"mensagem": f"Arquivo {file.filename} processado com sucesso"}
            except KeyError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro: coluna {str(e)} não encontrada no CSV"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Falha ao processar o arquivo CSV: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Apenas arquivos CSV são aceitos"
            )



    def list_files(self, file_name: str):
        """
        Listar todas as linhas de um arquivo selecionado.
        :param file_name: Nome do arquivo a ser listado
        :return: Todas linhas do arquivo CSV
        """
        # Construindo o caminho completo do arquivo a ser aberto
        file_path = os.path.join(self.directory, file_name)

        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Arquivo {file_name} não encontrado")

        try:
            # Abre o arquivo e lê todas as linhas
            with open(file_path, 'r', newline='') as file:
                lines = file.readlines()

            # Verifica se o arquivo está vazio
            if not lines:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                    detail=f"O arquivo {file_name} está vazio")

            return {"file_name": file_name, "content": lines}

        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Arquivo {file_name} não encontrado")

        except PermissionError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Permissão negada para acessar o arquivo {file_name}")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Erro ao ler o arquivo {file_name}: {str(e)}")
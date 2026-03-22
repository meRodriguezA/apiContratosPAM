from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import shutil
import os
from datetime import datetime
import json
import base64
from src.utils.logger import Logger
from src.core.app_paths import AppPaths
from src.core.template_manager_chip import TemplateInstaller
from src.core.template_manager_contrato import TemplateInstallerContrato
from src.core.template_manager_baja_reiac import TemplateInstallerBajaReiac
from src.integrations.sheet_row_reader import SpreadsheetDataReader
from src.core.document_generator import DocumentGenerationService
import gspread
from src.config import SPREADSHEET_NAME

app = FastAPI(title="PAM Generador de Documentos API", version="1.0.0")

class DocumentRequest(BaseModel):
    pass  # No necesitamos body por ahora, pero podemos extenderlo

# Inicializar servicios (similar a ConsoleUI)
logger = Logger()
paths = AppPaths()

# Crear archivo de credenciales desde variable de entorno si no existe
credentials_path = paths.get_credentials_json()
if not os.path.exists(credentials_path):
    gcp_json_env = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    if gcp_json_env:
        try:
            # Intentar decodificar si está en base64
            try:
                decoded = base64.b64decode(gcp_json_env).decode('utf-8')
                creds_data = json.loads(decoded)
            except:
                # Si no es base64, asumir que es JSON directo
                creds_data = json.loads(gcp_json_env)
            
            os.makedirs(os.path.dirname(credentials_path), exist_ok=True)
            with open(credentials_path, 'w') as f:
                json.dump(creds_data, f)
            logger.info(f"Archivo de credenciales creado desde variable de entorno")
        except Exception as e:
            logger.error(f"Error procesando GOOGLE_SERVICE_ACCOUNT_JSON: {str(e)}")
    else:
        logger.warn(f"No se encontró archivo de credenciales en {credentials_path} ni variable GOOGLE_SERVICE_ACCOUNT_JSON")

installer = TemplateInstaller(paths)
template_path_chip = installer.ensure_external_template()

installer_contrato = TemplateInstallerContrato(paths)
template_path_contrato = installer_contrato.ensure_external_template()

installer_baja_reiac = TemplateInstallerBajaReiac(paths)
template_path_baja_reiac = installer_baja_reiac.ensure_external_template()

reader = SpreadsheetDataReader(
    credentials_json_path=paths.get_credentials_json(),
    debug_table=True
)

generator = DocumentGenerationService(
    paths=paths,
    reader=reader,
    template_path=template_path_chip,
    template_path_contrato=template_path_contrato,
    template_path_baja_reiac=template_path_baja_reiac,
    logger=logger
)

@app.get("/")
async def root():
    return {"message": "PAM Generador de Documentos API", "status": "running"}

@app.get("/generate/animal/{animal_name}")
async def generate_by_animal(animal_name: str):
    try:
        logger.info(f"Generando documento para animal: {animal_name}")
        folder_path = generator.generate_for_animal_name(SPREADSHEET_NAME, animal_name)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"{animal_name}_{timestamp}"
        zip_path = shutil.make_archive(zip_filename, 'zip', folder_path)

        return FileResponse(
            path=zip_path,
            media_type='application/zip',
            filename=os.path.basename(zip_path),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generando documento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/generate/row/{row_number}")
async def generate_by_row(row_number: int):
    try:
        logger.info(f"Generando documento para fila: {row_number}")
        folder_path = generator.generate_for_sheet_row(SPREADSHEET_NAME, row_number)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"row_{row_number}_{timestamp}"
        zip_path = shutil.make_archive(zip_filename, 'zip', folder_path)

        return FileResponse(
            path=zip_path,
            media_type='application/zip',
            filename=os.path.basename(zip_path),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generando documento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # 8000 como fallback local
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")
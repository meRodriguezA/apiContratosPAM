from src.utils.logger import Logger
from src.core.app_paths import AppPaths
from src.core.template_manager_chip import TemplateInstaller
from src.core.template_manager_contrato import TemplateInstallerContrato
from src.core.template_manager_baja_reiac import TemplateInstallerBajaReiac
from src.integrations.sheet_row_reader import SpreadsheetDataReader
from src.core.document_generator import DocumentGenerationService
from src.utils.utils_text import is_blank
import gspread
import sys

from src.config import SPREADSHEET_NAME

class ConsoleUI:
    def __init__(self):
        self.logger = Logger()

        self.paths = AppPaths()

        installer = TemplateInstaller(self.paths)
        template_path_chip = installer.ensure_external_template()
        
        installer_contrato = TemplateInstallerContrato(self.paths)
        template_path_contrato = installer_contrato.ensure_external_template()
        
        installer_baja_reiac = TemplateInstallerBajaReiac(self.paths)
        template_path_baja_reiac = installer_baja_reiac.ensure_external_template()
        
        
        self.reader = SpreadsheetDataReader(
            credentials_json_path=self.paths.get_credentials_json(),
            debug_table=True
        )

        self.generator = DocumentGenerationService(
            paths=self.paths,
            reader=self.reader,
            template_path=template_path_chip,
            template_path_contrato=template_path_contrato,
            template_path_baja_reiac=template_path_baja_reiac,
            logger=self.logger
        )

    def run(self):
        spreadsheet_name = SPREADSHEET_NAME

        print("===================================")
        print("PAM - Generador de documentos")
        print("===================================")
        print(f"[INFO] Carpeta salida: {self.paths.output_dir}")
        print(f"[INFO] Plantillas:     {self.paths.external_templates_dir}")
        print("")

        if len(sys.argv) > 1:
            user_input = sys.argv[1].strip()
        elif sys.stdin.isatty():
            user_input = input("Introduce nombre del animal o nº de fila: ").strip()
        else:
            print("Uso: PAM_GeneradorDocs.exe <nombre_animal_o_numero_fila>")
            return

        if is_blank(user_input):
            self.logger.warn("No has escrito nada.")
            print("")
            return

        try:
            self.logger.info("Conectando con Google Sheets...")
            self.logger.info("Generando documento...")

            if user_input.isdigit():
                row_number = int(user_input)
                output_docx = self.generator.generate_for_sheet_row(spreadsheet_name, row_number)
            else:
                output_docx = self.generator.generate_for_animal_name(spreadsheet_name, user_input)

            print("\n===================================")
            print(f"Word generado: {output_docx}")
            print("===================================")

        except ValueError as e:
            self.logger.warn(str(e))
            print("")

        except Exception as e:
            msg = str(e)

            if isinstance(e, gspread.exceptions.SpreadsheetNotFound):
                self.logger.error(f"No se encontró el Spreadsheet con nombre: {spreadsheet_name}")
                self.logger.info("Revisa el nombre exacto en Google Drive y que esté compartido con el service account.")
                return

            if "NameResolutionError" in msg or "Failed to establish a new connection" in msg:
                self.logger.error("No se pudo conectar a internet (o Google no responde).")
                self.logger.info("Revisa tu conexión y vuelve a intentarlo.")
                return

            self.logger.error("No se pudo generar el documento.")
            self.logger.error(f"Detalle: {msg}")

            if "The caller does not have permission" in msg or "403" in msg:
                self.logger.error("Permiso denegado (403).")
                self.logger.info("Comparte el Spreadsheet con el email del service_account.json como Editor.")
            elif "Google Drive API has not been used" in msg:
                self.logger.error("Google Drive API no está activada.")
                self.logger.info("Actívala en Google Cloud Console.")

        input("\nPulsa ENTER para finalizar...")

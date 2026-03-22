from csv import reader, writer, writer

from src.core.docx_renderer import DocxRenderer
from src.core.output_paths import DocumentOutputBuilder
from src.utils.logger import Logger
from pathlib import Path
from src.utils.row_validator import SpreadsheetRowValidator
from src.utils.field_validation_config import VALIDATION_RULES
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import pikepdf 
import os 


class DocumentGenerationService:
    def __init__(self, paths, reader, template_path: str, template_path_contrato:str, template_path_baja_reiac:str, logger: Logger = None):
        self.paths = paths
        self.reader = reader
        self.template_path = template_path
        self.template_path_contrato = template_path_contrato
        self.template_path_baja_reiac = template_path_baja_reiac
        self.logger = logger or Logger()

        self.output_builder = DocumentOutputBuilder(paths.output_dir)

    def _validate_or_raise(self, context_excel: dict):
        errors = self.validator.validate(context_excel)
        if errors:
            raise ValueError("Errores de validación:\n- " + "\n- ".join(errors))

    def generate_from_context(self, animal_name: str, context_word: dict) -> str:
        # Crear carpeta con timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        animal_name_with_timestamp = f"{animal_name}_{timestamp}"
        
        folder_path = Path(self.output_builder.base_output_dir) / animal_name_with_timestamp
        folder_path.mkdir(parents=True, exist_ok=True)

        # Fichero 1
        output_doc1 = folder_path / f"{animal_name}_cesion_chip.docx"
        renderer = DocxRenderer(self.template_path)
        renderer.render(str(output_doc1), context_word)

        # Fichero 2
        output_doc2 = folder_path / f"{animal_name}_contrato.docx"
        renderer2 = DocxRenderer(self.template_path_contrato)
        renderer2.render(str(output_doc2), context_word)
        
        #PDF baja Reiac - verificar si existe
        if os.path.exists(self.template_path_baja_reiac):
            try:
                reader = PdfReader(self.template_path_baja_reiac)
                writer = PdfWriter()
                page = reader.pages[0]
                fields = reader.get_fields()

                writer.update_page_form_field_values(
                    page,
                    {
                        "Cuadro de texto 1": context_word.get("microchip", ""),
                        "Cuadro de texto 2": context_word.get("diaFirma", "") + "/" + context_word.get("mesFirma", "") + "/" + context_word.get("anyofirma", ""),
                        "Cuadro de texto 3": "Protectora de Animales y Plantas de Montehermoso",
                        "Cuadro de texto 4": "G02903870",
                        "Cuadro de texto 5": context_word.get("nombreAdoptante", ""),
                        "Cuadro de texto 6": context_word.get("dni", ""),
                    },
                )

                writer.add_page(page)
                
                pdf_path = folder_path / f"{animal_name}_baja_reiac.pdf"
                with open(pdf_path, "wb") as f:
                    writer.write(f)
                
                # Aplanar el PDF
                with pikepdf.open(str(pdf_path), allow_overwriting_input=True) as pdf:
                    pdf.flatten_annotations()
                    pdf.save(str(pdf_path))
            except Exception as e:
                self.logger.warning(f"Error al generar PDF baja_reiac: {str(e)}")
        else:
            self.logger.warning(f"Plantilla PDF no encontrada en {self.template_path_baja_reiac}")
            
        return str(folder_path)

    def generate_for_animal_name(self, spreadsheet_name: str, animal_input: str) -> str:
        context_word, context_excel = self.reader.get_context_by_animal(spreadsheet_name, animal_input)
        #self._validate_or_raise(context_excel)

        animal_excel = context_word.get("Nombre", animal_input)
        return self.generate_from_context(animal_excel, context_word)

    def generate_for_sheet_row(self, spreadsheet_name: str, sheet_row_number: int) -> str:
        context_word, context_excel = self.reader.get_context_by_sheet_row(spreadsheet_name, sheet_row_number)
        #self._validate_or_raise(context_excel)

        animal_excel = context_word.get("nombre")
        return self.generate_from_context(animal_excel, context_word)

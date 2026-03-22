import os
from datetime import datetime

from src.utils.utils_text import safe_filename


class DocumentOutputBuilder:
    def __init__(self, base_output_dir: str):
        self.base_output_dir = base_output_dir
        os.makedirs(self.base_output_dir, exist_ok=True)

    @staticmethod
    def _today_str() -> str:
        return datetime.now().strftime("%d_%m_%Y")

    def build_output_folder(self, animal_name: str) -> str:
        safe_name = safe_filename(animal_name)
        folder_name = f"{safe_name}_{self._today_str()}"

        folder_path = os.path.join(self.base_output_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    def build_docx_path(self, animal_name: str) -> str:
        safe_name = safe_filename(animal_name)
        today = self._today_str()
        folder = self.build_output_folder(animal_name)

        return os.path.join(folder, f"Documento_cesion_{safe_name}_{today}.docx")

    def build_pdf_path(self, animal_name: str) -> str:
        return os.path.splitext(self.build_docx_path(animal_name))[0] + ".pdf"

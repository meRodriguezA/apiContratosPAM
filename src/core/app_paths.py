import os
import sys

from src.config import (
    OUTPUT_DIR_NAME,
    TEMPLATES_DIR_NAME,
    TEMPLATES_EXTERNAL_DIR_NAME,
    DEFAULT_TEMPLATE_FILENAME,
    DEFAULT_TEMPLATE_FILENAME_CONTRATO,
    CONFIG_DIR_NAME,
    SERVICE_ACCOUNT_JSON_FILENAME,
)


class AppPaths:
    def __init__(self):
        self.project_root = self._get_project_root()
        self.app_dir = self._get_app_dir()

        # Donde se generan los documentos (junto al exe)
        self.output_dir = os.path.join(self.app_dir, OUTPUT_DIR_NAME)
        os.makedirs(self.output_dir, exist_ok=True)

        # Plantillas externas visibles (junto al exe)
        self.external_templates_dir = os.path.join(self.app_dir, TEMPLATES_EXTERNAL_DIR_NAME)
        os.makedirs(self.external_templates_dir, exist_ok=True)

    @staticmethod
    def _get_project_root() -> str:
        """
        Raíz del proyecto en modo Python (carpeta donde está GenerarDocs.py).
        En modo exe no se usa para leer archivos, se usa _MEIPASS.
        """
        # src/core/app_paths.py -> subimos 2 niveles -> src -> proyecto
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @staticmethod
    def _get_app_dir() -> str:
        """
        Carpeta real de ejecución:
        - en exe: carpeta del ejecutable
        - en python: carpeta del proyecto (donde está GenerarDocs.py)
        """
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)

        # raiz del proyecto (donde está GenerarDocs.py)
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def bundled_path(self, relative_path: str) -> str:
        """
        Devuelve una ruta absoluta para:
        - modo exe: archivos dentro del bundle (_MEIPASS)
        - modo python: archivos en el proyecto real
        """
        if getattr(sys, "frozen", False):
            base = sys._MEIPASS
        else:
            base = self.project_root

        return os.path.join(base, relative_path)

    def get_credentials_json(self) -> str:
        return self.bundled_path(os.path.join(CONFIG_DIR_NAME, SERVICE_ACCOUNT_JSON_FILENAME))

    def get_bundled_template(self) -> str:
        return self.bundled_path(os.path.join(TEMPLATES_DIR_NAME, DEFAULT_TEMPLATE_FILENAME))

    def get_external_template(self) -> str:
        return os.path.join(self.external_templates_dir, DEFAULT_TEMPLATE_FILENAME)
    
    def get_bundled_template_contrato(self) -> str:
        return self.bundled_path(os.path.join(TEMPLATES_DIR_NAME, DEFAULT_TEMPLATE_FILENAME_CONTRATO))

    def get_external_template_contrato(self) -> str:
        return os.path.join(self.external_templates_dir, DEFAULT_TEMPLATE_FILENAME_CONTRATO)
    

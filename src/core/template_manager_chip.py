import os
import shutil

from src.core.app_paths import AppPaths
from src.utils.logger import Logger
from src.config import DEFAULT_TEMPLATE_FILENAME

class TemplateInstaller:
    def __init__(self, paths: AppPaths, logger: Logger = None):
        self.paths = paths
        self.logger = logger or Logger()

    def ensure_external_template(self) -> str:
        dst = os.path.join(self.paths.external_templates_dir, DEFAULT_TEMPLATE_FILENAME)

        if os.path.exists(dst):
            return dst

        src = self.paths.get_bundled_template()

        if not os.path.exists(src):
            raise FileNotFoundError(f"No se encuentra la plantilla original en: {src}")

        self.logger.info("Copiando plantilla a la carpeta Plantillas...")
        shutil.copyfile(src, dst)

        return dst

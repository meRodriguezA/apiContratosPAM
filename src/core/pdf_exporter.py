import os
import subprocess


class DocxToPdfConverter:
    @staticmethod
    def _find_soffice_path():
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        for p in possible_paths:
            if os.path.exists(p):
                return p
        return None

    def docx_to_pdf(self, input_docx_path: str, output_pdf_path: str):
        try:
            from docx2pdf import convert
            convert(input_docx_path, output_pdf_path)
            return output_pdf_path
        except Exception:
            pass

        soffice_path = self._find_soffice_path()
        if not soffice_path:
            raise FileNotFoundError("No se encontró Word ni LibreOffice (soffice.exe).")

        outdir = os.path.dirname(output_pdf_path)

        cmd = [
            soffice_path,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", outdir,
            input_docx_path
        ]

        subprocess.run(cmd, check=True)

        generated = os.path.splitext(input_docx_path)[0] + ".pdf"
        if os.path.exists(generated) and generated != output_pdf_path:
            os.replace(generated, output_pdf_path)

        if not os.path.exists(output_pdf_path):
            raise RuntimeError("LibreOffice terminó pero no se encontró el PDF generado.")

        return output_pdf_path

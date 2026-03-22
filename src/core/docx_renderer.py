from docxtpl import DocxTemplate


class DocxRenderer:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def render(self, output_docx_path: str, context: dict):
        doc = DocxTemplate(self.template_path)
        doc.render(context)
        doc.save(output_docx_path)

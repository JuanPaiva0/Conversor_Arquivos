from reportlab.pdfgen import canvas
from docx import Document
import os
import pdfplumber
import subprocess

class DocumentService:
    def ensure_output_dir(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        return OUTPUT_DIR
    
    async def convert_txt_to_pdf(self, file):
        ouptu_dir = self.ensure_output_dir()

        name, _ = os.path.splitext(file.filename)
        output_path = os.path.join(ouptu_dir, f"{name}.pdf")

        content = (await file.read()).decode("utf-8")

        pdf = canvas.Canvas(output_path)
        pdf.drawString(100, 750, content)
        pdf.save()

        return output_path

    async def convert_txt_to_docx(self, file):
        output_dir = self.ensure_output_dir()

        name, _ = os.path.splitext(file.filename)
        output_path = os.path.join(output_dir, f"{name}.docx")

        content = (await file.read()).decode("utf-8")

        doc = Document()
        doc.add_paragraph(content)
        doc.save(output_path)

        return output_path

    async def convert_docx_to_pdf(self, file):
        output_dir = self.ensure_output_dir()

        name, _ = os.path.splitext(file.filename)
        input_path = os.path.join(output_dir, file.filename)
        output_path = os.path.join(output_dir, f"{name}.pdf")

        with open(input_path, "wb") as f:
            f.write(await file.read())

        try:
            subprocess.run(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    input_path,
                    "--outdir",
                    output_dir,
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            raise Exception("Erro ao converter DOCX para PDF")


        return output_path

    async def convert_pdf_to_docx(self, file):
        output_dir = self.ensure_output_dir()

        name, _ = os.path.splitext(file.filename)

        input_path = os.path.join(output_dir, file.filename)
        output_path = os.path.join(output_dir, f"{name}.docx")

        with open(input_path, "wb") as f:
            f.write(await file.read())

        doc = Document()

        with pdfplumber.open(input_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    for line in text.splitlines():
                        doc.add_paragraph(line)
        
        doc.save(output_path)
        return output_path
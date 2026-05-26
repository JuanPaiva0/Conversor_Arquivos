from app.exceptions.custom_exceptions import ConversionError, InvalidFileExtensionError
from app.core.utils import ensure_output_dir
from app.core.validators import validate_extension
from reportlab.pdfgen import canvas
from docx import Document
import os
import pdfplumber
import subprocess

class DocumentService:
    async def convert_txt_to_pdf(self, file):
        validate_extension(file.filename, [".txt"])

        try:
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.pdf")

            content = (await file.read()).decode("utf-8")

            pdf = canvas.Canvas(output_path)
            pdf.drawString(100, 750, content)
            pdf.save()

            return output_path
        
        except InvalidFileExtensionError:
            raise
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter TXT para PDF: {str(e)}"
            ) from e

    async def convert_txt_to_docx(self, file):
        validate_extension(file.filename, [".txt"])

        try:
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.docx")

            content = (await file.read()).decode("utf-8")

            doc = Document()
            doc.add_paragraph(content)
            doc.save(output_path)

            return output_path
        
        except InvalidFileExtensionError:
            raise

        except Exception as e:
            raise ConversionError(
                f"Erro ao converter TXT para DOCX: {str(e)}"
            ) from e

    async def convert_docx_to_pdf(self, file):
        validate_extension(file.filename, [".docx"])
        
        try:
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            input_path = os.path.join(output_dir, file.filename)
            output_path = os.path.join(output_dir, f"{name}.pdf")

            with open(input_path, "wb") as f:
                f.write(await file.read())

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

            return {
                "output_path": output_path,
                "input_path": input_path,
            }
        
        except InvalidFileExtensionError:
            raise
        
        except subprocess.CalledProcessError as e:
            raise ConversionError(
                "Erro ao converter DOCX para PDF"
            ) from e
        
        except FileNotFoundError as e:
            raise ConversionError(
                "LibreOffice não encontrado no sistema"
            ) from e
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter DOCX para PDF: {str(e)}"
            ) from e

    async def convert_pdf_to_docx(self, file):
        validate_extension(file.filename, [".pdf"])

        try:
            output_dir = ensure_output_dir()

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
            return {
                "output_path": output_path,
                "input_path": input_path
            } 
        
        except InvalidFileExtensionError:
            raise

        except Exception as e:
            raise ConversionError(
                f"Erro ao converter PDF para DOCX: {str(e)}"
            ) from e

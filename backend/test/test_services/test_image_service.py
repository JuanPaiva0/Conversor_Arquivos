from fastapi import UploadFile
from starlette.datastructures import Headers
from app.services.image_service import ImageService
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
import pytest
import os

from app.exceptions.custom_exceptions import (
    InvalidFileExtensionError, 
    InvalidMimeTypeError,
    ConversionError
)

service = ImageService()

@pytest.fixture()
def png_file():
        image = Image.new("RGB", (100, 100), color="red")

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer

@pytest.fixture()
def jpg_file():
    image = Image.new("RGB", (100, 100), color="white")

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer

@pytest.fixture()
def pdf_file():
     buffer = BytesIO()

     pdf = canvas.Canvas(buffer)
     pdf.drawString(100, 750, "PDF de teste")
     pdf.save()

     buffer.seek(0)

     return buffer

class TestImageService:
    #TESTS FOR SERVICE convert_png_to_pdf
    @pytest.mark.asyncio
    async def test_png_to_pdf_success(self, png_file):
        png = png_file

        upload_file = UploadFile(
             filename="test.png",
             file=png,
             headers=Headers({
                 "content-type": "image/png"
             })
        )

        response = await service.convert_png_to_pdf(upload_file)

        assert response.endswith(".pdf")
        assert os.path.exists(response)

    @pytest.mark.asyncio
    async def test_png_to_pdf_conversion_error(self, png_file, mocker):
        png = png_file

        upload_file = UploadFile(
                filename="test.png",
                file=png,
                headers=Headers({
                    "content-type": "image/png"
                })
        )

        mocker.patch(
            "app.services.image_service.Image.open", 
            side_effect=Exception("Image Error")
        )

        with pytest.raises(ConversionError) as exc:
            await service.convert_png_to_pdf(upload_file)

        assert str(exc.value).startswith("Erro ao converter PNG para PDF: ")

    @pytest.mark.asyncio
    async def test_png_to_pdf_invalid_extension(self, png_file):
        png = png_file

        upload_file = UploadFile(
                filename="test.jpg",
                file=png,
                headers=Headers({
                    "content-type": "image/png"
                })
        )

        with pytest.raises(InvalidFileExtensionError) as exc:
             await service.convert_png_to_pdf(upload_file)

        assert str(exc.value) == (
            "Extensão inválida. Extensões permitidas: .png"
        )

    @pytest.mark.asyncio
    async def test_png_to_pdf_invalid_mime_type(self, png_file):
        png = png_file

        upload_file = UploadFile(
            filename="test.png",
            file=png,
            headers=Headers({
                "content-type": "image/jpeg"
            })
        )

        with pytest.raises(InvalidMimeTypeError) as exc:
            await service.convert_png_to_pdf(upload_file)

        assert str(exc.value) == (
            "Tipo MIME inválido. Tipos MIME permitidos: image/png"
        )

    #TESTS FOR SERVICE convert_pdf_to_png
    @pytest.mark.asyncio
    async def test_pdf_to_png_success(self, pdf_file):
        pdf = pdf_file

        upload_file = UploadFile(
            filename="test.pdf",
            file=pdf,
            headers=Headers({
                "content-type": "application/pdf"
            })
        )

        response = await service.convert_pdf_to_png(upload_file)

        assert response.endswith(".png")
        assert os.path.exists(response)

    @pytest.mark.asyncio
    async def test_pdf_to_png_conversion_error(self, pdf_file, mocker):
        pdf = pdf_file

        upload_file = UploadFile(
            filename="test.pdf",
            file=pdf,
            headers=Headers({
                "content-type": "application/pdf"
            })
        )

        mocker.patch(
            "app.services.image_service.convert_from_bytes",
            side_effect=Exception("PDF Conversion Error") 
        )

        with pytest.raises(ConversionError) as exc:
            await service.convert_pdf_to_png(upload_file)
        
        assert str(exc.value).startswith("Erro ao converter PDF para PNG: ")
    
    @pytest.mark.asyncio
    async def test_pdf_to_png_invalid_extension(self, pdf_file):
        pdf = pdf_file

        upload_file = UploadFile(
            filename="test.txt",
            file=pdf,
            headers=Headers({
                "content-type": "application/pdf"
            })
        )

        with pytest.raises(InvalidFileExtensionError) as exc:
            await service.convert_pdf_to_png(upload_file)

        assert str(exc.value) == (
            "Extensão inválida. Extensões permitidas: .pdf"
        )

    @pytest.mark.asyncio
    async def test_pdf_to_png_invalid_mime_type(self, pdf_file):
        pdf = pdf_file

        upload_file = UploadFile(
            filename="test.pdf",
            file=pdf,
            headers=Headers({
                "content-type": "text/plain"
            })
        )

        with pytest.raises(InvalidMimeTypeError) as exc:
            await service.convert_pdf_to_png(upload_file)

        assert str(exc.value) == (
            "Tipo MIME inválido. Tipos MIME permitidos: application/pdf"
        )
    
    #TESTS FOR SERVICE convert_jpg_to_png
    @pytest.mark.asyncio
    async def test_jpg_to_png_success(self, jpg_file):
        jpg = jpg_file

        upload_file = UploadFile(
            filename="test.jpg",
            file=jpg,
            headers=Headers({
                "content-type": "image/jpeg"
            })
        )

        response = await service.convert_jpg_to_png(upload_file)

        assert response.endswith(".png")
        assert os.path.exists(response)

    @pytest.mark.asyncio
    async def test_jpg_to_png_conversion_error(self, jpg_file, mocker):
        jpg = jpg_file

        upload_file = UploadFile(
            filename="test.jpg",
            file=jpg,
            headers=Headers({
                "content-type": "image/jpeg"
            })
        )

        mocker.patch(
            "app.services.image_service.Image.open", 
            side_effect=Exception("Image Error")
        )

        with pytest.raises(ConversionError) as exc:
            await service.convert_jpg_to_png(upload_file)

        assert str(exc.value).startswith("Erro ao converter JPG para PNG: ")

    @pytest.mark.asyncio
    async def test_jpg_to_png_invalid_extension(self, jpg_file):
        jpg = jpg_file

        upload_file = UploadFile(
            filename="test.png",
            file=jpg,
            headers=Headers({
                "content-type": "image/jpeg"
            })
        )

        with pytest.raises(InvalidFileExtensionError) as exc:
             await service.convert_jpg_to_png(upload_file)

        assert str(exc.value) == (
            "Extensão inválida. Extensões permitidas: .jpg, .jpeg"
        )

    @pytest.mark.asyncio
    async def test_jpg_to_png_invalid_mime_type(self, jpg_file):
        jpg = jpg_file

        upload_file = UploadFile(
            filename="test.jpg",
            file=jpg,
            headers=Headers({
                "content-type": "image/png"
            })
        )

        with pytest.raises(InvalidMimeTypeError) as exc:
            await service.convert_jpg_to_png(upload_file)

        assert str(exc.value) == (
            "Tipo MIME inválido. Tipos MIME permitidos: image/jpeg"
        )
        
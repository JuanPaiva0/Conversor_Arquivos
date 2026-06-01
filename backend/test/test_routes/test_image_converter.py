from fastapi.testclient import TestClient
from app.main import app

client = TestClient(
    app,
    raise_server_exceptions=False
)

class TestImageConverter:
    #TESTS FOR ROUTE /image/png-to-pdf
    def test_png_to_pdf(self, mocker, tmp_path):
        fake_file = tmp_path / "output.pdf"
        fake_file.write_bytes(b"fake pdf content")

        mock_convert = mocker.patch(
            "app.routes.image_converter.service.convert_png_to_pdf",
            return_value=str(fake_file)
        )

        response = client.post(
            "/images/png-to-pdf",
            files={
                "file": (
                    "test.png",
                    b"fake png content",
                    "image/png"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()
        
        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.png"

    def test_png_to_pdf_invalid_file(self):
        response = client.post(
            "/images/png-to-pdf",
            files={
                "file": (
                    "test.txt",
                    b"invalid content",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .png'}

    def test_png_to_pdf_without_file(self):
        response = client.post("/images/png-to-pdf")

        assert response.status_code == 422

    def test_png_to_pdf_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.image_converter.service.convert_png_to_pdf",
            side_effect=Exception("Erro ao converter arquivo PNG para PDF")
        )

        response = client.post(
            "/images/png-to-pdf",
            files={
                "file": (
                    "test.png",
                    b"fake png content",
                    "image/png"
                )
            }
        )

        assert response.status_code == 500

    #TESTS FOR ROUTE /image/pdf-to-png
    def test_pdf_to_png(self, mocker, tmp_path):
        fake_file = tmp_path / "output.png"
        fake_file.write_bytes(b"fake png content")

        mock_convert = mocker.patch(
            "app.routes.image_converter.service.convert_pdf_to_png",
            return_value=str(fake_file)
        )

        response = client.post(
            "/images/pdf-to-png",
            files={
                "file": (
                    "test.pdf",
                    b"fake pdf content",
                    "application/pdf"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()

        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.pdf"

    def test_pdf_to_png_invalid_file(self):
        response = client.post(
            "/images/pdf-to-png",
            files={
                "file": (
                    "test.txt",
                    b"invalid content",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .pdf'}

    def test_pdf_to_png_without_file(self):
        response = client.post("/images/pdf-to-png")

        assert response.status_code == 422

    def test_pdf_to_png_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.image_converter.service.convert_pdf_to_png",
            side_effect=Exception("Erro ao converter arquivo PDF para PNG")
        )

        response = client.post(
            "/images/pdf-to-png",
            files={
                "file": (
                    "test.pdf",
                    b"fake pdf content",
                    "application/pdf"
                )
            }
        )

        assert response.status_code == 500

    #TESTS FOR ROUTE /image/jpg-to-png
    def test_jpg_to_png(self, mocker, tmp_path):
        fake_file = tmp_path / "output.png"
        fake_file.write_bytes(b"fake png content")

        mock_convert = mocker.patch(
            "app.routes.image_converter.service.convert_jpg_to_png",
            return_value=str(fake_file)
        )

        response = client.post(
            "/images/jpg-to-png",
            files={
                "file": (
                    "test.jpg",
                    b"fake jpg content",
                    "image/jpeg"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()

        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.jpg"

    def test_jpg_to_png_invalid_file(self):
        response = client.post(
            "/images/jpg-to-png",
            files={
                "file": (
                    "test.txt",
                    b"invalid content",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .jpg, .jpeg'}

    def test_jpg_to_png_without_file(self):
        response = client.post("/images/jpg-to-png")

        assert response.status_code == 422

    def test_jpg_to_png_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.image_converter.service.convert_jpg_to_png",
            side_effect=Exception("Erro ao converter arquivo JPG para PNG")
        )

        response = client.post(
            "/images/jpg-to-png",
            files={
                "file": (
                    "test.jpg",
                    b"fake jpg content",
                    "image/jpeg"
                )
            }
        )

        assert response.status_code == 500
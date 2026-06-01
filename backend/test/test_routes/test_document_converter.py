from fastapi.testclient import TestClient
from app.main import app

client = TestClient(
    app,
    raise_server_exceptions=False
)

class TestDocumentConverter:
    #TESTS FOR ROUTE /document/txt-to-pdf
    def test_txt_to_pdf(self, mocker, tmp_path):
        fake_file = tmp_path / "output.pdf"
        fake_file.write_bytes(b"fake pdf content")

        mock_convert = mocker.patch(
            "app.routes.document_converter.service.convert_txt_to_pdf",
            return_value=str(fake_file)
        )

        response = client.post(
            "/document/txt-to-pdf",
            files={
                "file": (
                    "test.txt",
                    b"Hello, this is a test.",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()
        
        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.txt"
    
    def test_txt_to_pdf_invalid_file(self):
        response = client.post(
            "/document/txt-to-pdf",
            files={
                "file": (
                    "test.pdf",
                    b"invalid content",
                    "application/pdf"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .txt'}

    def test_txt_to_pdf_without_file(self):
        response = client.post("/document/txt-to-pdf")

        assert response.status_code == 422
    
    def test_txt_to_pdf_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.document_converter.service.convert_txt_to_pdf",
            side_effect=Exception("Erro ao converter arquivo TXT para PDF")
        )

        response = client.post(
            "/document/txt-to-pdf",
            files={
                "file": (
                    "test.txt",
                    b"Hello, this is a test.",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 500

    #TESTS FOR ROUTE /document/txt-to-docx
    def test_txt_to_docx(self, mocker, tmp_path):
        fake_file = tmp_path / "output.docx"
        fake_file.write_bytes(b"fake docx content")

        mock_convert = mocker.patch(
            "app.routes.document_converter.service.convert_txt_to_docx",
            return_value=str(fake_file)
        )

        response = client.post(
            "/document/txt-to-docx",
            files={
                "file": (
                    "test.txt",
                    b"Hello, this is a test.",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()
        
        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.txt"

    def test_txt_to_docx_invalid_file(self):
        response = client.post(
            "/document/txt-to-docx",
            files={
                "file": (
                    "test.docx",
                    b"invalid content",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .txt'}

    def test_txt_to_docx_without_file(self):
        response = client.post("/document/txt-to-docx")

        assert response.status_code == 422

    def test_txt_to_docx_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.document_converter.service.convert_txt_to_docx",
            side_effect=Exception("Erro ao converter arquivo TXT para DOCX")
        )

        response = client.post(
            "/document/txt-to-docx",
            files={
                "file": (
                    "test.txt",
                    b"Hello, this is a test.",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 500

    #TESTS FOR ROUTE /document/docx-to-pdf
    def test_docx_to_pdf(self, mocker, tmp_path):
        fake_file = tmp_path / "output.pdf"
        fake_file.write_bytes(b"fake pdf content")

        mock_convert = mocker.patch(
            "app.routes.document_converter.service.convert_docx_to_pdf",
            return_value={
                'output_path': str(fake_file),
                'input_path': str(tmp_path / "input.docx")
            }
        )

        response = client.post(
            "/document/docx-to-pdf",
            files={
                "file": (
                    "test.docx",
                    b"Hello, this is a test.",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()
        
        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.docx"

    def test_docx_to_pdf_invalid_file(self):
        response = client.post(
            "/document/docx-to-pdf",
            files={
                "file": (
                    "test.txt",
                    b"invalid content",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .docx'}

    def test_docx_to_pdf_without_file(self):
        response = client.post("/document/docx-to-pdf")

        assert response.status_code == 422

    def test_docx_to_pdf_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.document_converter.service.convert_docx_to_pdf",
            side_effect=Exception("Erro ao converter arquivo DOCX para PDF")
        )

        response = client.post(
            "/document/docx-to-pdf",
            files={
                "file": (
                    "test.docx",
                    b"Hello, this is a test.",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            }
        )

        assert response.status_code == 500

    #TESTS FOR ROUTE /document/pdf-to-docx
    def test_pdf_to_docx(self, mocker, tmp_path):
        fake_file = tmp_path / "output.docx"
        fake_file.write_bytes(b"fake docx content")

        mock_convert = mocker.patch(
            "app.routes.document_converter.service.convert_pdf_to_docx",
            return_value={
                'output_path': str(fake_file),
                'input_path': str(tmp_path / "input.pdf")
            }
        )

        response = client.post(
            "/document/pdf-to-docx",
            files={
                "file": (
                    "test.pdf",
                    b"Hello, this is a test.",
                    "application/pdf"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()
        
        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.pdf"

    def test_pdf_to_docx_invalid_file(self):
        response = client.post(
            "/document/pdf-to-docx",
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

    def test_pdf_to_docx_without_file(self):
        response = client.post("/document/pdf-to-docx")

        assert response.status_code == 422

    def test_pdf_to_docx_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.document_converter.service.convert_pdf_to_docx",
            side_effect=Exception("Erro ao converter arquivo PDF para DOCX")
        )

        response = client.post(
            "/document/pdf-to-docx",
            files={
                "file": (
                    "test.pdf",
                    b"Hello, this is a test.",
                    "application/pdf"
                )
            }
        )

        assert response.status_code == 500
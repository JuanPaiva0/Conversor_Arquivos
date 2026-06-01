from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(
    app,
    raise_server_exceptions=False
)

class TestSpreadsheetConverter:
    #TESTS FOR ROUTE /spreadsheet/csv-to-xlsx
    def test_csv_to_xlsx(self, mocker, tmp_path):
        fake_file = tmp_path / "output.xlsx"
        fake_file.write_bytes(b"fake xlsx content")

        mock_convert = mocker.patch(
            "app.routes.spreadsheet_converter.service.convert_csv_to_xlsx",
            return_value=str(fake_file)
        )

        response = client.post(
            "/spreadsheet/csv-to-xlsx",
            files={
                "file": (
                    "test.csv",
                    b"nome,idade\nAlice,30\nBob,25",
                    "text/csv"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()
        
        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.csv"

    def test_csv_to_xlsx_invalid_file(self):
        response = client.post(
            "/spreadsheet/csv-to-xlsx",
            files={
                "file": (
                    "test.txt",
                    b"invalid content",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .csv'}

    def test_csv_to_xlsx_without_file(self):
        response = client.post("/spreadsheet/csv-to-xlsx")

        assert response.status_code == 422

    def test_csv_to_xlsx_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.spreadsheet_converter.service.convert_csv_to_xlsx",
            side_effect=Exception("Erro ao converter arquivo CSV para XLSX")
        )

        response = client.post(
            "/spreadsheet/csv-to-xlsx",
            files={
                "file": (
                    "test.csv",
                    b"nome,idade\nAlice,30\nBob,25",
                    "text/csv"
                )
            }
        )

        assert response.status_code == 500

    #TESTS FOR ROUTE /spreadsheet/xlsx-to-csv
    def test_xlsx_to_csv(self, mocker, tmp_path):
        fake_file = tmp_path / "output.csv"
        fake_file.write_bytes(b"fake csv content")

        mock_convert = mocker.patch(
            "app.routes.spreadsheet_converter.service.convert_xlsx_to_csv",
            return_value=str(fake_file)
        )

        response = client.post(
            "/spreadsheet/xlsx-to-csv",
            files={
                "file": (
                    "test.xlsx",
                    b"fake xlsx content",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }
        )

        assert response.status_code == 200
        mock_convert.assert_called_once()
        
        args = mock_convert.call_args[0]
        uploaded_file = args[0]

        assert uploaded_file.filename == "test.xlsx"

    def test_xlsx_to_csv_invalid_file(self):
        response = client.post(
            "/spreadsheet/xlsx-to-csv",
            files={
                "file": (
                    "test.txt",
                    b"invalid content",
                    "text/plain"
                )
            }
        )

        assert response.status_code == 400
        assert response.json() == {'detail': 'Extensão inválida. Extensões permitidas: .xlsx'}

    def test_xlsx_to_csv_without_file(self):
        response = client.post("/spreadsheet/xlsx-to-csv")

        assert response.status_code == 422

    def test_xlsx_to_csv_conversion_error(self, mocker):
        mocker.patch(
            "app.routes.spreadsheet_converter.service.convert_xlsx_to_csv",
            side_effect=Exception("Erro ao converter arquivo XLSX para CSV")
        )

        response = client.post(
            "/spreadsheet/xlsx-to-csv",
            files={
                "file": (
                    "test.xlsx",
                    b"fake xlsx content",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }
        )

        assert response.status_code == 500
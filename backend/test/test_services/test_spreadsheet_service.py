from fastapi import UploadFile
from starlette.datastructures import Headers
from io import BytesIO
from app.services.spreadsheet_service import SpreadsheetService
from io import BytesIO
import pandas as pd
import pytest
import os

from app.exceptions.custom_exceptions import (
    InvalidFileExtensionError, 
    InvalidMimeTypeError,
    ConversionError
)

service = SpreadsheetService()

@pytest.fixture()
def csv_file():
    csv_content = "name,age\nAlice,30\nBob,25"
    return BytesIO(csv_content.encode("utf-8"))
    
@pytest.fixture()
def xlsx_file():
    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [30, 25]
    })

    buffer = BytesIO()
    dataframe.to_excel(buffer, index=False)
    buffer.seek(0)

    return buffer

class TestSpreadsheetService:
    #TESTS FOR SERVICE convert_csv_to_xlsx
    @pytest.mark.asyncio
    async def test_csv_to_xlsx_success(self, csv_file):
        csv_content = csv_file
        
        upload_file = UploadFile(
            filename="test.csv",
            file=csv_content,
            headers=Headers({
                "content-type": "text/csv"
            })
        )

        response = await service.convert_csv_to_xlsx(upload_file)
        spreadsheet = pd.read_excel(response)

        assert response.endswith(".xlsx")
        assert len(spreadsheet) == 2
        assert list(spreadsheet.columns) == ["name", "age"]
        
    @pytest.mark.asyncio
    async def test_csv_to_xlsx_invalid_extension(self, csv_file):
        csv_content = csv_file

        upload_file = UploadFile(
            filename="test.txt",
            file=csv_content,
            headers=Headers({
                "content-type": "text/plain"
            })
        )

        with pytest.raises(InvalidFileExtensionError) as exc:
            await service.convert_csv_to_xlsx(upload_file)

        assert str(exc.value) == (
            "Extensão inválida. Extensões permitidas: .csv"
        )

    @pytest.mark.asyncio
    async def test_csv_to_xlsx_invalid_mime_type(self, csv_file):
        csv_content = csv_file

        upload_file = UploadFile(
            filename="test.csv",
            file=csv_content,
            headers=Headers({
                "content-type": "text/plain"
            })
        )

        with pytest.raises(InvalidMimeTypeError) as exc:
            await service.convert_csv_to_xlsx(upload_file)

        assert str(exc.value) == (
            "Tipo MIME inválido. Tipos MIME permitidos: text/csv, application/csv, application/vnd.ms-excel"
        )

    @pytest.mark.asyncio
    async def test_csv_to_xlsx_pandas_error(self, csv_file, mocker):
        csv_content = csv_file

        upload_file = UploadFile(
            filename="test.csv",
            file=csv_content,
            headers=Headers({
                "content-type": "text/csv"
            })
        )

        mocker.patch(
            "pandas.read_csv",
            side_effect=Exception("Erro Pandas")
        )

        with pytest.raises(ConversionError) as exc:
            await service.convert_csv_to_xlsx(upload_file)
        
        assert str(exc.value) == (
            "Erro ao converter CSV para XLSX: Erro Pandas"
        )

    #TESTS FOR SERVICE convert_xlsx_to_csv
    @pytest.mark.asyncio
    async def test_xlsx_to_csv_success(self, xlsx_file):
        xlsx_content = xlsx_file

        upload_file = UploadFile(
            filename="test.xlsx",
            file=xlsx_content,
            headers=Headers({
                "content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            })
        )

        response = await service.convert_xlsx_to_csv(upload_file)
        spreadsheet = pd.read_csv(response)
        
        assert response.endswith(".csv")
        assert len(spreadsheet) == 2
        assert list(spreadsheet.columns) == ["name", "age"]

    @pytest.mark.asyncio
    async def test_xlsx_to_csv_invalid_extension(self, xlsx_file):
        xlsx_content = xlsx_file

        upload_file = UploadFile(
            filename="test.txt",
            file=xlsx_content,
            headers=Headers({
                "content-type": "text/plain"
            })
        )

        with pytest.raises(InvalidFileExtensionError) as exc:
            await service.convert_xlsx_to_csv(upload_file)

        assert str(exc.value) == (
            "Extensão inválida. Extensões permitidas: .xlsx"
        )

    @pytest.mark.asyncio
    async def test_xlsx_to_csv_invalid_mime_type(self, xlsx_file):
        xlsx_content = xlsx_file

        upload_file = UploadFile(
            filename="test.xlsx",
            file=xlsx_content,
            headers=Headers({
                "content-type": "text/plain"
            })
        )

        with pytest.raises(InvalidMimeTypeError) as exc:
            await service.convert_xlsx_to_csv(upload_file)

        assert str(exc.value) == (
            "Tipo MIME inválido. Tipos MIME permitidos: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/zip"
        )

    @pytest.mark.asyncio
    async def test_xlsx_to_csv_pandas_error(self, xlsx_file, mocker):
        xlsx_content = xlsx_file

        upload_file = UploadFile(
            filename="test.xlsx",
            file=xlsx_content,
            headers=Headers({
                "content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            })
        )

        mocker.patch(
            "pandas.read_excel",
            side_effect=Exception("Erro Pandas")
        )

        with pytest.raises(ConversionError) as exc:
            await service.convert_xlsx_to_csv(upload_file)
        
        assert str(exc.value) == (
            "Erro ao converter XLSX para CSV: Erro Pandas"
        )

from app.exceptions.custom_exceptions import ConversionError, InvalidFileExtensionError
from app.core.utils import ensure_output_dir
from app.core.validators import validate_extension
import pandas as pd
import os

class SpreadsheetService:
    async def convert_csv_to_xlsx(self, file):
        try:
            validate_extension(file.filename, [".csv"])
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.xlsx")

            spreadsheet = pd.read_csv(file.file)
            spreadsheet.to_excel(output_path, index=False)

            return output_path

        except InvalidFileExtensionError:
            raise
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter CSV para XLSX: {str(e)}"
            ) from e
        
    async def convert_xlsx_to_csv(self, file):
        try:
            validate_extension(file.filename, [".xlsx"])
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.csv")

            spreadsheet = pd.read_excel(file.file)
            spreadsheet.to_csv(output_path, index=False)

            return output_path

        except InvalidFileExtensionError:
            raise
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter XLSX para CSV: {str(e)}"
            ) from e

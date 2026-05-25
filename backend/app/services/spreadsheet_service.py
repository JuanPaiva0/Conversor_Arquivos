from app.exceptions.custom_exceptions import ConversionError
import pandas as pd
import os

class SpreadsheetService:
    def ensure_output_dir(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        return OUTPUT_DIR

    async def convert_csv_to_xlsx(self, file):
        try:
            output_dir = self.ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.xlsx")

            spreadsheet = pd.read_csv(file.file)
            spreadsheet.to_excel(output_path, index=False)

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter CSV para XLSX: {str(e)}"
            ) from e
        
    async def convert_xlsx_to_csv(self, file):
        try:
            output_dir = self.ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.csv")

            spreadsheet = pd.read_excel(file.file)
            spreadsheet.to_csv(output_path, index=False)

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter XLSX para CSV: {str(e)}"
            ) from e

# File Converter API

A REST API built with **FastAPI** that converts files between common formats — documents, images, and spreadsheets. Designed with a focus on input validation and security: every uploaded file is verified by extension, declared MIME type, and actual file content (using `libmagic`), preventing disguised file attacks.

---

## Features

| Category | Conversions |
|---|---|
| Documents | TXT → PDF, TXT → DOCX, DOCX → PDF, PDF → DOCX |
| Images | PNG → PDF, PDF → PNG, JPG → PNG |
| Spreadsheets | CSV → XLSX, XLSX → CSV |

---

## Tech Stack

- **Runtime** — Python 3.12
- **Framework** — FastAPI + Uvicorn
- **Validation** — `python-magic` (libmagic bindings for real content inspection)
- **Document processing** — `python-docx`, `reportlab`, `pdfplumber`, LibreOffice (headless)
- **Image processing** — Pillow, `pdf2image` (poppler)
- **Spreadsheet processing** — pandas, openpyxl
- **Dependency management** — Poetry
- **Testing** — pytest, pytest-asyncio, pytest-cov, pytest-mock
- **Containerization** — Docker + Docker Compose

---

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── utils.py            # Output dir management and file cleanup helpers
│   │   └── validators.py       # File validation (extension, MIME, size, real content)
│   ├── exceptions/
│   │   ├── custom_exceptions.py  # Typed exceptions with HTTP status codes
│   │   └── handlers.py           # Global exception handler registration
│   ├── routes/
│   │   ├── document_converter.py
│   │   ├── image_converter.py
│   │   └── spreadsheet_converter.py
│   ├── services/
│   │   ├── document_service.py
│   │   ├── image_service.py
│   │   └── spreadsheet_service.py
│   └── main.py
├── test/
│   ├── test_routes/
│   │   ├── test_document_converter.py
│   │   ├── test_image_converter.py
│   │   └── test_spreadsheet_converter.py
│   └── test_services/
│       ├── test_document_service.py
│       ├── test_image_service.py
│       └── test_spreadsheet_service.py
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## Prerequisites

### Without Docker

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)
- LibreOffice (required for DOCX → PDF conversion)
- Poppler (required for PDF → PNG conversion)

```bash
# Ubuntu / Debian
sudo apt-get install libreoffice poppler-utils libmagic1

# macOS
brew install libreoffice poppler libmagic
```

### With Docker

- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/install/) v2+

---

## Setup & Installation

### Using Docker (recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/conversor_arquivos.git
cd conversor_arquivos/backend

# Start the API
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Manual setup

```bash
cd conversor_arquivos/backend

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Start the development server
uvicorn app.main:app --reload
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | `http://localhost:5173` |

Create a `.env` file in the `backend/` directory:

```env
ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend-domain.com
```

---

## API Documentation

Once the server is running, interactive documentation is available at:

- **Swagger UI** — `http://localhost:8000/docs`
- **ReDoc** — `http://localhost:8000/redoc`

### Endpoints overview

All endpoints accept `multipart/form-data` with a single `file` field and return the converted file as a binary download.

```
POST /document/txt-to-pdf
POST /document/txt-to-docx
POST /document/docx-to-pdf
POST /document/pdf-to-docx

POST /images/png-to-pdf
POST /images/pdf-to-png
POST /images/jpg-to-png

POST /spreadsheet/csv-to-xlsx
POST /spreadsheet/xlsx-to-csv
```

### Example request

```bash
curl -X POST "http://localhost:8000/document/txt-to-pdf" \
  -F "file=@document.txt" \
  --output converted.pdf
```

### Error responses

| Status | Meaning |
|---|---|
| `400` | Invalid file extension or MIME type mismatch |
| `413` | File exceeds the 10 MB size limit |
| `500` | Conversion failed |

---

## Security

Uploaded files go through a four-layer validation pipeline before any processing occurs:

1. **Filename check** — rejects requests with missing filenames
2. **Extension validation** — verifies the file extension matches the expected format
3. **File size limit** — rejects files larger than 10 MB
4. **Declared MIME type** — checks the `Content-Type` header
5. **Real content inspection** — reads the first 2 KB of the file using `libmagic` to verify the actual format, preventing extension-spoofing attacks

---

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=app --cov-report=term-missing

# Run a specific test file
poetry run pytest test/test_routes/test_document_converter.py -v
```

---

## File Size Limit

The API enforces a **10 MB** maximum per upload. This limit is defined in `app/core/validators.py` and can be adjusted by changing the `MAX_FILE_SIZE` constant.

---

## License

This project is licensed under the MIT License.
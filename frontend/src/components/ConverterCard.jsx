import { useState, useEffect } from "react";
import { api } from "../services/api";

export default function ConverterCard({ category}) {
    const [file, setFile] = useState(null)
    const [conversionType, setConversionType] = useState("png-to-pdf")

    const conversionOptions = {
        images: [
            { value: "png-to-pdf", label: "PNG → PDF" },
            { value: "pdf-to-png", label: "PDF → PNG" },
            { value: "jpg-to-png", label: "JPG → PNG" },
        ],

        documents: [
            { value: "txt-to-pdf", label: "TXT → PDF" },
            { value: "txt-to-docx", label: "TXT → DOCX" },
            { value: "docx-to-pdf", label: "DOCX → PDF" },
            { value: "pdf-to-docx", label: "PDF → DOCX" },
        ],

        spreadsheets: [
            { value: "csv-to-xlsx", label: "CSV → XLSX" },
            { value: "xlsx-to-csv", label: "XLSX → CSV" },
        ],
    }

    useEffect(() => {
        setConversionType(conversionOptions[category][0].value);
    }, [category])

    const handleConvert = async () => {
        if (!file) {
            alert("Selecione um arquivo!")
            return;
        }

        try {
            const formData = new FormData();
            formData.append("file", file);

            const routeMap = {
                images: "images",
                documents: "document",
                spreadsheets: "spreadsheet"
            }

            const response = await api.post(
                `/${routeMap[category]}/${conversionType}`,
                formData,
                {
                    responseType: "blob"
                }
            );

            const url = window.URL.createObjectURL(response.data);

            const link = document.createElement("a");
            link.href = url;

            const name = file.name.split(".")[0];
            const extension = conversionType.split("-").pop();
            link.download = `${name}.${extension}`
            document.body.appendChild(link)

            link.click()

            link.remove()
            window.URL.revokeObjectURL(url)
        } catch (error) {
            console.error(error);
            alert("Erro na conversão")
        }
    };

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 rounded-2xl shadow-md border">
            <h2 className="text-xl font-bold mb-4">
                Converter Arquivo
            </h2>

            <input
                type="file"
                className="mb-4 w-full"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <select
                className="w-full border rounded-lg p-2 mb-4"
                value={conversionType}
                onChange={(e) => setConversionType(e.target.value)}
            >
                {conversionOptions[category].map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>

            <button 
                className="bg-green-500 max-w-40 rounded-lg p-3 shadow"
                onClick={handleConvert}
            >
                CONVERTER
            </button>
        </div>
    );
}
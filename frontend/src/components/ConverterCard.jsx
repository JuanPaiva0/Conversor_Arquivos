import { useState, useEffect, useRef } from "react";
import { toast } from "sonner";
import { api } from "../services/api";
import uploadIcon from "../assets/icons/upload-solid-full.svg"

export default function ConverterCard({ category}) {
    const [file, setFile] = useState(null);
    const fileInputRef = useRef(null);

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

    const [conversionType, setConversionType] = useState(
        conversionOptions[category][0].value
    );

    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setFile(null);

        if (fileInputRef.current) {
          fileInputRef.current.value = "";
        }

        setConversionType(
          conversionOptions[category][0].value
        );
    }, [category])

    const handleConvert = async () => {
        if (!file) {
            toast.warning("Selecione um arquivo!")
            return;
        }

        setLoading(true);

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

            toast.success("Arquivo convertido com sucesso!")

            setFile(null);

            if (fileInputRef.current) {
              fileInputRef.current.value = "";
            }
        } catch (error) {
            let message = "Erro na conversão"

            if (error.response?.data instanceof Blob) {
              const text = await error.response.data.text();

              try {
                const json = JSON.parse(text);
                message = json.detail || message;
              } catch {
                message = text;
              }
            }
            toast.error(message)
        } finally{
          setLoading(false)
        }
    };

    return (
    <main className="flex justify-center px-4 mt-6">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-xl p-6">
        <div className="flex flex-col gap-4">
          <select
            value={conversionType}
            onChange={(e) => setConversionType(e.target.value)}
            className="
              w-full
              p-4
              rounded-2xl
              bg-gray-100
              font-semibold
              text-center
              outline-none
              border-none
              appearance-none
              cursor-pointer
            "
          >
            {conversionOptions[category].map((option) => (
              <option
                key={option.value}
                value={option.value}
              >
                {option.label}
              </option>
            ))}
          </select>

          <label
            className="
              border-2 border-dashed border-gray-400
              rounded-2xl
              h-56
              flex flex-col items-center justify-center
              cursor-pointer
              hover:bg-gray-50
              transition
            "
          >

            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <img
              src={uploadIcon}
              alt="Upload"
              className="w-10 h-10 mb-4"
            />

            <span className="font-semibold">
              {file ? file.name : "Upload File"}
            </span>

          </label>

          <button
            onClick={handleConvert}
            disabled={loading}
            className="
              bg-green-500
              hover:bg-green-600
              transition
              text-white
              font-bold
              rounded-2xl
              py-4
              mt-2
              shadow-md

              disabled:bg-green-700
              disabled:cursor-not-allowed
              disabled:opacity-70
            "
          >
            {loading ? "CONVERTENDO..." : "CONVERTER"}
          </button>
        </div>
      </div>
    </main>
  );
}
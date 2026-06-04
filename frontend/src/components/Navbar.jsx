import imageIcon from "../assets/icons/image-solid-full.svg"
import fileIcon from "../assets/icons/file-solid-full.svg"
import tableIcon from "../assets/icons/table-solid-full.svg"

export default function Navbar({
    activeSection,
    setActiveSection,
}) {
  const categories = [
    {
      value: "images",
      label: "Imagens",
      icon: imageIcon,
    },
    {
      value: "documents",
      label: "Documentos",
      icon: fileIcon,
    },
    {
      value: "spreadsheets",
      label: "Planilhas",
      icon: tableIcon,
    }
  ];

  return (
    <header className="w-full flex justify-center px-4">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-xl p-6">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold">
            Conversor de Arquivos
          </h1>

          <p className="text-gray-500 mt-2">
            Converta diversos tipos de arquivos em um único lugar
          </p>
        </div>

        <nav className="bg-gray-200 rounded-2xl p-3 flex gap-4 justify-between">
          {categories.map((category) => (
            <button
              key={category.value}
              onClick={() => setActiveSection(category.value)}
              className={`
                flex items-center justify-center gap-2 cursor-pointer
                w-full py-3 rounded-xl font-bold
                transition-all duration-300

                ${
                  activeSection === category.value
                    ? "bg-white shadow-md -translate-y-1"
                    : "hover:-translate-y-1"
                }
              `}
            >
              <img
                src={category.icon}
                alt={category.label}
                className="w-6 h-6"
              />

              {category.label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}
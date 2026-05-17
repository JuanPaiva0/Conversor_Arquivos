export default function Navbar({
    activeSection,
    setActiveSection,
}) {
    return (
        <nav className="w-full p-1 shadow-md">
            <div className="mx-auto flex max-w-6xl justify-center">
                <h1 className="text-3xl font-extrabold">Conversor de Arquivos</h1>
            </div>

            <div className="p-2">
                <ul className="flex justify-evenly w-full">
                <li
                  className="cursor-pointer"
                  onClick={() => setActiveSection("images")}
                >
                  Imagens
                </li>

                <li 
                  className="cursor-pointer"
                  onClick={() => setActiveSection("documents")}
                >
                  Documentos
                </li>

                <li
                  className="cursor-pointer"
                  onClick={() => setActiveSection("spreadsheets")}
                >
                  Planilhas
                </li>
                </ul>
            </div>
        </nav>
    );
}
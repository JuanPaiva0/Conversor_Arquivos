import { useState } from "react";
import { Toaster } from "sonner";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";

function App() {
  const [activeSection, setActiveSection] = useState("images")

  return (
    <div className="bg-gray-200 min-h-screen flex items-center justify-center">
      <div className="w-full">
        <Toaster richColors position="top-center" />

        <Navbar
          activeSection={activeSection}
          setActiveSection={setActiveSection}
        />

        <Home activeSection={activeSection} />
      </div>
    </div>
  );
}

export default App;
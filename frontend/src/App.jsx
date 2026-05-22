import { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";

function App() {
  const [activeSection, setActiveSection] = useState("images")

  return (
    <div className="min-h-screen bg-gray-200">

      <Navbar
        activeSection={activeSection}
        setActiveSection={setActiveSection}
      />

      <Home activeSection={activeSection} />

    </div>
  );
}

export default App;
import { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";

function App() {
  const [activeSection, setActiveSection] = useState("images")

  return (
    <>
      <Navbar
        activeSection={activeSection}
        setActiveSection={setActiveSection}
      />

      <Home activeSection={activeSection} />
    </>
  );
}

export default App;
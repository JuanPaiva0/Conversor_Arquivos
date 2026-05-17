import ConverterCard from "../components/ConverterCard";

export default function Home({ activeSection }) {
    return (
       <main>
          <ConverterCard category={activeSection} />
       </main>
    );
}
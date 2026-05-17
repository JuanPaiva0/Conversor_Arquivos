import { useState } from "react";

export default function FileUpload() {
    cont [file, setFile] = useState(null);

    return (
        <div>
            <input 
                type="text"
                onChange={(e) => setFile(e.target.files[0])}
            />
        </div>
    )
}
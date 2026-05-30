import { useState } from "react";

export default function EnrichForm({
  onSubmit,
  loading
}) {

  const [url, setUrl] = useState("");

  const handleSubmit = () => {

    if (!url.trim()) return;

    onSubmit(url);
  };

  return (
    <div>

      <h2>Enrich Company</h2>

      <input
        type="text"
        placeholder="https://company.com"
        value={url}
        onChange={(e)=>setUrl(e.target.value)}
        style={{
          width:"400px",
          padding:"10px"
        }}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Processing..." : "Enrich"}
      </button>

    </div>
  );
}
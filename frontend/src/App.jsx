import { useState } from "react";
import axios from "axios";

import EnrichForm from "./components/EnrichForm";
import ResultsTable from "./components/ResultsTable";

function App() {

  const [loading,setLoading] = useState(false);

  const [result,setResult] = useState(null);

  const [allResults,setAllResults] = useState([]);

  const API_URL = "https://prospect-research-agent-wtzj.onrender.com";

  const enrichCompany = async (url) => {

    try {

      setLoading(true);

      const response = await axios.post(
        `${API_URL}/enrich`,
        { url }
      );

      setResult(response.data);

    } catch(error) {

      console.log(error);

    } finally {

      setLoading(false);
    }
  };

  const fetchResults = async () => {

    try {

      const response = await axios.get(
        `${API_URL}/results`
      );

      setAllResults(response.data);

    } catch(error) {

      console.log(error);
    }
  };

  return (
    <div style={{padding:"30px"}}>

      <h1>
        Prospect Research Agent
      </h1>

      <EnrichForm
        onSubmit={enrichCompany}
        loading={loading}
      />

      <br/>

      <button onClick={fetchResults}>
        Show All Results
      </button>

      {result && (
        <>
          <h2>Latest Result</h2>

          <pre>
            {JSON.stringify(
              result,
              null,
              2
            )}
          </pre>
        </>
      )}

      <ResultsTable
        results={allResults}
      />

    </div>
  );
}

export default App;
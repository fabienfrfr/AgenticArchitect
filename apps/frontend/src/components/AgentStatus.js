import React, { useState } from 'react';
import axios from 'axios';

export default function AgentStatus() {
  const [report, setReport] = useState(null);
  const analyze = async () => {
    const res = await axios.post('http://localhost:8000/analyze_cdc', { cdc_text: "Test CDC" });
    setReport(res.data);
  };
  return <div><button onClick={analyze}>Analyze</button><pre>{JSON.stringify(report, null, 2)}</pre></div>;
}

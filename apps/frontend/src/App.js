import React, { useState, useEffect } from 'react';
import axios from 'axios';
import mermaid from 'mermaid';

// SOLID: API Service isolated from UI
const ArchitectureAPI = {
  processProject: async (requirements) => {
    const response = await axios.post('http://localhost:8000/process_project', { requirements });
    return response.data;
  }
};

// Component for Mermaid rendering
const MermaidViewer = ({ chart }) => {
  useEffect(() => {
    if (chart) {
      mermaid.contentLoaded();
    }
  }, [chart]);

  if (!chart) return null;

  return (
    <div className="mermaid-container bg-gray-100 p-4 rounded-lg mt-4">
      <div className="mermaid">{chart}</div>
    </div>
  );
};

// Main Dashboard Component
export default function AgenticArchitectDashboard() {
  const [requirements, setRequirements] = useState('');
  const [status, setStatus] = useState('idle'); // idle | processing | completed | error
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('processing');
    try {
      const data = await ArchitectureAPI.processProject(requirements);
      setResult(data.data);
      setStatus('completed');
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 font-sans">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-blue-700">TheArchitect Dashboard</h1>
        <p className="text-gray-500">Agentic Swimlane Orchestrator</p>
      </header>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="mb-8">
        <textarea
          className="w-full p-4 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
          rows="5"
          placeholder="Enter your project requirements (SMART)..."
          value={requirements}
          onChange={(e) => setRequirements(e.target.value)}
          required
        />
        <button
          type="submit"
          disabled={status === 'processing'}
          className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          {status === 'processing' ? 'Agents Orchestrating...' : 'Generate Architecture'}
        </button>
      </form>

      {/* Progress Bar (The Swimlane) */}
      <div className="flex justify-between mb-8">
        {['PM', 'Analyst', 'Architect', 'Engineer'].map((step, idx) => (
          <div key={step} className="text-center">
            <div className={`w-10 h-10 rounded-full mx-auto flex items-center justify-center border-2 
              ${status === 'completed' ? 'bg-green-500 border-green-500 text-white' : 'border-gray-300'}`}>
              {idx + 1}
            </div>
            <span className="text-xs mt-2 block">{step}</span>
          </div>
        ))}
      </div>

      {/* Output Results */}
      {result && (
        <div className="space-y-6">
          <section className="p-4 border rounded-lg bg-white">
            <h2 className="font-bold border-b pb-2 mb-2">C4 Architecture Diagram</h2>
            <MermaidViewer chart={result.architecture_specs?.diagram} />
          </section>

          <section className="p-4 border rounded-lg bg-white">
            <h2 className="font-bold border-b pb-2 mb-2">Generated SOLID Code</h2>
            <pre className="bg-gray-800 text-green-400 p-4 rounded overflow-x-auto text-sm">
              <code>{JSON.stringify(result.final_code, null, 2)}</code>
            </pre>
          </section>
        </div>
      )}
    </div>
  );
}
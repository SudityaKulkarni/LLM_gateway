import React, { useState } from 'react';
import InputBox from '../components/InputBox';
import ResultCard from '../components/ResultCard';
import { checkToxicity } from '../api';

const ToxicityDetector = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheck = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await checkToxicity(prompt);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to check prompt');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-100 mb-2">Toxicity Detector</h2>
        <p className="text-gray-400">
          Detects toxic, offensive, or harmful language in prompts.
        </p>
      </div>

      <InputBox
        value={prompt}
        onChange={setPrompt}
        onSubmit={handleCheck}
        disabled={loading}
        placeholder="Enter a prompt to check for toxicity..."
      />

      {error && (
        <div className="bg-danger/20 border border-danger text-danger px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <ResultCard title="Toxicity Detection Result" result={result} loading={loading} />
    </div>
  );
};

export default ToxicityDetector;

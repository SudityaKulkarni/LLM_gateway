import React, { useState } from 'react';
import InputBox from '../components/InputBox';
import ResultCard from '../components/ResultCard';
import { checkGibberish } from '../api';

const GibberishDetector = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheck = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await checkGibberish(prompt);
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
        <h2 className="text-2xl font-bold text-gray-100 mb-2">Gibberish Detector</h2>
        <p className="text-gray-400">
          Detects nonsensical or random text that may indicate spam or automated attacks.
        </p>
      </div>

      <InputBox
        value={prompt}
        onChange={setPrompt}
        onSubmit={handleCheck}
        disabled={loading}
        placeholder="Enter text to check for gibberish..."
      />

      {error && (
        <div className="bg-danger/20 border border-danger text-danger px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <ResultCard title="Gibberish Detection Result" result={result} loading={loading} />
    </div>
  );
};

export default GibberishDetector;

import React, { useState } from 'react';
import InputBox from '../components/InputBox';
import ResultCard from '../components/ResultCard';
import { checkRuleBased } from '../api';

const RuleBasedDetector = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheck = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await checkRuleBased(prompt);
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
        <h2 className="text-2xl font-bold text-gray-100 mb-2">Rule-Based Detector</h2>
        <p className="text-gray-400">
          Uses predefined rules and patterns to detect potentially harmful content.
        </p>
      </div>

      <InputBox
        value={prompt}
        onChange={setPrompt}
        onSubmit={handleCheck}
        disabled={loading}
        placeholder="Enter text to check against rules..."
      />

      {error && (
        <div className="bg-danger/20 border border-danger text-danger px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <ResultCard title="Rule-Based Detection Result" result={result} loading={loading} />
    </div>
  );
};

export default RuleBasedDetector;

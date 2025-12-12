import React, { useState } from 'react';
import InputBox from '../components/InputBox';
import ResultCard from '../components/ResultCard';
import { checkPromptInjection } from '../api';

const PromptInjectionDetector = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheck = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await checkPromptInjection(prompt);
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
        <h2 className="text-2xl font-bold text-gray-100 mb-2">Prompt Injection Detector</h2>
        <p className="text-gray-400">
          Detects attempts to inject malicious instructions or override system prompts.
        </p>
      </div>

      <InputBox
        value={prompt}
        onChange={setPrompt}
        onSubmit={handleCheck}
        disabled={loading}
        placeholder="Enter a prompt to check for injection attempts..."
      />

      {error && (
        <div className="bg-danger/20 border border-danger text-danger px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <ResultCard title="Prompt Injection Detection Result" result={result} loading={loading} />
    </div>
  );
};

export default PromptInjectionDetector;

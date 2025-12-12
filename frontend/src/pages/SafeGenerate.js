import React, { useState } from 'react';
import DetectorStatus from '../components/DetectorStatus';
import LoadingSpinner from '../components/LoadingSpinner';
import { safeGenerate } from '../api';

const SafeGenerate = () => {
  const [prompt, setPrompt] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    if (!apiKey.trim()) {
      setError('Please enter your Gemini API key');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await safeGenerate(prompt, apiKey);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate response');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleGenerate();
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-100 mb-2">Safe Generate</h2>
        <p className="text-gray-400">
          Comprehensive safety check with prompt sanitization and AI response generation.
        </p>
      </div>

      {/* API Key Input */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Gemini API Key
        </label>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter your Gemini API key..."
          className="w-full p-3 bg-slate-900 text-white rounded-lg border border-slate-700 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50"
        />
        <p className="text-xs text-gray-500 mt-2">
          Your API key is only used for this request and is not stored.
        </p>
      </div>

      {/* Prompt Input */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Your Prompt
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter your prompt here..."
          disabled={loading}
          className="w-full p-4 bg-slate-900 text-white rounded-lg border border-slate-700 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none min-h-[150px] disabled:opacity-50"
          rows={6}
        />
        <button
          onClick={handleGenerate}
          disabled={loading || !prompt.trim() || !apiKey.trim()}
          className="mt-4 px-8 py-3 bg-primary text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium text-lg"
        >
          {loading ? 'Processing...' : 'Generate Safe Response'}
        </button>
      </div>

      {error && (
        <div className="bg-danger/20 border border-danger text-danger px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {loading && (
        <div className="bg-slate-800 rounded-lg p-12 border border-slate-700">
          <LoadingSpinner />
          <p className="text-center text-gray-400 mt-4">
            Running safety checks and generating response...
          </p>
        </div>
      )}

      {result && !loading && (
        <div className="space-y-6">
          {/* Overall Safety Status */}
          <div className={`rounded-lg p-6 border-2 ${
            result.risk_assessment?.risk_score === 0 || result.risk_assessment?.risk_score === undefined
              ? 'border-success bg-success/10' 
              : 'border-danger bg-danger/10'
          }`}>
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">{result.risk_assessment?.risk_score === 0 || result.risk_assessment?.risk_score === undefined ? '✅' : '⚠️'}</span>
              <div>
                <h3 className="text-xl font-bold text-gray-100">
                  {result.risk_assessment?.risk_score === 0 || result.risk_assessment?.risk_score === undefined ? 'Prompt is Safe' : 'Safety Issues Detected'}
                </h3>
                <p className="text-gray-400 text-sm">
                  {result.risk_assessment?.risk_score === 0 || result.risk_assessment?.risk_score === undefined
                    ? 'All safety checks passed successfully' 
                    : 'Risk score is above 0 - content may be unsafe'}
                </p>
              </div>
            </div>
            {result.risk_assessment?.risk_score !== undefined && (
              <div className="mt-4">
                <span className="text-sm text-gray-400">Risk Score:</span>
                <div className="mt-2 flex items-center gap-2">
                  <div className="flex-1 bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full ${
                        result.risk_assessment.risk_score === 0 ? 'bg-success' :
                        result.risk_assessment.risk_score < 30 ? 'bg-warning' :
                        'bg-danger'
                      }`}
                      style={{ width: `${Math.max(result.risk_assessment.risk_score, 5)}%` }}
                    ></div>
                  </div>
                  <span className="text-sm text-gray-300 min-w-[50px]">
                    {result.risk_assessment.risk_score}/100
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Detector Results */}
          {result.risk_assessment?.results && (
            <DetectorStatus detectors={result.risk_assessment.results} />
          )}

          {/* AI Response */}
          {result.llm_response && (
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold mb-3 text-gray-200 flex items-center gap-2">
                <span>💬</span> AI Response
              </h3>
              <div className="bg-slate-900 p-4 rounded-lg">
                <p className="text-gray-300 whitespace-pre-wrap leading-relaxed">
                  {result.llm_response}
                </p>
              </div>
            </div>
          )}

          {/* Blocked Message */}
          {result.status !== 'allowed' && !result.llm_response && (
            <div className="bg-danger/20 border border-danger rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2 text-danger">
                ⛔ Request Blocked
              </h3>
              <p className="text-gray-300">
                This prompt was blocked due to safety concerns (Risk Score: {result.risk_assessment?.risk_score}/100). 
                Please modify your prompt and try again.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SafeGenerate;

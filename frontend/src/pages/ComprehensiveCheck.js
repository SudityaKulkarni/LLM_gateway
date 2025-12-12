import React, { useState } from 'react';
import DetectorStatus from '../components/DetectorStatus';
import LoadingSpinner from '../components/LoadingSpinner';
import { comprehensiveCheck } from '../api';

const ComprehensiveCheck = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheck = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await comprehensiveCheck(prompt);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to perform comprehensive check');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleCheck();
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-100 mb-2">Comprehensive Check</h2>
        <p className="text-gray-400">
          Run all safety detectors simultaneously to get a complete safety analysis.
        </p>
      </div>

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
          onClick={handleCheck}
          disabled={loading || !prompt.trim()}
          className="mt-4 px-8 py-3 bg-primary text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium text-lg"
        >
          {loading ? 'Analyzing...' : 'Run All Checks'}
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
            Running comprehensive safety analysis...
          </p>
        </div>
      )}

      {result && !loading && (
        <div className="space-y-6">
          {/* Overall Safety Status */}
          <div className={`rounded-lg p-6 border-2 ${
            result.overall_safe 
              ? 'border-success bg-success/10' 
              : 'border-danger bg-danger/10'
          }`}>
            <div className="flex items-center gap-3">
              <span className="text-3xl">{result.overall_safe ? '✅' : '⚠️'}</span>
              <div>
                <h3 className="text-xl font-bold text-gray-100">
                  {result.overall_safe ? 'All Checks Passed' : 'Safety Issues Detected'}
                </h3>
                <p className="text-gray-400 text-sm">
                  {result.overall_safe 
                    ? 'No safety concerns found' 
                    : `${result.flagged_count || 0} detector(s) flagged this content`}
                </p>
              </div>
            </div>
          </div>

          {/* Detector Results */}
          {result.results && (
            <DetectorStatus detectors={result.results} />
          )}

          {/* Detailed Results */}
          {result.results && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(result.results).map(([detector, data]) => {
                // Check score first (0 = safe, >0 = unsafe), then fallback to flagged
                const isUnsafe = data.score !== undefined ? data.score > 0 : data.flagged;
                return (
                  <div
                    key={detector}
                    className={`bg-slate-800 rounded-lg p-5 border-2 ${
                      isUnsafe
                        ? 'border-danger bg-danger/5'
                        : 'border-success bg-success/5'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-gray-200 capitalize">
                        {detector.replace(/_/g, ' ')}
                      </h4>
                      <span className={`text-2xl`}>
                        {isUnsafe ? '⚠️' : '✅'}
                      </span>
                    </div>
                    
                    {data.reason && (
                      <p className="text-sm text-gray-400 mb-2">{data.reason}</p>
                    )}
                    
                    {data.confidence !== undefined && (
                      <div className="flex items-center gap-2 text-sm">
                        <span className="text-gray-500">Confidence:</span>
                        <div className="flex-1 bg-slate-700 rounded-full h-1.5">
                          <div
                            className={`h-1.5 rounded-full ${
                              isUnsafe ? 'bg-danger' : 'bg-success'
                            }`}
                            style={{ width: `${data.confidence * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-gray-400 min-w-[45px]">
                          {(data.confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                    )}

                    {data.score !== undefined && (
                      <p className="text-sm text-gray-500 mt-2">
                        Score: {data.score.toFixed(3)}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ComprehensiveCheck;

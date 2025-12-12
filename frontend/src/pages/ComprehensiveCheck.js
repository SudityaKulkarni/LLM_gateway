import React, { useState } from 'react';
import DetectorStatus from '../components/DetectorStatus';
import LoadingSpinner from '../components/LoadingSpinner';
import { comprehensiveCheck } from '../api';
import { addLog } from '../utils/logStorage';

const ComprehensiveCheck = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Detector selection state
  const [detectorSettings, setDetectorSettings] = useState({
    check_gibberish: true,
    check_toxicity: true,
    check_jailbreak: true,
    check_prompt_injection: true,
    check_pii: true,
    check_entropy: true,
    check_jailbreak_rules: true,
  });

  const detectorOptions = [
    { key: 'check_gibberish', label: '🔤 Gibberish Detection', description: 'Detect nonsensical text' },
    { key: 'check_toxicity', label: '☠️ Toxicity Detection', description: 'Detect harmful or toxic content' },
    { key: 'check_jailbreak', label: '🔓 Jailbreak Detection', description: 'Detect jailbreak attempts' },
    { key: 'check_prompt_injection', label: '💉 Prompt Injection', description: 'Detect injection attacks' },
    { key: 'check_pii', label: '🔒 PII Detection', description: 'Detect personal information' },
    { key: 'check_entropy', label: '📈 Entropy Analysis', description: 'Detect high randomness' },
    { key: 'check_jailbreak_rules', label: '📋 Rule-based Detection', description: 'Pattern matching checks' },
  ];

  const handleDetectorToggle = (key) => {
    setDetectorSettings(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleSelectAll = () => {
    const allSelected = Object.values(detectorSettings).every(v => v);
    const newSettings = {};
    Object.keys(detectorSettings).forEach(key => {
      newSettings[key] = !allSelected;
    });
    setDetectorSettings(newSettings);
  };

  const handleCheck = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    // Check if at least one detector is selected
    const hasSelection = Object.values(detectorSettings).some(v => v);
    if (!hasSelection) {
      setError('Please select at least one detector');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await comprehensiveCheck(prompt, {
        ...detectorSettings,
        entropy_threshold: 4.5
      });
      setResult(response.data);
      
      // Log the result - check if ANY detector failed
      const selectedDetectors = Object.keys(detectorSettings)
        .filter(key => detectorSettings[key])
        .map(key => key.replace('check_', '').replace(/_/g, ' '));
      
      // Check if any detector flagged the content
      let anyFailed = false;
      if (response.data.detailed_results) {
        anyFailed = Object.entries(response.data.detailed_results).some(([detector, data]) => {
          if (detector === 'toxicity') {
            // For toxicity: is_toxic=true OR score > threshold means FAILED
            return data.is_toxic === true || (data.score !== undefined && data.score > 0.5);
          }
          if (detector === 'pii') {
            // For PII: contains_pii=true means FAILED
            return data.contains_pii === true;
          }
          // For other detectors
          return data.is_gibberish || data.is_jailbreak || 
                 data.detected || data.is_high_entropy || 
                 (data.score !== undefined && data.score > 0);
        });
      }
      
      addLog({
        type: 'comprehensive',
        prompt: prompt,
        passed: !anyFailed,
        detectors: selectedDetectors,
        response: null
      });
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
          Select detectors and run a complete safety analysis on your prompt.
        </p>
      </div>

      {/* Detector Selection */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-200">Select Detectors</h3>
          <button
            onClick={handleSelectAll}
            className="text-sm text-primary hover:text-blue-400 transition-colors"
          >
            {Object.values(detectorSettings).every(v => v) ? 'Deselect All' : 'Select All'}
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {detectorOptions.map(option => (
            <label
              key={option.key}
              className={`flex items-start gap-3 p-4 rounded-lg border-2 cursor-pointer transition-all ${
                detectorSettings[option.key]
                  ? 'border-primary bg-primary/10'
                  : 'border-slate-700 bg-slate-900 hover:border-slate-600'
              }`}
            >
              <input
                type="checkbox"
                checked={detectorSettings[option.key]}
                onChange={() => handleDetectorToggle(option.key)}
                className="mt-1 h-5 w-5 text-primary bg-slate-700 border-slate-600 rounded focus:ring-primary focus:ring-offset-slate-800"
              />
              <div className="flex-1">
                <div className="font-medium text-gray-200 mb-1">{option.label}</div>
                <div className="text-xs text-gray-400">{option.description}</div>
              </div>
            </label>
          ))}
        </div>
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
          {loading ? 'Analyzing...' : 'Run Selected Checks'}
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
          {/* Detection Results */}
          {result.detailed_results && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {Object.entries(result.detailed_results).map(([detector, data]) => {
                // Determine if this detector flagged the content
                let isFlagged = false;
                
                if (detector === 'toxicity') {
                  // For toxicity: is_toxic=true OR score > threshold means FAILED
                  isFlagged = data.is_toxic === true || (data.score !== undefined && data.score > 0.5);
                } else if (detector === 'pii') {
                  // For PII: contains_pii=true means FAILED
                  isFlagged = data.contains_pii === true;
                } else {
                  // For other detectors
                  isFlagged = data.is_gibberish || data.is_jailbreak || 
                             data.detected || data.is_high_entropy || 
                             (data.score !== undefined && data.score > 0);
                }
                
                return (
                  <div 
                    key={detector} 
                    className={`rounded-lg p-5 border-2 transition-all ${
                      isFlagged 
                        ? 'border-danger bg-danger/5' 
                        : 'border-success bg-success/5'
                    }`}
                  >
                    {/* Header */}
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-bold text-gray-100 capitalize flex items-center gap-2">
                        <span className="text-2xl">
                          {detector === 'gibberish' && '🔤'}
                          {detector === 'toxicity' && '☠️'}
                          {detector === 'jailbreak' && '🔓'}
                          {detector === 'prompt_injection' && '💉'}
                          {detector === 'pii' && '🔒'}
                          {detector === 'entropy' && '📈'}
                          {detector === 'jailbreak_rules' && '📋'}
                        </span>
                        {detector.replace(/_/g, ' ')}
                      </h3>
                      <span className={`px-4 py-1.5 rounded-full font-bold text-sm ${
                        isFlagged 
                          ? 'bg-danger text-white' 
                          : 'bg-success text-white'
                      }`}>
                        {isFlagged ? '⚠️ FAILED' : '✓ PASSED'}
                      </span>
                    </div>
                    
                    {/* Key Metrics */}
                    <div className="space-y-2">
                      {Object.entries(data).map(([key, value]) => {
                        // Skip rendering nested objects in a simple way, handle them specially
                        if (key === 'toxicity_categories' && typeof value === 'object') {
                          return (
                            <div key={key} className="mt-3">
                              <div className="text-xs font-semibold text-gray-400 uppercase mb-2">
                                Toxicity Categories
                              </div>
                              <div className="grid grid-cols-2 gap-2">
                                {Object.entries(value).map(([cat, score]) => (
                                  <div key={cat} className="bg-slate-900 rounded px-3 py-2">
                                    <div className="text-xs text-gray-400 capitalize">
                                      {cat.replace(/_/g, ' ')}
                                    </div>
                                    <div className="text-sm font-bold text-gray-200">
                                      {typeof score === 'number' ? score.toFixed(4) : score}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          );
                        }
                        
                        if (key === 'detections' && Array.isArray(value)) {
                          return value.length > 0 ? (
                            <div key={key} className="mt-3">
                              <div className="text-xs font-semibold text-gray-400 uppercase mb-2">
                                Patterns Detected
                              </div>
                              <div className="space-y-1">
                                {value.map((detection, idx) => (
                                  <div key={idx} className="bg-slate-900 rounded px-3 py-2 text-sm text-gray-300">
                                    {typeof detection === 'object' ? detection.pattern : detection}
                                  </div>
                                ))}
                              </div>
                            </div>
                          ) : null;
                        }
                        
                        if (key === 'entities' && Array.isArray(value)) {
                          return value.length > 0 ? (
                            <div key={key} className="mt-3">
                              <div className="text-xs font-semibold text-gray-400 uppercase mb-2">
                                PII Entities Found
                              </div>
                              <div className="space-y-1">
                                {value.map((entity, idx) => (
                                  <div key={idx} className="bg-slate-900 rounded px-3 py-2">
                                    <div className="text-xs text-gray-400">{entity.type}</div>
                                    <div className="text-sm text-gray-200 font-mono">{entity.value}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          ) : null;
                        }
                        
                        if (key === 'redactions' && Array.isArray(value)) {
                          return value.length > 0 ? (
                            <div key={key} className="mt-3">
                              <div className="text-xs font-semibold text-gray-400 uppercase mb-2">
                                PII Redactions Applied
                              </div>
                              <div className="space-y-1">
                                {value.map((redaction, idx) => (
                                  <div key={idx} className="bg-slate-900 rounded px-3 py-2">
                                    <div className="text-xs text-gray-400 capitalize">{redaction.type}</div>
                                    <div className="text-sm text-gray-200 font-mono">{redaction.redacted_to}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          ) : null;
                        }
                        
                        if (key === 'detection' && typeof value === 'object' && value !== null) {
                          return (
                            <div key={key} className="bg-slate-900 rounded px-3 py-2">
                              <div className="text-xs text-gray-400 capitalize">Entropy Details</div>
                              <div className="text-sm text-gray-200 font-mono whitespace-pre-wrap break-all">
                                {JSON.stringify(value, null, 2)}
                              </div>
                            </div>
                          );
                        }
                        
                        // Skip any other objects or arrays to prevent rendering errors
                        if (typeof value === 'object' && value !== null) {
                          return null;
                        }
                        
                        // Regular key-value pairs (primitives only)
                        return (
                          <div key={key} className="flex justify-between items-center bg-slate-900 rounded px-3 py-2">
                            <span className="text-xs font-medium text-gray-400 capitalize">
                              {key.replace(/_/g, ' ')}
                            </span>
                            <span className="text-sm font-semibold text-gray-200">
                              {typeof value === 'boolean' 
                                ? (value ? '✓ Yes' : '✗ No')
                                : typeof value === 'number'
                                ? value.toFixed(4)
                                : String(value)}
                            </span>
                          </div>
                        );
                      })}
                    </div>
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

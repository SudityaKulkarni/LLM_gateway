import React from 'react';

const ResultCard = ({ title, result, loading }) => {
  if (loading) {
    return (
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-semibold mb-4 text-gray-200">{title}</h3>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (!result) return null;

  const getFlaggedStyle = () => {
    // Check score first, then fallback to flagged
    const isUnsafe = result.score !== undefined ? result.score > 0 : result.flagged;
    if (isUnsafe) {
      return 'border-danger bg-danger/10';
    }
    return 'border-success bg-success/10';
  };

  const getFlaggedBadge = () => {
    // Check score first, then fallback to flagged
    const isUnsafe = result.score !== undefined ? result.score > 0 : result.flagged;
    if (isUnsafe) {
      return (
        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-danger text-white">
          ⚠️ Flagged
        </span>
      );
    }
    return (
      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-success text-white">
      
      </span>
    );
  };

  return (
    <div className={`rounded-lg p-6 border-2 ${getFlaggedStyle()}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-200">{title}</h3>
        {getFlaggedBadge()}
      </div>
      
      <div className="space-y-3">
        {/* Display formatted response data */}
        <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg p-5 border border-slate-700 shadow-lg">
          <div className="space-y-4">
            {/* Status */}
            {result.status && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Status:</span>
                <span className="text-gray-200 font-medium">{result.status}</span>
              </div>
            )}
            
            {/* Is Jailbreak / Is Flagged / Is Toxic / Is Gibberish / Is Prompt Injection */}
            {(result.is_jailbreak !== undefined || result.is_toxic !== undefined || 
              result.is_gibberish !== undefined || result.is_prompt_injection !== undefined || 
              result.flagged !== undefined) && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">
                  {result.is_jailbreak !== undefined ? 'Is Jailbreak:' : 
                   result.is_toxic !== undefined ? 'Is Toxic:' :
                   result.is_gibberish !== undefined ? 'Is Gibberish:' :
                   result.is_prompt_injection !== undefined ? 'Is Prompt Injection:' :
                   'Flagged:'}
                </span>
                <span className={`font-semibold ${(result.is_jailbreak || result.is_toxic || result.is_gibberish || result.is_prompt_injection || result.flagged) ? 'text-red-400' : 'text-green-400'}`}>
                  {(result.is_jailbreak || result.is_toxic || result.is_gibberish || result.is_prompt_injection || result.flagged) ? 'true' : 'false'}
                </span>
              </div>
            )}
            
            {/* Risk Level */}
            {result.risk_level && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Risk Level:</span>
                <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                  result.risk_level === 'High' ? 'bg-red-500/20 text-red-400 border border-red-500/50' :
                  result.risk_level === 'Medium' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/50' :
                  'bg-green-500/20 text-green-400 border border-green-500/50'
                }`}>
                  {result.risk_level}
                </span>
              </div>
            )}
            
            {/* Confidence */}
            {result.confidence !== undefined && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Confidence:</span>
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <div className="flex-1 bg-slate-700 rounded-full h-2.5 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2.5 rounded-full transition-all duration-500 shadow-lg"
                        style={{ width: `${result.confidence * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-bold text-purple-400 min-w-[60px]">
                      {(result.confidence * 100).toFixed(2)}%
                    </span>
                  </div>
                </div>
              </div>
            )}
            
            {/* Score */}
            {result.score !== undefined && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Score:</span>
                <span className="text-gray-200 font-mono bg-slate-800 px-3 py-1 rounded border border-slate-600">
                  {result.score.toFixed(6)}
                </span>
              </div>
            )}
            
            {/* Classification / Label */}
            {(result.classification || result.label) && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">
                  {result.classification ? 'Classification:' : 'Label:'}
                </span>
                <span className="text-orange-400 font-medium bg-orange-500/10 px-3 py-1 rounded border border-orange-500/30">
                  {result.classification || result.label}
                </span>
              </div>
            )}
            
            {/* Reason */}
            {result.reason && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Reason:</span>
                <p className="text-gray-300 flex-1 leading-relaxed">{result.reason}</p>
              </div>
            )}
            
            {/* Categories (Toxicity specific) */}
            {result.categories && (
              <div>
                <span className="text-sm font-semibold text-blue-400 block mb-2">Toxicity Categories:</span>
                <div className="grid grid-cols-2 gap-2 pl-4">
                  {Object.entries(result.categories).map(([category, score]) => (
                    <div key={category} className="bg-slate-800/50 rounded p-3 border border-slate-600">
                      <div className="flex flex-col gap-1">
                        <span className="text-sm text-gray-300 font-medium capitalize">
                          {category.replace(/_/g, ' ')}
                        </span>
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                            <div
                              className={`h-1.5 rounded-full transition-all duration-500 ${
                                score > 0.7 ? 'bg-red-500' : 
                                score > 0.4 ? 'bg-yellow-500' : 
                                'bg-green-500'
                              }`}
                              style={{ width: `${score * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-xs font-mono text-gray-400 min-w-[60px]">
                            {(score * 100).toFixed(2)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* PII Entities */}
            {result.entities && result.entities.length > 0 && (
              <div>
                <span className="text-sm font-semibold text-blue-400 block mb-2">Detected Entities:</span>
                <div className="space-y-2 pl-4">
                  {result.entities.map((entity, idx) => (
                    <div key={idx} className="bg-slate-800/50 rounded p-3 border border-slate-600">
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-gray-400">Entity:</span>
                          <span className="text-yellow-400 font-medium ml-2">{entity.entity}</span>
                        </div>
                        <div>
                          <span className="text-gray-400">Type:</span>
                          <span className="text-cyan-400 font-medium ml-2">{entity.type}</span>
                        </div>
                        <div className="col-span-2">
                          <span className="text-gray-400">Score:</span>
                          <span className="text-green-400 font-mono ml-2">{entity.score.toFixed(4)}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Entropy Value */}
            {result.entropy_value !== undefined && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Entropy Value:</span>
                <span className="text-gray-200 font-mono bg-slate-800 px-3 py-1 rounded border border-slate-600">
                  {result.entropy_value.toFixed(4)}
                </span>
              </div>
            )}
            
            {/* Is High Entropy */}
            {result.is_high_entropy !== undefined && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">High Entropy:</span>
                <span className={`font-semibold ${result.is_high_entropy ? 'text-red-400' : 'text-green-400'}`}>
                  {result.is_high_entropy ? 'true' : 'false'}
                </span>
              </div>
            )}
            
            {/* Pattern Matches */}
            {result.patterns_matched !== undefined && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Patterns Matched:</span>
                <span className="text-gray-200 font-bold">{result.patterns_matched}</span>
              </div>
            )}
            
            {/* PII Detection - Contains PII */}
            {result.contains_pii !== undefined && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Contains PII:</span>
                <span className={`font-semibold ${result.contains_pii ? 'text-red-400' : 'text-green-400'}`}>
                  {result.contains_pii ? 'Yes' : 'No'}
                </span>
              </div>
            )}
            
            {/* Redaction Count */}
            {result.redaction_count !== undefined && (
              <div className="flex items-start">
                <span className="text-sm font-semibold text-blue-400 min-w-[140px]">Redaction Count:</span>
                <span className="text-gray-200 font-bold">{result.redaction_count}</span>
              </div>
            )}
            
            {/* Original Text */}
            {result.original_text && (
              <div>
                <span className="text-sm font-semibold text-blue-400 block mb-2">Original Text:</span>
                <div className="bg-slate-900/50 rounded p-3 border border-slate-600">
                  <p className="text-gray-300 text-sm">{result.original_text}</p>
                </div>
              </div>
            )}
            
            {/* Redacted Text */}
            {result.redacted_text && (
              <div>
                <span className="text-sm font-semibold text-green-400 block mb-2">Redacted Text:</span>
                <div className="bg-green-500/10 rounded p-3 border border-green-500/30">
                  <p className="text-green-300 text-sm font-mono">{result.redacted_text}</p>
                </div>
              </div>
            )}
            
            {/* Redactions List */}
            {result.redactions && result.redactions.length > 0 && (
              <div>
                <span className="text-sm font-semibold text-blue-400 block mb-2">Redactions Applied:</span>
                <div className="space-y-2 pl-4">
                  {result.redactions.map((redaction, idx) => (
                    <div key={idx} className="bg-yellow-500/10 rounded p-3 border border-yellow-500/30">
                      <div className="text-sm">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-yellow-400 font-medium capitalize">{redaction.type.replace('_', ' ')}</span>
                          <span className="text-gray-400 text-xs">→</span>
                          <span className="text-gray-300 font-mono text-xs">{redaction.redacted_to}</span>
                        </div>
                        <div className="text-gray-400 text-xs">Original length: {redaction.original_length} characters</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Detections */}
            {result.detections && result.detections.length > 0 && (
              <div>
                <span className="text-sm font-semibold text-blue-400 block mb-2">Detections:</span>
                <div className="space-y-2 pl-4">
                  {result.detections.map((detection, idx) => (
                    <div key={idx} className="bg-red-500/10 rounded p-3 border border-red-500/30">
                      <div className="text-sm">
                        <div className="text-red-400 font-medium mb-1">{detection.pattern}</div>
                        <div className="text-gray-300 text-xs">{detection.reason}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {/* Other Details */}
            {result.details && (
              <div>
                <span className="text-sm font-semibold text-blue-400 block mb-2">Additional Details:</span>
                <pre className="text-gray-300 text-xs bg-slate-800/50 p-3 rounded border border-slate-600 overflow-x-auto">
                  {JSON.stringify(result.details, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;

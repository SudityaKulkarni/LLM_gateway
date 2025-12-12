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
        ✓ Safe
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
        {result.reason && (
          <div>
            <span className="text-sm text-gray-400">Reason:</span>
            <p className="text-gray-200 mt-1">{result.reason}</p>
          </div>
        )}
        
        {result.confidence !== undefined && (
          <div>
            <span className="text-sm text-gray-400">Confidence:</span>
            <div className="mt-2">
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all"
                    style={{ width: `${result.confidence * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm text-gray-300 min-w-[50px]">
                  {(result.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>
        )}

        {result.score !== undefined && (
          <div>
            <span className="text-sm text-gray-400">Score:</span>
            <p className="text-gray-200 mt-1">{result.score.toFixed(3)}</p>
          </div>
        )}

        {result.details && (
          <div>
            <span className="text-sm text-gray-400">Details:</span>
            <pre className="text-gray-200 mt-1 text-sm bg-slate-900 p-3 rounded overflow-x-auto">
              {JSON.stringify(result.details, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultCard;

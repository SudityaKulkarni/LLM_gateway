import React from 'react';

const DetectorStatus = ({ detectors }) => {
  if (!detectors || Object.keys(detectors).length === 0) return null;

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <h3 className="text-lg font-semibold mb-4 text-gray-200">All Detectors Status</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {Object.entries(detectors).map(([key, value]) => {
          // Check score first (0 = safe, >0 = unsafe), then fallback to flagged
          const isUnsafe = value?.score !== undefined ? value.score > 0 : (value?.flagged || false);
          return (
            <div
              key={key}
              className={`p-3 rounded-lg border-2 ${
                isUnsafe
                  ? 'border-danger bg-danger/10'
                  : 'border-success bg-success/10'
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="text-xl">
                  {isUnsafe ? '⚠️' : '✓'}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-200 truncate capitalize">
                    {key.replace(/_/g, ' ')}
                  </p>
                  {value?.confidence !== undefined && (
                    <p className="text-xs text-gray-400">
                      {(value.confidence * 100).toFixed(0)}%
                    </p>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DetectorStatus;

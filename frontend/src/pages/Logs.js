import React, { useState, useEffect } from 'react';

const Logs = () => {
  const [logs, setLogs] = useState([]);
  const [filter, setFilter] = useState('all'); // all, passed, failed

  useEffect(() => {
    // Load logs from localStorage
    const storedLogs = localStorage.getItem('promptLogs');
    if (storedLogs) {
      try {
        setLogs(JSON.parse(storedLogs));
      } catch (e) {
        console.error('Failed to parse logs:', e);
      }
    }
  }, []);

  const clearLogs = () => {
    if (window.confirm('Are you sure you want to clear all logs?')) {
      localStorage.removeItem('promptLogs');
      setLogs([]);
    }
  };

  const deleteLog = (id) => {
    const updatedLogs = logs.filter(log => log.id !== id);
    setLogs(updatedLogs);
    localStorage.setItem('promptLogs', JSON.stringify(updatedLogs));
  };

  const filteredLogs = logs.filter(log => {
    if (filter === 'passed') return log.passed;
    if (filter === 'failed') return !log.passed;
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-100 mb-2">Prompt Logs</h2>
          <p className="text-gray-400">
            History of all prompts analyzed ({logs.length} total)
          </p>
        </div>
        {logs.length > 0 && (
          <button
            onClick={clearLogs}
            className="px-4 py-2 bg-danger text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
          >
            Clear All Logs
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'all'
              ? 'bg-primary text-white'
              : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
          }`}
        >
          All ({logs.length})
        </button>
        <button
          onClick={() => setFilter('passed')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'passed'
              ? 'bg-success text-white'
              : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
          }`}
        >
          Passed ({logs.filter(l => l.passed).length})
        </button>
        <button
          onClick={() => setFilter('failed')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'failed'
              ? 'bg-danger text-white'
              : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
          }`}
        >
          Failed ({logs.filter(l => !l.passed).length})
        </button>
      </div>

      {/* Logs List */}
      {filteredLogs.length === 0 ? (
        <div className="bg-slate-800 rounded-lg p-12 border border-slate-700 text-center">
          <div className="text-6xl mb-4">📋</div>
          <h3 className="text-xl font-semibold text-gray-300 mb-2">No logs yet</h3>
          <p className="text-gray-500">
            {filter === 'all' 
              ? 'Start analyzing prompts to see them here'
              : `No ${filter} logs found`}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredLogs.map((log) => (
            <div
              key={log.id}
              className={`bg-slate-800 rounded-lg p-5 border-2 ${
                log.passed ? 'border-success/30' : 'border-danger/30'
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <span className={`px-3 py-1 rounded-full font-bold text-xs ${
                      log.passed 
                        ? 'bg-success text-white' 
                        : 'bg-danger text-white'
                    }`}>
                      {log.passed ? '✓ PASSED' : '⚠️ FAILED'}
                    </span>
                    <span className="text-xs text-gray-500">
                      {new Date(log.timestamp).toLocaleString()}
                    </span>
                    <span className="text-xs text-gray-500 capitalize">
                      {log.type}
                    </span>
                  </div>
                  
                  <div className="bg-slate-900 rounded-lg p-4 mb-3">
                    <div className="text-xs text-gray-400 uppercase font-semibold mb-2">
                      Prompt
                    </div>
                    <div className="text-gray-200 text-sm">
                      {log.prompt}
                    </div>
                  </div>

                  {log.detectors && log.detectors.length > 0 && (
                    <div>
                      <div className="text-xs text-gray-400 uppercase font-semibold mb-2">
                        Detectors Used
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {log.detectors.map((detector, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-slate-900 text-gray-300 rounded text-xs"
                          >
                            {detector}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {log.response && (
                    <div className="mt-3 bg-slate-900 rounded-lg p-4">
                      <div className="text-xs text-gray-400 uppercase font-semibold mb-2">
                        Response
                      </div>
                      <div className="text-gray-200 text-sm">
                        {log.response}
                      </div>
                    </div>
                  )}
                </div>

                <button
                  onClick={() => deleteLog(log.id)}
                  className="text-gray-500 hover:text-danger transition-colors p-2"
                  title="Delete log"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Logs;
// utils/logStorage.js
// Utility functions for managing prompt logs in localStorage

export const addLog = (logData) => {
  try {
    const existingLogs = JSON.parse(localStorage.getItem('promptLogs') || '[]');
    const newLog = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      ...logData
    };
    const updatedLogs = [newLog, ...existingLogs]; // Newest first
    localStorage.setItem('promptLogs', JSON.stringify(updatedLogs));
    return newLog;
  } catch (e) {
    console.error('Failed to add log:', e);
    return null;
  }
};

export const getLogs = () => {
  try {
    return JSON.parse(localStorage.getItem('promptLogs') || '[]');
  } catch (e) {
    console.error('Failed to get logs:', e);
    return [];
  }
};

export const clearLogs = () => {
  localStorage.removeItem('promptLogs');
};

import React from 'react';

const InputBox = ({ value, onChange, onSubmit, placeholder, disabled }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="w-full">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={placeholder || "Enter your prompt here..."}
        disabled={disabled}
        className="w-full p-4 bg-slate-800 text-white rounded-lg border border-slate-700 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none min-h-[120px] disabled:opacity-50"
        rows={4}
      />
      <button
        onClick={onSubmit}
        disabled={disabled || !value.trim()}
        className="mt-3 px-6 py-2 bg-primary text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
      >
        Check Safety
      </button>
    </div>
  );
};

export default InputBox;

import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import SafeGenerate from './pages/SafeGenerate';
import ComprehensiveCheck from './pages/ComprehensiveCheck';
import JailbreakDetector from './pages/JailbreakDetector';
import ToxicityDetector from './pages/ToxicityDetector';
import PIIDetector from './pages/PIIDetector';
import PromptInjectionDetector from './pages/PromptInjectionDetector';
import GibberishDetector from './pages/GibberishDetector';
import EntropyDetector from './pages/EntropyDetector';
import RuleBasedDetector from './pages/RuleBasedDetector';

function App() {
  const navItems = [
    { path: '/', label: '🛡️ Safe Generate', component: SafeGenerate },
    { path: '/comprehensive', label: '📊 Comprehensive Check', component: ComprehensiveCheck },
    { path: '/jailbreak', label: '🔓 Jailbreak', component: JailbreakDetector },
    { path: '/toxicity', label: '☠️ Toxicity', component: ToxicityDetector },
    { path: '/pii', label: '🔒 PII', component: PIIDetector },
    { path: '/injection', label: '💉 Prompt Injection', component: PromptInjectionDetector },
    { path: '/gibberish', label: '🔤 Gibberish', component: GibberishDetector },
    { path: '/entropy', label: '📈 Entropy', component: EntropyDetector },
    { path: '/rule-based', label: '📋 Rule-Based', component: RuleBasedDetector },
  ];

  return (
    <Router>
      <div className="min-h-screen bg-slate-950">
        {/* Header */}
        <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center gap-3">
              <div className="text-3xl">🛡️</div>
              <div>
                <h1 className="text-2xl font-bold text-white">LLM Safety Gateway</h1>
                <p className="text-sm text-gray-400">Protect your AI applications</p>
              </div>
            </div>
          </div>
        </header>

        <div className="flex">
          {/* Sidebar Navigation */}
          <aside className="w-64 bg-slate-900 min-h-[calc(100vh-80px)] border-r border-slate-800 sticky top-[80px]">
            <nav className="p-4">
              <div className="space-y-1">
                {navItems.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      `block px-4 py-3 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-primary text-white font-medium'
                          : 'text-gray-400 hover:bg-slate-800 hover:text-white'
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
              </div>
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 p-8">
            <div className="container mx-auto max-w-7xl">
              <Routes>
                {navItems.map((item) => (
                  <Route
                    key={item.path}
                    path={item.path}
                    element={<item.component />}
                  />
                ))}
              </Routes>
            </div>
          </main>
        </div>

        {/* Footer */}
        <footer className="bg-slate-900 border-t border-slate-800 py-6 mt-12">
          <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
            <p>LLM Safety Gateway - Built with React & FastAPI</p>
            <p className="mt-1">Protecting AI applications from harmful content</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;

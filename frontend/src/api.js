import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const checkJailbreak = (prompt) => 
  api.post('/detect_jailbreak', { text: prompt });

export const checkToxicity = (prompt) => 
  api.post('/detect_toxicity', { text: prompt });

export const checkPII = (prompt) => 
  api.post('/detect_pii', { text: prompt });

export const checkPromptInjection = (prompt) => 
  api.post('/detect_prompt_injection', { text: prompt });

export const checkGibberish = (prompt) => 
  api.post('/detect_gibberish', { text: prompt });

export const checkEntropy = (prompt) => 
  api.post('/shannon_entropy', { text: prompt });

export const checkRuleBased = (prompt) => 
  api.post('/jailbreak_rules', { text: prompt });

export const safeGenerate = (prompt, apiKey) => 
  api.post('/safe_generate_gemini', { text: prompt, gemini_api_key: apiKey });

export const comprehensiveCheck = (prompt) => 
  api.post('/comprehensive_check', { text: prompt });

export default api;

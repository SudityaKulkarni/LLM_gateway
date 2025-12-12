# Frontend Quick Reference

## Pages Overview

### 🛡️ Safe Generate (Home)
**Path:** `/`
**Purpose:** Main interface for safe AI generation
**Features:**
- Sanitizes potentially harmful prompts
- Runs all safety checks
- Generates AI response using Gemini
- Shows detector status dashboard
- Displays sanitized vs original prompt

**Usage:**
1. Enter your Gemini API key
2. Type your prompt
3. Click "Generate Safe Response"
4. View safety analysis and AI response

---

### 📊 Comprehensive Check
**Path:** `/comprehensive`
**Purpose:** Run all detectors without AI generation
**Features:**
- Executes all 7 safety detectors
- Shows detailed results for each detector
- Visual status dashboard
- Confidence scores and reasons

**Best For:** Testing prompts before using in production

---

### 🔓 Jailbreak Detector
**Path:** `/jailbreak`
**Purpose:** Detect attempts to bypass AI safety measures
**Detects:**
- DAN prompts
- Role-playing attacks
- System prompt override attempts
- Instruction manipulation

---

### ☠️ Toxicity Detector
**Path:** `/toxicity`
**Purpose:** Identify toxic and harmful language
**Detects:**
- Offensive language
- Hate speech
- Threats
- Harassment

---

### 🔒 PII Detector
**Path:** `/pii`
**Purpose:** Find personally identifiable information
**Detects:**
- Email addresses
- Phone numbers
- SSN (US)
- Aadhar numbers (India)
- Credit card numbers
- IP addresses
- API keys
- AWS keys

---

### 💉 Prompt Injection Detector
**Path:** `/injection`
**Purpose:** Detect malicious prompt injections
**Detects:**
- Instruction override attempts
- System prompt leaking
- Command injection
- Hidden instructions

---

### 🔤 Gibberish Detector
**Path:** `/gibberish`
**Purpose:** Identify nonsensical text
**Detects:**
- Random character sequences
- Spam text
- Automated bot messages
- Encoding attacks

---

### 📈 Entropy Detector
**Path:** `/entropy`
**Purpose:** Analyze text randomness
**Measures:**
- Shannon entropy
- Character distribution
- Pattern detection
- Encoded content

---

### 📋 Rule-Based Detector
**Path:** `/rule-based`
**Purpose:** Pattern-based safety checks
**Uses:**
- Predefined keyword lists
- Regular expressions
- Custom rules
- Fast detection

---

## Components Used

### InputBox
Reusable text input with submit button
- Supports Enter key submission
- Disabled state during loading
- Custom placeholder text

### ResultCard
Displays detection results
- Color-coded (green = safe, red = flagged)
- Shows confidence scores
- Displays detailed information
- Progress bars for metrics

### DetectorStatus
Grid view of all detector results
- Compact status cards
- Visual indicators (✓ or ⚠️)
- Quick overview of all checks

### LoadingSpinner
Animated loading indicator
- Used during API calls
- Consistent across all pages

---

## API Integration

All API calls are in `src/api.js`:
- Base URL: `http://localhost:8000`
- Uses Axios for HTTP requests
- Centralized error handling
- Consistent request format

---

## Styling

**Framework:** Tailwind CSS
**Theme:**
- Dark mode (slate colors)
- Primary: Blue (#2563eb)
- Success: Green (#16a34a)
- Danger: Red (#dc2626)
- Background: Dark slate (#0f172a)

**Layout:**
- Responsive design
- Sticky header and sidebar
- Full-height layout
- Scrollable content areas

---

## Navigation

**Sidebar Menu:**
- Fixed on larger screens
- Responsive on mobile
- Active page highlighting
- Icon + label format

**Routes:**
All routes handled by React Router v6
- Client-side navigation
- No page reloads
- Browser history support

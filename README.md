# 🌐 Web Page Indexer — Smart Web Content Management

![Build](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square)


A sleek and intelligent system combining a **Chrome extension** with a **FastAPI-powered Python backend** to help you index, manage, and semantically search through web content you've visited — all in real-time.

## 🚀 Overview

**Web Page Indexer** is your personal web memory. It continuously monitors and stores key content from pages you visit and empowers you to ask natural language questions to retrieve past insights, summaries, and sources.

---

## ✨ Key Features

- 🔎 **Automatic Indexing**: Seamlessly track and capture content from visited web pages.
- 🧠 **Semantic Search**: Search using natural language — not just keywords.
- 📚 **Context-Aware Summaries**: Get intelligent summaries with contextual awareness.
- ⚡ **Real-Time Processing**: Instant indexing and search without delays.
- 🌍 **Cross-Platform Support**: Works on any OS running Google Chrome.
- 🛠️ **Smart Query Refinement**: AI-powered suggestions to improve your queries.
- 🔗 **URL Status Tracking**: Keep tabs on which URLs are indexed and their status.

---

## 🧩 Repository Structure

```bash
.
├── chrome_extension/           # Chrome Extension frontend
│   ├── manifest.json           # Extension configuration (Manifest V3)
│   ├── popup.html              # UI for extension popup
│   ├── popup.js                # Extension popup logic
│   ├── background.js           # Service worker for background tasks
│   └── styles.css              # CSS styling for extension
│
└── python_server/              # Python backend (FastAPI)
    ├── agent.py                # Main FastAPI app
    ├── test_backend.py         # Unit tests
    └── utils/                  # Core utility modules
        ├── model.py            # Data models
        ├── memory.py           # Memory management
        ├── perception.py       # Page content processor
        └── prompt.py           # Prompt generation and AI logic
```

---

## 🛠️ Getting Started

### ✅ Prerequisites

- [Google Chrome](https://www.google.com/chrome/)
- Python 3.10+
- [UV package manager](https://github.com/astral-sh/uv)

### ⚙️ Setting Up the Python Backend

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>/python_server

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv pip install --requirement uv.lock
```

Create a `.env` or `token.env` file with your API credentials:

```env
API_TOKEN=your_api_key_here
```

Run the backend server:

```bash
uv run agent.py
```

Your server will be available at: `http://localhost:8000`

---

### 🧩 Installing the Chrome Extension

1. Go to `chrome://extensions/` in Chrome
2. Enable **Developer Mode** (top-right toggle)
3. Click **Load unpacked**
4. Select the `chrome_extension` folder from the repository
5. Extension icon should now appear in the Chrome toolbar

---

## 💡 How to Use

1. Open the extension by clicking its icon in the toolbar.
2. Start browsing — pages are indexed automatically in the background.
3. Type natural language queries into the popup search bar.
4. Instantly receive summarized results with links to original content.

---

## 🔧 Development Notes

- **Backend**: Built using [FastAPI](https://fastapi.tiangolo.com/) for high-performance async APIs.
- **Frontend**: Chrome Extension using Manifest V3.
- **AI Engine**: Powered by Google's Generative AI and custom semantic processing.
- **Memory Handling**: Advanced memory management in `utils/memory.py`.

---

## 🤝 Contributing

Contributions are welcome! Whether it's a bug fix, a feature request, or a new idea — open a pull request or submit an issue.

---

## 📄 License

MIT License. See `LICENSE` file for details.

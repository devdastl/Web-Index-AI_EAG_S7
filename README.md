# Web Page Indexer - Smart Web Content Management

A powerful Chrome extension paired with a Python backend that helps you index and semantically search through web pages you've visited. This tool automatically processes web pages, converts them to a searchable format, and allows you to perform intelligent searches across your indexed content.

## Features

- **Automatic Web Page Indexing**: Automatically indexes web pages you visit through the Chrome extension
- **Semantic Search**: Perform natural language searches across your indexed content
- **Smart Context Retrieval**: Get relevant context and summaries from your indexed pages
- **Cross-Platform Support**: Works on any platform that supports Chrome
- **Real-time Processing**: Instant indexing and search capabilities
- **Intelligent Query Refinement**: Uses AI to refine and improve search queries
- **URL Management**: Keep track of processed URLs and their status

## Repository Structure

```
.
├── chrome_extension/           # Chrome Extension files
│   ├── manifest.json          # Extension configuration
│   ├── popup.html            # Extension popup interface
│   ├── popup.js              # Popup functionality
│   ├── background.js         # Background service worker
│   └── styles.css            # Extension styling
│
└── python_server/            # Backend server
    ├── agent.py             # Main FastAPI server
    ├── test_backend.py      # Backend tests
    └── utils/               # Utility modules
        ├── model.py         # Data models
        ├── memory.py        # Memory management
        ├── perception.py    # Input processing
        └── prompt.py        # AI prompts
```

## Getting Started

### Prerequisites

- Google Chrome browser
- Python 3.8 or higher
- UV package manager

### Setting up the Python Backend

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>/python_server
   ```

2. Install dependencies using UV:
   ```bash
   # Install UV if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies from uv.lock and pyproject.toml
   uv pip install --requirement uv.lock
   ```

3. Create a `token.env` file in the root directory with your API credentials:
   ```
   API_TOKEN=your_api_key_here
   ```

4. Start the backend server:
   ```bash
   uv run agent.py
   ```
   The server will start at `http://localhost:8000`

### Installing the Chrome Extension

1. Open Google Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right corner
3. Click "Load unpacked" and select the `chrome_extension` directory from this repository
4. The extension icon should appear in your Chrome toolbar

## Usage

1. Click the extension icon to open the popup interface
2. Browse web pages normally - they will be automatically indexed
3. Use the search bar in the extension popup to perform semantic searches
4. View search results with relevant context and source URLs

## Development

- The backend uses FastAPI for the REST API
- The Chrome extension uses Manifest V3
- Memory management is handled through a custom implementation in `utils/memory.py`
- AI processing is done using Google's Generative AI

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

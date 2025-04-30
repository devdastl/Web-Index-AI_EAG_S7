document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('searchInput');
  const searchButton = document.getElementById('searchButton');
  const statusDiv = document.getElementById('status');
  const loadingDiv = document.getElementById('loading');
  const errorDiv = document.getElementById('error');

  const API_BASE_URL = 'http://localhost:8000';

  async function performSearch(query) {
    try {
      showLoading();
      hideError();

      const response = await fetch(`${API_BASE_URL}/api/get_context`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      
      // Open each URL in a new tab
      for (const result of data.results) {
        const tab = await chrome.tabs.create({ url: result.url });
        
        // Wait for the tab to load
        chrome.tabs.onUpdated.addListener(function listener(tabId, info) {
          if (tabId === tab.id && info.status === 'complete') {
            chrome.tabs.onUpdated.removeListener(listener);
            
            // Inject content script to highlight text
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              function: highlightText,
              args: [result.text]
            });
          }
        });
      }

      showStatus('Search completed successfully');
    } catch (error) {
      showError('Failed to perform search: ' + error.message);
    } finally {
      hideLoading();
    }
  }

  function showLoading() {
    loadingDiv.classList.remove('hidden');
    searchButton.disabled = true;
  }

  function hideLoading() {
    loadingDiv.classList.add('hidden');
    searchButton.disabled = false;
  }

  function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
  }

  function hideError() {
    errorDiv.classList.add('hidden');
    errorDiv.textContent = '';
  }

  function showStatus(message) {
    statusDiv.textContent = message;
    setTimeout(() => {
      statusDiv.textContent = '';
    }, 3000);
  }

  searchButton.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (query) {
      performSearch(query);
    } else {
      showError('Please enter a search query');
    }
  });

  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      searchButton.click();
    }
  });
});

// Function to be injected into the page for highlighting text
function highlightText(text) {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );

  const nodes = [];
  let node;
  while (node = walker.nextNode()) {
    if (node.textContent.includes(text)) {
      nodes.push(node);
    }
  }

  nodes.forEach(node => {
    const span = document.createElement('span');
    span.style.backgroundColor = 'yellow';
    span.style.color = 'black';
    span.textContent = node.textContent;
    node.parentNode.replaceChild(span, node);
  });

  // Scroll to the first highlight
  const firstHighlight = document.querySelector('span[style*="background-color: yellow"]');
  if (firstHighlight) {
    firstHighlight.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
} 
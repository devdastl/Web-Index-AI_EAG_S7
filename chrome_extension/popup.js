document.addEventListener('DOMContentLoaded', function() {
  const API_BASE_URL = 'http://your-server-ip:8000';
  
  // Get DOM elements
  const searchInput = document.getElementById('searchInput');
  const searchButton = document.getElementById('searchButton');
  const loadingDiv = document.getElementById('loading');
  const errorDiv = document.getElementById('error');
  const resultsDiv = document.getElementById('results');
  const textOutput = document.getElementById('textOutput');
  const urlList = document.getElementById('urlList');

  // Show/hide elements
  function toggleLoading(show) {
    loadingDiv.classList.toggle('hidden', !show);
    searchButton.disabled = show;
  }

  function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
  }

  function hideError() {
    errorDiv.classList.add('hidden');
    errorDiv.textContent = '';
  }

  function displayResults(data) {
    // Display the text response
    textOutput.textContent = data.text;

    // Display the URLs
    urlList.innerHTML = ''; // Clear existing URLs
    data.url.forEach(url => {
      const li = document.createElement('li');
      li.textContent = url;
      urlList.appendChild(li);
    });

    // Show results section
    resultsDiv.classList.remove('hidden');
  }

  async function performSearch(query) {
    try {
      toggleLoading(true);
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
      displayResults(data);
    } catch (error) {
      showError('Failed to perform search: ' + error.message);
    } finally {
      toggleLoading(false);
    }
  }

  // Event listeners
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

  // Focus search input when popup opens
  searchInput.focus();
}); 
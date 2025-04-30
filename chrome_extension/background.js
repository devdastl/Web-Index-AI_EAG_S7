// You can change this to your server's address
const API_BASE_URL = 'http://your-server-ip:8000';

// Initialize storage with empty set if not exists
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['processedUrls'], (result) => {
    if (!result.processedUrls) {
      chrome.storage.local.set({ processedUrls: [] });
    }
  });
});

// Monitor tab updates
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  // Only process when the page is fully loaded
  if (changeInfo.status === 'complete' && tab.url) {
    try {
      // Check if URL has been processed
      const { processedUrls } = await chrome.storage.local.get(['processedUrls']);
      
      if (!processedUrls.includes(tab.url)) {
        // Send URL to server
        const response = await fetch(`${API_BASE_URL}/api/send_url`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: tab.url }),
        });

        if (response.ok) {
          // Add URL to processed list
          processedUrls.push(tab.url);
          await chrome.storage.local.set({ processedUrls });
          
          // Show success notification
          chrome.action.setBadgeText({ text: '✓' });
          chrome.action.setBadgeBackgroundColor({ color: '#4CAF50' });
          setTimeout(() => {
            chrome.action.setBadgeText({ text: '' });
          }, 3000);
        } else {
          throw new Error('Failed to process URL');
        }
      }
    } catch (error) {
      console.error('Error processing URL:', error);
      // Show error notification
      chrome.action.setBadgeText({ text: '!' });
      chrome.action.setBadgeBackgroundColor({ color: '#F44336' });
      setTimeout(() => {
        chrome.action.setBadgeText({ text: '' });
      }, 3000);
    }
  }
});

// Check URL status
async function checkUrlStatus(url) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/get_status?url=${encodeURIComponent(url)}`);
    if (!response.ok) {
      throw new Error('Failed to check URL status');
    }
    const data = await response.json();
    return data.status;
  } catch (error) {
    console.error('Error checking URL status:', error);
    return 'error';
  }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'checkStatus') {
    checkUrlStatus(request.url)
      .then(status => sendResponse({ status }))
      .catch(error => sendResponse({ error: error.message }));
    return true; // Required for async sendResponse
  }
}); 
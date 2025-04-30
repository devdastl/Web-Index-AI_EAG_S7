// Listen for messages from the extension
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'highlight') {
    highlightText(request.text);
    sendResponse({ success: true });
  }
});

// Function to highlight text on the page
function highlightText(text) {
  // Remove any existing highlights
  const existingHighlights = document.querySelectorAll('.web-page-indexer-highlight');
  existingHighlights.forEach(el => {
    const parent = el.parentNode;
    parent.replaceChild(document.createTextNode(el.textContent), el);
    parent.normalize();
  });

  // Create a tree walker to find text nodes
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        // Skip script and style tags
        if (node.parentNode.tagName === 'SCRIPT' || 
            node.parentNode.tagName === 'STYLE') {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    },
    false
  );

  const nodes = [];
  let node;
  while (node = walker.nextNode()) {
    if (node.textContent.includes(text)) {
      nodes.push(node);
    }
  }

  // Highlight matching text
  nodes.forEach(node => {
    const span = document.createElement('span');
    span.className = 'web-page-indexer-highlight';
    span.style.backgroundColor = 'yellow';
    span.style.color = 'black';
    span.style.padding = '2px';
    span.style.borderRadius = '2px';
    span.textContent = node.textContent;
    node.parentNode.replaceChild(span, node);
  });

  // Scroll to the first highlight
  const firstHighlight = document.querySelector('.web-page-indexer-highlight');
  if (firstHighlight) {
    firstHighlight.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'center' 
    });
  }
}

// Add styles for the highlight
const style = document.createElement('style');
style.textContent = `
  .web-page-indexer-highlight {
    background-color: yellow !important;
    color: black !important;
    padding: 2px !important;
    border-radius: 2px !important;
    transition: background-color 0.3s ease !important;
  }
  .web-page-indexer-highlight:hover {
    background-color: #ffeb3b !important;
  }
`;
document.head.appendChild(style); 
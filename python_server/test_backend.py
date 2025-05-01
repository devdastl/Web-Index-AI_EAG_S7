# from utils.memory import MemoryManager

# mm_instance = MemoryManager()

# url = "https://ollama/content"
# markdown = "Ollama is a locally deployed AI model runner, designed to allow users to download and execute large language models (LLMs) directly on their personal computer, such as a MacBook or Windows machine."

# print(mm_instance.add_memory(markdown, url))

# content = mm_instance.retrieve_memories("what is ollama", 1)
# print(content, type(content))

import requests
from markitdown import MarkItDown
import os
# Initialize MarkItDown
markitdown_instance = MarkItDown()

# Test URL
url = "https://www.hostinger.in/tutorials/what-is-ollama"

# Fetch HTML content
response = requests.get(url)
html_content = response.text

#save html content to a file and get absolute file path
html_file_path = os.path.abspath("content.html")
with open(html_file_path, "w") as file:
    file.write(html_content)

# Convert HTML to markdown by passing the HTML string directly
markdown_content = markitdown_instance.convert(html_file_path)

#delete the html file
os.remove(html_file_path)

print(markdown_content.text_content, type(markdown_content.text_content))

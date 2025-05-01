from typing import List, Dict, Any
import json
import logging
from pathlib import Path
import faiss
from tqdm import tqdm
import numpy as np
import requests

EMBED_URL = "http://192.168.0.111:11434/api/embeddings"
EMBED_MODEL = "mxbai-embed-large:335m"

# Configure logger
logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, chunk_size=500, overlap=50):
        self.session_id = None
        self.chunk_size = chunk_size
        self.overlap = overlap

        file_root = Path(__file__).parent.resolve()
        self.metadata_file = file_root / "faiss_index" / "metadata.json"
        self.faiss_index_file = file_root / "faiss_index" / "index.bin"

    def __chunk_markdown__(self, text):
        size = self.chunk_size
        overlap = self.overlap
        words = text.split()
        for i in range(0, len(words), size - overlap):
            yield " ".join(words[i:i+size])

    def __get_embedding__(self, text: str) -> np.ndarray:
        response = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text})
        response.raise_for_status()
        return np.array(response.json()["embedding"], dtype=np.float32)


    def check_duplicate_url(self, given_url) -> bool:
        """Check if a memory already exists in the list"""
        metadata_list = json.loads(self.metadata_file.read_text()) if self.metadata_file.exists() else []
        if metadata_list == []:
            return False

        is_duplicate = False
        for metadata in metadata_list:
            if given_url == metadata['url']:
                is_duplicate = True
                break
        return is_duplicate

    def add_memory(self, markdown_content, url) -> bool:
        """Add a new memory item"""

        if self.check_duplicate_url(url):
            print(f"INFO: URL {url} indexing already exists")
            return True
        
        metadata = json.loads(self.metadata_file.read_text()) if self.metadata_file.exists() else []
        index = faiss.read_index(str(self.faiss_index_file)) if self.faiss_index_file.exists() else None
        print(f"INFO: metadata and index has been loaded")

        all_embeddings = []
        chunks = list(self.__chunk_markdown__(markdown_content))

        # try:
        embeddings_for_file = []
        new_metadata = []
        for i, chunk in enumerate(tqdm(chunks, desc=f"Embedding {url}")):
            embedding = self.__get_embedding__(chunk)
            embeddings_for_file.append(embedding)
            new_metadata.append({"url": url, "chunk": chunk, "chunk_id": f"{url}_{i}"})
        if embeddings_for_file:
            if index is None:
                dim = len(embeddings_for_file[0])
                index = faiss.IndexFlatL2(dim)
            index.add(np.stack(embeddings_for_file))
            metadata.extend(new_metadata)
        # except Exception as e:
        #     print(f"ERROR: Failed to process: {e}")

        self.metadata_file.write_text(json.dumps(metadata, indent=2))
        if index and index.ntotal > 0:
            faiss.write_index(index, str(self.faiss_index_file))
            print("SUCCESS", "Saved FAISS index and metadata")
        else:
            print("WARN", "No new documents or updates to process.")
        
        return True

    def retrieve_memories(self, query: str, limit: int = 1) -> List[Dict[str, str]]:

        try:
            index = faiss.read_index(str(self.faiss_index_file))
            metadata = json.loads((self.metadata_file).read_text())
            query_vec = self.__get_embedding__(query).reshape(1, -1)
            D, I = index.search(query_vec, k=limit)
            results = []
            for idx in I[0]:
                data = metadata[idx]
                results.append({"data":data['chunk'], "url":data['url']})
            return results

        except Exception as e:
            return [f"ERROR: Failed to search: {str(e)}"]
from typing import List, Dict, Any
import json
import logging
from pathlib import Path
import faiss
from tqdm import tqdm
import numpy as np
import requests
from datetime import datetime
import traceback

EMBED_URL = "http://192.168.0.111:11434/api/embeddings"
EMBED_MODEL = "mxbai-embed-large:335m"

# Configure logger
logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, chunk_size=500, overlap=50):
        self.session_id = None
        self.chunk_size = chunk_size
        self.overlap = overlap

        try:
            file_root = Path(__file__).parent.resolve()
            self.metadata_file = file_root / "faiss_index" / "metadata.json"
            self.faiss_index_file = file_root / "faiss_index" / "index.bin"
            logger.info(f"Initialized MemoryManager with chunk_size={chunk_size}, overlap={overlap}")
        except Exception as e:
            logger.error(f"Failed to initialize MemoryManager: {str(e)}")
            raise

    def __chunk_markdown__(self, text):
        try:
            size = self.chunk_size
            overlap = self.overlap
            words = text.split()
            for i in range(0, len(words), size - overlap):
                yield " ".join(words[i:i+size])
        except Exception as e:
            logger.error(f"Error in chunking markdown: {str(e)}")
            raise

    def __get_embedding__(self, text: str) -> np.ndarray:
        try:
            response = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text})
            response.raise_for_status()
            return np.array(response.json()["embedding"], dtype=np.float32)
        except requests.RequestException as e:
            logger.error(f"Failed to get embedding from API: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting embedding: {str(e)}")
            raise

    def get_datetime(self) -> str:
        try:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
        except Exception as e:
            logger.error(f"Error getting datetime: {str(e)}")
            raise

    def check_duplicate_url(self, given_url) -> bool:
        """Check if a memory already exists in the list"""
        try:
            metadata_list = json.loads(self.metadata_file.read_text()) if self.metadata_file.exists() else []
            if metadata_list == []:
                return False

            is_duplicate = False
            for metadata in metadata_list:
                if given_url == metadata['url']:
                    is_duplicate = True
                    break
            return is_duplicate
        except Exception as e:
            logger.error(f"Error checking duplicate URL: {str(e)}")
            raise

    def add_memory(self, markdown_content, url) -> bool:
        """Add a new memory item"""
        try:
            if self.check_duplicate_url(url):
                logger.info(f"URL {url} indexing already exists")
                return True
            
            metadata = json.loads(self.metadata_file.read_text()) if self.metadata_file.exists() else []
            index = faiss.read_index(str(self.faiss_index_file)) if self.faiss_index_file.exists() else None
            logger.info("Successfully loaded metadata and index")

            all_embeddings = []
            chunks = list(self.__chunk_markdown__(markdown_content))

            embeddings_for_file = []
            new_metadata = []
            for i, chunk in enumerate(tqdm(chunks, desc=f"Embedding {url}")):
                try:
                    embedding = self.__get_embedding__(chunk)
                    embeddings_for_file.append(embedding)
                    new_metadata.append({"url": url, "chunk": chunk, "chunk_id": f"{url}_{i}", "timestamp": self.get_datetime()})
                except Exception as e:
                    logger.error(f"Error processing chunk {i}: {str(e)}")
                    continue

            if embeddings_for_file:
                if index is None:
                    dim = len(embeddings_for_file[0])
                    index = faiss.IndexFlatL2(dim)
                index.add(np.stack(embeddings_for_file))
                metadata.extend(new_metadata)

            try:
                self.metadata_file.write_text(json.dumps(metadata, indent=2))
                if index and index.ntotal > 0:
                    faiss.write_index(index, str(self.faiss_index_file))
                    logger.info("Successfully saved FAISS index and metadata")
                else:
                    logger.warning("No new documents or updates to process.")
            except Exception as e:
                logger.error(f"Failed to save index and metadata: {str(e)}")
                raise
            
            return True

        except Exception as e:
            logger.error(f"Error in add_memory: {str(e)}\n{traceback.format_exc()}")
            raise

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
            logger.info(f"Successfully retrieved {len(results)} memories")
            return results

        except Exception as e:
            logger.error(f"Error retrieving memories: {str(e)}\n{traceback.format_exc()}")
            return [f"ERROR: Failed to search: {str(e)}"]
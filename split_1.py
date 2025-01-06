from langchain.docstore.document import Document
from typing import List
from langchain.document_loaders.base import BaseLoader
import re

class CustomMarkdownSplitter(BaseLoader):
    def __init__(self, file_path: str, max_chunk_size: int = 2000):
        self.file_path = file_path
        self.max_chunk_size = max_chunk_size

    def split_chunk(self, chunk: str, header: str, chunk_index: int) -> List[Document]:
        docs = []
        if len(chunk) <= self.max_chunk_size:
            return [Document(
                page_content=chunk,
                metadata={
                    "source": self.file_path,
                    "header": header,
                    "chunk": chunk_index,
                    "is_code": chunk.startswith('```')
                }
            )]
        
        sentences = re.split(r'(?<=[.!?])\s+', chunk)
        current_doc = ""
        
        for sentence in sentences:
            if len(current_doc) + len(sentence) > self.max_chunk_size:
                if current_doc:
                    docs.append(Document(
                        page_content=current_doc.strip(),
                        metadata={
                            "source": self.file_path,
                            "header": header,
                            "chunk": chunk_index,
                            "is_code": False
                        }
                    ))
                current_doc = sentence
            else:
                current_doc += " " + sentence if current_doc else sentence
                
        if current_doc:
            docs.append(Document(
                page_content=current_doc.strip(),
                metadata={
                    "source": self.file_path,
                    "header": header,
                    "chunk": chunk_index,
                    "is_code": False
                }
            ))
            
        return docs

    def load(self) -> List[Document]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        chunks = re.split(r'(?=^#|\n#|\n```)', text)
        docs = []
        
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
                
            lines = chunk.split('\n', 1)
            header_match = re.match(r'^#+\s*(.+)$', lines[0])
            header = header_match.group(1) if header_match else f"Section {i+1}"
            
            docs.extend(self.split_chunk(chunk, header, i))
            
        return docs

def split_karo():
    file_path = "data2.md"
    loader = CustomMarkdownSplitter(file_path)
    docs = loader.load()
    return docs

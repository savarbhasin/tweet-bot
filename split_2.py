from typing import List, Tuple
from langchain.docstore.document import Document

class CustomMarkdownSplitter:
    def __init__(self, max_chunk_size: int = 2000):
        self.max_chunk_size = max_chunk_size

    def split_on_headers(self, text: str, headers_to_split_on: List[str]) -> List[Tuple[str, str]]:
        """Split text based on specified headers."""
        chunks = []
        current_header = None
        current_chunk = []
        
        for line in text.splitlines():
            if any(line.startswith(header) for header in headers_to_split_on):
                if current_chunk:
                    chunks.append((current_header, "\n".join(current_chunk)))
                current_header = line.strip()
                current_chunk = []
            else:
                current_chunk.append(line)
        
        if current_chunk:
            chunks.append((current_header, "\n".join(current_chunk)))
        
        return chunks

    def split_large_chunks(self, chunks: List[Tuple[str, str]], file_path: str) -> List[Document]:
        """Split chunks exceeding max_chunk_size into smaller ones."""
        split_chunks = []
        for header, content in chunks:
            if len(content) <= self.max_chunk_size:
                split_chunks.append(Document(
                    page_content=content,
                    metadata={
                        "source": file_path,
                        "header": header,
                        "is_code": content.startswith('```')
                    }
                ))
            else:
                lines = content.splitlines()
                temp_chunk = []
                current_size = 0

                for line in lines:
                    line_length = len(line) + 1 
                    if current_size + line_length > self.max_chunk_size:
                        split_chunks.append(Document(
                            page_content="\n".join(temp_chunk),
                            metadata={
                                "source": file_path,
                                "header": header,
                                "is_code": "\n".join(temp_chunk).startswith('```')
                            }
                        ))
                        temp_chunk = []
                        current_size = 0
                    
                    temp_chunk.append(line)
                    current_size += line_length

                if temp_chunk:
                    split_chunks.append(Document(
                        page_content="\n".join(temp_chunk),
                        metadata={
                            "source": file_path,
                            "header": header,
                            "is_code": "\n".join(temp_chunk).startswith('```')
                        }
                    ))
        
        return split_chunks

    def process_markdown(self, text: str, headers_to_split_on: List[str], file_path: str) -> List[Document]:
        """Process the markdown file."""
        initial_chunks = self.split_on_headers(text, headers_to_split_on)
        final_chunks = self.split_large_chunks(initial_chunks, file_path)
        return final_chunks

def split_karo_2():
    file_path = "data2.md" 

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    splitter = CustomMarkdownSplitter(max_chunk_size=2000)
    headers_to_split_on = ["##"]  
    chunks = splitter.process_markdown(markdown_content, headers_to_split_on, file_path)

    return chunks

"""Simple reader that reads wikipedia."""
from typing import Any, List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class KnowAlmostReader(BaseReader):
    """KnowAlmost reader.

    Reads a page.

    """

    def load_data(self, query: str, token, **load_kwargs: Any) -> List[Document]:
        """Load data from the input directory.

        Args:
            pages (List[str]): List of pages to read.

        """
        from setup import api

        results = []
        page_content = api.request(query=query, token=token).content
        results.append(Document(page_content))
        return results

import os
import re
from os import PathLike

from Document import Document


class Corpus:

    def __init__(self, root_directory: str | bytes | PathLike[str]):
        self.root_directory = root_directory
        self.documents: [Document] = self.load_documents_from_text_files(root_directory)

    def load_documents_from_text_files(self, root_path: str | bytes | PathLike[str], recursive=True) -> [Document]:
        documents = []

        directory_entries = os.scandir(root_path)

        directory_entry: os.DirEntry

        txt_pattern = re.compile("\\.txt$")

        for directory_entry in directory_entries:
            if directory_entry.is_dir() and recursive:
                documents += self.load_documents_from_text_files(directory_entry, recursive)
            elif re.search(txt_pattern, directory_entry.name) is not None:
                documents.append(Document(directory_entry.path))

        return documents

    def generate_inverted_index(self) -> {str: {int: int}}:
        inverted_index = {}

        for (document_index, document) in enumerate(self.documents):
            for word in document.words:
                if word not in inverted_index:
                    inverted_index[word] = {}

                if document_index not in inverted_index[word]:
                    inverted_index[word][document_index] = 0

                inverted_index[word][document_index] += 1

        return inverted_index

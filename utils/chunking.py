from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import config


class TextChunker:
    """
    Enterprise Text Chunking Service

    Responsibilities:
    -----------------
    1. Split documents into chunks
    2. Maintain chunk configuration
    3. Support future chunking strategies
    """

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=config.CHUNK_SIZE,

            chunk_overlap=config.CHUNK_OVERLAP,

            separators=[

                "\n\n",

                "\n",

                ". ",

                " ",

                ""

            ]

        )

    def chunk_documents(self, documents):

        return self.text_splitter.split_documents(

            documents

        )


# ======================================================
# Singleton Instance
# ======================================================

text_chunker = TextChunker()
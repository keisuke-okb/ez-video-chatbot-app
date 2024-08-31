import os
import numpy as np

from llama_index.embeddings.openai import OpenAIEmbedding

from constants import Constants

os.environ["OPENAI_API_KEY"] = Constants.OPENAI_API_KEY


def main():
    embed_model = OpenAIEmbedding(
        model="text-embedding-3-large"
    )
    

if __name__ == '__main__':
    main()
# humleaf
A collection of GPT-based examples and tutorials, featuring libraries and frameworks such as Langchain, Tiktoken, LlamaIndex etc. to empower developers in building innovative plugins and applications with ChatGPT.

## Getting Started

Instructions for setting up the project and running the examples will be provided here.

## Contributing

Guidelines for contributing to the project will be provided here.

## License

This project is licensed under the [LICENSE NAME] - see the [LICENSE](LICENSE) file for details.

## ToDo

- download langchain documents
- embed using gpt3.5 and store in QDran vector store


## Technical Details

- Document Loaders
    - ReadTheDocsLoader
    - PythonLoader

- Text Splitters
    - tiktoken
        - chunk size, chunk overlap, metadata, length_function
    - PythonCodeTextSplitter


- Indexers


- Retrievers


## Findings and Learnings
- tiktoken is the best text splitter for openAI embeddings. However, if a document contains a combination of texts and code snippets, we might need a better split approach between code and text. For example - PythonCodeTextSplitter + tiktoken?
- Whats the best chunking/splitting strategy? What should be the length and overlap?


## Resources
- https://python.langchain.com/en/latest/youtube.html
- https://www.youtube.com/watch?v=Ix9WIZpArm0
- https://github.com/pinecone-io/examples/blob/master/generation/chatgpt/plugins/langchain-docs-plugin.ipynb
- https://python.langchain.com/en/latest/modules/indexes/getting_started.html
- https://github.com/menloparklab/langchain-cohere-qdrant-doc-retrieval/blob/main/app.py
- https://karpathy.ai/zero-to-hero.html
- https://github.com/pinecone-io/examples/blob/master/generation/chatgpt/plugins/langchain-docs-plugin.ipynb
- https://e2eml.school/transformers.html

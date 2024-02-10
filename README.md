# Microsoft Azure solution architecture brainstorming buddy
A chat app with Microsoft Azure architectures to discover answer to architecture questions on Azure

# Description
Microsoft Azure solution architecture brainstorming buddy aims to find answers to your queries on Azure architectures especially on analytics use cases. 

Relevant Azure architectures were identified from the [Azure Architecture Centre](https://learn.microsoft.com/en-us/azure/architecture). The content from these links were downloaded and post processed by splitting the text and adding metadata. Embeddings for the text content was generated using [Sentence transformers](https://www.sbert.net/). The final output was stored locally in [ChromaDB](https://www.trychroma.com/).

The chat app developed using [Streamlit](https://streamlit.io/) has 2 prompts which are sent to OpenAI's chat completion models. The first prompt is used to generate a highly relevant search query to get the relevant documents from ChromaDB based on the current conversation. The second prompt is used to synthesize an answer for the user query using the relevant documents. Prompts are stored as [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/) for faster iteration.
The final search results are streamed to the user for lower perceived latency.

The main beneficiaries of this app would be the solution architects or Azure developers in different enterprises who need a brainstorming buddy to come up with an initial architecture for a solution in Azure with references from existing successful Microsoft Azure solution implementations.

# Going forward
The same could be implemented in the Microsoft Azure ecosystem where both the chat completion and embeddings models are deployed in Azure OpenAI. The vector database ChromaDB can be replaced by the more powerful [Azure AI search service](https://azure.microsoft.com/en-us/products/ai-services/ai-search). The streamlit app itself could be deployed to [Azure App Service](https://azure.microsoft.com/en-us/products/app-service) with user authentication via [Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/).
The performance of the application itself could be further improved by extracting topics and tags from the articles and creating a knowledge graph by combining such topics and tags using a data Ontology. During the query the user's question could then find the relevant articles both from the vector database and the knowledge graph and the final answer is derived from a combination of the 2 results.


# How to set secrets

1. Set up OpenAI API key as a streamlit secret
- Create `.streamlit/secrets.toml` file in the project/current directory and add the following lines to it:

`OPENAI_API_KEY = "YOUR_API_KEY"`

# How to run the chat application
1. Install [poetry](https://python-poetry.org/)
2. `poetry install` to install all packages required to run the chat application
3. Set up ChromaDB index:
    - Create a directory called `data` inside this project directory
    - Download and extract the contents from [here](https://drive.google.com/drive/folders/1Kao9bWSSNpUIT8nRIph4fQlLJlBPc1Ui?usp=sharing) and copy the same inside the `data` directory
    - Ensure the directory name after the above extraction is `chroma` inside the `data` directory
4. `make run-app` to start the chat app
5. Navigate to `http://localhost:8501/` in your favourite browser

# Configurations
- Update the `configs.py` file to update the current configurations

# Sample conversation
- What are some ways of supporting high number of concurrent users in Azure?
- What if the users are distributed across geographies?
- How can we deploy forecasting models in Azure?

# Useful links
- [Demo video](https://youtu.be/A-sTTBofIA4)
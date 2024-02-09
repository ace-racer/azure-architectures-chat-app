# azure-architectures-chat-app
A chat app with Azure architectures to discover answer to architecture questions on Azure


# How to set secrets

1. Set up OpenAI API key as a streamlit secret
- Create `.streamlit/secrets.toml` file in the project/current directory and add the following lines to it:

`OPENAI_API_KEY = "YOUR_API_KEY"`

# How to run the chat application
1. Install [poetry](https://python-poetry.org/)
2. `poetry install` to install all packages
3. `make run-app` to run app


# Sample conversation
- What are some ways of supporting high number of concurrent users in Azure?
- What if the users are distributed across geographies?
- How can we deploy forecasting models in Azure?
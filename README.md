# Blaxel Agent - Blog Post Generator

<p align="center">
  <img src="https://blaxel.ai/logo.png" alt="Blaxel"/>
</p>

A template implementation of an automated blog post generator built using the [Blaxel SDK](https://blaxel.ai).

## How it works

This agent creates comprehensive blog posts on any given topic by:

1. Analyzing the topic and generating a content outline
2. Performing targeted web searches using Exa for research
3. Writing engaging blog content with proper structure and SEO optimization
4. Generating relevant illustrations using AI image generation
5. Publishing the complete post to a Notion database

The implementation uses LangGraph for orchestrating the blog creation workflow. It leverages GPT-4 for content generation, Exa search API for research, an AI image generation service for illustrations, and the Notion API for publishing.

### Key Features

- Automated blog post planning and writing
- SEO-optimized content generation
- Web research integration via Exa
- AI-generated custom illustrations
- Direct publishing to Notion database
- Proper citation and source attribution

## Prerequisites

- **Python:** 3.12 or later
- **UV:** An extremely fast Python package and project manager, written in Rust
- **Blaxel CLI:** Ensure you have the Blaxel CLI installed. If not, install it globally:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/beamlit/toolkit/main/install.sh | BINDIR=$HOME/.local/bin sh
  ```
- **Blaxel login:** Login to Blaxel platform
  ```bash
    bl login YOUR-WORKSPACE
  ```

## Installation

- **Clone the repository and install the dependencies**:

  ```bash
  git clone https://github.com/beamlit/template-notion-blog-writer.git
  cd template-notion-blog-writer
  uv sync
  ```

- **Environment Variables:** Create a `.env` file with your configuration. You can begin by copying the sample file:

  ```bash
  cp .env-sample .env
  ```

  Then, update the following values with your own credentials:

  - Notion: `NOTION_TOKEN`, `NOTION_DATABASE_ID`
  - Open AI: `OPENAI_API_KEY`
  - Exa: `EXA_API_KEY`

- **Blaxel apply:** register your integration connection / functions / models on blaxel.ai
  ```bash
  bl apply -R -f .blaxel
  ```

## Running the Server Locally

Start the development server with hot reloading using the Blaxel CLI command:

```bash
bl serve --hotreload
```

_Note:_ This command starts the server and enables hot reload so that changes to the source code are automatically reflected.

## Testing the agent

The server will start on port 1338. You can test the agent using the Blaxel CLI:

```bash
bl run agent my-agent --local --data '{"input": "Write a blog post about AI in healthcare"}'
OR
bl chat my-agent --local
```

## Deploying to Blaxel

When you are ready to deploy your application, run:

```bash
bl deploy
```

This command uses your code and the configuration files under the `.blaxel` directory to deploy your application.

## Project Structure

- **src/**
  - `agent.py` - Configures the blog post agent, manages workflow, and handles API integrations
  - `functions/` - Custom functions (Notion)
  - `functions/notion.py` - Notion API integration and publishing logic
- **.blaxel/** - Contains configuration files for Blaxel functions and models to use in the agent (OpenAI and Exa)
- **pyproject.toml** - UV package manager file

## Acknowledgements

- **Langchain:** For providing the LangGraph framework
- **OpenAI:** For GPT-4 and DALL-E capabilities
- **Notion:** For their API and content publishing
- **Exa:** For powerful web search capabilities

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

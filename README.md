# Blaxel Agent - Blog Post Generator

A template implementation of an automated blog post generator using LangGraph and GPT-4. This agent creates comprehensive blog posts on any given topic by:

1. Analyzing the topic and generating a content outline
2. Performing targeted web searches using Exa for research
3. Writing engaging blog content with proper structure and SEO optimization
4. Generating relevant illustrations using AI image generation
5. Publishing the complete post to a Notion database

The implementation uses LangGraph for orchestrating the blog creation workflow. It leverages GPT-4 for content generation, Exa search API for research, an AI image generation service for illustrations, and the Notion API for publishing.

## Key Features

* Automated blog post planning and writing
* SEO-optimized content generation
* Web research integration via Exa
* AI-generated custom illustrations
* Direct publishing to Notion database
* Proper citation and source attribution

## Acknowledgements

* **Langchain:** For providing the LangGraph framework
* **OpenAI:** For GPT-4 and DALL-E capabilities
* **Notion:** For their API and content publishing
* **Exa:** For powerful web search capabilities

## Prerequisites

* **Python:** 3.12 or later
* **UV:** An extremely fast Python package and project manager, written in Rust
* **Blaxel CLI:** Ensure you have the Blaxel CLI installed. If not, install it globally:

```bash 
curl -fsSL https://raw.githubusercontent.com/beamlit/toolkit/main/install.sh | BINDIR=$HOME/.local/bin sh
```

## Development Setup

If you want to modify the agent or contribute to its development:

1. **Clone the repository**:

```bash
git clone https://github.com/beamlit/template-notion-blog-writer.git
cd template-notion-blog-writer
```

2. **Install dependencies**:

```bash
uv sync
```

3. **Set up your environment variables**:
Create a `.env` file with your API keys:

```bash
EXA_API_KEY=your_exa_key
OPENAI_API_KEY=your_openai_key
NOTION_API_KEY=your_notion_key
NOTION_DATABASE_ID=your_database_id
```

4. **Register your integration**:

```bash
bl apply -R -f .blaxel
```

5. **Start development server**:

```bash
bl serve --hotreload
```

## Testing

Test the agent locally using either:

Interactive chat mode

```bash
bl chat --local blog-writer
```

Or direct execution

```bash
bl run agent blog-writer --local --data '{"input": "Write a blog post about AI in healthcare"}'
```

## Deployment

1. **Deploy to Blaxel Hub**:

```bash
bl deploy
```

## Project Structure

* **src/**
  * `agent.py` - Configures the blog post agent, manages workflow, and handles API integrations
  * `notion.py` - Notion API integration and publishing logic
  * `functions/` - Custom functions (Notion)
* **.blaxel/** - Contains configuration files for Blaxel functions and models to use in the agent (OpenAI and Exa)
* **pyproject.toml** - UV package manager file

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

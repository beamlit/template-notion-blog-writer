import uuid
from logging import getLogger
from typing import Union

from blaxel.agents import agent, get_default_thread
from fastapi import Request
from langgraph.graph.graph import CompiledGraph

logger = getLogger(__name__)

@agent(
    agent={
        "metadata": {
            "name": "blog-writer",
        },
        "spec": {
            "model": "gpt-4o",
            "description": "Automated blog post generator using LangGraph and GPT-4",
            "runtime": {
                "envs": [
                    {
                    "name": "NOTION_TOKEN",
                    "value": "${secrets.NOTION_TOKEN}",
                },
                {
                    "name": "NOTION_DATABASE_ID",
                    "value": "${secrets.NOTION_DATABASE_ID}",
                }
                ]
            }
        }
    },
    remote_functions=["exa", "dall-e"]
)
async def main(request: Request, agent: Union[None, CompiledGraph]):
    body = await request.json()
    thread_id = get_default_thread(request) or str(uuid.uuid4())
    agent_config = {"configurable": {"thread_id": thread_id}}

    if body.get("inputs"):
        body["input"] = body["inputs"]

    prompt = f"""Write a comprehensive blog post about: {body['input']}

    Follow these steps in order:
    1. First, generate an appropriate cover image using DALL-E that represents the topic visually.
       Create a prompt that will generate a professional, tech-focused image suitable for a blog.
       Store the image URL separately - do not include it in the blog content.

    2. Then create a well-structured post with:
       - A catchy main title using # (single hash)
       - An engaging introduction (no header) that goes straight into the topic
       - Main content sections using ### (triple hash) for all section headings
       - A thoughtful conclusion with ### Conclusion

    3. Finally, use the create_notion_post function to save it, making sure to:
       - Pass the title as the first argument
       - Pass the formatted content as the second argument
       - Pass the DALL-E generated image URL as the cover_image_url argument

    Important formatting rules:
    - Use a single # for the main title
    - Use ### for all section headings
    - Do not include the image URL or any image markdown in the blog content itself
    - You can use lists with bullet points or numbered lists
    - Do not repeat the title or topic as a heading in the content
    - Maintain consistent spacing between sections

    Remember to maintain a professional and technical tone throughout the post."""

    agent_body = {"messages": [("user", prompt)]}
    responses = []

    async for chunk in agent.astream(agent_body, config=agent_config):
        responses.append(chunk)

    final_response = responses[-1]["agent"]["messages"][-1]
    logger.debug(f"Agent response type: {type(final_response)}")  # Debug print
    logger.debug(f"Agent response: {final_response}")  # Debug print
    return {"response": final_response.content}

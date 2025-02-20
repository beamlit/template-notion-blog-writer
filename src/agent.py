import uuid
from typing import Union
from fastapi import Request
from langgraph.graph.graph import CompiledGraph
from blaxel.agents import agent, get_default_thread
from functions.notion import create_notion_post

@agent(
    agent={
        "metadata": {
            "name": "blog-writer",
        },
        "spec": {
            "model": "gpt-4o",
            "description": """You are a professional technical blog post writer in the field of AI. You can search the web for information. Your task is to:
            1. Understand the topic provided by the user
            2. Generate an appropriate cover image using DALL-E
            3. Create a well-structured, engaging blog post about that topic
            4. The blog post must include:
               - A cover image to illustrate the blog post (generated with DALL-E)
               - A short and catchy title
               - An introduction
               - Main content with proper headings
               - A conclusion
            5. The content should be informative, engaging, and well-researched
            6. After writing the post, use the create_notion_post function to save it to Notion
               by passing the title, content, and cover_image_url.""",
            "functions": [create_notion_post]
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
    
    try:
        final_response = responses[-1]["agent"]["messages"][-1]
        print(f"Agent response type: {type(final_response)}")  # Debug print
        print(f"Agent response: {final_response}")  # Debug print
        return {"response": final_response.content}
    except Exception as e:
        print(f"Agent error: {str(e)}")  # Debug print
        return {"error": str(e)}

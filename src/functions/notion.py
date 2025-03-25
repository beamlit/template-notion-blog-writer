import os
import re
from logging import getLogger

from blaxel.functions import function
from notion_client import Client

logger = getLogger(__name__)

def chunk_content(content: str, max_length: int = 2000) -> list:
    """Split content into chunks of maximum length."""
    return [content[i:i + max_length] for i in range(0, len(content), max_length)]

def markdown_to_notion_blocks(markdown_text: str) -> list:
    """Convert markdown text to Notion blocks following official API structure."""
    blocks = []

    # Split content into paragraphs
    paragraphs = markdown_text.split('\n')

    i = 0
    while i < len(paragraphs):
        paragraph = paragraphs[i].strip()
        if not paragraph:
            i += 1
            continue

        # Handle headers
        if paragraph.startswith('#'):
            header_level = len(paragraph.split()[0])  # Count the number of #
            header_text = paragraph.lstrip('#').strip()

            if header_level <= 3:  # Notion supports h1, h2, h3
                blocks.append({
                    "object": "block",
                    "type": f"heading_{header_level}",
                    f"heading_{header_level}": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": header_text}
                        }]
                    }
                })
            else:  # Fallback to paragraph for h4 and beyond
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": header_text},
                            "annotations": {"bold": True}
                        }]
                    }
                })
            i += 1
            continue

        # Handle numbered lists
        numbered_match = re.match(r'^\d+\.\s+(.+)$', paragraph)
        if numbered_match:
            current_list_type = "numbered"
            content = numbered_match.group(1)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": process_inline_formatting(content)
                }
            })
            i += 1
            continue

        # Handle bullet points
        if paragraph.startswith('- ') or paragraph.startswith('* '):
            current_list_type = "bulleted"
            content = paragraph[2:].strip()
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": process_inline_formatting(content)
                }
            })
            i += 1
            continue

        # Handle regular paragraphs
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": process_inline_formatting(paragraph)
            }
        })
        i += 1

    return blocks

def process_inline_formatting(text: str) -> list:
    """Process inline text formatting including bold, italic, and code."""
    formatted_text = []

    # Pattern for finding formatted text segments
    pattern = r'(\*\*.*?\*\*|\*.*?\*|`.*?`|[^*`]+)'

    segments = re.findall(pattern, text)

    for segment in segments:
        if segment.startswith('**') and segment.endswith('**'):
            # Bold text
            formatted_text.append({
                "type": "text",
                "text": {"content": segment[2:-2]},
                "annotations": {
                    "bold": True,
                    "italic": False,
                    "code": False
                }
            })
        elif segment.startswith('*') and segment.endswith('*'):
            # Italic text
            formatted_text.append({
                "type": "text",
                "text": {"content": segment[1:-1]},
                "annotations": {
                    "bold": False,
                    "italic": True,
                    "code": False
                }
            })
        elif segment.startswith('`') and segment.endswith('`'):
            # Code text
            formatted_text.append({
                "type": "text",
                "text": {"content": segment[1:-1]},
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "code": True
                }
            })
        else:
            # Regular text
            if segment.strip():
                formatted_text.append({
                    "type": "text",
                    "text": {"content": segment},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "code": False
                    }
                })

    return formatted_text

@function(
    function={
        "spec": {
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
    }
)
async def create_notion_post(title: str, content: str, cover_image_url: str = None) -> dict:
    """Creates a new blog post in Notion with an optional cover image.

    Args:
        title: The title of the blog post
        content: The markdown content of the blog post
        cover_image_url: Optional URL for the cover image
    """
    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not token or not database_id:
        raise ValueError("Missing Notion configuration")

    notion = Client(auth=token)
    notion_blocks = markdown_to_notion_blocks(content)

    # Prepare the page creation parameters
    page_params = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": title}}]
            }
        },
        "children": notion_blocks
    }

    # Add cover image if URL is provided
    if cover_image_url:
        page_params["cover"] = {
            "type": "external",
            "external": {
                "url": cover_image_url
            }
        }

    new_page = notion.pages.create(**page_params)

    return {
        "page_id": new_page["id"],
        "url": f"https://notion.so/{new_page['id'].replace('-', '')}",
        "status": "success",
        "message": "Blog post created successfully!"
    }
from beamlit.functions import function


@function()
async def helloworld(query: str):
    """
    Say hello to the world from beamlit
    """
    return "Hello from Beamlit"

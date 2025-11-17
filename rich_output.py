from rich.console import Console
from rich.markdown import Markdown

console = Console()

def render_rich_output(text):
    """
    Render text as rich Markdown output. Suppress for CLI.
    """
    # Suppress rich output for CLI to avoid clutter
    return text  # Return plain text for compatibility

def print_rich(text):
    """
    Print text with rich formatting.
    """
    console.print(text)

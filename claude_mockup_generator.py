import anthropic
import json
import os
from typing import Optional


class ClaudeMockupGenerator:
    def __init__(self, api_key: str):
        """
        Initialize the Claude Mockup Generator with an API key.

        Args:
            api_key (str): Your Anthropic API key
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5"

    def generate_mockup(self, prompt: str, max_tokens: int = 1024) -> str:
        """
        Generate a mockup using Claude Sonnet 4.5 based on the provided prompt.

        Args:
            prompt (str): Description of the mockup you want to generate
            max_tokens (int): Maximum number of tokens in the response

        Returns:
            str: Generated mockup content
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            return f"Error generating mockup: {str(e)}"

    def generate_html_mockup(self, description: str, max_tokens: int = 2048) -> str:
        """
        Generate an HTML mockup based on a description.

        Args:
            description (str): Description of the HTML mockup
            max_tokens (int): Maximum number of tokens in the response

        Returns:
            str: Generated HTML mockup
        """
        prompt = f"""
        Create an HTML mockup based on the following description:
        {description}

        Please provide only the HTML code (without markdown code blocks) that includes:
        1. Basic HTML structure with appropriate tags
        2. Inline CSS styling for visual presentation
        3. Responsive design elements where appropriate
        4. Placeholder content where needed

        Do not include any explanations, just the HTML code.
        """

        return self.generate_mockup(prompt, max_tokens)

    def generate_ui_component(
        self, component_type: str, description: str, max_tokens: int = 1024
    ) -> str:
        """
        Generate a specific UI component.

        Args:
            component_type (str): Type of UI component (e.g., "button", "form", "card")
            description (str): Specific description of the component
            max_tokens (int): Maximum number of tokens in the response

        Returns:
            str: Generated UI component code
        """
        prompt = f"""
        Create a {component_type} component based on the following description:
        {description}

        Please provide only the code (HTML/CSS/JS as appropriate) without any explanations.
        If it's a visual component, include styling to make it look professional.
        """

        return self.generate_mockup(prompt, max_tokens)


def main():
    # Initialize the generator with your API key from environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return

    generator = ClaudeMockupGenerator(api_key)

    # Example usage
    print("Claude Sonnet 4.5 Mockup Generator")
    print("=" * 40)

    # Generate a simple HTML mockup
    html_mockup = generator.generate_html_mockup(
        "A modern landing page for a tech startup with a navigation bar, hero section with call-to-action buttons, features section, and footer."
    )
    print("Generated HTML Mockup:")
    print(html_mockup)
    print("\n" + "=" * 40 + "\n")

    # Generate a specific UI component
    button_component = generator.generate_ui_component(
        "button",
        "A primary call-to-action button with hover effects in a modern gradient style",
    )
    print("Generated Button Component:")
    print(button_component)


if __name__ == "__main__":
    main()

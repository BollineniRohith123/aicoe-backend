import anthropic
import json
import os
from typing import Optional
from datetime import datetime


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

    def save_to_file(self, content: str, filename: str) -> str:
        """
        Save content to a file with a timestamp.

        Args:
            content (str): Content to save
            filename (str): Base filename

        Returns:
            str: Path to the saved file
        """
        # Create outputs directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)

        # Add timestamp to filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        filename_with_timestamp = f"{name}_{timestamp}{ext}"

        file_path = os.path.join("outputs", filename_with_timestamp)

        with open(file_path, "w") as f:
            f.write(content)

        return file_path


def main():
    # Initialize the generator with your API key from environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return
    generator = ClaudeMockupGenerator(api_key)

    print("Claude Sonnet 4.5 Mockup Generator")
    print("=" * 40)

    # Generate a simple HTML mockup
    print("Generating HTML mockup...")
    html_mockup = generator.generate_html_mockup(
        "A modern landing page for a tech startup with a navigation bar, hero section with call-to-action buttons, features section, and footer."
    )

    # Save to file
    html_file_path = generator.save_to_file(html_mockup, "tech_startup_landing.html")
    print(f"Generated HTML Mockup saved to: {html_file_path}")
    print("\n" + "=" * 40 + "\n")

    # Generate a specific UI component
    print("Generating UI component...")
    button_component = generator.generate_ui_component(
        "button",
        "A primary call-to-action button with hover effects in a modern gradient style",
    )

    # Save to file
    button_file_path = generator.save_to_file(button_component, "cta_button.html")
    print(f"Generated Button Component saved to: {button_file_path}")
    print("\n" + "=" * 40 + "\n")

    # Generate a dashboard mockup
    print("Generating dashboard mockup...")
    dashboard_mockup = generator.generate_html_mockup(
        "A modern analytics dashboard with a sidebar navigation, header with user profile, and three data cards showing key metrics (revenue, users, conversion rate) with charts."
    )

    # Save to file
    dashboard_file_path = generator.save_to_file(
        dashboard_mockup, "analytics_dashboard.html"
    )
    print(f"Generated Dashboard Mockup saved to: {dashboard_file_path}")
    print("\n" + "=" * 40 + "\n")

    print("All mockups generated successfully!")


if __name__ == "__main__":
    main()

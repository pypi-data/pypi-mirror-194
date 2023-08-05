import openai
import click
import sys
import os

# Set up OpenAI API credentials
openai.api_key = "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"

# Define function to get CLI command from OpenAI API
def get_cli_command( question):
    os_name = sys.platform
    # Create the prompt for the API
    prompt = "Get CLI command for {}: {}\nOS Type: {}\nQuestion: {}\nCLI Command:".format(os_name, question, os_name, question)
    # Call the OpenAI API to get the response
    print("Old man is thinking...")
    print(sys.platform)
 
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop="\n",
        temperature=0.5,
    )

    # Parse the response and return the CLI command
    # return response.choices[0]
    # print(response.choices[0].text.strip())
    return response.choices[0].text.strip()

# Define command-line interface using the Click library
@click.command()
# @click.option("--os", prompt="Enter the OS type", help="The type of operating system")
@click.option("--question", prompt="Enter the question", help="The question for which you want a CLI command")
def main(question):
    # Call the get_cli_command function and print the result
    cli_command = get_cli_command(question)
    print("CLI command: {}".format(cli_command))
# Call the main function if this script is executed directly
if __name__ == "__main__":
    main()
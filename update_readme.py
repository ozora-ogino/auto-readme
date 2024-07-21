"""
README Generator for GitHub Repositories

This script automatically generates or updates a README file for a GitHub repository
based on recent changes, a template, and the repository structure. It uses OpenAI's
language models to analyze changes and generate appropriate content.

The script performs the following main tasks:
1. Fetches the repository structure and recent changes from a pull request
2. Identifies important files based on the README template
3. Retrieves the content of important files
4. Generates new README content using OpenAI's language model
5. Updates the README file if significant changes are detected

Usage:
    Set the following environment variables before running the script:
    - GH_TOKEN: GitHub personal access token
    - OPENAI_API_KEY: OpenAI API key
    - GITHUB_REPOSITORY: Name of the GitHub repository (e.g., "username/repo")
    - PR_NUMBER: Pull request number to analyze
    - OPENAI_MODEL: (Optional) OpenAI model to use (default: "gpt-3.5-turbo")

    Then run the script:
    $ python readme_generator.py
"""

import os
import sys
import logging
import time
import re

from github import Github
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_repo_tree(repo_name):
    """
    Fetch the full tree of the repository recursively.

    Args:
        repo_name (str): The name of the repository in the format "username/repo".

    Returns:
        list: A list of file paths in the repository.
    """
    g = Github(os.environ["GH_TOKEN"])
    repo = g.get_repo(repo_name)
    tree = repo.get_git_tree("main", recursive=True)
    return [element.path for element in tree.tree]

def get_pr_diff(repo_name, pr_number):
    """
    Fetch the diff of a specific pull request.

    Args:
        repo_name (str): The name of the repository in the format "username/repo".
        pr_number (int): The number of the pull request to analyze.

    Returns:
        list: A list of file objects that have been changed in the pull request.
    """
    g = Github(os.environ["GH_TOKEN"])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return pr.get_files()

def read_template(template_path=".github/README_TEMPLATE.md"):
    """
    Read the README template from the specified file.

    Args:
        template_path (str): The path to the README template file.

    Returns:
        str: The content of the README template, or None if an error occurs.
    """
    try:
        with open(template_path, "r") as f:
            return f.read()
    except IOError as e:
        logging.error(f"Error reading README template: {e}")
        return None

def read_current_readme(readme_path="README.md"):
    """
    Read the current README content.

    Args:
        readme_path (str): The path to the current README file.

    Returns:
        str: The content of the current README, or None if an error occurs.
    """
    try:
        with open(readme_path, "r") as f:
            return f.read()
    except IOError as e:
        logging.error(f"Error reading current README: {e}")
        return None

def is_critical_change(file_name, file_patch):
    """
    Determine if a change is critical based on the file name and patch.

    Args:
        file_name (str): The name of the changed file.
        file_patch (str): The patch content of the changed file.

    Returns:
        bool: True if the change is considered critical, False otherwise.
    """
    critical_patterns = [
        r"\.github/workflows/.*\.ya?ml",  # Workflow files
        r"package\.json",  # package.json
        r".*\.(js|ts|py|rb|php|java|cs|go|rs|scala|kt|swift)$",  # Potential endpoint files
    ]

    if any(re.match(pattern, file_name) for pattern in critical_patterns):
        return True

    # Check for endpoint changes in code files
    endpoint_patterns = [
        # ... (endpoint patterns remain unchanged)
    ]

    return any(re.search(pattern, file_patch, re.IGNORECASE) for pattern in endpoint_patterns)

def extract_important_files(tree_content, template_content):
    """
    Use LLM to extract important files from the repository tree based on the README template.

    Args:
        tree_content (str): A string representation of the repository file structure.
        template_content (str): The content of the README template.

    Returns:
        list: A list of file paths considered important for the README.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps identify important files in a repository structure based on a README template. Focus on files that are crucial for filling in the template sections."
        },
        {
            "role": "user",
            "content": f"Given the following repository structure and README template, list the top 10 most important files that should be considered when updating the README. Only provide the file paths, one per line, without any additional text or explanations:\n\nRepository structure:\n{tree_content}\n\nREADME template:\n{template_content}"
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model, messages=messages, max_tokens=500
        )
        return response.choices[0].message.content.strip().split('\n')
    except Exception as e:
        logging.error(f"Error in extracting important files: {e}")
        return []

def get_file_content(repo, file_path):
    """
    Fetch the content of a specific file from the repository.

    Args:
        repo (github.Repository.Repository): The GitHub repository object.
        file_path (str): The path to the file in the repository.

    Returns:
        str: The content of the file, or None if an error occurs.
    """
    try:
        file_content = repo.get_contents(file_path, ref="main")
        return file_content.decoded_content.decode('utf-8')
    except Exception as e:
        logging.error(f"Error fetching content for {file_path}: {e}")
        return None

def generate_readme(diff_content, template_content, current_readme, repo_name, important_files, file_contents, max_tokens=4000):
    """
    Generate new README content using the specified OpenAI model.

    Args:
        diff_content (str): The diff content of the recent changes.
        template_content (str): The content of the README template.
        current_readme (str): The content of the current README.
        repo_name (str): The name of the repository.
        important_files (list): A list of important file paths.
        file_contents (dict): A dictionary mapping file paths to their contents.
        max_tokens (int): The maximum number of tokens for the OpenAI API response.

    Returns:
        str: The generated README content, or None if an error occurs.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    logging.info(f"Using OpenAI model: {model}")

    file_content_str = "\n\n".join([f"File: {path}\nContent:\n{content}" for path, content in file_contents.items()])

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates README content in Markdown format based on code changes, a given template, the current README, a list of important files, and their contents. Focus on critical changes such as updates to workflows, package.json, and application endpoints. If no significant changes are necessary, respond with 'NO_CHANGES_NEEDED'.",
        },
        {
            "role": "user",
            "content": f"""Update the README content based on the following information:

README Template:
{template_content}

Current README:
{current_readme}

Repository Name: {repo_name}

Code Changes:
{diff_content}

Important Files and Their Contents:
{file_content_str}

Instructions:
1. Use the provided template structure.
2. Incorporate relevant information from the current README, code changes, and important file contents.
3. Use table, toggle, code block or etc for readability
4. Focus on key changes, especially those related to workflows, package.json, and application endpoints.
5. Consider any new features or breaking changes.
6. Replace {{placeholder}} with actual content.
7. Provide the complete README in Markdown format without any additional text or explanations. And don't start from code block.
8. If no significant changes are needed, respond only with 'NO_CHANGES_NEEDED'.
9. Don't use something like "refer to the installation guide found in the installation.md file."
10. Create inclusive README as you can make.

Generate the updated README content:""",
        },
    ]

    try:
        response = client.chat.completions.create(
            model=model, messages=messages, max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        if "maximum context length" in str(e):
            logging.warning(
                "Exceeded maximum context length. Reducing content and retrying."
            )
            return None
        else:
            raise

def update_readme(new_content, readme_path="README.md"):
    """
    Update the README file with new content.

    Args:
        new_content (str): The new content to write to the README file.
        readme_path (str): The path to the README file.

    Raises:
        IOError: If there's an error writing to the README file.
    """
    try:
        with open(readme_path, "w") as f:
            f.write(new_content)
        logging.info(f"README updated successfully at {readme_path}")
    except IOError as e:
        logging.error(f"Error updating README: {e}")
        raise

def main():
    """
    Main function to orchestrate the README update process.

    This function performs the following steps:
    1. Fetches the repository structure and pull request diff
    2. Reads the README template and current README
    3. Identifies important files and fetches their contents
    4. Generates new README content based on changes and important files
    5. Updates the README if significant changes are detected

    Raises:
        ValueError: If unable to read the README template or current README.
        Exception: For any other errors during the process.
    """
    repo_name = os.environ["GITHUB_REPOSITORY"]
    pr_number = int(os.environ["PR_NUMBER"])

    try:
        # Initialize Github client
        g = Github(os.environ["GH_TOKEN"])
        repo = g.get_repo(repo_name)

        # Get repository tree
        tree_content = get_repo_tree(repo_name)
        
        # Read README template
        template_content = read_template()
        if template_content is None:
            raise ValueError("Failed to read README template")

        # Extract important files based on the template
        important_files = extract_important_files('\n'.join(tree_content), template_content)
        
        # Fetch content of important files
        file_contents = {}
        for file_path in important_files:
            content = get_file_content(repo, file_path)
            if content:
                file_contents[file_path] = content

        current_readme = read_current_readme()
        if current_readme is None:
            raise ValueError("Failed to read current README")

        files = get_pr_diff(repo_name, pr_number)
        critical_changes = [f for f in files if is_critical_change(f.filename, f.patch)]

        if not critical_changes:
            logging.info("No critical changes detected. Skipping README update.")
            return

        all_diff_content = "\n".join(
            [
                f"File: {file.filename}\nChanges:\n{file.patch}\n"
                for file in critical_changes
            ]
        )

        # Split diff content into chunks if it's too large
        diff_chunks = [
            all_diff_content[i : i + 3000]
            for i in range(0, len(all_diff_content), 3000)
        ]

        readme_updated = False
        for i, diff_chunk in enumerate(diff_chunks):
            logging.info(f"Processing chunk {i+1} of {len(diff_chunks)}")
            new_readme_content = generate_readme(
                diff_chunk, template_content, current_readme, repo_name, important_files, file_contents
            )

            if new_readme_content is None:
                logging.warning(
                    f"Failed to generate content for chunk {i+1}. Skipping."
                )
                continue

            if new_readme_content.strip() == "NO_CHANGES_NEEDED":
                logging.info(
                    "LLM determined no significant changes are needed for this chunk."
                )
                continue

            update_readme(new_readme_content)
            current_readme = new_readme_content  # Update current README for next iteration
            readme_updated = True

            if i < len(diff_chunks) - 1:
                time.sleep(20)  # Add delay between API calls to avoid rate limiting

        if not readme_updated:
            logging.info("No changes were made to the README.")

    except Exception as e:
        logging.error(f"Failed to update README: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
import os
import sys
from github import Github
from openai import OpenAI
import logging
import time
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_pr_diff(repo_name, pr_number):
    """
    Fetch the diff of a specific pull request.
    """
    g = Github(os.environ["GH_TOKEN"])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return pr.get_files()


def read_template(template_path=".github/README_TEMPLATE.md"):
    """
    Read the README template from the specified file.
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
    """
    critical_patterns = [
        r"\.github/workflows/.*\.ya?ml",  # Workflow files
        r"package\.json",  # package.json
        r".*\.(js|ts|py)$",  # Potential endpoint files
    ]

    if any(re.match(pattern, file_name) for pattern in critical_patterns):
        return True

    # Check for endpoint changes in code files
    endpoint_patterns = [
        r"@app\.route\(",  # Flask
        r"app\.get\(",  # Express
        r"@api_view\(",  # Django REST framework
        r'path\([\'"]/',  # React Router
    ]

    return any(re.search(pattern, file_patch) for pattern in endpoint_patterns)


def generate_readme(
    diff_content, template_content, current_readme, repo_name, max_tokens=4000
):
    """
    Generate new README content using the specified OpenAI model.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    logging.info(f"Using OpenAI model: {model}")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates README content in Markdown format based on code changes, a given template, and the current README. Focus on critical changes such as updates to workflows, package.json, and application endpoints. If no significant changes are necessary, respond with 'NO_CHANGES_NEEDED'.",
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

Instructions:
1. Use the provided template structure.
2. Incorporate relevant information from the current README and the code changes.
3. Focus on key changes, especially those related to workflows, package.json, and application endpoints.
4. Consider any new features or breaking changes.
5. Replace {{placeholder}} with actual content.
6. Provide the complete README in Markdown format without any additional text or explanations.
7. If no significant changes are needed, respond only with 'NO_CHANGES_NEEDED'.

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
    """
    repo_name = os.environ["GITHUB_REPOSITORY"]
    pr_number = int(os.environ["PR_NUMBER"])

    try:
        template_content = read_template()
        if template_content is None:
            raise ValueError("Failed to read README template")

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
                diff_chunk, template_content, current_readme, repo_name
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
            current_readme = (
                new_readme_content  # Update current README for next iteration
            )
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

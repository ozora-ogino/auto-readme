import os
import sys
import logging
import time
import re

from github import Github
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_repo_tree(repo_name):
    """
    Fetch the full tree of the repository recursively.
    """
    g = Github(os.environ["GH_TOKEN"])
    repo = g.get_repo(repo_name)
    tree = repo.get_git_tree("main", recursive=True)
    return [element.path for element in tree.tree]

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
        r".*\.(js|ts|py|rb|php|java|cs|go|rs|scala|kt|swift)$",  # Potential endpoint files
    ]

    if any(re.match(pattern, file_name) for pattern in critical_patterns):
        return True

    # Check for endpoint changes in code files
    endpoint_patterns = [
        # Python
        r"@app\.route\(",  # Flask
        r"@api_view\(",  # Django REST framework
        r"app\.add_url_rule\(",  # Flask
        r"path\(['\"]",  # Django

        # JavaScript/TypeScript
        r"app\.(get|post|put|delete|patch)\(",  # Express.js
        r"router\.(get|post|put|delete|patch)\(",  # Express.js with Router
        r"app\.use\(['\"]",  # Express.js middleware
        r"new Route\(",  # Angular
        r"@(Get|Post|Put|Delete|Patch)\(",  # NestJS
        r"path: ['\"]",  # Angular routing

        # Ruby
        r"get ['\"]",  # Ruby on Rails
        r"post ['\"]",  # Ruby on Rails
        r"put ['\"]",  # Ruby on Rails
        r"delete ['\"]",  # Ruby on Rails
        r"resources? :",  # Ruby on Rails resources

        # PHP
        r"Route::(get|post|put|delete|patch)\(",  # Laravel
        r"\$router->(get|post|put|delete|patch)\(",  # Slim Framework

        # Java
        r"@(Get|Post|Put|Delete|Patch)Mapping",  # Spring Boot
        r"@Path\(['\"]",  # JAX-RS

        # C#
        r"\[Http(Get|Post|Put|Delete|Patch)\]",  # ASP.NET Core
        r"app\.Map",  # ASP.NET Core Minimal API

        # Go
        r"(r|http)\.(Handle|HandleFunc)\(",  # Go standard library
        r"(r|e)\.(GET|POST|PUT|DELETE|PATCH)\(",  # Echo and Gin frameworks

        # Rust
        r"#\[get\(",  # Rocket framework
        r"#\[post\(",  # Rocket framework
        r"#\[put\(",  # Rocket framework
        r"#\[delete\(",  # Rocket framework
        r"#\[patch\(",  # Rocket framework

        # Scala
        r"path\(['\"]",  # Play framework
        r"(get|post|put|delete|patch)\(['\"]",  # Play framework

        # Kotlin
        r"@(Get|Post|Put|Delete|Patch)Mapping",  # Spring Boot with Kotlin

        # Swift
        r"router\.(get|post|put|delete|patch)\(",  # Vapor framework
        r"app\.get\(",  # Vapor framework
        r"app\.post\(",  # Vapor framework
        r"app\.put\(",  # Vapor framework
        r"app\.delete\(",  # Vapor framework
        r"app\.patch\(",  # Vapor framework
    ]

    return any(re.search(pattern, file_patch, re.IGNORECASE) for pattern in endpoint_patterns)


def extract_important_files(tree_content):
    """
    Use LLM to extract important files from the repository tree.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps identify important files in a repository structure. Focus on files that are crucial for understanding the project structure, main functionalities, and configuration."
        },
        {
            "role": "user",
            "content": f"Given the following repository structure, list the top 10 most important files that should be considered when updating the README. Only provide the file paths, one per line, without any additional text or explanations:\n\n{tree_content}"
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

def generate_readme(diff_content, template_content, current_readme, repo_name, important_files, max_tokens=4000):
    """
    Generate new README content using the specified OpenAI model.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    logging.info(f"Using OpenAI model: {model}")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates README content in Markdown format based on code changes, a given template, the current README, and a list of important files. Focus on critical changes such as updates to workflows, package.json, and application endpoints. If no significant changes are necessary, respond with 'NO_CHANGES_NEEDED'.",
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

Important Files:
{', '.join(important_files)}

Instructions:
1. Use the provided template structure.
2. Incorporate relevant information from the current README, code changes, and important files.
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
        # Get repository tree
        tree_content = get_repo_tree(repo_name)
        
        # Extract important files
        important_files = extract_important_files('\n'.join(tree_content))
        
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
                diff_chunk, template_content, current_readme, repo_name, important_files
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
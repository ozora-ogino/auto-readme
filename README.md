# ozora-ogino/auto-readme

## Description
This project utilizes an OpenAI-powered tool designed to automatically generate and update README files based on the changes detected in pull requests. It has an optimized mechanism for managing large diffs by breaking them down into manageable chunks and processing them individually.

## Dependencies
- Python packages: PyGithub, openai

## Features
- Automatic README generation and updates based on incoming pull requests.
- Critical changes identification on workflows, package.json, application endpoints, and other significant code modifications.
- Exposed functions for obtaining the PR diff, reading the current and template README, and detecting critical changes based on file name and patches.
- Improved handling for large diffs; the changes are now divided into 3000-character chunks for better readability and processing.
- Time delay feature inserted between API calls to avoid rate limiting.
- Logging system for reporting issues during content generation.
- Validation checks have been introduced during README generation to handle 'NO_CHANGES_NEEDED' scenarios and skip unnecessary updates.
- Unnecessary updates prevention when no critical changes are detected or if the generated content does not trigger notable modifications.
- Ability to change the OpenAI model version for further customization.

## Installation
To utilize the README Updater Action, follow the steps below:
1. Copy .github/workflows/auto-readme.yml file to the .github/workflows/ directory in your repository.
2. Create a .github/README_TEMPLATE.md file with the structured template.
3. Add the OPENAI_API_KEY with your OpenAI API key and the GH_TOKEN with your GitHub Personal Access Token in 'Settings > Secrets'.
4. In 'Settings > Actions > General', configure the "Workflow permissions" to "Read and write permissions" and allow "GitHub Actions to create and approve pull requests".
5. The action uses a custom GH_TOKEN for authentication by default.
6. Customize the action's performance by adjusting the 'on:' section in the workflows file.

## Usage
The tool automatically updates the README whenever a pull request is made, excluding changes directed at the README itself, after you've finished setting it up.

## Recent Updates
- Introduced `generate_readme` and `update_readme` functions for automated generation and updating of README files based on OpenAI’s model.
- Enhanced the `main` function to orchestrate the README update process seamlessly. A mechanism to handle large diffs was added, where large diffs are divided into 3000-character chunks.
- Included a time delay between API calls to avoid rate limiting.
- Validation checks were added during the README generation process, where if 'NO_CHANGES_NEEDED' is returned, the update is skipped.
- Existing features and workflows remain unaffected.

## Contributing
We invite the community to contribute and help us improve this action! Please submit a pull request or open an issue on the repository.

## License
This project is licensed under the terms of the MIT license.

## Contact
For more information or to report issues, please visit: https://github.com/ozora-ogino/auto-readme/issues

## Troubleshooting
If you encounter any issues, please perform the following checks:
1. Ensure the `OPENAI_API_KEY` and `GH_TOKEN` secrets are correctly set in your repository.
2. The `GH_TOKEN` should possess the necessary permissions - `repo` scope for private repositories, `public_repo` for public repositories.
3. Verify the repository settings for Actions, as mentioned in the setup instructions.
4. Review the Action logs for any error messages or unexpected behavior. 
5. Make sure the `OPENAI_MODEL` variable is set to a valid OpenAI model - "gpt-4" by default.

## Customization
You have the opportunity to customize this action by adjusting the Python script in the "Update README" step, allowing you to adjust the prompt, determine how critical changes are detected, or change the OpenAI model version. You can also modify the 'on:' section in the workflows file to control when this action runs based on your necessities.
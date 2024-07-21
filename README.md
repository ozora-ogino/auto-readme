# auto-readme

## Latest Updates

## New README Auto-updater Action Added

A helpful GitHub Action has been introduced named 'README Updater Action'. This action will automatically update the README.md file based on changes proposed in Pull Requests.

### Key Features

* It leverages OpenAI's GPT-4 for generating concise and informative updates to README.md.
* It activates on every Pull Request that makes changes excluding the README.md itself.
* It has a feature of automatically committing and pushing any changes made to README.md.
* It allows customization according to user's requirements.

### Usage Instructions 

1. Copy the auto-readme.yml file to .github/workflows/update-readme.yml in your repository.
2. Set up the following secrets in your repository's Settings > Secrets and variables > Actions:
   - OPENAI_API_KEY with your OpenAI API key
   - GH_TOKEN with your GitHub Personal Access Token, with 'repo' scope for private repositories, or 'public_repo' scope for public ones.
3. Configure your repository settings:
   - In your repository's Settings > Actions > General, under "Workflow permissions", select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

_Note_: This action uses a custom GH_TOKEN for authentication replacing the default GITHUB_TOKEN. 

### Troubleshooting 

If there are any issues in its operation, ensure the OPENAI_API_KEY and GH_TOKEN secrets are set correctly and permissions for GH_TOKEN are properly granted. Also, verify your repository settings for Actions.

### Customization and Contributions 

This Action allows flexibility - you can modify the Python script in the "Update README" step. Contributions for improving the Action are more than welcome!

For more details, refer to the auto-readme.yml file.

### Breaking Changes 

None. This was a new feature addition; it won't affect the existing functionality.
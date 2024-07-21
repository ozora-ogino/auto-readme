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

## Latest Updates

# auto-readme

## Latest Updates

## New Feature: README Auto-updater Action

We have added a new GitHub Action, 'README Updater Action', which automatically updates the README.md file based on changes proposed in Pull Requests.

### Key Features

- Uses OpenAI's GPT-4 to generate concise and informative updates.
- Triggers on every Pull Request that changes files, excluding the README.md itself.
- Automatically commits and pushes amendments to README.md.
- Ability to be fine-tuned according to user's requirements.

### Usage 

1. Copy the auto-readme.yml file to .github/workflows/update-readme.yml in your repository.
2. Go to your repository's Settings > Secrets > Actions and set up:
   - OPENAI_API_KEY with your OpenAI API key
   - GH_TOKEN with a GitHub Personal Access Token - ensure to grant 'repo' scope for private repositories, or 'public_repo' scope for public ones.
3. Configure your repository settings:
   - Under Settings > Actions > General > "Workflow permissions", choose "Read and write permissions"
   - Enable "Allow GitHub Actions to create and approve pull requests"

_Important_: This action uses a custom GH_TOKEN for authentication instead of the default GITHUB_TOKEN. 

### Troubleshooting 

For troubleshooting, please check that OPENAI_API_KEY and GH_TOKEN secrets are correctly set, the GH_TOKEN has the necessary permissions, and that your repository settings for Actions are correctly configured.

### Customization and Contributions 

You can customize this action as per your needs by modifying the Python script in the "Update README" step. We welcome contributions to improve this action - feel free to submit a pull request or raise an issue on the repository!

Refer to the auto-readme.yml file for more details.

### Breaking Changes 

There are no breaking changes. This action was a new feature addition and does not affect existing functionality.

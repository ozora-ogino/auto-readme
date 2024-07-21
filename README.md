# ozora-ogino/auto-readme

## Description
Auto-readme is a Python application designed to automatically generate README files for GitHub repositories. The application fetches updates or changes made in the repository, retrieves content from important files, and seamlessly rebuilds the updated README.

Updates have been made to the `update_readme.py` file, altering the guidelines for generating the best possible README content.

## Features
- Automatic generation of updated README files triggered by changes in the repository code.
- Enhanced detection range for endpoint changes in multiple languages, including Python, Java, JavaScript, and Go.
- Recursive fetching of the repository tree to extract all file paths.
- Integration of relevant details from the current README, important file contents, and the detected code changes.
- Truncation of extensive file contents and diff information to optimize the README update process and enhance performance.
- Various error handling mechanisms, including retries and validation steps, to ensure robust and reliable README updates.

## Usage
1. Copy the following into `.github/workflows/auto-readme.yml` in your repo.

```yaml
# {{repository_name}}

## Description
{{description}}

## Features
{{features}}

## Usage
1. Copy following under `.github/workflows/auto-readme.yml` in your repo.

```.github/workflows/auto-readme.yml

name: Update README

on:
  pull_request:
    types: [closed]
    paths-ignore:
      - 'README.md'

env:
  OPENAI_MODEL: gpt-4
  TARGET_BRANCH: main

jobs:
  update-readme:
    runs-on: ubuntu-latest
    if: |
      github.event.pull_request.merged == true &&
      !startsWith(github.event.pull_request.title, 'AutoReadme:')
    permissions:
      contents: write
      pull-requests: write
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
        token: ${{ secrets.GH_TOKEN }}

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install PyGithub openai
        git clone https://github.com/ozora-ogino/auto-readme /tmp/auto-readme

    - name: Update README
      env:
        GH_TOKEN: ${{ secrets.GH_TOKEN }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        PR_NUMBER: ${{ github.event.pull_request.number }}
        PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}
        PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}
        OPENAI_MODEL: ${{ env.OPENAI_MODEL }}
      run: python3 /tmp/auto-readme/update_readme.py

    - name: Check for README changes
      id: check_changes
      run: |
        if git diff --quiet README.md; then
          echo "No changes to README.md"
          echo "readme_changed=false" >> $GITHUB_OUTPUT
        else
          echo "README.md has been modified"
          echo "readme_changed=true" >> $GITHUB_OUTPUT
        fi

    - name: Commit and push if changed
      if: steps.check_changes.outputs.readme_changed == 'true'
      env:
        GH_TOKEN: ${{ secrets.GH_TOKEN }}
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add README.md
        branch_name="update-readme/${{ github.run_number }}"
        git checkout -b $branch_name
        git commit -m "Auto-update README [skip ci]"
        git push --set-upstream origin $branch_name

    - name: Create Pull Request
      if: steps.check_changes.outputs.readme_changed == 'true'
      uses: repo-sync/pull-request@v2
      with:
        github_token: ${{ secrets.GH_TOKEN }}
        source_branch: "update-readme/${{ github.run_number }}"
        destination_branch: "${{ env.TARGET_BRANCH }}"
        pr_title: "AutoReadme: Update based on PR #${{ github.event.pull_request.number }}"
        pr_body: "This pull request automatically updates the README based on changes in PR #${{ github.event.pull_request.number }}."
```

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push to the branch.
5. Create a new Pull Request.

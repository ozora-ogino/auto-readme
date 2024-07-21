# {{repository_name}}

## Description
auto-readme is Github Action to automatically generate README by LLM.

## Features
{{features}}

## Usage
1. Copy following into `.github/workflows/auto-readme.yml` in your repo.

```.github/workflows/auto-readme.yml
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

2. Add `.github/README_TEMPLATE.md`. ([example](.github/README_TEMPLATE.md`))

## License
{{license}}




# Apiable GitHub Action

This custom GitHub Action allows you to automate interactions with the Apiable API, such as uploading OpenAPI specifications and updating documentation for a specified API plan.

## Features

- **JWT Authentication**: The action generates a JWT token by using the provided API credentials (`api_key` and `api_secret`).
- **OpenAPI Spec Upload**: It downloads the OpenAPI specification from the provided URL and uploads it to Apiable.
- **Documentation Update**: It updates the documentation of a specific API plan with the uploaded OpenAPI spec, setting the version based on the current date.

## Inputs

This action requires the following inputs:

| Input              | Description                                                                                         | Required |
|--------------------|-----------------------------------------------------------------------------------------------------|----------|
| `api_key`          | The API key (client ID) to authenticate with Apiable.                                                | Yes      |
| `api_secret`       | The API secret (client secret) to authenticate with Apiable.                                         | Yes      |
| `api_url`          | The base URL of the Apiable API. Example: `https://dev.api.apiable.io`.                              | Yes      |
| `open_api_spec_url`| The URL of the OpenAPI specification to be uploaded. Example: `https://dev-api.apiable.io/api-docs`.  | Yes      |
| `planid`           | The ID of the API plan to update the documentation for.                                              | Yes      |

## Example Usage

Here’s an example GitHub Actions workflow that uses this custom action:

\`\`\`yaml
name: Update Apiable Documentation

on:
push:
branches:
- main
paths-ignore:
- '*.md'

jobs:
update-apiable-docs:
runs-on: ubuntu-latest
steps:
# Step 1: Checkout the repository
- name: Checkout repository
uses: actions/checkout@v3

      # Step 2: Run the custom Apiable GitHub Action
      - name: Run custom Apiable GitHub Action
        id: run-apiable-action
        uses: .
        with:
          api_key: \${{ env.APIABLE_DEVELOPER_PORTAL_CLIENT_ID }}
          api_secret: \${{ env.APIABLE_DEVELOPER_PORTAL_CLIENT_SECRET }}
          api_url: "https://dev.api.apiable.io"
          open_api_spec_url: "https://dev-api.apiable.io/api/int/public/v3/api-docs"
          planid: "659fa46a2f08a41f65664bba"

      # Step 3: Output the result of the action
      - name: Display Action Output
        run: |
          echo "Apiable Action Response: \${{ steps.run-apiable-action.outputs.response }}"
\`\`\`

### Explanation of the Example Workflow:

1. **Checkout the Repository**: The repository is checked out to access any necessary files or configurations.
2. **Run Apiable GitHub Action**: The custom action is executed with the provided API credentials, URLs, and plan ID.
3. **Display Action Output**: The response from the Apiable API is displayed as part of the workflow logs.

## Setup and Secrets

To use this action in your workflow, make sure to provide the required environment variables (`APIABLE_DEVELOPER_PORTAL_CLIENT_ID` and `APIABLE_DEVELOPER_PORTAL_CLIENT_SECRET`) via GitHub Secrets for security:

1. Go to **Settings > Secrets and Variables > Actions** in your repository.
2. Add the following secrets:
    - `APIABLE_DEVELOPER_PORTAL_CLIENT_ID`: Your Apiable developer portal client ID.
    - `APIABLE_DEVELOPER_PORTAL_CLIENT_SECRET`: Your Apiable developer portal client secret.

## Outputs

| Output    | Description                                    |
|-----------|------------------------------------------------|
| `response`| The response from the Apiable API after updating the documentation. |

## License

This project is licensed under the MIT License.

# Development
## Integrations
This project involves the following third parties, the accounts for which will need to be set up.

- Airtable 
- Give Butter

## Adding API keys
1. **Create a `.env` file in the base directory.** This file can be used for any variables that you need to keep secret, including API keys. This file should not be checked into git. This exclusion will happen automatically, as `.env` is listed in the `.gitignore` file.
3. **Add the following variables to the `.env` file.**

    ```
    AIRTABLE_BASE=[your_base]
    AIRTABLE_API_KEY=[your_key]
    ```

## Running Locally
TBD
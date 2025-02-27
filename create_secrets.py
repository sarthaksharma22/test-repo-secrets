import os
from github import Github, Auth

def create_github_secrets(github_token, github_owner, github_repo, secrets_dict):
    """Creates secrets in the specified GitHub repository using inherited secrets."""
    try:
        # ✅ Authenticate using GitHub PAT
        auth = Auth.Token(github_token)
        github_client = Github(auth=auth)

        # ✅ Get the target repository
        repo = github_client.get_repo(f"{github_owner}/{github_repo}")

        # ✅ Add inherited secrets to the repository
        for secret_name, secret_value in secrets_dict.items():
            if secret_value:  # Ensure secret is not empty
                repo.create_secret(secret_name, secret_value)
                print(f"✅ Secret '{secret_name}' created successfully in {github_repo}")
            else:
                print(f"⚠️ Skipping '{secret_name}': No value found.")

    except Exception as e:
        print(f"❌ Failed to create secrets: {e}")

    finally:
        github_client.close()  # Close connection

if __name__ == "__main__":
    # ✅ Read required environment variables
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

    # ✅ Read secrets (Inherited from the calling workflow)
    secrets_dict = {
        "SECRET_1": os.getenv("SECRET_1"),
        "SECRET_2": os.getenv("SECRET_2"),
        "SECRET_3": os.getenv("SECRET_3"),
    }

    # ✅ Ensure required variables are set
    if not GITHUB_TOKEN or not GITHUB_OWNER or not GITHUB_REPOSITORY:
        raise ValueError("❌ Missing required environment variables!")

    # ✅ Run the function with inherited secrets
    create_github_secrets(GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPOSITORY, secrets_dict)

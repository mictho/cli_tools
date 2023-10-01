
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# You'll need to install the necessary Python packages using pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client.
# Make sure to replace 'credentials.json' with the path to your OAuth 2.0 client credentials file, obtained from the Google Cloud Console.
# This script assumes that the credentials.json file and the subscriptions.json file are in the same directory as the script. Adjust the paths as needed.
# This script uses OAuth 2.0 for authentication. It first authenticates the first account, retrieves and stores the subscriptions, and then uses the stored subscriptions to subscribe to channels in a second account.
#



# Function to authenticate with the Google API
def authenticate(api_key=None, account_name=None):
    # If API key is provided, use it for API requests
    if api_key:
        return build('youtube', 'v3', developerKey=api_key)

    # If account name is provided, use OAuth 2.0 for authentication
    if account_name:
        # The file token.json stores the user's access and refresh tokens
        creds = None
        token_path = f"{account_name}_token.json"

        # Load existing credentials if available
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/youtube.readonly'])
            creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('youtube', 'v3', credentials=creds)


# Function to retrieve and store subscriptions
def get_and_store_subscriptions(api, file_name):
    subscriptions = api.subscriptions().list(
        part='snippet,contentDetails',
        mine=True
    ).execute()

    with open(file_name, 'w') as file:
        json.dump(subscriptions, file)


# Function to connect to a second account and subscribe to channels
def subscribe_to_channels(api, file_name):
    with open(file_name, 'r') as file:
        subscriptions = json.load(file)

    for item in subscriptions.get('items', []):
        channelId = item['snippet']['resourceId']['channelId']
        api.subscriptions().insert(
            part='snippet',
            body={
                'snippet': {
                    'resourceId': {
                        'channelId': channelId
                    }
                }
            }
        ).execute()


if __name__ == '__main__':
    # Step 1: Allow the user to supply API key and/or account name
    api_key = input("Enter API key (if any): ")
    account_name = input("Enter account name (if any): ")

    # Step 2: Authenticate to the Google API
    api = authenticate(api_key=api_key, account_name=account_name)

    # Step 3: Retrieve and store subscriptions
    get_and_store_subscriptions(api, 'subscriptions.json')

    # Step 4: Connect to a second account and subscribe to channels
    second_account_api_key = input("Enter API key for the second account: ")
    second_account_name = input("Enter account name for the second account: ")
    second_account_api = authenticate(api_key=second_account_api_key, account_name=second_account_name)

    # Step 5: Subscribe to channels using the stored subscriptions
    subscribe_to_channels(second_account_api, 'subscriptions.json')

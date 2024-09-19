import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from thefuzz import process

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SPREADSHEET_ID = "1XClUlo2FOa1ETBBgGuxJ_IyUAsw2evxd4YtToN77Qa4"
NORMALIZED = "MASTRAN-normalized"
HEADERS = "MASTRAN-headers"


def verify_credentials():
    """Verify the credentials."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as e:
        print(e)

def get_values(range, service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()
    values = result.get("values", [])
    return values


def get_headers(table, service):
    """Get the headers of the table."""
    sheet = service.spreadsheets()
    table_headers = get_values(HEADERS + "!A2:N", service)
    for row in table_headers:
        if row[1] == table:
            table_row = row
            break
    headers = table_row[3:]
    return headers

def get_results(value, table, service):
    """Return the value as a dictionary."""
    headers = get_headers(table, service)
    results = get_values(NORMALIZED + "!A2:N", service)
    for row in results:
        if row[1] == table and row[2] == value:
            result = row
            break
    result_dict = dict(zip(headers, result[3:]))
    return result_dict

def fuzzy_match(value, service, num_results=1):
    """Fuzzy match the value to the headers."""
    sheet = service.spreadsheets()
    results = get_values(NORMALIZED + "!A2:N", service)
    choices = [row[2] + " " + row[1] for row in results]
    info_dict = dict(zip(choices, results))
    processed = process.extract(value, choices, limit=num_results)
    output = []
    for match in processed:
        value, score = match
        output.append(
            {
                "primary": info_dict[value][0],
                "fuzz_score": score,
                "table": info_dict[value][1],
                "value": info_dict[value][2],
            }
        )
    return output

def main():
    """Shows basic usage of the MASTRAN API.
    """
    service = verify_credentials()
    headers = get_headers("Fluids Parameters1", service)
    print(headers)

    result = get_results("Thrust", "Engine Parameters", service)
    print(result)

    fuzzy = fuzzy_match("Thrust", service)
    print(fuzzy)

    fuzzy_result = get_results(fuzzy[0]["value"], fuzzy[0]["table"], service)
    print(fuzzy_result)


if __name__ == "__main__":
    main()


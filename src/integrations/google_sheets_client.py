import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsConnector:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

    def connect(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=scopes
        )

        return gspread.authorize(creds)

    def open_by_name(self, spreadsheet_name: str):
        client = self.connect()
        return client.open(spreadsheet_name)

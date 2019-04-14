from dotenv import load_dotenv
import os


load_dotenv()


class Config():
    def __init__(self, test_env=False):
        self.test_env = test_env

        if self.test_env == True:
            self.username = os.getenv("QA_USER")
            self.password = os.getenv("QA_PASSWORD")
            self.api_key = os.getenv("QA_API_KEY")
            self.base_url = os.getenv("QA_URL")
            self.team_id = os.getenv("QA_TEAM_ID")
        else:
            self.username = os.getenv("USER")
            self.password = os.getenv("PASSWORD")
            self.api_key = os.getenv("API_KEY")
            self.base_url = os.getenv("URL")
            self.team_id = os.getenv("TEAM_ID")
    
    def get_username(self):
        return self.username

    def get_api_key(self):
        return self.api_key

    def get_password(self):
        return self.password

    def get_base_url(self):
        return self.base_url

    def get_team_id(self):
        return self.team_id

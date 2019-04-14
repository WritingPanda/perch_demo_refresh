"""
Must have a .env file in the root folder with this data:

USER=""
PASSWORD=""
API_KEY=""
URL="https://api.perch.rocks/v1"
TEAM_ID=1234

QA_USER=""
QA_PASSWORD=""
QA_API_KEY=""
QA_URL="https://api.qa.perchsecurity.com/v1"
QA_TEAM_ID=4321
"""

from client.client import PerchAPIClient
from config.settings import Config


def main():
    conf = Config(test_env=True)
    client = PerchAPIClient(api_key=conf.get_api_key(), 
                            username=conf.get_username(), 
                            password=conf.get_password(), 
                            base_url=conf.get_base_url(), 
                            team_id=conf.get_team_id())

    res = client.get_alerts_list(1)
    first_result = res[0]

    print(client.suppress_alert(indicator_id=first_result['indicator_id'],
                                community_id=first_result['community_id'],
                                observable_id=first_result['observable_id']))

if __name__ == '__main__':
    main()

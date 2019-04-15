"""
Must have a .env file in the root folder with this data:

USER=STR
PASSWORD=STR
API_KEY=STR
URL=STR
TEAM_ID=INT

QA_USER=STR
QA_PASSWORD=STR
QA_API_KEY=STR
QA_URL=STR
QA_TEAM_ID=INT
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

    # Get a list of up to 1000 results
    res = client.get_alerts_list(1000)
    # Count through all of the requests (for debug and optimization purposes)
    counter = 0
    # Run through the loop of the results to suppress each one and increase the counter
    # Print the results to the console
    for alert in res:
        print(client.suppress_alert(indicator_id=alert['indicator_id'],
                                    community_id=alert['community_id']))
        counter += 1
        print(counter)

if __name__ == '__main__':
    main()

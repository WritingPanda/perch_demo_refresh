import argparse
from client.client import PerchAPIClient
from decouple import config


def main(test_env: bool) -> None:
    if test_env is False:
        username = config('USER')
        password = config('PASSWORD')
        api_key = config('API_KEY')
        base_url = config('URL')
        team_id = config('TEAM_ID')
    elif test_env is True:
        username = config('QA_USER')
        password = config('QA_PASSWORD')
        api_key = config('QA_API_KEY')
        base_url = config('QA_URL')
        team_id = config('QA_TEAM_ID')

    client = PerchAPIClient(
            api_key=api_key,
            username=username,
            password=password,
            base_url=base_url,
            team_id=team_id)

    # Get a list of up to 1000 results
    res = client.get_alerts_list(1000)
    # Count through all of the requests (for debug and optimization purposes)
    counter = 0
    print(res)
    # Run through the loop of the results to suppress each one and increase the counter
    # Print the results to the console
    # for alert in res:
    #     print(client.suppress_alert(indicator_id=alert['indicator_id'],
    #                                 community_id=alert['community_id']))
    #     counter += 1
    #     print(counter)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Determine whether to use test env or production env.')
    parser.add_argument(
            'Environment',
            type=str,
            choices=['test', 'prod'],
            help='Determine the environment to send requests: test or prod.')
    args = parser.parse_args()
    if args.Environment == 'test':
        main(test_env=True)
    elif args.Environment == 'prod':
        main(test_env=False)

import argparse
import logging
from client.PerchAPIClient import PerchAPIClient
from decouple import config


logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)
logger = logging.getLogger('perch_demo_refresh')


def set_configuration(test_env: bool) -> dict:
    if test_env is False:
        configuration = {
            "username": config('PERCH_USER'),
            "password": config('PASSWORD'),
            "api_key": config('API_KEY'),
            "base_url": config('URL'),
            "team_id": config('TEAM_ID'),
        }
    elif test_env is True:
        configuration = {
            "username": config('QA_PERCH_USER'),
            "password": config('QA_PASSWORD'),
            "api_key": config('QA_API_KEY'),
            "base_url": config('QA_URL'),
            "team_id": config('QA_TEAM_ID'),
        }
    return configuration


def close_alerts(client: PerchAPIClient, test_env: bool, number_of_alerts: int) -> None:
    # Get a list of up to 1000 results
    res = client.get_alerts_list(number_of_alerts)
    # Count through all of the requests (for debug and optimization purposes)
    counter = 0
    
    # Run through the loop of the results to suppress each one and increase the counter
    # Print the results to the console
    if res is not None:
        for alert in res:
            if test_env is True:
                client.suppress_alert(
                    indicator_id=alert['indicator_id'],
                    community_id=alert['community_id'],
                    test_env=True
                )
            elif test_env is False:
                client.suppress_alert(
                    indicator_id=alert['indicator_id'],
                    community_id=alert['community_id'],
                    test_env=False
                )
            counter += 1
            logger.info(counter)
    elif res is None:
        logger.warning("There are no results.")
    return None


def print_env_variables():
    env_variables = {
        "username": config('PERCH_USER'),
        "password": config('PASSWORD'),
        "api_key": config('API_KEY'),
        "base_url": config('URL'),
        "team_id": config('TEAM_ID'),
        "qa_username": config('QA_PERCH_USER'),
        "qa_password": config('QA_PASSWORD'),
        "qa_api_key": config('QA_API_KEY'),
        "qa_base_url": config('QA_URL'),
        "qa_team_id": config('QA_TEAM_ID'),
    }
    for key, value in env_variables.items():
        logger.debug(f'{key} = {value}')



def main(test_env: bool, num: int) -> None:
    client = PerchAPIClient(**set_configuration(test_env))
    close_alerts(client, test_env, num)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Determine whether to use test env or production env.')
    parser.add_argument('-t', '--test', action='store_true', help='use the QA environment')
    parser.add_argument('-n', '--num', action='store', help='show number of alerts, up to 1000')
    parser.add_argument('--check_env', action='store_true', help='check your environment variables')
    args = parser.parse_args()
    print(args)
    if args.check_env is True:
        print_env_variables()
    elif args.check_env is False:
        if args.num is None:
            logger.error("Must use add a number for the alerts you want to see.")
        elif isinstance(args.num, str) is True:
            num = int(args.num)
            main(test_env=args.test, num=num)

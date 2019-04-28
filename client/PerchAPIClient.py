from requests import Session
import logging


module_logger = logging.getLogger('perch_demo_refresh.client.PerchAPIClient')


class PerchAPIClient():
    def __init__(
            self,
            api_key: str,
            username: str,
            password: str,
            base_url: str,
            team_id: int):
        # Prepare the client with relevant API information and get a token for continued requests
        self.username = username
        self.password = password
        self.api_key = api_key
        self.base_url = base_url
        self.team_id = team_id
        self.session = Session()
        self.auth_token = self.get_auth_token()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.auth_token
        })
        self.logger = logging.getLogger('perch_demo_refresh.client.PerchAPIClient')

    # Every API request needs an auth_token, and we generate one for use with every request
    # of this instance of the client
    def get_auth_token(self):
        request_body = {
            'username': self.username, 
            'password': self.password
        }

        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        })

        # This is a versioned API endpoint
        url = self.base_url + '/v1/auth/access_token'
        
        res = self.session.post(url, json=request_body)
        
        if not res.status_code == 200:
            self.logger.error(f'Status code: {res.status_code}. URL: {url}\nReason: {res.text}')
        else:
            res_body = res.json()
            return res_body['access_token']

    # Pull a list of all alerts and sort them by last seen
    # Limit number of results by 
    def get_alerts_list(
            self,
            number_of_results: int) -> None or list:
        if number_of_results > 1000:
            self.logger.error(f"Too many results. Requested amount: {number_of_results}. Max amount: 1000.")
            return None
        params = {
            'team_id': self.team_id,
            'was_suppressed': False,
            'page_size': number_of_results,
            'status': 0,
            'closed': False,
            'ordering': '-last_seen_at'
        }
        # This is a versioned API endpoint
        url = self.base_url + '/v1/alerts'
        res = self.session.get(url, params=params)

        if not res.status_code == 200:
            self.logger.error(f'Status code: {res.status_code}\nReason: {res.text}')
            return None
        elif len(res.json()['results']) < 1:
            self.logger.warning(f'There are no alerts in the organization.')
            return res.json()['results']
        else:
            results = res.json()['results']
            return results

    def suppress_alert(
            self,
            indicator_id: str,
            community_id: int,
            test_env: bool = False):
        # This is not a versioned API endpoint
        if test_env is True:
            url = self.base_url + '/alerts/suppressions'
        elif test_env is False:
            # The Perch application API (not the api.perch.rocks endpoint).
            # The reason to use this is because the /alerts/suppressions
            # endpoint is not yet public under api.perch.rocks.
            # Once this is changed, I will remove this from the script.
            url = 'https://api.perchsecurity.com/alerts/suppressions'
        data = {
            'indicatorId': indicator_id,
            'community': community_id,
            'teamId': self.team_id,
            'sendEmail': False,
            'reason': 1,
            'reasonDetail': 0,
            'notes': 'Removing demo alerts.',
            'scope': 0,
            'observableId': None,
        }

        res = self.session.post(url, json=data)
        
        # Check the status code -- as long as it is within the 200 range, it has been accepted
        if not res.status_code < 300:
            self.logger.error(f'Status code: {res.status_code}\nReason: {res.text}')
        else:
            # For debugging purposes
            self.logger.info(f'Status code: {res.status_code}\nJSON Result: {res.json()}')

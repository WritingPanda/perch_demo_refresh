from requests import Session
import logging


# Set logging level for debug purposes
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class PerchAPIClient():
    def __init__(
            self,
            api_key: str,
            username: str,
            password: str,
            base_url: str,
            team_id: int):
        # Prepare the client with relevant API information and get a token for continued requests
        self.api_key = api_key
        self.username = username
        self.password = password
        self.team_id = team_id
        self.base_url = base_url
        self.session = Session()
        self.auth_token = self.get_auth_token()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.auth_token
        })

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
            logger.error(f'Status code: {res.status_code}. URL: {url}\nReason: {res.text}')
        else:
            res_body = res.json()
            return res_body['access_token']

    # Pull a list of all alerts and sort them by last seen
    # Limit number of results by 
    def get_alerts_list(
            self,
            number_of_results: int):
        if number_of_results > 1000:
            logger.error(f"Too many results. Requested amount: {number_of_results}. Max amount: 1000.")
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
            logger.error(f'Status code: {res.status_code}\nReason: {res.text}')
        elif len(res.json()['results']) < 1:
            logger.warning(f'There are no alerts in the organization.')
            return None
        else:
            results = res.json()['results']
            return results

    def suppress_alert(
            self,
            indicator_id: str,
            community_id: int):
        # This is not a versioned API endpoint
        url = self.base_url + '/alerts/suppressions'
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
            logger.error(f'Status code: {res.status_code}\nReason: {res.text}')
        else:
            # For debugging purposes
            logger.info(f'Status code: {res.status_code}\nJSON Result: {res.json()}')

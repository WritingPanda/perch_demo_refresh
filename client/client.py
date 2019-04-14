import requests, json


class PerchAPIClient():
    def __init__(self, 
                 api_key: str, 
                 username: str, 
                 password: str,
                 base_url: str,
                 team_id: int):

        self.api_key = api_key
        self.username = username
        self.password = password
        self.team_id = team_id
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = self.get_auth_token()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.auth_token
        })

    def get_auth_token(self):
        request_body = json.dumps({'username': self.username, 'password': self.password})
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        })
        url = self.base_url + '/auth/access_token/'
        
        res = self.session.post(url, data=request_body)

        if not res.status_code == 200:
            return f"Error. Status code: {res.status_code}\nReason: {res.text}"

        res_body = res.json()
        return res_body['access_token']

    def get_alerts_list(self, number_of_results: int):
        params = {
            'team_id': self.team_id,
            'was_suppressed': False,
            'page_size': number_of_results,
            'status': 0,
            'closed': False,
            'ordering': '-last_seen_at'
        }
        res = self.session.get(self.base_url + '/alerts', params=params)

        if not res.status_code == 200:
            return f"Error. Status code: {res.status_code}\nReason: {res.text}"
        
        results = res.json()['results']
        return results

    def suppress_alert(self, 
                       indicator_id: str, 
                       community_id: int, 
                       observable_id: int):
        url = self.base_url + '/alerts/suppressions'
        data = {
            'indicatorId': indicator_id,
            'community': community_id,
            'observableId': observable_id,
            'teamId': self.team_id,
            'sendEmail': 0,
            'reason': 1,
            'reasonDetail': 0,
            'notes': 'Removing demo alerts.',
            'scope': 0,
        }

        res = self.session.post(url, json=data)
        
        if not res.status_code == 200:
            return f"Error. Status code: {res.status_code}\nReason: {res.text}"

        return res.json()

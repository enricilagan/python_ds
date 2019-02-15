import requests
import uplink
from uplink_helper import raise_for_status
from uplink_helper import API_KEY


@uplink.json
@raise_for_status
class MovieSearchOMDB(uplink.Consumer):

    def __init__(self):
        super().__init__(base_url=f'http://www.omdbapi.com')

    @uplink.get('/?apikey={apikey}&type=movie&s={title}&page={page}')
    def movie_search(self, title, page=1, apikey=API_KEY) -> requests.models.Response:
        """Search for movies"""

    @uplink.get('/?apikey={apikey}&type=series&s={title}&page={page}')
    def series_search(self, title, page=1, apikey=API_KEY) -> requests.models.Response:
        """Search using director"""

    @uplink.get('/?apikey={apikey}&i={code}')
    def code_search(self, code, apikey=API_KEY) -> requests.models.Response:
        """Search one item based on title"""

    @uplink.get('/?apikey={apikey}&t={title}')
    def title_search(self, title, apikey=API_KEY) -> requests.models.Response:
        """Search a single item based on title"""

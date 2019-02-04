import requests
import os


class TmdbApi(object):
    """
        This is a base class that all api endpoints will inherit from
    """

    def __init__(self):

        api_key = os.getenv("TMDB_KEY")
        if api_key is None:
            raise Exception("The api_key is missing.")

        self.base_url = "https://api.themoviedb.org/3"
        self.api_key = "?api_key={}".format(api_key)


    def _get_appended_data(self, data_to_append):
        return "&append_to_response={}".format(",".join(data_to_append) if isinstance(data_to_append, list) else data_to_append)

    def _check_status_code(self, status_code):
        if status_code != 200:
            raise AssertionError("The api call failed.  The response's status code was {}".format(status_code))


class TmdbMoviesApi(TmdbApi):
    """
        This is a class specific to testing the movies endpoint.
    """

    def __init__(self):
        super(TmdbMoviesApi, self).__init__()
        self.movie_url = "{}/movie".format(self.base_url)

    def get_movie_details(self, media_id, detail_type=None, append_detail=None, check_response_code=True):
        # Verify detail_type and append_detail aren't being used at the same time
        if detail_type is not None and append_detail is not None:
            raise Exception("You don't need to set data_type if you are using append_detail.")

        # Create the url
        detail_type = "/{}".format(detail_type) if detail_type is not None else ""
        append = "{}".format(self._get_appended_data(append_detail)) if append_detail is not None else ""
        url = "{}/{}{}{}{}".format(self.movie_url, str(media_id), detail_type, self.api_key, append)

        response = requests.get(url)

        if check_response_code:
            self._check_status_code(response.status_code)

        return response

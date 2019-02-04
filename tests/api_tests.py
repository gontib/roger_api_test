import simplejson as json
from base_test import BaseTest
from tmdb_api import TmdbMoviesApi


class MovieApiTests(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        self.movie_api = TmdbMoviesApi()

    def tearDown(self):
        BaseTest.tearDown(self)

    def test_movie_details(self):
        """
            Test the correct movie id and title are returned using "How to train your dragon 3" id number 166428
        """
        movie_id = "166428"
        title = "How to Train Your Dragon: The Hidden World"

        # Send data request and convert response to json
        response = self.movie_api.get_movie_details(movie_id)
        data = json.loads(response.text)

        # Assert against response data
        self.assertTrue(data["id"] == int(movie_id), "The returned movie id: {} did't match the expected id: {}.".format(data["id"], movie_id))
        self.assertTrue(data["original_title"] == title, "The returned movie title: {} did't match the expected title: {}.".format(data["original_title"], title))

    def test_non_existing_movie_id(self):
        """
            Test that a 404 response if given for a non existing movie id
        """
        code = 404
        message = "The resource you requested could not be found."

        # Send data request and convert response to json
        response = self.movie_api.get_movie_details("1", check_response_code=False)
        data = json.loads(response.text)

        # Assert against response data
        self.assertTrue(response.status_code == code, "The response's status code was {} when {} was expected.".format(response.status_code, code))
        self.assertTrue(data["status_message"] == message, "The responses message was {} when {} was expected.".format(data["status_message"], message))

    def test_movie_images(self):
        """
            Test that movie image data is returned using "Lord of the Rings" id number 123
        """
        movie_id = "123"

        # Send data request and convert response to json
        response = self.movie_api.get_movie_details(movie_id, "images")
        data = json.loads(response.text)

        # Assert against response data
        self.assertTrue(data["id"] == int(movie_id), "The returned movie id: {} did't match the expected id: {}.".format(data["id"], movie_id))
        self.assertTrue(len(data["backdrops"]) > 0 and len(data["posters"]) > 0, "No movie image data was found.")

    def test_append_to_response_functionality(self):
        """
            Test that multiple sets of movie data is returned with one request using "The Empire Stikes Back" id number 1891
        """
        movie_id = "1891"
        title = "The Empire Strikes Back"

        # Send data request and convert response to json
        response = self.movie_api.get_movie_details(movie_id, append_detail=["release_dates", "credits"])
        data = json.loads(response.text)

        # Assert against response data
        self.assertTrue(data["id"] == int(movie_id), "The returned movie id: {} did't match the expected id: {}.".format(data["id"], movie_id))
        self.assertTrue(data["title"] == title, "The returned movie title: {} did't match the expected title: {}.".format(data["title"], title))
        self.assertIn("release_dates", data)
        self.assertIn("credits", data)

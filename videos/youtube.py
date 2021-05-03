import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


class Youtube:
    def __init__(self):
        self.client_secrets_file = "secret_key.json"
        self.api_version = "v3"
        self.api_service_name = "youtube"

    def get_youtube_object(self):
        """"
        This is to make youtube connection
        """
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials)

        return youtube

    def search_youtube_videos(self, search, publish_after, publish_before, next_page_token=None):
        """
        This is to get the videos uploaded in a particular time
        """
        youtube = self.get_youtube_object()
        final_params = {"part": "snippet",
                        "maxResults": 50,
                        "publishedAfter": str(publish_after),
                        "publishedBefore": str(publish_before),
                        "q": search}
        if next_page_token:
            final_params["pageToken"] = next_page_token
        request = youtube.search().list(
            **final_params
        )
        response = request.execute()
        return response

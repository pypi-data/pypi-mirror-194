import requests


class BaseAPIConsumer:
    base_url = None

    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url

        if not base_url:
            raise ValueError(
                "A base URL is required. Specify it as a class member, or when initializing your class instance."
            )

    def construct_url(self, *url_parts):
        parts = [self.base_url] + [part.strip("/") for part in url_parts]
        return "/".join(parts)

    def base_request(self, method, path):
        return requests.request(method, self.construct_url(path))

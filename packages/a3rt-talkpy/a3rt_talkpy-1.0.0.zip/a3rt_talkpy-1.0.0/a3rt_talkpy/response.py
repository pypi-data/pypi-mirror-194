class Response:
    def __init__(self, response: dict):
        self.resp: dict = response

    def is_empty(self) -> bool:
        return self.status == 2000

    @property
    def status(self) -> int:
        return self.resp['status']

    @property
    def message(self) -> str:
        return self.resp['message']

    @property
    def results(self) -> list[dict]:
        return self.resp['results']

    @property
    def perplexity(self) -> float:
        return self.results[0]['perplexity']

    @property
    def reply(self) -> str:
        return self.results[0]['reply']



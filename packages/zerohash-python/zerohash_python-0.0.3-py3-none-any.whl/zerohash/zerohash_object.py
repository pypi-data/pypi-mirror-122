from zerohash import api_requestor, util


class ZerohashObject(dict):
    def __init__(self, id=None, credentials=None, **params):
        super().__init__()

        for k, v in params.items():
            self.__setattr__(k, v)

        self.__setattr__("credentials", credentials)
        if id:
            self["id"] = id

    @classmethod
    def construct_from(cls, values, credentials):
        instance = cls(values.get("id"), credentials=credentials)
        instance.refresh_from(values, credentials)
        return instance

    def request(self, method, url, params=None, headers=None):
        requestor = api_requestor.APIRequestor()
        response = requestor.request(method, url, params, headers)

        return util.convert_to_zerohash_object(response, credentials=self.credentials)

    def refresh_from(self, values, credentials=None, partial=False):
        self.credentials = credentials or getattr(values, "credentials", None)

        # TODO: conditional for if partial=True

        # Any values not set in values will be cleared/removed from the object returned after refresh
        removed = set(self.keys()) - set(values)

        # self._transient_values = self._transient_values - set(values)

        for k, v in values.items():
            super().__setitem__(k, util.convert_to_zerohash_object(v, credentials))

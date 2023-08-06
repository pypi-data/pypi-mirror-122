import requests

from .base import GenericAPI, ERROR_THRESHOLD


class SearchAPI(GenericAPI):
    """
    Search API switchboard.

    Contains methods that correspond to HyperThought search endpoints.

    At the present time, there is only one search endpoint that is intended
    for API use.  Search features are in active development, however, so this
    will not be true for long.

    Parameters
    ----------
    auth : auth.Authorization
        Authorization object used to get headers and cookies needed to call
        HyperThought endpoints.
    """

    VALID_FACETS = {
        'CreatedOn',
        'ModifiedOn',
        'CreatedBy',
        'ModifiedBy',
        'FileType',
    }

    def __init__(self, auth):
        super().__init__(auth)

    def get_valid_facets(self):
        """Get a set of facet keys that can be used with the search method."""
        return set(self.VALID_FACETS)

    def search(self, query, start_record=0, page_length=25, facets=None):
        """
        Get information on parsers available to the current user.

        Parameters
        ----------
        query : str
            The requested search query.
        start_record : int
            The starting location in the list of matching records to return.
            Defaults to `0`.
        start_record : int
            How many records to return with each call.  Defaults to `25`.
        start_record : list of str
            An optional list of facets to filter the requested query by.
            Defaults to `None`.
        """
        if facets is None:
            facets = []
        else:
            facets = list(facets)

        # TODO:  Validate facet keys.
        curried_request = partial(
            requests.post,
            url=f'{self._base_url}/api/search/v1/api-search/',
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            json={
                'query': query,
                'start': start_record,
                'length': page_length,
                'facets': facets,
            },
            verify=self.auth.verify
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

import requests
from urllib3.util import parse_url
from .utils.common_types \
    import DownloadType, ResultPerPage, ViewType, SearchField, SearchPhrasing,\
    SortField, SortType

class SearchQuery():
    def __init__(self, main_query,
                 dl_type: DownloadType =
                 DownloadType.RESUMED_DL_WITH_ORIGINAL_FILENAME,
                 res_number: ResultPerPage = ResultPerPage.TwentyFive,
                 view_type: ViewType = ViewType.Simple,
                 search_phrasing: SearchPhrasing = SearchPhrasing.WITHOUT_MASK,
                 search_field: SearchField = SearchField.Default,
                 sort_field: SortField = None,
                 sort_type: SortType = None):
        self.base_url = 'https://libgen.rs/search.php'
        self.main_query = main_query
        self.dl_type = dl_type
        self.res_number = res_number
        self.view_type = view_type
        self.search_phrasing = search_phrasing
        self.search_field = search_field
        self.sort_field = sort_field
        self.sort_type = sort_type

    def __eq__(self, other):
        return \
            self.base_url == other.base_url and\
            self.main_query == other.main_query and\
            self.dl_type == other.dl_type and\
            self.res_number == other.res_number and\
            self.view_type == other.view_type and\
            self.search_phrasing == other.search_phrasing and\
            self.search_field == other.search_field and\
            self.sort_field == other.sort_field and\
            self.sort_type == other.sort_type

    # TODO: Add Sort To This
    def __str__(self):
        return f"""
                {self.main_query}\n
                {self.dl_type}\n
                {self.res_number}\n
                {self.view_type}\n
                {self.search_phrasing}\n
                {self.search_field}\n
              """

    @staticmethod
    def from_url(url):
        # This is because when sorting is added, an empty query is produced by
        # urlparse.
        queries = requests.utils.urlparse(url).query.split('&')
        queries = list(filter(lambda x: x != '', queries))
        # print(queries)

        equivalent_args = {
            'req': 'main_query',
            'open': 'dl_type',
            'res': 'res_number',
            'view': 'view_type',
            'phrase': 'search_phrasing',
            'column': 'search_field',
            'sort': 'sort_field',
            'sortmode': 'sort_type'
        }
        arguments = {}

        for item in queries:
            key, value = item.split('=', maxsplit=1)
            key = equivalent_args[key]
            if key == 'main_query':
                # This is because the whitespace in query is automatically
                # converted to '+' in the resulting url on libgen
                value = " ".join(value.split('+'))
            elif key == 'dl_type':
                value = DownloadType(int(value))
            elif key == 'res_number':
                value = ResultPerPage(int(value))
            elif key == 'view_type':
                value = ViewType(value)
            elif key == 'search_phrasing':
                value = SearchPhrasing(int(value))
            elif key == 'search_field':
                value = SearchField(value)
            elif key == 'sort_field':
                value = SortField(value)
            elif key == 'sort_type':
                value = SortType(value)

            arguments[key] = value

        search_query = SearchQuery(**arguments)

        return search_query

    def get_results_page_url(self) -> str:
        url_params = {
            'req': self.main_query,
            'open': self.dl_type.value,
            'res': self.res_number.value,
            'view': self.view_type.value,
            'phrase': self.search_phrasing.value,
            'column': self.search_field.value,
        }

        if self.sort_field and self.sort_type:
            url_params = {
                'req': self.main_query,
                'open': self.dl_type.value,
                'res': self.res_number.value,
                'view': self.view_type.value,
                'phrase': self.search_phrasing.value,
                'column': self.search_field.value,
                'sort': self.sort_field.value,
                'sortmode': self.sort_type.value,
            }

        # Here we're only using requests library to parse url not to create or
        # send a request
        my_url = requests.Request('get',
                                  self.base_url,
                                  params=url_params).prepare().url
        return my_url if my_url else ""

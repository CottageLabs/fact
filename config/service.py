# overrides for the webapp deployment
DEBUG = False
PORT = 5015
SSL = False
THREADED = True

# You need to put this in your local.cfg - it allows us to connect to the fact api
ROMEO_API_KEY = ""

# configuration for elasticsearch connection for autocomplete handling

ELASTIC_SEARCH_HOST = "http://localhost:9200"
ELASTIC_SEARCH_INDEX = "fact"

ELASTIC_SEARCH_VERSION = "1.4.2"

ELASTIC_SEARCH_MAPPINGS = [
    "service.dao.JournalAutocompleteDAO"
]

def journal_ac_input_filter(val):
    return val.lower()

AUTOCOMPLETE_COMPOUND = {
    "journal" : {                                  # name of the autocomplete, as represented in the URL (have as many of these sections as you need)
        "fields" : ["issn", "journal"],         # fields to return in the compound result
        "filters" : {                           # filters to apply to the result set
            "issn.exact" : {                    # field on which to filter
                "start_wildcard" : True,        # apply start wildcard?
                "end_wildcard": True,           # apply end wildcard?
                "boost" : 2.0                   # boost to apply to matches on this field
            },
            "journal_lower.exact" : {
                "start_wildcard" : True,
                "end_wildcard": True,
                "boost" : 1.0
            }
        },
        "input_filter" : journal_ac_input_filter,
        "default_size" : 10,                    # if no size param is specified, this is how big to make the response
        "max_size" : 25,                        # if a size param is specified, this is the limit above which it won't go
        "dao" : "service.dao.JournalAutocompleteDAO"           # classpath for DAO which accesses the underlying ES index
    }
}
import esprit
from portality.core import app

class JournalAutocompleteDAO(esprit.dao.DomainObject):
    __type__ = 'journal'
    __conn__ = esprit.raw.Connection(app.config.get('ELASTIC_SEARCH_HOST'), app.config.get('ELASTIC_SEARCH_INDEX'))

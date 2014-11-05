import esprit
from octopus.core import app
from octopus.modules.es import dao

class JournalAutocompleteDAO(dao.ESDAO):
    __type__ = 'journal'

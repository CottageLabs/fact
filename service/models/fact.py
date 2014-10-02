from service import dao

class JournalAutocomplete(dao.JournalAutocompleteDAO):
    @property
    def issn(self):
        return self.data.get("issn", [])

    @issn.setter
    def issn(self, val):
        if not isinstance(val, list):
            val= [val]
        self.data["issn"] = val

    @property
    def journal(self):
        return self.data.get("journal")

    @journal.setter
    def journal(self, val):
        self.data["journal"] = val
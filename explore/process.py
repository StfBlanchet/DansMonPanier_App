"""
dansMonPanier
string processing module
"""


from unidecode import unidecode


"""
This class pre processes
the user's query
"""


class Process:

    def __init__(self):
        self.q = str()

    def formatting(self, raw_query):
        """
        Put the main entity in the plural
        if not the case
        """
        self.q = unidecode(raw_query).split()
        self.q[0] = self.q[0].capitalize()
        if not self.q[0].endswith('s') and not self.q[0].endswith('x') and not self.q[0].endswith('au'):
            self.q[0] = self.q[0] + 's'
        elif self.q[0].endswith('au'):
            self.q[0] = self.q[0] + 'x'
        self.q = " ".join(self.q)
        return self.q

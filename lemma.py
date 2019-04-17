import requests
"""Way to get stem, to find different ways to write a word"""

class Lemma(object):
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({'referer': 'http://woordenlijst.org/'})
        self.url = "http://woordenlijst.org/api-proxy/"
        self.params = {
            'm': 'search',
            'tactical': 'true'
        }

    def request(self, word):
        self.params['searchValue'] = word
        return self.s.get(url=self.url, params=self.params)

    def get_entries(self, word):
        r = self.request(word)
        if r.status_code == 200:
            return r.json()["_embedded"]["exact"]
        else:
            return []

    def get_lemmas(self, word, include_type=False):
        forms = [(entry['lemma'], entry['type']) for entry in self.get_entries(word)]

        if not include_type:
            forms = [form[0] for form in forms]

        return forms

    def get_all_forms(self, word, include_type=False):
        forms = [(form['orth'], form['type']) for entry in self.get_entries(word) for forms in entry["positions"] for
                 form in forms["forms"]]

        if not include_type:
            forms = [form[0] for form in forms]

        return forms


if __name__ == "__main__":
    lemma = Lemma()
    word = 'wetten'
    print(lemma.get_lemmas(word))
    print(lemma.get_all_forms(word))

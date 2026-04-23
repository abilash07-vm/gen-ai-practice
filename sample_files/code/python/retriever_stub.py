class Retriever:
    def __init__(self, store):
        self.store = store

    def search(self, query):
        return self.store.get(query, [])

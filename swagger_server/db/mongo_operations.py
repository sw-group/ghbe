from pymongo import MongoClient
from datetime import datetime

class MongoOperations:
    def __init__(self, db_name='mining', collection_name='issues', uri='mongodb://localhost:27017/'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_issues(self, repo, state=None, date_range=None, page=1, sort=None):
        query = {'repo': repo}

        if state:
            query['issue.state'] = state.upper()
        if date_range:
            start_date, end_date = date_range.split(',')
            query['issue.createdAt'] = {
                '$gte': datetime.strptime(start_date, '%Y-%m-%d'),
                '$lte': datetime.strptime(end_date, '%Y-%m-%d')
            }

        # Sorting (1 = asc; -1 = desc)
        sort_order = -1
        if sort:
            field, order = sort.split('-')
            sort_order = 1 if order == 'asc' else -1
        else:
            field = 'createdAt'

        # Pagination
        per_page = 20  # Define your pagination size
        skip = (page - 1) * per_page

        cursor = self.collection.find(query).sort('issue.'+field, sort_order).skip(skip).limit(per_page)

        issues = list(cursor)
        return issues

    def close(self):
        self.client.close()

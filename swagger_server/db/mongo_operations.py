from datetime import datetime
from pymongo import MongoClient


class MongoOperations:
    def __init__(self, db_name='mining', collection_name='repositories', uri='mongodb://localhost:27017/'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_repositories(self, name=None, language=None, is_private=None, date_range=None, stars=None, forks=None,
                         issues=None, pulls=None, workflows=None, watchers=None, page=None, sort=None):
        query = {}

        if name:
            query['data.full_name'] = name.split(':')[1] if '/' in name else {'$regex': name, '$options': 'i'}

        if language:
            query['data.language'] = language

        if is_private is not None:
            query['data.private'] = is_private

        if date_range:
            start_date, end_date = date_range.split(',')
            s_date = datetime.strptime(start_date, '%Y-%m-%d')
            e_date = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(), datetime.max.time())
            query['data.updated_at'] = {
                '$gte': s_date.isoformat(),  # Start of the filter_date
                '$lt': e_date.isoformat()  # End of the filter_date
            }

        if stars:
            min_stars, max_stars = stars.split(',')
            query['data.starts_count'] = {'$gte': int(min_stars), '$lte': int(max_stars)}

        if pulls:
            min_pull, max_pull = pulls.split(',')
            query['data.pull_request_count'] = {'$gte': int(min_pull), '$lte': int(max_pull)}

        if forks:
            min_forks, max_forks = forks.split(',')
            query['data.forks_count'] = {'$gte': int(min_forks), '$lte': int(max_forks)}

        if issues:
            min_issues, max_issues = issues.split(',')
            query['data.issue_count'] = {'$gte': int(min_issues), '$lte': int(max_issues)}

        if workflows:
            min_workflows, max_workflows = workflows.split(',')
            query['data.workflows_count'] = {'$gte': int(min_workflows), '$lte': int(max_workflows)}

        if watchers:
            min_watchers, max_watchers = watchers.split(',')
            query['data.watchers_count'] = {'$gte': int(min_watchers), '$lte': int(max_watchers)}

        # Sorting (1 = asc; -1 = desc)
        sort_order = -1
        if sort:
            field, order = sort.split('-')
            sort_order = 1 if order == 'asc' else -1
        else:
            field = 'updated_at'

        # Pagination
        per_page = 20  # Define your pagination size
        skip = (page - 1) * per_page

        if page == -1:
            cursor = self.collection.find(query).sort('data.' + field, sort_order)
        else:
            cursor = self.collection.find(query).sort('data.' + field, sort_order).skip(skip).limit(per_page)

        repositories = list(cursor)
        return repositories

    def get_repository(self, full_name):
        return self.collection.find_one({"_id": full_name})

    def get_issues(self, repo, state=None, date_range=None, page=1, sort=None):
        query = {'repo': repo}

        if state:
            query['state'] = state.upper()
        if date_range:
            start_date, end_date = date_range.split(',')
            s_date = datetime.strptime(start_date, '%Y-%m-%d')
            e_date = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(), datetime.max.time())
            query['updatedAt'] = {
                '$gte': s_date.isoformat(),  # Start of the filter_date
                '$lt': e_date.isoformat()  # End of the filter_date
            }

        # Sorting (1 = asc; -1 = desc)
        sort_order = -1
        if sort:
            field, order = sort.split('-')
            sort_order = 1 if order == 'asc' else -1
        else:
            field = 'updatedAt'

        # Pagination
        per_page = 20  # Define your pagination size
        skip = (page - 1) * per_page

        if page == -1:
            cursor = self.collection.find(query).sort(field, sort_order)
        else:
            cursor = self.collection.find(query).sort(field, sort_order).skip(skip).limit(per_page)

        issues = list(cursor)
        return issues

    def get_comments(self, repo, number, page=1):
        query = {'repo': repo, 'issue_number': int(number)}

        # Sorting (1 = asc; -1 = desc)
        sort_order = -1
        field = 'createdAt'

        # Pagination
        per_page = 20  # Define your pagination size
        skip = (page - 1) * per_page

        cursor = self.collection.find(query).sort(field, sort_order).skip(skip).limit(per_page)

        comments = list(cursor)
        return comments

    def get_workflows(self, full_name):
        return self.collection.find_one({"_id": full_name})

    def close(self):
        self.client.close()

    def count_repositories(self, name=None, language=None, is_private=None, date_range=None, stars=None, forks=None,
                           issues=None, pulls=None, workflows=None, watchers=None):
        query = {}

        if name:
            query['data.full_name'] = name.split(':')[1] if '/' in name else {'$regex': name, '$options': 'i'}

        if language:
            query['data.language'] = language

        if is_private is not None:
            query['data.private'] = is_private

        if date_range:
            start_date, end_date = date_range.split(',')
            s_date = datetime.strptime(start_date, '%Y-%m-%d')
            e_date = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(), datetime.max.time())
            query['data.updated_at'] = {
                '$gte': s_date.isoformat(),  # Start of the filter_date
                '$lt': e_date.isoformat()  # End of the filter_date
            }

        if stars:
            min_stars, max_stars = stars.split(',')
            query['data.starts_count'] = {'$gte': int(min_stars), '$lte': int(max_stars)}

        if pulls:
            min_pull, max_pull = pulls.split(',')
            query['data.pull_request_count'] = {'$gte': int(min_pull), '$lte': int(max_pull)}

        if forks:
            min_forks, max_forks = forks.split(',')
            query['data.forks_count'] = {'$gte': int(min_forks), '$lte': int(max_forks)}

        if issues:
            min_issues, max_issues = issues.split(',')
            query['data.issue_count'] = {'$gte': int(min_issues), '$lte': int(max_issues)}

        if workflows:
            min_workflows, max_workflows = workflows.split(',')
            query['data.workflows_count'] = {'$gte': int(min_workflows), '$lte': int(max_workflows)}

        if watchers:
            min_watchers, max_watchers = watchers.split(',')
            query['data.watchers_count'] = {'$gte': int(min_watchers), '$lte': int(max_watchers)}

        total = self.collection.count_documents(query)
        return total

    def count_issues(self, repo, state=None, date_range=None):
        query = {'repo': repo}

        if state:
            query['state'] = state.upper()
        if date_range:
            start_date, end_date = date_range.split(',')
            s_date = datetime.strptime(start_date, '%Y-%m-%d')
            e_date = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(), datetime.max.time())
            query['updatedAt'] = {
                '$gte': s_date.isoformat(),  # Start of the filter_date
                '$lt': e_date.isoformat()  # End of the filter_date
            }

        total = self.collection.count_documents(query)

        return total

    def count_issue_comments(self, repo, number=None):
        query = {'repo': repo, 'issue_number': int(number)}

        total = self.collection.count_documents(query)

        return total

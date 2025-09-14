from datetime import datetime

import swagger_server.db.database


class MongoOperations:
    @staticmethod
    def get_repositories(name=None, language=None, is_private=None, date_range=None, stars=None, forks=None,
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
            query['data.stars_count'] = {'$gte': int(min_stars), '$lte': int(max_stars)}

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

        if page <= -1:
            cursor = swagger_server.db.database.mongo.db.repositories.find(query).sort('data.' + field, sort_order)
        else:
            cursor = (swagger_server.db.database.mongo.db.repositories.find(query).sort('data.' + field, sort_order)
                                    .skip(skip).limit(per_page))

        repositories = list(cursor)
        return repositories

    @staticmethod
    def get_repository(full_name):
        return swagger_server.db.database.mongo.db.repositories.find_one({"_id": full_name})

    @staticmethod
    def get_issues(repo, state=None, date_range=None, page=1, sort=None):
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

        if page <= -1:
            cursor = swagger_server.db.database.mongo.db.issues.find(query).sort(field, sort_order)
        else:
            cursor = (swagger_server.db.database.mongo.db.issues.find(query).sort(field, sort_order)
                      .skip(skip).limit(per_page))

        issues = list(cursor)
        return issues

    @staticmethod
    def get_prs(repo, state=None, date_range=None, page=1, sort=None):
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

        if page <= -1:
            cursor = swagger_server.db.database.mongo.db.prs.find(query).sort(field, sort_order)
        else:
            cursor = (swagger_server.db.database.mongo.db.prs.find(query).sort(field, sort_order)
                      .skip(skip).limit(per_page))

        prs = list(cursor)
        return prs

    @staticmethod
    def get_comments(repo, number, page=1):
        query = {'repo': repo, 'issue_number': int(number)}

        # Sorting (1 = asc; -1 = desc)
        sort_order = -1
        field = 'createdAt'

        # Pagination
        per_page = 20  # Define your pagination size
        skip = (page - 1) * per_page

        cursor = (swagger_server.db.database.mongo.db.comments.find(query).sort(field, sort_order)
                  .skip(skip).limit(per_page))

        comments = list(cursor)
        return comments

    @staticmethod
    def get_workflows(full_name):
        return swagger_server.db.database.mongo.db.workflows.find_one({"_id": full_name})

    @staticmethod
    def count_repositories(name=None, language=None, is_private=None, date_range=None, stars=None, forks=None,
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
            query['data.stars_count'] = {'$gte': int(min_stars), '$lte': int(max_stars)}

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

        total = swagger_server.db.database.mongo.db.repositories.count_documents(query)
        return total

    @staticmethod
    def count_issues(repo, state=None, date_range=None):
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

        total = swagger_server.db.database.mongo.db.issues.count_documents(query)

        return total

    @staticmethod
    def count_prs(repo, state=None, date_range=None):
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

        total = swagger_server.db.database.mongo.db.prs.count_documents(query)

        return total

    @staticmethod
    def count_issue_comments(repo, number=None):
        query = {'repo': repo, 'issue_number': int(number)}

        total = swagger_server.db.database.mongo.db.comments.count_documents(query)

        return total

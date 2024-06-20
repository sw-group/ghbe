
def generate_date_count_map(issue_list):
    from collections import defaultdict
    from swagger_server.models import MapStringNumber

    date_count_map = defaultdict(int)

    for issue in issue_list:
        # Extract the date part from the created_at field
        created_date = issue['created_at'].date()
        # Convert the date to a string for dictionary keys
        created_date_str = created_date.isoformat()
        # Increment the count for the extracted date
        date_count_map[created_date_str] += 1

    return MapStringNumber.from_dict(date_count_map)


def __check_labels(issue_labels, labels, label_count_map):
    for label in labels:
        for issue_label in issue_labels:
            if label in issue_label["name"]:
                label_count_map[label] += 1
                return True
    return False


def __check_body_and_title(issue, labels, label_count_map):
    for label in labels:
        if label in issue["body"] or label in issue["title"]:
            label_count_map[label] += 1
            return


def generate_label_count_map(issues):
    from collections import defaultdict
    labels = ['bug', 'documentation', 'duplicate', 'enhancement', 'good first issue', 'help wanted', 'invalid',
              'question', 'wontfix']
    label_count_map = defaultdict(int)

    for issue in issues:
        if issue["labels"]:  # Ensure issue.labels is not empty or None
            if __check_labels(issue["labels"], labels, label_count_map):
                continue

        __check_body_and_title(issue, labels, label_count_map)

    return label_count_map


def generate_metrics_workflow_map(workflows):
    from collections import defaultdict
    label_count_map = defaultdict(float)
    # Filter workflows where "lines" is not None
    valid_workflows = [w for w in workflows if w["lines"] is not None]

    # Calculate the sum of lines and count of valid workflows
    total_lines = sum(w["lines"] for w in valid_workflows)

    # Calculate the sum of sizes in bytes and count of valid workflows
    total_size_bytes = sum(convert_size_to_bytes(w["size"]) for w in valid_workflows)

    count_valid_workflows = len(valid_workflows)

    # Calculate the mean
    if count_valid_workflows > 0:
        mean_lines = total_lines / count_valid_workflows
        mean_size_bytes = total_size_bytes / count_valid_workflows
    else:
        mean_lines = 0  # Handle case where there are no valid workflows with "lines" defined
        mean_size_bytes = 0

    label_count_map["lines"] = float(format(mean_lines, ".2f"))
    label_count_map["size"] = float(format(mean_size_bytes, ".2f"))
    return label_count_map


def convert_size_to_bytes(size_str):
    multipliers = {'Bytes': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3}
    size_str = size_str.strip()
    num, unit = size_str.split()
    return float(num) * multipliers[unit]


def accumulate_stats(stats, stats_issues, stats_pulls, stats_workflows, stats_repositories):
    # Initialize nested dictionaries if they are None
    __initialize_nested_dict(stats['issues'], 'daily_closed_progress', {})
    __initialize_nested_dict(stats['issues'], 'daily_opened_progress', {})
    __initialize_nested_dict(stats['pulls'], 'daily_closed_progress', {})
    __initialize_nested_dict(stats['pulls'], 'daily_opened_progress', {})
    __initialize_nested_dict(stats['pulls'], 'merged', 0)
    __initialize_nested_dict(stats['workflows'], 'metrics', {})
    __initialize_nested_dict(stats['repositories'], 'stats', {})

    # Accumulate issues
    __accumulate_dict_values(stats['issues']['daily_closed_progress'], stats_issues.daily_closed_progress)
    __accumulate_dict_values(stats['issues']['daily_opened_progress'], stats_issues.daily_opened_progress)

    # Accumulate pull requests
    __accumulate_dict_values(stats['pulls']['daily_closed_progress'], stats_pulls.daily_closed_progress)
    __accumulate_dict_values(stats['pulls']['daily_opened_progress'], stats_pulls.daily_opened_progress)
    stats['pulls']['merged'] += stats_pulls.merged

    # Accumulate workflows
    __accumulate_dict_values(stats['workflows']['metrics'], stats_workflows.metrics)

    # Accumulate repositories stats
    __accumulate_dict_values(stats['repositories']['stats'], stats_repositories.stats)


def __initialize_nested_dict(d, key, default):
    if d.get(key) is None:
        d[key] = default


def __accumulate_dict_values(target, source):
    for key, value in source.items():
        target.setdefault(key, 0)
        target[key] += value

def validate_date_range(date_range):
    from datetime import datetime
    try:
        start_date_str, end_date_str = date_range.split(',')
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        if (end_date - start_date).days > 31:
            return "dateRange cannot exceed 30 days"
        return None
    except ValueError:
        return "Invalid dateRange format"

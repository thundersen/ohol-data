from timeutils.timeutils import date_range


LOCAL_DIR = '../lifelogs'


def build_names(servers, start_date, end_date):
    result = []

    for day in date_range(start_date, end_date):
        for s in servers:
            for name in build_filenames_for_server_and_day(s, day).values():
                result.append(name)

    return result


def build_local_filenames_for_server_and_day(server_no, day):
    files = build_filenames_for_server_and_day(server_no, day)
    files['log'] = f'{LOCAL_DIR}/{files["log"]}'
    files['names'] = f'{LOCAL_DIR}/{files["names"]}'
    return files


def build_filenames_for_server_and_day(server_no, day):
    server_dir = f'lifeLog_server{server_no}.onehouronelife.com'

    prefix = f'{server_dir}/{day.strftime("%Y_%m%B_%d_%A")}'

    return {
        'log': f'{prefix}.txt',
        'names': f'{prefix}_names.txt'
    }

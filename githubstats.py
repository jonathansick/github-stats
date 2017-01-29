#!/usr/bin/env python
"""
GitHub contribution statistics.

This package is currently design to list all packages in the LSST
organizations that I contributed to over a specific period.
"""

import platform
from getpass import getpass
from datetime import datetime
import os
import github3
from pprint import pprint


def main():
    # Configuration
    start_time = datetime(2015, 10, 1)
    end_time = datetime(2016, 9, 30, hour=23, minute=59, second=59)
    org_names = ['lsst', 'lsst-dm', 'lsst-sqre']
    username = 'jonathansick'

    github = login(username)

    contributed_repos = []
    for org_name in org_names:
        org = github.organization(org_name)
        for repo in org.iter_repos():
            for stats in repo.iter_contributor_statistics():
                # Filter by user's overall contribution presence in repo.
                if stats.author.login == username and stats.total > 0:
                    # Filter by activity in time period
                    active_weeks = [datetime.fromtimestamp(w['w'], tz=None)
                                    for w in stats.weeks
                                    if w['c'] > 0]
                    filtered_weeks = [t for t in active_weeks
                                      if t >= start_time and t < end_time]
                    if len(filtered_weeks) > 0:
                        contributed_repos.append(repo.html_url)
    contributed_repos.sort()
    pprint(contributed_repos)


def login(username):
    cred_path = os.path.expanduser('~/.github-stats-login')
    if not os.path.isfile(cred_path):
        create_token(username, cred_path)

    with open(cred_path, 'r') as fdo:
        token = fdo.readline().strip()

    github = github3.login(token=token,
                           two_factor_callback=github_2fa_callback)

    return github


def create_token(username, cred_path):
    password = getpass('Password for {0}: '.format(username))

    note_template = '{app} via github3 on {host} by {user} {creds}'
    note = note_template.format(app='github-stats',
                                host=platform.node(),
                                user=username,
                                creds=cred_path)
    note_url = 'https://lsst.org/'

    scopes = ['repo', 'user']

    auth = github3.authorize(
        username, password, scopes, note, note_url,
        two_factor_callback=github_2fa_callback)

    with open(cred_path, 'w') as fdo:
        fdo.write(auth.token + '\n')
        fdo.write(str(auth.id))


def github_2fa_callback():
    """
    Prompt for two-factor code
    """
    # http://github3py.readthedocs.org/en/master/examples/two_factor_auth.html
    code = ''
    while not code:
        # The user could accidentally press Enter before being ready,
        # let's protect them from doing that.
        code = input('Enter 2FA code: ')
    return code


if __name__ == '__main__':
    main()

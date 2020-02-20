"""



"""

import csv
import sys
import logging 
import os.path
from datetime import datetime
from collections import defaultdict
from typing import List
from typing import Optional
from typing import Dict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from git import Repo
from tabulate import tabulate


# If logging is set to debug you will see individual git commands in the console
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger("githistory")


@dataclass
class AuthorHistory:
    """Author history information for a single repo"""
    repo: str 
    name: str 
    email: str 
    first_commit_at: datetime = None
    first_commit_message: str = None
    last_commit_at: datetime = None
    last_commit_message: str = None
    commit_count: int = 0


@dataclass
class AuthorHistoryOverMultipleRepos:
    """Author history information spanning over multiple repos"""

    # repo name -> history
    histories: Dict[str, AuthorHistory] = field(default_factory=dict) 
    first_commit_at: datetime = datetime(2030, 1, 1)
    last_commit_at: datetime = datetime(1970, 1, 1)
    commit_count: int = 0

    @property
    def email(self):
        return next(iter(self.histories.values())).email

    @property
    def name(self):
        return next(iter(self.histories.values())).name


@dataclass
class RepositoryHistory:
    """History of a single repo"""
    name: str
    commit_count: int = 0
    
    #: email -> history maps
    authors: Dict[str, AuthorHistory] = field(default_factory=dict)


@dataclass
class FullHistory:
    """History of a project spanning multiple repositories"""
    repos: List[RepositoryHistory] = field(default_factory=list)

    #: Pointers to individiaul author histories 
    #: email -> repo -> AuthorHistory
    all_author_histories: Dict[str, AuthorHistoryOverMultipleRepos] = field(default_factory=dict)


def extract_history(path: Path) -> Optional[RepositoryHistory]:
    """Extract history of one git repository.

    @param :repo: Path to git repository
    @param :all_author_histories: Track author work across multiple repos
    """
    logger.info("Extracting history from %s", path)

    r = Repo(path)
    repo_name = os.path.split(path)[-1]

    # Sanity check
    heads = r.heads    
    if len(heads) == 0:
        logger.warning("Not a git repository: %s", path)
        return None

    master = heads.master

    history = RepositoryHistory(name=repo_name)
    authors = history.authors

    # This will iterate commits from firs to last
    all_commits = list(r.iter_commits('master'))
    for c in all_commits:  # type: Commit
        # https://gitpython.readthedocs.io/en/stable/reference.html#git.objects.commit.Commit
        # https://stackoverflow.com/questions/58550252/how-to-get-commit-author-name-and-email-with-gitpython
        name = c.author.name
        email = c.author.email
    
        author = authors.get(email)  # type: AuthorHistory

        if not author:
            # We are initialising this author
            author = AuthorHistory(repo_name, name, email)
            authors[email] = author
            author.first_commit_at = datetime.fromtimestamp(c.committed_date) # Is UNIX time
            author.first_commit_message = c.message
            author.last_commit_at = datetime.fromtimestamp(c.committed_date)  
            author.last_commit_message = author.last_commit_message            
        else:
            # Adding more commits for the author
            author.last_commit_at = datetime.fromtimestamp(c.committed_date)
            author.last_commit_message = c.message

        author.commit_count += 1
        history.commit_count += 1
        
    return history


def mine_authors_over_repos(history: List[RepositoryHistory]) -> Dict[str, AuthorHistoryOverMultipleRepos]:
    """Create a history info spanning over multiple repos."""
    
    all_author_histories = defaultdict(AuthorHistoryOverMultipleRepos)
    for r in history.repos:
        for email, history in r.authors.items():            
            all_history = all_author_histories[email]
            all_history.first_commit_at = min(all_history.first_commit_at, history.first_commit_at)
            all_history.last_commit_at = max(all_history.last_commit_at, history.last_commit_at)
            all_history.commit_count += history.commit_count
            all_history.histories[r.name] = history
            print("set history ", r.name, history)

    return all_author_histories


def mine_data(repos: List[str]) -> FullHistory:
    """Extract history from multiple git repositories.
    
    Will skip directories that do not look like git repos.
    """
    
    logger.info("Working on %d repositores", len(repos))
    history = FullHistory()
    for repo in repos:
        repo_history = extract_history(Path(repo))
        if repo_history:
            history.repos.append(repo_history)

    history.all_author_histories = mine_authors_over_repos(history)
    return history


def output_author_data(history: FullHistory):
    """Write out information about authors"""

    print("All authors")
    print("*" * 80)

    table = []
    for author in history.all_author_histories.values():
        repos = ", ".join([h.repo for h in author.histories.values()])
        table.append([author.name, author.email, author.first_commit_at, author.last_commit_at, author.commit_count, repos])

    # Sort by the first commit
    table = sorted(table, key=lambda row: row[2])
    
    headers = ["Email", "Name", "First commit", "Last commit", "Commit count", "Repos"]
    print(tabulate(table, headers=headers))
    print()

    # Export also as CSV
    with open('authors.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(table)


def main():
    """Entry point"""
    history = mine_data(sys.argv[1:])
    output_author_data(history)

if __name__ == "__main__":
    main()
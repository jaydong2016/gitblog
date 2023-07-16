# -*- coding: utf-8 -*-
import argparse
import os
import re

from marko.ext.gfm import gfm as marko
from github import Github
from feedgen.feed import FeedGenerator
from lxml.etree import CDATA

MD_HEAD = """
#### [Github issues 博客](https://github.adone.eu.org/) & [Notion 博客](https://nb.adone.eu.org/) 喜欢您来
[![](https://s2.loli.net/2023/07/03/WxmifsloVXrYz2I.png)](https://nb.adone.eu.org/)
"""

BACKUP_DIR = "BACKUP"
ANCHOR_NUMBER = 50
TOP_ISSUES_LABELS = ["Top"]
TODO_ISSUES_LABELS = ["TODO"]
IGNORE_LABELS = TOP_ISSUES_LABELS + TODO_ISSUES_LABELS


def get_me(user):
    return user.get_user().login


def is_me(issue, me):
    return issue.user.login == me


def format_time(time):
    return str(time)[:10]


def login(token):
    return Github(token)


def get_repo(user, repo):
    return user.get_repo(repo)


def parse_TODO(issue):
    body = issue.body.splitlines()
    todo_undone = [l for l in body if l.startswith("- [ ] ")]
    todo_done = [l for l in body if l.startswith("- [x] ")]
    # just add info all done
    if not todo_undone:
        return f"[{issue.title}]({issue.html_url}) all done", []
    return (
        f"[{issue.title}]({issue.html_url})--{len(todo_undone)} jobs to do--{len(todo_done)} jobs done",
        todo_done + todo_undone,
    )


def get_issues_with_label(repo, label):
    return repo.get_issues(labels=(label,))


def add_issue_info(issue, md):
    time = format_time(issue.created_at)
    md.write(f"- [{issue.title}]({issue.html_url})--{time}\n")


def add_md_section(repo, md, me, section_name, issues, limit=None):
    count = 0
    with open(md, "a+", encoding="utf-8") as md:
        md.write(f"## {section_name}\n")
        for issue in issues:
            if count == limit:
                md.write("<details><summary>显示更多</summary>\n")
                md.write("\n")
            if is_me(issue, me):
                add_issue_info(issue, md)
                count += 1
        if count > limit:
            md.write("</details>\n")
            md.write("\n")


def add_md_header(md, repo_name):
    with open(md, "w", encoding="utf-8") as md_file:
        md_file.write(MD_HEAD)


def get_to_generate_issues(repo, dir_name, issue_number=None):
    md_files = os.listdir(dir_name)
    generated_issues_numbers = [
        int(i.split("_")[0]) for i in md_files if i.split("_")[0].isdigit()
    ]
    to_generate_issues = [
        i
        for i in list(repo.get_issues())
        if int(i.number) not in generated_issues_numbers
    ]
    if issue_number:
        to_generate_issues.append(repo.get_issue(int(issue_number)))
    return to_generate_issues


def generate_rss_feed(repo, filename, me):
    generator = FeedGenerator()
    generator.id(repo.html_url)
    generator.title(f"RSS feed of {repo.owner.login}'s {repo.name}")
    generator.author(
        {"name": os.getenv("GITHUB_NAME"), "email": os.getenv("GITHUB_EMAIL")}
    )
    generator.link(href=repo.html_url)
    generator.link(
        href=f"https://raw.githubusercontent.com/{repo.full_name}/master/{filename}",
        rel="self",
    )
    for issue in repo.get_issues():
        if not issue.body or not is_me(issue, me) or issue.pull_request:
            continue
        item = generator.add_entry(order="append")
        item.id(issue.html_url)
        item.link(href=issue.html_url)
        item.title(issue.title)
        item.published(issue.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
        for label in issue.labels:
            item.category({"term": label.name})
        body = "".join(c for c in issue.body if _valid_xml_char_ordinal(c))
        item.content(CDATA(marko.convert(body)), type="html")
    generator.atom_file(filename)


def main(token, repo_name, issue_number=None, dir_name=BACKUP_DIR):
    user = login(token)
    me = get_me(user)
    repo = get_repo(user, repo_name)

    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

    add_md_header("README.md", repo_name)

    top_issues = list(get_issues_with_label(repo, "Top"))
    add_md_section(repo, "README.md", me, "置顶文章", top_issues)

    recent_issues = list(repo.get_issues())
    add_md_section(repo, "README.md", me, "最近更新", recent_issues, limit=10)

    labels = [label for label in repo.get_labels() if label.name not in IGNORE_LABELS]
    for label in labels:
        issues = get_issues_with_label(repo, label)
        add_md_section(repo, "README.md", me, label.name, issues)

    generate_rss_feed(repo, "feed.xml", me)

    to_generate_issues = get_to_generate_issues(repo, dir_name, issue_number)
    for issue in to_generate_issues:
        save_issue(issue)


def save_issue(issue, me):
    md_name = os.path.join(
        BACKUP_DIR, f"{issue.number}_{issue.title.replace(' ', '.')}.md"
    )
    with open(md_name, "w") as f:
        f.write(f"# [{issue.title}]({issue.html_url})\n\n")
        f.write(issue.body)
        if issue.comments:
            for c in issue.get_comments():
                if is_me(c, me):
                    f.write("\n\n---\n\n")
                    f.write(c.body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument(
        "--issue_number", help="issue_number", default=None, required=False
    )
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)

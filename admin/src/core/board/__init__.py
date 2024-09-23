from src.core.database import db
from src.core.board.issue import Issue
from src.core.board.label import Label

def list_issues():
    issues = Issue.query.all()

    return issues

def create_issue(**kwargs):
    issue = Issue(**kwargs)
    db.session.add(issue)
    db.session.commit()

    return issue

def assign_user(issue, user):
    issue.user = user
    db.session.commit()

    return issue


def assing_labels(issue, labels):
    issue.labels.extend(labels)
    db.session.add(issue)
    db.session.commit()

    return issue

def list_labels():
    return Label.query.all()


def create_label(**kwargs):
    label = Label(**kwargs)
    db.session.add(label)
    db.session.commit()

    return label

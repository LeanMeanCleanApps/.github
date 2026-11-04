"""Keep the Lean Mean Clean templates project up to date, so nobody has to.

Two jobs, picked by the first argument:

  issue    Runs when an issue in this repository is opened, closed or reopened. It adds the issue
           to the project, and when the issue closes it fills in Done on, the Month and the next
           release milestone, then moves it to Merged.
  release  Runs on the 2nd of each month. If all five templates have a release for the 1st, it
           moves that milestone's Merged items to Released, rolls anything still open into next
           month, closes the milestone and makes sure the next two months exist. If a template
           has no release, it opens an issue here instead and leaves the board alone.

It talks to GitHub through the gh CLI, with GH_TOKEN set to a token that can edit org projects.
"""

import calendar
import datetime as dt
import json
import os
import subprocess
import sys

ORG = "LeanMeanCleanApps"
REPO = f"{ORG}/.github"
PROJECT_NUMBER = 1
TEMPLATES = [
    "CleanMinimalApi",
    "CleanModelContextProtocol",
    "CleanGraphQLApi",
    "CleanWebApi",
    "CleanLambdaFunction",
]


def gh(*args, payload=None):
    result = subprocess.run(
        ["gh", *args],
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise SystemExit(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def graphql(query, **variables):
    data = gh("api", "graphql", "--input", "-", payload={"query": query, "variables": variables})
    if data.get("errors"):
        raise SystemExit(f"GraphQL failed: {data['errors']}")
    return data["data"]


def summary(line):
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as file:
            file.write(line + "\n")


# The project and its fields, looked up by name so renaming an option in the UI doesn't break this.

class Project:
    def __init__(self):
        data = graphql(
            """query($org: String!, $number: Int!) {
              organization(login: $org) { projectV2(number: $number) { id fields(first: 50) { nodes {
                ... on ProjectV2FieldCommon { id name }
                ... on ProjectV2SingleSelectField { options { id name } }
                ... on ProjectV2IterationField { configuration {
                  duration startDay
                  iterations { id title startDate duration }
                  completedIterations { id title startDate duration } } }
              } } } } }""",
            org=ORG,
            number=PROJECT_NUMBER,
        )["organization"]["projectV2"]
        self.id = data["id"]
        self.fields = {field["name"]: field for field in data["fields"]["nodes"] if field}

    def option(self, field, name):
        for option in self.fields[field]["options"]:
            if option["name"] == name:
                return option["id"]
        raise SystemExit(f"{field} has no option called {name}")

    def iterations(self):
        config = self.fields["Month"]["configuration"]
        return config["completedIterations"] + config["iterations"]

    def iteration_for(self, day):
        for iteration in self.iterations():
            start = dt.date.fromisoformat(iteration["startDate"])
            if start <= day < start + dt.timedelta(days=iteration["duration"]):
                return iteration
        return None

    def ensure_month(self, year, month):
        """Add a Month iteration titled like 2027-03 covering the whole month, if it's missing."""
        start = dt.date(year, month, 1)
        if self.iteration_for(start):
            return
        config = self.fields["Month"]["configuration"]
        keep = [
            {"id": i["id"], "title": i["title"], "startDate": i["startDate"], "duration": i["duration"]}
            for i in self.iterations()
        ]
        keep.append({
            "title": f"{year}-{month:02}",
            "startDate": start.isoformat(),
            "duration": calendar.monthrange(year, month)[1],
        })
        updated = graphql(
            """mutation($field: ID!, $config: ProjectV2IterationFieldConfigurationInput!) {
              updateProjectV2Field(input: {fieldId: $field, iterationConfiguration: $config}) {
                projectV2Field { ... on ProjectV2IterationField { configuration {
                  duration startDay
                  iterations { id title startDate duration }
                  completedIterations { id title startDate duration } } } } } }""",
            field=self.fields["Month"]["id"],
            config={"startDate": keep[0]["startDate"], "duration": config["duration"], "iterations": keep},
        )
        self.fields["Month"]["configuration"] = updated["updateProjectV2Field"]["projectV2Field"]["configuration"]
        summary(f"- Added the {year}-{month:02} iteration")

    def item(self, issue_node_id):
        """The issue's item in this project, adding it if it isn't there yet. Returns (id, values)."""
        data = graphql(
            """query($id: ID!) { node(id: $id) { ... on Issue { projectItems(first: 20) { nodes {
              id project { id }
              fieldValues(first: 30) { nodes {
                ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2FieldCommon { name } } }
                ... on ProjectV2ItemFieldIterationValue { title field { ... on ProjectV2FieldCommon { name } } }
                ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2FieldCommon { name } } }
              } } } } } } }""",
            id=issue_node_id,
        )
        for node in data["node"]["projectItems"]["nodes"]:
            if node["project"]["id"] == self.id:
                values = {}
                for value in node["fieldValues"]["nodes"]:
                    if value and value.get("field"):
                        values[value["field"]["name"]] = value.get("name") or value.get("title") or value.get("date")
                return node["id"], values
        added = graphql(
            """mutation($project: ID!, $content: ID!) {
              addProjectV2ItemById(input: {projectId: $project, contentId: $content}) { item { id } } }""",
            project=self.id,
            content=issue_node_id,
        )
        return added["addProjectV2ItemById"]["item"]["id"], {}

    def set(self, item, field, value):
        graphql(
            """mutation($project: ID!, $item: ID!, $field: ID!, $value: ProjectV2FieldValue!) {
              updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: $value}) {
                clientMutationId } }""",
            project=self.id,
            item=item,
            field=self.fields[field]["id"],
            value=value,
        )

    def clear(self, item, field):
        graphql(
            """mutation($project: ID!, $item: ID!, $field: ID!) {
              clearProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field}) {
                clientMutationId } }""",
            project=self.id,
            item=item,
            field=self.fields[field]["id"],
        )

    def set_status(self, item, name):
        self.set(item, "Status", {"singleSelectOptionId": self.option("Status", name)})

    def set_month(self, item, day):
        iteration = self.iteration_for(day)
        if iteration:
            self.set(item, "Month", {"iterationId": iteration["id"]})


# Milestones are releases, titled like the tag: 2026.12.01.

def release_title(day):
    return f"{day:%Y.%m}.01"


def first_of_next_month(day):
    return (day.replace(day=1) + dt.timedelta(days=32)).replace(day=1)


def milestones(state="all"):
    return gh("api", f"repos/{REPO}/milestones?state={state}&per_page=100")


def ensure_milestone(first):
    title = release_title(first)
    for milestone in milestones():
        if milestone["title"] == title:
            return milestone
    created = gh(
        "api", "-X", "POST", f"repos/{REPO}/milestones",
        "-f", f"title={title}",
        "-f", f"due_on={first.isoformat()}T12:00:00Z",
        "-f", f"description=The {title} release of all five templates.",
    )
    summary(f"- Added the {title} milestone")
    return created


def next_open_milestone(after):
    """The open release milestone due on or after the given day."""
    upcoming = [
        m for m in milestones("open")
        if m["due_on"] and dt.date.fromisoformat(m["due_on"][:10]) >= after
    ]
    return min(upcoming, key=lambda m: m["due_on"]) if upcoming else None


# Job one: an issue was opened, closed or reopened.

def on_issue():
    event = json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8"))
    action, issue = event["action"], event["issue"]
    if issue["user"]["type"] == "Bot":
        # Housekeeping issues the workflows open, like a missing release, stay off the board.
        print(f"Issue #{issue['number']} was opened by a bot, so it stays off the board.")
        return
    project = Project()
    item, values = project.item(issue["node_id"])
    summary(f"Issue #{issue['number']} was {action}.")

    if action == "opened":
        if "Status" not in values:
            project.set_status(item, "Backlog")
        return

    if action == "reopened":
        project.set_status(item, "In progress")
        project.clear(item, "Done on")
        return

    if issue.get("state_reason") != "completed":
        summary("- Closed as not planned, so the board is left as it is.")
        return

    closed = dt.date.fromisoformat(issue["closed_at"][:10])
    project.set(item, "Done on", {"date": closed.isoformat()})
    if "Month" not in values:
        project.set_month(item, closed)
    if values.get("Status") != "Released":
        project.set_status(item, "Merged")
    if not issue.get("milestone"):
        milestone = next_open_milestone(closed) or ensure_milestone(first_of_next_month(closed))
        gh("api", "-X", "PATCH", f"repos/{REPO}/issues/{issue['number']}", "-F", f"milestone={milestone['number']}")
        summary(f"- Ships in {milestone['title']}")
    summary(f"- Done on {closed}, moved to Merged")


# Job two: the monthly release went out on the 1st.

def missing_releases(title):
    missing = []
    for template in TEMPLATES:
        releases = gh("api", f"repos/{ORG}/{template}/releases?per_page=30")
        if not any(r["tag_name"].startswith(title + ".") and not r["draft"] for r in releases):
            missing.append(template)
    return missing


def report_missing(title, missing):
    issue_title = f"The {title} release is missing"
    body = "\n".join([
        f"These templates have no `{title}.*` release, so the project board hasn't been rolled over:",
        "",
        *[f"- [{t}](https://github.com/{ORG}/{t}/actions)" for t in missing],
        "",
        "Re-run the release, then run **Project sync** by hand from the Actions tab.",
        "",
        f"Checked in {os.environ.get('RUN_URL', 'a scheduled run')}.",
    ])
    existing = gh("issue", "list", "-R", REPO, "--state", "open", "--search", f'in:title "{issue_title}"', "--json", "number")
    if existing:
        subprocess.run(["gh", "issue", "comment", str(existing[0]["number"]), "-R", REPO, "--body", body], check=True)
    else:
        subprocess.run(["gh", "issue", "create", "-R", REPO, "--title", issue_title, "--body", body, "--assignee", "stphnwlsh"], check=True)
    summary(f"- {title} is missing from {', '.join(missing)}; opened an issue and left the board alone.")


def on_release(today):
    first = today.replace(day=1)
    title = release_title(first)
    summary(f"## Rolling over {title}")

    missing = missing_releases(title)
    if missing:
        report_missing(title, missing)
        return

    project = Project()
    following = first_of_next_month(first)
    after_that = first_of_next_month(following)
    project.ensure_month(first.year, first.month)
    project.ensure_month(following.year, following.month)
    next_milestone = ensure_milestone(following)
    ensure_milestone(after_that)

    current = next((m for m in milestones() if m["title"] == title), None)
    if not current:
        summary(f"- No {title} milestone, so there's nothing to move.")
        return

    issues = gh("api", f"repos/{REPO}/issues?milestone={current['number']}&state=all&per_page=100")
    released = slipped = 0
    for issue in issues:
        if "pull_request" in issue:
            continue
        item, values = project.item(issue["node_id"])
        if issue["state"] == "closed":
            if values.get("Status") == "Merged":
                project.set_status(item, "Released")
                released += 1
        else:
            # A slip moves a whole month: next release, next iteration.
            gh("api", "-X", "PATCH", f"repos/{REPO}/issues/{issue['number']}", "-F", f"milestone={next_milestone['number']}")
            project.set_month(item, first)
            slipped += 1

    gh("api", "-X", "PATCH", f"repos/{REPO}/milestones/{current['number']}", "-f", "state=closed")
    summary(f"- Released {released}, rolled {slipped} into {next_milestone['title']}, closed {title}")


if __name__ == "__main__":
    job = sys.argv[1] if len(sys.argv) > 1 else ""
    if job == "issue":
        on_issue()
    elif job == "release":
        override = os.environ.get("RELEASE_MONTH", "").strip()
        today = dt.date.fromisoformat(override + "-02") if override else dt.date.today()
        on_release(today)
    else:
        raise SystemExit("Say issue or release.")

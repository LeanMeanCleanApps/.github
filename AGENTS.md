# Agent instructions

This is the shared repository for the Lean Mean Clean Apps organisation: the organisation profile, the default community files, the issues behind the [Lean Mean Clean templates](https://github.com/orgs/LeanMeanCleanApps/projects/1) project, and two workflows. There's no application code here. Read the matching skill before you change anything.

## What's here

| Path | What it is |
| --- | --- |
| `profile/README.md` | The page at github.com/LeanMeanCleanApps |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `FUNDING.yml`, `pull_request_template.md`, `ISSUE_TEMPLATE/` | Default community files every organisation repository without its own picks up |
| `.github/workflows/project-sync.yml`, `.github/scripts/project_sync.py` | Keeps the project board up to date when issues close and after each monthly release |
| `.github/workflows/shared-layers-drift.yml` | Checks every Monday that the five templates' shared files still match |
| `.agents/skills` | How we do things here, one skill per folder |

## Rules

- Every change goes through a pull request against `main` on a `feature/`, `fix/` or `chore/` branch. The maintainer merges.
- A change to a community file shows up in every organisation repository, so keep it short and in the house voice.
- Never commit secrets. The project workflow reads its app ID and key from variables and secrets.

## Skills

| Skill | Use it when you |
| --- | --- |
| `planning` | Start a piece of work, ask for a decision, plan a month or release, open issues or pull requests for template work, or pick up someone else's work |

The engineering skills, and the persona Jacques, live in each template repository under `.agents`. Read them there for template changes.

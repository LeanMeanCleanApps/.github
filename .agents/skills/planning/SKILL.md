---
name: planning
description: How the maintainer and agents plan Lean Mean Clean Apps work together - decisions first as one question per item with a recommendation, the plan as a checklist in an issue here, the Lean Mean Clean templates project board, months and release milestones, branches and pull requests across the five templates, and the handoff when work stops. Use when starting a piece of work, planning a month or a release, asking for a decision, opening issues or pull requests for template work, or picking up work someone else started.
metadata:
  scope: repository
---

# Planning

## The rule

The maintainer decides; agents do the prep and recommend. Every piece of template work starts with its open decisions, has its plan written as a checklist in an issue in this repository, moves across the [Lean Mean Clean templates](https://github.com/orgs/LeanMeanCleanApps/projects/1) board on its own, and ends with a handoff that someone with no context can pick up.

| Thing | Where it lives |
| --- | --- |
| Findings, options and the reasoning behind them | A document linked from the issue |
| Each open decision | One question on its own, with options and a recommendation |
| The plan and its progress | The issue body, as phases of checkboxes |
| The handoff | A comment on the issue, or the pull request if there's no issue |
| How things are done today | The skills in each template. They describe the current answer and cite no decisions |

## Steps

### 1. Start with the decisions

1. Read what's already there first: the issue, the board, the skills and the code. Don't ask what they already answer.
2. List every open decision: scope, anything users of the templates depend on, new packages, packaging, the pipeline and releases.
3. Ask each one as its own question: two to four options, the one you recommend, and why in a sentence. One question per item, so each can be answered with a tap. Never as a list of questions in one long message.
4. Ask at the start of each phase, not halfway through it. A decision found mid-phase is asked the same way, then the plan is updated.
5. Don't ask about small choices that are easy to undo. Pick the likely option, say which, and carry on. Keep working on the recommended option while a reversible question waits for an answer; stop for anything that can't be undone.

### 2. Write the plan in an issue

Every piece of template work has an issue here, never in a template repository. The issue body is the plan:

``` markdown
Why the work matters, in two or three sentences.

## Phase 1: Agree the API shape
- [ ] Write up the options for the search endpoints
- [ ] Decide the paging defaults

## Phase 2: Minimal API first
- [ ] Endpoints, handlers and tests in CleanMinimalApi

Checks: the build pipeline passes, and Shared Layers Drift finds no differences.
```

Each item is a task someone could finish, not a theme. Each phase ends with checks anyone can run. Tick items as they finish, and change the plan in the issue rather than quietly doing something different.

### 3. Put it on the board

| Field | Value | Set by |
| --- | --- | --- |
| Month | The iteration for the month the work is done, named like `2026-11` | Project sync when the issue closes, or you when planning ahead |
| Milestone | The release it ships in, named like its tag, `2026.12.01`. A hotfix gets its own dated milestone | Project sync when the issue closes, or you when planning ahead |
| Status | `Merged` when the issue closes, `Released` on the 2nd once all five templates have released | Project sync only |
| Done on | The day the issue closed | Project sync only |

Don't set Status or Done on by hand. Anything still open on the 2nd rolls into the next month on its own.

### 4. Branches and pull requests

One pull request per repository for each completed feature, so cut each issue at the size of the pull request you'd want to review: one feature, one issue, one pull request per repository that closes it. A decision made partway through a feature goes on that feature's branch, not a new pull request. Small, unrelated fixes still get their own `fix/` branch.

1. Branch names start with `feature/`, `fix/` or `chore/`. Rulesets reject anything else.
2. Shared changes go to the templates in this order, with the same branch name, title and description: Minimal API, MCP, GraphQL, Web API, Lambda Function (`family-sync` in any template).
3. Link each pull request to the issue: `Part of LeanMeanCleanApps/.github#30` on every one but the last to merge, `Closes LeanMeanCleanApps/.github#30` on the last, usually Lambda Function.
4. Assign every pull request to the maintainer, `stphnwlsh`.
5. The description is the pull request template filled in plainly: a short summary, the linked issue, the checklist.
6. Wait for every required check. The maintainer reviews and merges; nobody else merges.

### 5. Fit the release calendar

| When | What |
| --- | --- |
| The 1st, 09:17 America/Chicago | Each template releases whatever is merged, if anything outside `.github/` changed |
| The 2nd | Project sync moves the release's items to `Released` and closes its milestone |
| The 15th, 09:17 America/Chicago | Maintenance: Dependabot and the scheduled build |

A month holds as many features as are ready. Merge by the date on the milestone; anything that slips moves to next month rather than rushing.

### 6. Leave a handoff

When work stops, whether it's done, blocked or just paused, comment on the issue:

- **Done:** what changed, with links to the pull requests.
- **Checked:** which checks ran and what they showed. Say plainly if anything failed or was skipped.
- **Left:** the unticked items, in order.
- **Waiting on:** the decisions or reviews the maintainer owes, as links.

Write it as you stop, so the next person or agent can start from the issue alone.

## Example

[LeanMeanCleanApps/.github#70](https://github.com/LeanMeanCleanApps/.github/issues/70) is planned this way: two phases of checkboxes with their checks, a pull request here and one per template linked with `Part of` and `Closes`.

## Don't

- Bundle several decisions into one message, or ask without a recommendation.
- Start building before the phase's decisions are answered, unless the work is easy to undo.
- Open issues in a template repository. They live here, so the board sees them.
- Keep a decision log or put decision history in skills or docs. They say how things are now.
- Use another branch prefix, merge a pull request, or skip the `Part of` and `Closes` links.
- Open a second pull request for a decision made partway through a feature, or split one feature's pull request in a repository across branches.
- Add AI attribution lines, tool footers, or "Testing" and "Not in this PR" sections to pull requests or commits. Commits are authored by the maintainer.
- Call the project a hobby or over-engineered. It's a side project built to production standards.

## Check

- The issue has phases, each item is a concrete task, and each phase has checks.
- Every open decision was asked on its own with a recommendation, and its answer is reflected in the plan.
- Every pull request is assigned to `stphnwlsh` and links the issue with `Part of` or `Closes`.
- When work stopped, the issue's last comment is a handoff.

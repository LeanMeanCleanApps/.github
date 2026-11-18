<p align="center">
  <img src="https://raw.githubusercontent.com/LeanMeanCleanApps/brand/main/assets/banners/png/org.png" alt="Lean Mean Clean Apps: The Shared Bits. Community files every repository picks up, minus the copy and paste." width="100%">
</p>

# Lean Mean Clean Apps – Shared

The shared bits of the [Lean Mean Clean Apps](https://github.com/LeanMeanCleanApps) organisation.

- `profile/README.md` is the page you see at [github.com/LeanMeanCleanApps](https://github.com/LeanMeanCleanApps).
- Everything else is a default community file. GitHub shows it in any organisation repository that doesn't have its own: the code of conduct, the contributing guide, governance, the security policy, the support page, the pull request template, and the bug, feature request and accessibility barrier forms with their links.
- `ACCESSIBILITY.md` and `LICENSE` are the exceptions. GitHub doesn't hand those down, so every repository keeps its own `ACCESSIBILITY.md`, and Shared Layers Drift keeps the templates' copies the same. The five templates have forms of their own, so these only show up in the other repositories.

Change these here and every repository picks them up.

## The templates' issue forms

GitHub won't mix the organisation's forms with a repository's own, so the templates' forms can't come from here directly. Instead `issue-forms/` is the pool: the master copy of every form the templates share, humour included, with `{{repo}}`, `{{short-name}}` and `{{docs-key}}` where each template's name, `dotnet new` short name and docs site key go.

- A template uses a pool form by keeping a copy in its `.github/ISSUE_TEMPLATE/` with those filled in. It can leave out any it doesn't need.
- A form that isn't in the pool is that template's own. Add it in the template, and nothing here needs to change.
- To change a shared form, change it here first, then copy it into every template that uses it.

Shared Layers Drift checks the copies against the pool every Monday.

## The project board

Every piece of template work has an issue here, on the [Lean Mean Clean templates](https://github.com/orgs/LeanMeanCleanApps/projects/1) project. Releases are milestones named like their tag, such as `2026.12.01`.

To link a pull request in a template to its issue, put this in the pull request:

- `Part of LeanMeanCleanApps/.github#30` on every pull request but the last.
- `Closes LeanMeanCleanApps/.github#30` on the last one to merge, usually Lambda.

Two workflows run here, and that's as busy as this repository gets:

- **Project sync** fills in the board when an issue closes, and rolls it over on the 2nd once all five templates have released.
- **Shared Layers Drift** checks every Monday that the templates' shared files still match, and that their issue forms still match the pool.

## Working with agents

`AGENTS.md` maps this repository for coding agents, and the `planning` skill in `.agents/skills` says how work is planned: decisions first, the plan as a checklist in an issue here, and a handoff when work stops. Neither is a community file, so they stay here.

<p align="center">
  <img src="https://raw.githubusercontent.com/LeanMeanCleanApps/brand/main/assets/banners/png/org.png" alt="Lean Mean Clean Apps: The Shared Bits. Community files every repository picks up, minus the copy and paste." width="100%">
</p>

# Lean Mean Clean Apps – Shared

The shared bits of the [Lean Mean Clean Apps](https://github.com/LeanMeanCleanApps) organisation.

- `profile/README.md` is the page you see at [github.com/LeanMeanCleanApps](https://github.com/LeanMeanCleanApps).
- Everything else is a default community file. GitHub shows it in any organisation repository that doesn't have its own: the code of conduct, the contributing guide, the security policy, the support page, the pull request template and the issue template links.

Change these here and every repository picks them up.

## The project board

Every piece of template work has an issue here, on the [Lean Mean Clean templates](https://github.com/orgs/LeanMeanCleanApps/projects/1) project. Releases are milestones named like their tag, such as `2026.12.01`.

To link a pull request in a template to its issue, put this in the pull request:

- `Part of LeanMeanCleanApps/.github#30` on every pull request but the last.
- `Closes LeanMeanCleanApps/.github#30` on the last one to merge, usually Lambda.

Two workflows run here, and that's as busy as this repository gets:

- **Project sync** fills in the board when an issue closes, and rolls it over on the 2nd once all five templates have released.
- **Shared Layers Drift** checks every Monday that the templates' shared files still match.

## Working with agents

`AGENTS.md` maps this repository for coding agents, and the `planning` skill in `.agents/skills` says how work is planned: decisions first, the plan as a checklist in an issue here, and a handoff when work stops. Neither is a community file, so they stay here.

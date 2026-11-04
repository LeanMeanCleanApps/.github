<p align="center">
  <img src="https://raw.githubusercontent.com/LeanMeanCleanApps/brand/main/assets/banners/png/org.png" alt="Lean Mean Clean Apps: the shared bits. Community files every repository picks up, minus the copy and paste." width="100%">
</p>

# .github

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

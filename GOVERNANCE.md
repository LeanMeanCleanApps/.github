# Governance

Lean Mean Clean Apps is run by the Lean Mean Clean Apps team, which is [Stephen Walsh](https://github.com/stphnwlsh) for now. This page says how decisions get made, so nobody has to guess, and so a "no" comes with a reason attached.

## Who decides

The maintainer. Every pull request in every repository is reviewed and merged by the maintainer, and the big calls (what goes into a template, which packages, when it ships) are theirs too. There's no committee, no steering group and no vote, because a vote of one is just a decision with extra steps.

That doesn't mean decisions happen in a dark room. Ideas and questions go in [Discussions](https://github.com/orgs/LeanMeanCleanApps/discussions), and anyone can comment on the plans.

## How work gets planned

- Every piece of planned work is an issue in [.github](https://github.com/LeanMeanCleanApps/.github/issues), tracked on the [project board](https://github.com/orgs/LeanMeanCleanApps/projects/1). The issue is the plan: what we decided, then a checklist.
- Anything bigger than a small fix starts as an issue or a discussion, so we agree on the approach before anyone spends an evening on it.
- The five templates share everything except their presentation layer, so a change to the shared parts lands in all five, or none.

## Releases

The templates release once a month, on the 1st, with a maintenance release on the 15th if one's needed. Security fixes don't wait for either. The [security policy](SECURITY.md) has the details.

## What's in scope

These are reference templates. They show one clean, tested shape for a .NET service, and they're meant to be copied and made your own.

In scope: the shape of the code, the tests, the local developer experience, CI, the docs, and keeping up with each .NET release.

Out of scope: running your service in production, choosing a real identity provider, and swapping SQLite for your database of choice. SQLite is there to show you can plug in anything, not to be the answer. Suggestions like these are welcome as ideas, but they won't become plans, and we'll point you here so it doesn't feel personal.

## Becoming a maintainer

Start with pull requests. After a run of good ones, ask. A team of two has a nice ring to it.

## If the maintainer steps away

Everything here is MIT licensed and public, so anyone can fork it and carry on. If the maintainer can't keep going, the repositories will say so in their READMEs and be archived, rather than left looking alive when nobody's home.

## Changing this page

Open a pull request against [.github](https://github.com/LeanMeanCleanApps/.github). The maintainer decides, which is rather the point of the page.

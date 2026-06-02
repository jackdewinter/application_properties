---
summary: How to contribute to the application.
authors:
  - Jack De Winter
---

# Contributing

Thanks for your interest in contributing to this project!

Here is a roadmap of what this page covers:

- [How To Go About Helping Us](#how-to-go-about-helping-us)
- [Are There Any Guidelines?](#are-there-any-guidelines)
- [Types of Contributions](#types-of-contributions)
- [Next Steps](#next-steps)

## How To Go About Helping Us

If your idea does not immediately fit our roadmap, or you are simply looking for
a way to help, we will work with you to find a contribution that aligns with the
project's direction. This section explains how to think about that and what to
do next.

You might be in one of two situations:

1. **You have a concrete idea.**

    You submit it to our
    [issues list](https://github.com/jackdewinter/application_properties/issues),
    and we respond that it will take time or does not fit the project's direction.

    In that case:

    - Read our feedback carefully. We review each issue seriously and try to be clear
      about constraints and priorities.
    - If the idea is important to you, contributing is often the best way to move
      it forward while still respecting the project's direction.
    - While your idea may not fit our roadmap, we can work with you to figure out
      if your idea has merit outside of our project, and how you can realize that.

2. **You want to help but do not have a specific idea yet.**  

    You might be looking for something you can
    [sink your teeth into](https://dictionary.cambridge.org/dictionary/english/sink-teeth-into),
    want to build your open-source resume, or just want to explore the project.

If you are sincere about helping and can collaborate effectively with our
team, we will work with you to see how you can help us out.

## Are There Any Guidelines?

Yes, definitely. And we are relaxed about most of our guidelines. But there
are certain things we will not budge on.

### Test Coverage

We worked hard to get 100% code coverage and nearly 100% scenario coverage. Code
coverage is easy; covering every scenario is not. By being strict about this from
the start, we reduce the number of issues our users encounter. That also helps ensure
that most remaining reports are truly new scenarios we did not anticipate.

### Static Project Analysis

We rely heavily on static project analysis. In practice, this means that before
opening a Pull Request, you should run `clean.cmd` (on Windows) or `clean.sh`
(on Unix-like systems).

These scripts:

- Run our standard static checks (including those configured in Pre-Commit).
- Perform extra tasks that are simpler to manage in a script, such as verifying
  that the `Pipfile` used by Pipenv is up to date as the first task.

We keep these checks in a script, rather than only in our Pre‑Commit configuration,
so that we can adjust and extend them more easily. This approach has saved us from
configuration problems many times. As a result, we plan to keep it.

### One Major Change Per Pull Request

Our guideline is simple:

- **Submit only one major change per Pull Request.**
- Minor, closely related fixes are acceptable.
- If your PR bundles many unrelated changes (or your title has multiple "and"s),
  split it into smaller PRs to keep reviews focused.
    - **Do:** Group logically related changes that support a single goal.
    - **Don't:** Combine refactors, new features, and large cleanups in one PR.

Once you are familiar with these guidelines, the next step is to decide how you
would like to contribute.

## Types of Contributions

Before you pick a contribution type, make sure you have read
["Are There Any Guidelines?"]( #are-there-any-guidelines ).

Our contributions generally fall into two categories:

- adding a new configuration provider to pull configuration from a data source
- adding a new function to pull configuration from already loaded data.

In both cases, you should take the time to think through what you want to add or
change and why you believe that should be in the base package. Be honest with yourself
about your contribution and all the ins and outs of its implementation. Be thorough
in thinking about how you will test your contribution and add those tests into our
package. Are there negative scenarios that will be hard to implement or test, and
why?

Our goal with these questions is not to prevent you from contributing. They are
to ensure that your contribution eventually arrives at a high quality addition to
the package. We are happy to help you along the way, as long as you are willing
to accept our help.

## Next Steps

If none of this has scared you off, you may want to consider helping our team
out with the development of this project. Even if it is only for something
small, we can help you learn what you need to contribute.

When you are ready, start by opening an issue in our
[issues list](https://github.com/jackdewinter/application_properties/issues) to discuss
your idea or proposed change, and then move on to a Pull Request once we have
aligned on the approach.

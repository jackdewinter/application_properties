---
summary: How to contribute to the application.
authors:
  - Jack De Winter
---

# Contributing

Thanks for your interest in contributing to this application!

## How To Go About Helping Us

Let us say that you have a great idea on what you want to see happen with this
project.  You submit it to our
[issues list](https://github.com/jackdewinter/application_properties/issues),
and we tell you it is going to be a long time before we get to it.  Or we say
that it does not fit the direction we have for the project.

What do you do next?

The first thing is to understand our feedback.  We carefully look at each issue
and try and be as honest and sincere with our feedback as possible. While something
may be a critical issue for you, it is possible that it does not carry the same
importance for us.

That is where your contributions to the project can help.  We have a small
team that works on this project, and we must prioritize based on that
team.  If you volunteer to help, we can provide guidance and help to you
at a low cost to us.  If what you want to do is not contrary to the direction of
the project, we can usually work something out to help you meet your needs.
  
<!--- pyml disable-next-line no-emphasis-as-heading-->
**OR**  
  
Let us say that you want to get involved with a project and help.  You
are looking for something you can [sink your teeth into](https://dictionary.cambridge.org/dictionary/english/sink-teeth-into)
but are not sure you would be a good fit for this project.  Or you want to have
open-source contributions on your resume because it looks good.  Or...

If you are sincere about helping and can collaborate effectively with our
team, we will work with you to see how you can help us out.

## Are There Any Guidelines?

Yes, definitely.  And we are relaxed about most of our guidelines.  But there
are certain things we will not budge on.

### Test Coverage

We worked hard to ensure that our project has 100% code coverage and near 100%
scenario coverage.  Getting the code covered is usually the easy part.  Getting
every scenario for every element is painful.  By being very stringent about this
upfront, we hope we reduce the number of errors reported by our
users when using our application to missed scenarios.

### Static Project Analysis

We are big proponents of static project analysis.  Static project analysis
is the parent group that includes static code analysis but extends that analysis
to the other aspects of the project.  For our team, this means running the
`clean.cmd` script or `clean.sh` script before creating a Pull Request.

Why are we using a script instead of putting everything in our Pre-Commit
configuration?  To be honest, it is mostly so that we can be more agile.
While we have moved most of our checks into our Pre-Commit configuration,
there are some things that are just easier to control with a script. A good
example of this is ensuring that the `Pipfile` configuration file used for
PipEnv is synced up as the first task in the clean scripts.  This has saved our
team on more than one occasion, and is something we intend to keep.

### One Major Change Per Pull Request

One pull request, one change.  Simple.  A minor change in another area that you
honestly found while making your change?  Probably acceptable.  A Pull Request
with a title that includes too many "and" phrases. Probably not acceptable.

Electrons are cheap.  Focus on merging one complete concept, and then
work on the merge for the next concept.  Remember the [KISS principle](https://en.wikipedia.org/wiki/KISS_principle):
Keep it simple... silly.

## Still Here?

If none of this has scared you off, you may want to consider helping our team
out with the development of this project.  Even if it is only for something
small, we can help you learn what you need to contribute.

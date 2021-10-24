# Frequently Asked Questions

## Why Is This Package Needed?

The shortest answer to this is that the
[PyMarkdown project](https://github.com/jackdewinter/pymarkdown) that spawned this
package required a properties file that had more options available than any of the
other packages provided.

The somewhat longer answer is that while there are numerous packages out there that
deal with properties, they each have their own little quirks, input formats, and
ways they respond to presented data.  In adding properties support to any of the
projects that we are a part of, we didn't want to have to search all over for the
best solution.  We wanted the best solution to be easily discoverable and easy to
include into a Python project.

## What if I have a special requirements for my configuration file?

If you configuration has special requirements, please consider taking a look
at our API document's section on
[Property Loaders](docs/api.md#loaders).
If you still cannot find a loader that fits your needs, you can write your
own custom loader by following the instructions located in our
[Developer's Notes](docs/developer.md#loaders).


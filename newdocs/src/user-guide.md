# User Guide

This document is geared towards getting you and your team up and running as
quickly as possible with this library.

## What This User Guide Is

Unlike the [Quick Start guides](./quick-starts/index.md) which try and get you up
and running
as fast as possible, this User Guide is meant as a deep dive into what the concepts
and components of the `application_properties` package
are all about. Instead of just leaving explanations at a high-level, we try and
dig deeper into how
things work and why our team made the choices it did.

To that end, we start with some higher-level topics before
getting into the more practical aspects of using this package. This ordering is
meant to ensure that you have
a solid grasp on the language the package uses and an understadning of why things
were done the way they were.
We believe that having that grasp on the culture of the `application_properties`
package will make it easier for
you to understand the other pages that follow.

If you want some great examples that show you how to use the `application_properties`
package and its components, [TBD]

### Basic Concepts

The [Basic Concepts](./basic-concepts.md) page serves as a crucial conceptual bridge,
introducing the foundational vocabulary for the `application_properties` package
for developers, complementing the Quick Start guides. It systematically defines
core terminology, such as **Configuration Item**, **Configuration Data Sources**,
and the role of the **Configuration Manager**. The document then breaks down primitive
types — **String**, **Integer**, **Boolean**, and **String List** — before explaining
structural concepts like **Hierarchical** and **Flattened Hierarchy**. It establishes
a working philosophy, emphasizing the "work by default" approach, and clarifies
that all configuration items are fundamentally composed of a name (expressed in
flattened format) and a typed value.

### Data Sources

The [Data Sources](./file-types.md) page serves as a foundational guide, introducing
developers to the core mechanism of application_properties. It first outlines how
simple `key-value` pairs are used to set default application settings, making initial
setup straightforward. The guide then progresses to show how these basic configurations
can be overridden by environment variables or command-line arguments, which is crucial
for containerized deployments. Furthermore, it introduces the concept of profile-specific
properties, allowing developers to tailor behavior for different operational contexts
like `dev`, `test`, or `prod`. By mastering these foundational steps, users are
prepared to tackle more complex topics in subsequent sections.

### Data Source Layering

The [Configuration Ordering and Layering](./layering.md) page outlines a hierarchical
configuration system designed to handle multiple data sources by prioritizing them
from least to most specific. This layered approach ensures that more specific inputs,
such as command-line arguments, reliably override broader defaults or file-based
settings. The documentation details six distinct layers, ranging from implicit default
values to specific command-line shortcuts, emphasizing a "last one wins" rule for
conflicting keys. This structure allows applications to flexibly manage complex
configuration needs while maintaining predictable and explainable behavior for users.

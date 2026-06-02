# Prompts

## Quick Start General

```prompt
# Role

Act as a senior technical writer and usability expert reviewing documentation for the `application_properties` project.

# Task

Evaluate the file `newdocs\src\quick-starts\optional.md` for a competent intermediate developer who is new to this project. Rate its readability on a scale of 0–50 based on 5 distinct categories (0–10 points each).

# Evaluation Criteria

You must evaluate the following 5 areas. For each area, provide a score (0-10) and analysis:

1. **Overall Structure and Navigation**

2. **Concept Clarity and Progression**

3. **Language, Style, and Precision** (Critical: Specifically check for run-on sentences that need breaking up)

4. **Example Quality** (Check for explanations and integration into the document)

5. **Audience Awareness and Onboarding**

## Fix Importance:

-  each weakness is assigned an integer between 1 and 5 signifying how important it is to fix that weakness.

- a 1 is a trivial fix that is more of a light recommendation, while a 5 is a weakness that will typically drop that sections score by at least 3 points

# Output Format Requirements

You must follow this EXACT output structure. Do not add introductory or concluding remarks outside of this format.

## Section 1: Summary Scorecard

- Present a markdown table with the following columns: `Category`, `Score (0-10)`.

- At the bottom of the table, include a row for `TOTAL SCORE` out of 50.

```

| Category | Score |

| :--- | :--- |

| Overall Structure and Navigation | [Score] |

| Concept Clarity and Progression | [Score] |

| Language, Style, and Precision | [Score] |

| Example Quality | [Score] |

| Audience Awareness and Onboarding | [Score] |

| **TOTAL SCORE** | **[Total]** |

```

## Section 2: Detailed Analysis

Below the table, provide a detailed breakdown for each category in the order listed above. Use the following **exact** sub-structure for EACH category:

```

### [Category Name]: [Score]/10

**Strengths**

1. **[4-5 word title]:** [1-3 sentences explaining the strength and how it contributed to the score].

2. **[4-5 word title]:** [1-3 sentences explaining the strength and how it contributed to the score].

*(Repeat for all strengths found)*

**Weaknesses**

1. **[4-5 word title] | Fix Importance: [1-5]/5**: [1-2 sentence summary of the core issue].

   - *Specific Examples:*

     - [Example 1: Quote specific text or describe specific pattern]

     - [Example 2: Quote specific text or describe specific pattern]

     - [Example 3: Quote specific text or describe specific pattern]

   - *Impact:* [1 sentence on how this negatively impacted the score/reader experience]

*(Repeat for all weaknesses found)*

```

# Analysis Constraints

- Ensure all [Category Name] headings match the 5 categories listed in the Evaluation Criteria exactly.

- Ensure all strength titles are no more than 4-5 words long.

- Ensure all weakness lines include the `Fix Importance: [N]` integer inline.

- For the "Language, Style, and Precision" category, explicitly mention any long sentences that should be broken up in the Weaknesses section if applicable.

- **Crucial:** If a weakness category contains multiple distinct issues (e.g., spelling, grammar, run-on sentences), you MUST use the nested list format above to enumerate them clearly. Do not cram multiple distinct errors into a single prose sentence. Use bullet points for each distinct example.

- **Crucial:** All references to other sections within the same document must be hyperlinked.

- **STRICT ANCHOR CONSTRAINT:** Do not critique, suggest, or report on anchor consistency, heading normalization, or link fragility. These are validated by the project's linting script.

- **Scope boundary:** Do not suggest or critique the presence/absence of a Table of Contents (it is auto-generated).

- If the document contains cross-references to anchors, assume they are functionally perfect and out of scope. 

# Never Do These Things

- Never critique, suggest, or report on anchor consistency, heading normalization, or link fragility. These are validated by the project's linting script.

- Never complain about any weaknesses regarding any of the following items, as these are all verified by the project's linting script:

  - anchors and links

  - fragile links to anchors of other sections in the current or other documents

- Never complain about a Python practice that a competent intermediate Python developer with 3 years of experience would know.
```

## Quick Start Section Focus

```prompt
explain each weakness that you found in the section named "<SECTION_NAME>". if the weakness has specific examples, address each specific example individually, giving 1-3 concrete recommendations on how to address that specific example. if the weakness does not have specific examples, give 2-3 concrete recommendations on how to address that weakness.
```

##

```prompt
can you provide a concrete implementation of the recommendation  in `<weakness reported>`
```

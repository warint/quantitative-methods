# Group work

Everything a group produces lives here, under its cohort and its own number:

```
groups/
└── A2026/                  ← the cohort: autumn 2026
    ├── group-01/
    │   ├── session-02/     ← one folder per session's practice
    │   ├── session-03/
    │   └── ...
    └── group-10/
```

**Why here and not inside each session folder.** A group's work used to be scattered across twelve
session directories, so seeing what one group had done meant opening twelve places, and running the
course again the following year would have written a second cohort's work on top of the first.
Under this layout a group's whole term is one directory, and a cohort is one directory above that —
which is what makes `A2027` a new folder rather than a merge conflict.

Marking a single session still reads as one glob, because the session is the leaf:

```bash
ls groups/A2026/*/session-04/
```

## What goes in a session folder

Whatever that session's practice brief asks for — normally a short note and the script that
produced your numbers. The brief is in the session's own `02-practice/README.md`; only the output
comes here.

## Naming

`group-07`, not `group-7` and not `Group 07`. Two digits, lower case, so the folders sort in order
and the glob above matches all of them.

## The cohort code

`A2026` is autumn 2026. A winter cohort would be `H2026`, following HEC's own convention. The code
is set once per term and never changes mid-term, because paths in twelve session briefs point at it.

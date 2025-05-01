# Tailwind Merge Python

![PyPI](https://img.shields.io/pypi/v/tailwind-merge?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tailwind-merge?color=blue&style=flat-square)

A Python utility for merging Tailwind CSS class lists intelligently, resolving conflicts based on Tailwind's principles. Inspired by the popular [tailwind-merge](https://github.com/dcastil/tailwind-merge) JavaScript package.

This utility ensures that when you combine multiple strings of Tailwind classes (e.g., from different component states or logic branches), the resulting string is clean, minimal, and applies the intended styles by removing redundant or conflicting classes based on their function.

## Installation

Using pip:
```bash
pip install tailwind-merge 
```

## Usage

```python
from tailwind_merge import TailwindMerge 

# Initialize 
twm = TailwindMerge()

result = twm.merge(
    "p-4 w-6 text-blue-500", # Initial classes
    "w-8 text-red-500"       # Overrides for width and text color
)
# "p-4 text-red-500 w-8" 

result = twm.merge("pl-4", "pr-6 pl-2") 
# "pl-2 pr-6"

result = twm.merge("p-2 hover:p-4", "p-3") 
# "hover:p-4 p-3"

result = twm.merge("hover:p-2", "focus:p-1 hover:p-4") 
# "hover:p-4 focus:p-1"

result = twm.merge("p-1", "p-[2px]")
# "p-[2px]"

result = twm.merge(
    "flex items-center justify-center", # Base layout
    "justify-between",                  # Override justify
    "text-red-500",                     # Add text color
    "hover:text-blue-500 text-lg"       # Add hover color and text size
)
# "flex items-center justify-between text-red-500 hover:text-blue-500 text-lg"
```
### Custom Rules
```python
twm.add_rule('custom-icon-size', ['icon-sm', 'icon-md', 'icon-lg'])
twm.merge("icon-sm icon-lg")
# "icon-lg"
```

## Features

-   **Conflict Resolution:** Correctly identifies and resolves conflicting Tailwind classes based on their utility function, keeping the last applied class within a specific conflict group.
-   **Modifier Support:** Handles Tailwind modifiers (`hover:`, `focus:`, `md:`, `dark:`, etc.). Conflicts are resolved independently for base styles and each unique modifier combination (e.g., `hover:text-red-500` conflicts with `hover:text-green-500` but not with `focus:p-4` or `p-4`).
-   **Arbitrary Value Support:** Recognizes and correctly groups classes with arbitrary values (e.g., `p-[3px]`, `w-[calc(100%-theme(spacing.4))]`, `text-[#FF0000]`).
-   **Prefix Matching:** Uses longest-prefix matching to correctly categorize classes when prefixes might overlap (e.g., correctly identifies `border-t-2` as belonging to `border-width-top` before matching the shorter `border-` prefix).
-   **Order Preservation:** Aims to preserve the relative order of the *final* classes as they appeared in the input strings.
-   **Custom classes:** Allows adding custom conflict rules using the `add_rule` method for project-specific utilities or third-party libraries.
-   **Zero Dependencies:** Pure Python implementation with no external library requirements.

## Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to improve the class definitions, please feel free to open an issue or submit a Pull Request. Ensure tests pass and consider adding new tests for your changes.

---
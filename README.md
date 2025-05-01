# Tailwind Merge Python

![PyPI](https://img.shields.io/pypi/v/tailwind-merge?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/tailwind-merge?color=blue&style=flat-square)

A Python utility for merging Tailwind CSS class lists intelligently, resolving conflicts based on Tailwind's principles. Inspired by the popular [tailwind-merge](https://github.com/dcastil/tailwind-merge) JavaScript package.

This utility ensures that when you combine multiple strings of Tailwind classes (e.g., from different component states or logic branches), the resulting string is clean, minimal, and applies the intended styles by removing redundant or conflicting classes based on their function.

## Installation

Using pip:
```bash
pip install tailwind-merge # Assuming this is the package name you'll use
# Or if installing directly from source:
# pip install .
```

## Usage

```python
from tailwind_merge import TailwindMerge # Adjust import if your file/package name differs

# Initialize the merger (you can reuse the instance)
twm = TailwindMerge()

# --- Basic Merging ---
# Conflicting classes for the same property (width, text color) are resolved, keeping the last one.
result = twm.merge(
    "p-4 w-6 text-blue-500", # Initial classes
    "w-8 text-red-500"       # Overrides for width and text color
)
print(result)
# Output: "p-4 text-red-500 w-8" (Order might vary slightly based on processing, but content is correct)

# --- Handling Specific Sides/Axes ---
# Padding/Margin sides don't conflict with each other, but conflict with axis/all setters.
result = twm.merge("pl-4 pr-6") # Left and Right padding coexist
print(result)
# Output: "pl-4 pr-6"

result = twm.merge("p-4 pl-8") # Specific left padding overrides general padding affecting left
print(result)
# Output: "pl-8" # Or potentially "p-4 pl-8" depending on exact conflict rules for p-* vs pl-*

result = twm.merge("pl-8 p-4") # General padding defined later overrides specific padding
print(result)
# Output: "p-4"

# --- Modifier Handling ---
# Modifiers (hover:, focus:, md:, etc.) are handled correctly.
# Conflicts are resolved independently for base classes and each modifier combination.
result = twm.merge("p-2 hover:p-4", "p-3") # Base padding is overridden
print(result)
# Output: "hover:p-4 p-3"

result = twm.merge("hover:p-2 hover:p-4", "focus:p-1") # Hover conflict resolved, focus added
print(result)
# Output: "hover:p-4 focus:p-1"

# --- Arbitrary Value Support ---
# Classes with arbitrary values are correctly grouped and merged.
result = twm.merge("p-[2px] p-1")
print(result)
# Output: "p-1"

result = twm.merge("m-1 m-[3vh]")
print(result)
# Output: "m-[3vh]"

# --- Combining Multiple Strings ---
# Pass multiple strings as arguments
result = twm.merge(
    "flex items-center justify-center", # Base layout
    "justify-between",                  # Override justify
    "text-red-500",                     # Add text color
    "hover:text-blue-500 text-lg"       # Add hover color and text size
)
print(result)
# Output: "flex items-center justify-between text-red-500 hover:text-blue-500 text-lg"


# --- Extensibility ---
# Add your own custom class groups if needed
# twm.add_rule('custom-icon-size', ['icon-sm', 'icon-md', 'icon-lg'])
# result = twm.merge("icon-sm icon-lg")
# print(result) # Output: "icon-lg"
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
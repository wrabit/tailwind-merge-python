# Tailwind Merge Python

A Python implementation of the popular [tailwind-merge](https://github.com/dcastil/tailwind-merge) js package. This utility helps you merge Tailwind CSS classes while handling conflicts appropriately.

## Installation

Using pip:
```bash
pip install tailwind-merge
```

## Usage

```python
from tailwind_merge import TailwindMerge

twmerge = TailwindMerge()

# Basic usage
result = twmerge.merge(
    "p-4 w-6 text-blue-500",
    "w-8 text-red-500" 
)
print(result)  # Output: "p-4 w-8 text-red-500"

# Add custom conflict patterns
twmerge.add_rule('custom', ['custom-'])
```

## Features

- Handles conflicting Tailwind utility classes
- Later classes override earlier ones within the same category
- Extensible with custom class groups
- Zero dependencies

## Roadmap

- Introduce class validation to ensure we only merge valid Tailwind classes
- Check support for Tailwind CSS v4

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

from typing import List, Dict, Set
import re


class TailwindMerge:
    def __init__(self):
        # Define conflicting class patterns
        self.groups = {
            'width': r'^w-',
            'height': r'^h-',
            'margin': r'^m[trblxy]?-',
            'padding': r'^p[trblxy]?-',
            'color': r'^(text|bg|border)-',
            'display': r'^(block|inline|flex|grid|hidden)',
            'position': r'^(static|fixed|absolute|relative|sticky)',
            'font_size': r'^text-',
            'font_weight': r'^font-',
            'flex': r'^flex-',
            'grid': r'^grid-',
            'order': r'^order-',
            'columns': r'^columns-',
            'rounded': r'^rounded',
            'shadow': r'^shadow',
        }

    def merge(self, *class_lists: str) -> str:
        """
        Merge multiple Tailwind CSS class strings while handling conflicts.
        Later classes override earlier ones within the same category.
        
        Args:
            *class_lists: Variable number of strings containing space-separated Tailwind classes
            
        Returns:
            str: Merged class string with conflicts resolved
        """
        # Split all input strings and flatten into a single list
        all_classes = []
        for classes in class_lists:
            if classes:
                all_classes.extend(classes.split())
        
        # Keep track of seen categories and their classes
        seen_categories: Dict[str, str] = {}
        final_classes: Set[str] = set()
        
        # Process classes in reverse order (so later classes take precedence)
        for class_name in reversed(all_classes):
            # Skip empty classes
            if not class_name:
                continue
                
            # Find which category this class belongs to (if any)
            matching_category = None
            for category, pattern in self.groups.items():
                if re.match(pattern, class_name):
                    matching_category = category
                    break
            
            # If this class belongs to a category we've seen, skip it
            # Otherwise, mark this category as seen and add the class
            if matching_category:
                if matching_category not in seen_categories:
                    seen_categories[matching_category] = class_name
                    final_classes.add(class_name)
            else:
                # Classes without a category are always included
                final_classes.add(class_name)
        
        # Sort the classes for consistent output
        return ' '.join(sorted(final_classes))

    def add_conflict_pattern(self, category: str, pattern: str) -> None:
        """
        Add a new conflict pattern to the merger.
        
        Args:
            category: The name of the category for conflicting classes
            pattern: Regular expression pattern to match classes in this category
        """
        self.groups[category] = pattern
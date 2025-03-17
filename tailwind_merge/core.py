from typing import List, Tuple, Dict, Optional, Set
import re

class TailwindMerge:
    def __init__(self):
        # Define conflict groups with ordered prefixes (more specific first)
        self.groups: List[Tuple[str, List[str]]] = [
            # Font Size (specific sizes)
            ('font_size', [
                'text-xs', 'text-sm', 'text-base',
                'text-lg', 'text-xl', 'text-2xl',
                'text-3xl', 'text-4xl', 'text-5xl',
                'text-6xl', 'text-7xl', 'text-8xl', 'text-9xl'
            ]),
            # Text Color (catch-all 'text-' after specific font sizes)
            ('text_color', ['text-']),
            # Text Alignment
            ('text_align', ['text-left', 'text-center', 'text-right', 'text-justify']),
            # Text Decoration
            ('text_decoration', ['underline', 'no-underline', 'line-through']),
            # Text Transform
            ('text_transform', ['uppercase', 'lowercase', 'capitalize', 'normal-case']),
            # Font Family
            ('font_family', ['font-sans', 'font-serif', 'font-mono']),
            # Font Weight
            ('font_weight', [
                'font-thin', 'font-extralight',
                'font-light', 'font-normal',
                'font-medium', 'font-semibold',
                'font-bold', 'font-extrabold',
                'font-black'
            ]),
            # Font Style
            ('font_style', ['italic', 'not-italic']),
            # Letter Spacing
            ('letter_spacing', ['tracking-']),
            # Line Height
            ('line_height', ['leading-']),

            # Background Color
            ('bg_color', ['bg-']),
            # Background Position
            ('bg_position', ['bg-bottom', 'bg-center', 'bg-left', 'bg-left-bottom',
                            'bg-left-top', 'bg-right', 'bg-right-bottom',
                            'bg-right-top', 'bg-top']),
            # Background Size
            ('bg_size', ['bg-auto', 'bg-cover', 'bg-contain']),
            # Background Repeat
            ('bg_repeat', ['bg-repeat', 'bg-no-repeat', 'bg-repeat-x',
                          'bg-repeat-y', 'bg-repeat-round', 'bg-repeat-space']),
            # Background Attachment
            ('bg_attachment', ['bg-fixed', 'bg-local', 'bg-scroll']),

            # Width
            ('width', ['w-']),
            # Min Width
            ('min_width', ['min-w-']),
            # Max Width
            ('max_width', ['max-w-']),

            # Height
            ('height', ['h-']),
            # Min Height
            ('min_height', ['min-h-']),
            # Max Height
            ('max_height', ['max-h-']),

            # Margin
            ('margin', ['m-', 'mt-', 'mr-', 'mb-', 'ml-', 'mx-', 'my-']),
            # Negative Margin (separate group because it could coexist with positive)
            ('negative_margin', ['-m-', '-mt-', '-mr-', '-mb-', '-ml-', '-mx-', '-my-']),

            # Padding
            ('padding', ['p-', 'pt-', 'pr-', 'pb-', 'pl-', 'px-', 'py-']),

            # Display
            ('display', [
                'block', 'inline', 'inline-block',
                'flex', 'inline-flex', 'grid',
                'inline-grid', 'hidden', 'contents', 'table',
                'inline-table', 'table-caption', 'table-cell',
                'table-column', 'table-column-group', 'table-footer-group',
                'table-header-group', 'table-row-group', 'table-row'
            ]),

            # Position
            ('position', ['static', 'fixed', 'absolute', 'relative', 'sticky']),
            # Top, Right, Bottom, Left
            ('top', ['top-']),
            ('right', ['right-']),
            ('bottom', ['bottom-']),
            ('left', ['left-']),

            # Z-Index
            ('z_index', ['z-']),

            # Flex Direction
            ('flex_direction', ['flex-row', 'flex-row-reverse', 'flex-col', 'flex-col-reverse']),
            # Flex Wrap
            ('flex_wrap', ['flex-wrap', 'flex-wrap-reverse', 'flex-nowrap']),
            # Flex Grow
            ('flex_grow', ['flex-grow', 'flex-grow-0']),
            # Flex Shrink
            ('flex_shrink', ['flex-shrink', 'flex-shrink-0']),
            # Flex
            ('flex', ['flex-']),
            # Flex Basis
            ('flex_basis', ['basis-']),

            # Grid Template Columns
            ('grid_template_cols', ['grid-cols-']),
            # Grid Column Start / End
            ('grid_col_start', ['col-start-']),
            ('grid_col_end', ['col-end-']),
            ('grid_col_span', ['col-span-']),
            # Grid Template Rows
            ('grid_template_rows', ['grid-rows-']),
            # Grid Row Start / End
            ('grid_row_start', ['row-start-']),
            ('grid_row_end', ['row-end-']),
            ('grid_row_span', ['row-span-']),
            # Grid Auto Flow
            ('grid_auto_flow', ['grid-flow-row', 'grid-flow-col', 'grid-flow-row-dense', 'grid-flow-col-dense']),
            # Grid Auto Columns
            ('grid_auto_cols', ['auto-cols-']),
            # Grid Auto Rows
            ('grid_auto_rows', ['auto-rows-']),
            # Gap
            ('gap', ['gap-']),
            ('gap_x', ['gap-x-']),
            ('gap_y', ['gap-y-']),

            # Justify Content
            ('justify_content', ['justify-']),
            # Justify Items
            ('justify_items', ['justify-items-']),
            # Justify Self
            ('justify_self', ['justify-self-']),
            # Align Content
            ('align_content', ['content-']),
            # Align Items
            ('align_items', ['items-']),
            # Align Self
            ('align_self', ['self-']),

            # Border Width
            ('border_width', ['border', 'border-0', 'border-2', 'border-4', 'border-8']),
            ('border_width_t', ['border-t-']),
            ('border_width_r', ['border-r-']),
            ('border_width_b', ['border-b-']),
            ('border_width_l', ['border-l-']),
            # Border Color
            ('border_color', ['border-']),
            # Border Style
            ('border_style', ['border-solid', 'border-dashed', 'border-dotted', 'border-double', 'border-none']),
            # Border Radius
            ('border_radius', ['rounded']),
            ('border_radius_t', ['rounded-t']),
            ('border_radius_r', ['rounded-r']),
            ('border_radius_b', ['rounded-b']),
            ('border_radius_l', ['rounded-l']),
            ('border_radius_tl', ['rounded-tl']),
            ('border_radius_tr', ['rounded-tr']),
            ('border_radius_br', ['rounded-br']),
            ('border_radius_bl', ['rounded-bl']),

            # Opacity
            ('opacity', ['opacity-']),

            # Box Shadow
            ('shadow', ['shadow']),

            # Transition Property
            ('transition', ['transition']),
            # Transition Duration
            ('transition_duration', ['duration-']),
            # Transition Timing Function
            ('transition_timing', ['ease-']),
            # Transition Delay
            ('transition_delay', ['delay-']),

            # Transform
            ('transform', ['transform', 'transform-gpu', 'transform-none']),
            # Scale
            ('scale', ['scale-']),
            ('scale_x', ['scale-x-']),
            ('scale_y', ['scale-y-']),
            # Rotate
            ('rotate', ['rotate-']),
            # Translate
            ('translate_x', ['translate-x-']),
            ('translate_y', ['translate-y-']),
            # Skew
            ('skew_x', ['skew-x-']),
            ('skew_y', ['skew-y-']),

            # Overflow
            ('overflow', ['overflow-']),
            ('overflow_x', ['overflow-x-']),
            ('overflow_y', ['overflow-y-']),
        ]

        # Precomputed prefix mapping for performance
        self._prefix_mapping = {}
        self._exact_mapping = {}
        self._initialize_mappings()

        # Regex pattern for dynamic arbitrary values
        self._arbitrary_pattern = re.compile(r'([a-zA-Z-]+)\[([^\]]+)\]')

    def _initialize_mappings(self):
        """Precompute mappings for better performance"""
        for group_name, prefixes in self.groups:
            # Handle exact matches
            for prefix in prefixes:
                if not prefix.endswith('-'):
                    self._exact_mapping[prefix] = group_name
                else:
                    self._prefix_mapping[prefix] = group_name

    def merge(self, *class_lists: str) -> str:
        """
        Merge Tailwind classes, resolving conflicts by keeping the last occurrence
        in each group.
        """
        # Flatten and filter empty classes
        all_classes: List[str] = []
        for class_str in class_lists:
            if class_str:
                all_classes.extend(class_str.split())

        if not all_classes:
            return ""

        # Track last occurrence of each group
        group_last_idx: Dict[str, int] = {}
        class_to_group: Dict[str, str] = {}

        # First pass: determine groups
        for idx, class_name in enumerate(all_classes):
            if not class_name:
                continue

            group = self._get_group(class_name)
            if group:
                group_last_idx[group] = idx
                class_to_group[class_name] = group

        # Second pass: collect final classes
        result: Set[str] = set()  # Using a set to avoid duplicate processing
        included_groups: Set[str] = set()

        # Process in reverse order for better performance in conflict resolution
        for idx in range(len(all_classes) - 1, -1, -1):
            class_name = all_classes[idx]
            if not class_name:
                continue

            group = class_to_group.get(class_name)

            if not group:
                # Not in any group, always include
                result.add(class_name)
            elif group not in included_groups and idx == group_last_idx.get(group, -1):
                # This is the last occurrence of this group and we haven't included it yet
                result.add(class_name)
                included_groups.add(group)

        # Preserve original order as much as possible
        return ' '.join(cls for cls in all_classes if cls in result)

    def _get_group(self, class_name: str) -> Optional[str]:
        """
        Find the group for a class name using precomputed mappings.
        First checks exact matches, then prefix matches, then arbitrary values.
        """
        # Check exact matches (fastest)
        if class_name in self._exact_mapping:
            return self._exact_mapping[class_name]

        # Check for arbitrary value pattern (like p-[20px])
        match = self._arbitrary_pattern.match(class_name)
        if match:
            base_class = match.group(1) + '-'
            if base_class in self._prefix_mapping:
                return self._prefix_mapping[base_class]

        # Check prefix matches
        for prefix, group in self._prefix_mapping.items():
            if class_name.startswith(prefix):
                return group

        return None

    def add_rule(self, category: str, prefixes: List[str]) -> None:
        """
        Add new conflict rule with highest priority.
        Inserts at beginning of groups list for precedence.
        """
        self.groups.insert(0, (category, prefixes))

        # Update mappings
        for prefix in prefixes:
            if not prefix.endswith('-'):
                self._exact_mapping[prefix] = category
            else:
                self._prefix_mapping[prefix] = category
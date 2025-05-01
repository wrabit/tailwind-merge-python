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

            # --- Margin --- (Split like padding for similar reasons)
            ('margin_top', ['mt-']),
            ('margin_right', ['mr-']),
            ('margin_bottom', ['mb-']),
            ('margin_left', ['ml-']),
            ('margin_x', ['mx-']),
            ('margin_y', ['my-']),
            ('margin_all', ['m-']),
            # Negative Margin (keep separate, maybe split further if needed)
            ('negative_margin_top', ['-mt-']),
            ('negative_margin_right', ['-mr-']),
            ('negative_margin_bottom', ['-mb-']),
            ('negative_margin_left', ['-ml-']),
            ('negative_margin_x', ['-mx-']),
            ('negative_margin_y', ['-my-']),
            ('negative_margin_all', ['-m-']),
            # --- End Margin ---

            # --- Padding ---
            # Order matters: More specific (sides) before less specific (axes/all)
            ('padding_top', ['pt-']),
            ('padding_right', ['pr-']),
            ('padding_bottom', ['pb-']),
            ('padding_left', ['pl-']),
            # Axes conflict with respective sides and the 'all' padding
            ('padding_x', ['px-']), # Conflicts with pl-, pr-, p-
            ('padding_y', ['py-']), # Conflicts with pt-, pb-, p-
            # General padding conflicts with all other padding types
            ('padding_all', ['p-']),
            # --- End Padding ---

            # Display
            ('display', [
                'block', 'inline', 'inline-block',
                'flex', 'inline-flex', 'grid',
                'inline-grid', 'hidden', 'contents', 'table',
                'inline-table', 'table-caption', 'table-cell',
                'table-column', 'table-column-group', 'table-footer-group',
                'table-header-group', 'table-row-group', 'table-row',
                'flow-root',
                'list-item'
            ]),

            # Position
            ('position', ['static', 'fixed', 'absolute', 'relative', 'sticky']),
            # Top, Right, Bottom, Left, Inset
            ('inset_all', ['inset-']),
            ('inset_x', ['inset-x-']),
            ('inset_y', ['inset-y-']),
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
            ('flex_grow', ['flex-grow', 'grow', 'grow-0']), # Added 'grow' alias
            # Flex Shrink
            ('flex_shrink', ['flex-shrink', 'shrink', 'shrink-0']), # Added 'shrink' alias
            # Flex
            ('flex', ['flex-1', 'flex-auto', 'flex-initial', 'flex-none']), # flex- is ambiguous now with direction etc. use specifics
            # Flex Basis
            ('flex_basis', ['basis-']),
            # Order
            ('order', ['order-']),

            # Grid Template Columns
            ('grid_template_cols', ['grid-cols-']),
            # Grid Column Start / End / Span
            ('grid_col_start', ['col-start-']),
            ('grid_col_end', ['col-end-']),
            ('grid_col_span', ['col-span-']), # Should conflict start/end conceptually, but often used together. Separate group ok.
            ('grid_col_auto', ['col-auto']), # Specific col span
            # Grid Template Rows
            ('grid_template_rows', ['grid-rows-']),
            # Grid Row Start / End / Span
            ('grid_row_start', ['row-start-']),
            ('grid_row_end', ['row-end-']),
            ('grid_row_span', ['row-span-']), # See col-span note
            ('grid_row_auto', ['row-auto']), # Specific row span
             # Grid Auto Flow
            ('grid_auto_flow', ['grid-flow-row', 'grid-flow-col', 'grid-flow-dense', 'grid-flow-row-dense', 'grid-flow-col-dense']), # Added 'dense' combinations
            # Grid Auto Columns
            ('grid_auto_cols', ['auto-cols-']),
            # Grid Auto Rows
            ('grid_auto_rows', ['auto-rows-']),
            # Gap (Split like padding)
            ('gap_all', ['gap-']),
            ('gap_x', ['gap-x-']),
            ('gap_y', ['gap-y-']),

            # Justify Content
            ('justify_content', ['justify-start', 'justify-end', 'justify-center', 'justify-between', 'justify-around', 'justify-evenly']),
            # Justify Items
            ('justify_items', ['justify-items-start', 'justify-items-end', 'justify-items-center', 'justify-items-stretch']),
            # Justify Self
            ('justify_self', ['justify-self-auto', 'justify-self-start', 'justify-self-end', 'justify-self-center', 'justify-self-stretch']),
            # Align Content
            ('align_content', ['content-center', 'content-start', 'content-end', 'content-between', 'content-around', 'content-evenly', 'content-baseline']), # Added baseline
            # Align Items
            ('align_items', ['items-start', 'items-end', 'items-center', 'items-baseline', 'items-stretch']),
            # Align Self
            ('align_self', ['self-auto', 'self-start', 'self-end', 'self-center', 'self-stretch', 'self-baseline']), # Added baseline

            # --- Border Width --- (Split sides)
            ('border_width_all', ['border', 'border-0', 'border-2', 'border-4', 'border-8']), # General width first
            ('border_width_t', ['border-t', 'border-t-0', 'border-t-2', 'border-t-4', 'border-t-8']),
            ('border_width_r', ['border-r', 'border-r-0', 'border-r-2', 'border-r-4', 'border-r-8']),
            ('border_width_b', ['border-b', 'border-b-0', 'border-b-2', 'border-b-4', 'border-b-8']),
            ('border_width_l', ['border-l', 'border-l-0', 'border-l-2', 'border-l-4', 'border-l-8']),
            # Tailwind also has border-x, border-y but let's keep it simpler for now or add if needed
            # --- End Border Width ---

            # Border Color (Needs care with opacity potentially)
            ('border_color', ['border-']), # Keep general for now, might need split if opacity added (e.g., border-red-500 vs border-opacity-50)
            # Border Style
            ('border_style', ['border-solid', 'border-dashed', 'border-dotted', 'border-double', 'border-hidden', 'border-none']), # Added hidden
            # Border Radius (Split corners/sides)
            ('border_radius_tl', ['rounded-tl-']),
            ('border_radius_tr', ['rounded-tr-']),
            ('border_radius_br', ['rounded-br-']),
            ('border_radius_bl', ['rounded-bl-']),
            ('border_radius_t', ['rounded-t-']),
            ('border_radius_r', ['rounded-r-']),
            ('border_radius_b', ['rounded-b-']),
            ('border_radius_l', ['rounded-l-']),
            ('border_radius_all', ['rounded', 'rounded-']), # General 'rounded' and 'rounded-[size]'

            # Opacity
            ('opacity', ['opacity-']),
             # Background Opacity (Conflicts with bg-color potentially, tricky) - Keep separate for now
            ('bg_opacity', ['bg-opacity-']),
             # Border Opacity
            ('border_opacity', ['border-opacity-']),
             # Text Opacity
            ('text_opacity', ['text-opacity-']),


            # Box Shadow
            ('shadow', ['shadow']), # shadow-sm, shadow, shadow-md etc.

            # Transition Property
            ('transition', ['transition']), # transition-all, transition-colors, etc.
            # Transition Duration
            ('transition_duration', ['duration-']),
            # Transition Timing Function
            ('transition_timing', ['ease-']),
            # Transition Delay
            ('transition_delay', ['delay-']),

            # Transform - Core enabling classes
            ('transform_core', ['transform', 'transform-gpu', 'transform-none']),
            # Scale
            ('scale_all', ['scale-']),
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
            # Transform Origin
            ('transform_origin', ['origin-']),


            # --- Overflow --- (Split axes)
            ('overflow_all', ['overflow-auto', 'overflow-hidden', 'overflow-visible', 'overflow-scroll']),
            ('overflow_x', ['overflow-x-auto', 'overflow-x-hidden', 'overflow-x-visible', 'overflow-x-scroll']),
            ('overflow_y', ['overflow-y-auto', 'overflow-y-hidden', 'overflow-y-visible', 'overflow-y-scroll']),
             # --- End Overflow ---

            # Whitespace
            ('whitespace', ['whitespace-normal', 'whitespace-nowrap', 'whitespace-pre', 'whitespace-pre-line', 'whitespace-pre-wrap']),
            # Word Break
            ('word_break', ['break-normal', 'break-words', 'break-all']),
            # Text Overflow
            ('text_overflow', ['truncate', 'overflow-ellipsis', 'text-ellipsis', 'overflow-clip', 'text-clip']), # Added aliases

            # Appearance
            ('appearance', ['appearance-none']),
            # Cursor
            ('cursor', ['cursor-']),
            # Pointer Events
            ('pointer_events', ['pointer-events-none', 'pointer-events-auto']),
            # Resize
            ('resize', ['resize-none', 'resize-y', 'resize-x', 'resize']),
            # User Select
            ('user_select', ['select-none', 'select-text', 'select-all', 'select-auto']),
        ]

        # Precomputed prefix mapping for performance
        self._prefix_mapping: Dict[str, str] = {}
        self._exact_mapping: Dict[str, str] = {}
        self._initialize_mappings()

        # Regex pattern for dynamic arbitrary values
        self._arbitrary_pattern = re.compile(r'^((?:[a-zA-Z0-9-]+(?:\[[^\]]+\])?:)*)?([a-zA-Z0-9-]+(?:-[a-zA-Z0-9]+)*)-\[([^\]]+)\]$')

    def _initialize_mappings(self):
        """Precompute mappings for better performance"""
        self._prefix_mapping = {}
        self._exact_mapping = {}
        for group_name, prefixes_or_exact in self.groups:
            for class_or_prefix in prefixes_or_exact:
                if class_or_prefix.endswith('-'):
                    # It's a prefix
                    self._prefix_mapping[class_or_prefix] = group_name
                else:
                    # It's an exact class name
                    self._exact_mapping[class_or_prefix] = group_name

    def merge(self, *class_lists: str) -> str:
        """
        Merge Tailwind classes, resolving conflicts by keeping the last occurrence
        in each group. Handles modifiers like hover: etc.
        """
        # Flatten, split, and filter empty classes
        all_classes: List[str] = []
        for class_str in class_lists:
            if class_str:
                all_classes.extend(filter(None, class_str.split()))

        if not all_classes:
            return ""

        # Track last occurrence index for each group *key* (group_name + modifiers)
        group_last_idx: Dict[str, int] = {}
        # Store the resolved group key for each class index
        class_to_group_key: Dict[int, str] = {}

        # First pass: determine groups and modifiers
        for idx, class_name in enumerate(all_classes):
            modifiers, base_class_name = self._extract_modifiers(class_name)
            group = self._get_group(base_class_name)

            if group:
                # Group key includes modifiers to handle conflicts correctly
                # e.g., 'hover:padding_left' vs 'padding_left'
                group_key = f"{modifiers}:{group}"
                group_last_idx[group_key] = idx
                class_to_group_key[idx] = group_key
            # else: class doesn't belong to a conflict group (or is only modifiers)

        # Second pass: collect final classes
        result_indices: Set[int] = set()
        included_group_keys: Set[str] = set()

        # Process in reverse order
        for idx in range(len(all_classes) - 1, -1, -1):
            group_key = class_to_group_key.get(idx)

            if group_key:
                # It belongs to a conflict group
                if group_key not in included_group_keys and idx == group_last_idx.get(group_key):
                    # This is the last occurrence for this specific group+modifier combination
                    result_indices.add(idx)
                    included_group_keys.add(group_key)
            elif idx not in class_to_group_key:
                 # Class does not belong to any known conflict group (or has no base class name after modifiers)
                 # Check if it has modifiers but no recognized base class - still potentially valid standalone modifier usage or custom class
                 modifiers, base_class_name = self._extract_modifiers(all_classes[idx])
                 if base_class_name or modifiers: # Include if it's a custom class or just modifiers
                     # Need to avoid adding duplicates if a non-grouped class appears multiple times
                     # Simple approach: check if the exact class string is already added via another index
                     # This isn't perfect for preserving order strictly but avoids simple duplicates.
                     is_duplicate = False
                     for added_idx in result_indices:
                         if all_classes[added_idx] == all_classes[idx]:
                             is_duplicate = True
                             break
                     if not is_duplicate:
                           result_indices.add(idx)


        # Reconstruct the string preserving original order as much as possible
        final_classes = [all_classes[i] for i in sorted(list(result_indices))]

        return ' '.join(final_classes)

    def _extract_modifiers(self, class_name: str) -> Tuple[str, str]:
        """Splits class name into modifiers (e.g., 'hover:focus:') and the base class name."""
        parts = class_name.split(':')
        if len(parts) == 1:
            return "", class_name  # No modifiers
        base_class_name = parts[-1]
        modifiers = ":".join(parts[:-1]) + ":"
        return modifiers, base_class_name

    def _get_group(self, base_class_name: str) -> Optional[str]:
        """
        Find the group for a *base* class name (without modifiers).
        Prioritizes exact matches, then arbitrary values, then the longest matching prefix.
        """
        if not base_class_name: # Handle cases like "hover:" which have no base class
            return None

        # 1. Check exact matches
        if base_class_name in self._exact_mapping:
            return self._exact_mapping[base_class_name]

        # 2. Check for arbitrary value pattern (e.g., p-[20px])
        # Use a simpler regex here as modifiers are already stripped
        arbitrary_match = re.match(r'([a-zA-Z0-9-]+(?:-[a-zA-Z0-9]+)*)-\[([^\]]+)\]$', base_class_name)
        arbitrary_base_prefix = None
        if arbitrary_match:
            arbitrary_base_prefix = arbitrary_match.group(1) + '-' # e.g., 'p-', 'border-t-'

        # 3. Check prefix matches - Find the *longest* matching prefix
        best_match_len = 0
        found_group = None

        # Check against the actual class name OR the base prefix from arbitrary value
        check_name = arbitrary_base_prefix if arbitrary_base_prefix else base_class_name

        for prefix, group in self._prefix_mapping.items():
            # Use startswith for flexibility (e.g., 'p-' matches 'p-4' and 'p-[20px]' base 'p-')
            if check_name.startswith(prefix):
                if len(prefix) > best_match_len:
                    best_match_len = len(prefix)
                    found_group = group

        # If we matched an arbitrary value's base prefix, return that group
        # Otherwise, return the group found matching the regular class name (if any)
        if arbitrary_base_prefix and found_group:
             return found_group
        elif not arbitrary_base_prefix and found_group:
             return found_group

        # 4. No group found
        return None


    def add_rule(self, category: str, classes_or_prefixes: List[str]) -> None:
        """
        Add a new conflict rule. It will have high precedence for lookups
        if its prefixes are longer or specific, due to the longest-match logic.
        """
        # Add to the internal groups list (less critical now with sorted lookup)
        self.groups.append((category, classes_or_prefixes)) # Append is fine

        # Update mappings immediately
        for item in classes_or_prefixes:
            if item.endswith('-'):
                # Check if prefix already exists and warn or decide overwrite policy
                # if item in self._prefix_mapping and self._prefix_mapping[item] != category:
                #     print(f"Warning: Overwriting prefix '{item}' group '{self._prefix_mapping[item]}' with '{category}'")
                self._prefix_mapping[item] = category
            else:
                # Check if exact match already exists
                # if item in self._exact_mapping and self._exact_mapping[item] != category:
                #     print(f"Warning: Overwriting exact match '{item}' group '{self._exact_mapping[item]}' with '{category}'")
                self._exact_mapping[item] = category
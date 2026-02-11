"""
Markdown File Splitter for VitePress

This module splits large markdown files into smaller, flat files based on
heading levels (# and ##), and generates corresponding VitePress sidebar configuration.

Workflow:
1. update.py downloads files to original/{name}.md
2. cutter.cut() reads from original/{name}.md and splits into individual files

Usage:
    import cutter
    cutter.cut({'cf', 'oj'})  # Process original/cf.md and original/oj.md files

Features:
- Splits markdown files by level 1 (#) and level 2 (##) headings based on section length
- Uses mistune library for robust markdown parsing
- Creates flat file structure under docs/{name}/ (no subdirectories)
- Generates VitePress sidebar configuration with links on headers (collapsed for level 1)
- Uses smart filename generation based on problem IDs or slugified titles
- Creates index.md (guide page) for each problem set (not in sidebar)
- Reads from original/{name}.md (downloaded by update.py)
- Smart splitting based on section length (500-line threshold):
  * Short sections (≤500 lines): Create only L1 file, keep L2 content intact, sidebar items = []
  * Long sections (>500 lines): Don't create L1 file, split L2 into individual files
- Converts level 2 headings to level 1 in individual files (for long sections)

Filename Generation Rules:
1. Extract problem ID from titles like "1A. Theatre Square" -> "1a.md"
2. Extract problem ID from titles like "01003: Hangover" -> "01003.md"
3. For other titles, use slugified name like "Basic Problems" -> "basic-problems.md"
4. Handle duplicates with -1, -2 suffixes

Output:
- Creates docs/{name}/ directory with flat structure
- Creates docs/{name}/index.md with welcome text (accessible directly, not in sidebar)
- Reads from original/{name}.md (source file downloaded by update.py)
- Updates docs/.vitepress/config.mjs with sidebar configuration
- File creation depends on section length (see Smart splitting above)

Note: Generated directories (docs/cf/, docs/oj/) are excluded from git via .gitignore
"""

import os
import re
import shutil
from collections.abc import Iterable
from pathlib import Path

import mistune


def heading_to_name(heading_text: str, used_names: set = None) -> str:
    r"""
    Convert heading text to a filename or directory name.
    
    New rules:
    1. If title matches ^\w*?(\d+\w*)[^\d\w], extract the captured group (\d+\w*) as filename
       - Extracts IDs like '1a' from '1A. Theatre Square'
       - Extracts IDs like '01003' from '01003: Hangover'
    2. Otherwise, use slugified name (no random hash)
    3. Handle duplicates with -1, -2, etc.
    
    Args:
        heading_text: The heading text (without # symbols)
        used_names: Set of already used filenames to avoid duplicates
    
    Returns:
        A valid filename/directory name
    """
    if used_names is None:
        used_names = set()

    # Rule 1: Try to extract ID from pattern like "1A. Theatre Square" -> "1a"
    # Pattern: ^\w*(\d*\w*)[^\d\w]
    match = re.match(r'^\w*?(\d+\w*)\W', heading_text)
    if match:
        base_name = match.group(1).lower()
    else:
        # Rule 2: Use slugified name without hash
        # Remove special characters and convert to lowercase
        base_name = re.sub(r'[^\w\s-]', '', heading_text)
        base_name = re.sub(r'[-\s]+', '-', base_name)
        base_name = base_name.strip('-').lower()
        if not base_name:
            base_name = 'unnamed'

    # Rule 3: Handle duplicates
    if base_name not in used_names:
        used_names.add(base_name)
        return base_name

    # Find next available name with suffix
    counter = 1
    while f"{base_name}-{counter}" in used_names:
        counter += 1

    final_name = f"{base_name}-{counter}"
    used_names.add(final_name)
    return final_name


def parse_markdown(content: str):
    """
    Parse markdown content and extract headings with their content.
    Uses mistune library for robust markdown parsing, automatically handling
    code blocks, inline code, and other markdown syntax correctly.
    
    Args:
        content: Markdown file content
    
    Returns:
        List of tuples: (level, heading_text, content_lines_start, content_lines_end)
    """
    # Parse markdown to AST using mistune
    markdown = mistune.create_markdown(renderer='ast')
    ast = markdown(content)

    # Split content into lines for indexing
    lines = content.split('\n')

    # Extract headings from AST
    headings = []

    def extract_heading_text(children):
        """Extract text from heading children nodes, handling various inline elements."""
        text_parts = []
        for child in children:
            if child['type'] == 'text':
                text_parts.append(child['raw'])
            elif child['type'] == 'codespan':
                text_parts.append(child['raw'])
            elif child['type'] == 'inline_html':
                text_parts.append(child['raw'])
            elif 'raw' in child:
                text_parts.append(child['raw'])
            elif 'children' in child:
                text_parts.append(extract_heading_text(child['children']))
        return ''.join(text_parts)

    # Build a mapping of heading text to their positions for faster lookup
    # First pass: find all heading positions in the original text
    heading_positions = {}
    for i, line in enumerate(lines):
        # Check for ATX-style headings (with or without space after #)
        match = re.match(r'^(#{1,2})\s*(.+)$', line)
        if match:
            level = len(match.group(1))
            if level <= 2:
                # Store position for this heading pattern
                if i not in heading_positions:
                    heading_positions[i] = (level, line)

    # Second pass: match AST headings to line numbers
    for node in ast:
        if node['type'] == 'heading':
            level = node['attrs']['level']
            # Only process level 1 and 2 headings
            if level <= 2:
                heading_text = extract_heading_text(node['children'])

                # Find the best matching line
                best_match = None
                for line_num, (line_level, line_content) in heading_positions.items():
                    if line_level == level:
                        # Check if this line contains the heading text
                        line_text = line_content[level:].strip()
                        # Match if the extracted text is in the line
                        # (handles inline markdown syntax differences)
                        if heading_text in line_text or line_text.startswith(
                                heading_text[:20] if len(heading_text) >= 20 else heading_text):
                            if best_match is None or line_num < best_match:
                                best_match = line_num

                if best_match is not None:
                    headings.append((level, heading_text, best_match))
                    # Remove the matched position to avoid duplicates
                    del heading_positions[best_match]

    # Build sections with content ranges
    sections = []
    for idx, (level, heading_text, start_line) in enumerate(headings):
        # Find the end of this section (next heading of same or higher level)
        end_line = len(lines)
        for next_level, _, next_start in headings[idx + 1:]:
            if next_level <= level:
                end_line = next_start
                break

        sections.append((level, heading_text, start_line, end_line))

    return sections


def create_file_structure(name: str, sections):
    """
    Create flat directory structure and write content files.
    All files are placed directly under docs/{name}/ with no subdirectories.
    
    Changes:
    - Reads from original/{name}.md instead of docs/{name}/full.md
    - Skips creating complete page for "too long" level 1 sections
    - Converts ## to # in level 2 individual files
    
    Args:
        name: Base name (e.g., 'cf', 'oj') - must be validated before calling
        sections: List of (level, heading_text, start_line, end_line) tuples
    
    Returns:
        Dictionary representing the sidebar structure
    """
    # Read the original content from original/{name}.md
    original_path = f'original/{name}.md'
    if not os.path.exists(original_path):
        raise FileNotFoundError(f"{original_path} not found. Please run update.py first to download the files.")

    with open(original_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    base_dir = Path(f'docs/{name}')

    # Clean up old structure if it exists
    if base_dir.exists():
        shutil.rmtree(base_dir)

    base_dir.mkdir(parents=True, exist_ok=True)

    # Track filenames to avoid duplicates
    used_names = set()

    # Track current level 1 section
    current_l1_name = None
    sidebar_structure = []
    current_l1_items = []
    current_l1_link = None

    # Define "too long" threshold for level 1 sections
    # Using line count: sections with more than 500 lines are considered too long
    # Logic:
    # - Short sections (≤500 lines): Create L1 file, DON'T split L2 headings, items = []
    # - Long sections (>500 lines): DON'T create L1 file, split L2 headings, items = [L2 links]
    TOO_LONG_THRESHOLD = 500

    for level, heading_text, start_line, end_line in sections:
        # Extract content for this section
        content = '\n'.join(lines[start_line:end_line])
        content_line_count = end_line - start_line

        if level == 1:
            # Save previous level 1 items if any
            # Note: Always save L1 sections, even with empty items, for visual consistency
            # Short sections will have items=[], long sections will have L2 items
            if current_l1_name:
                sidebar_structure.append({
                    'text': current_l1_name,
                    'link': current_l1_link,
                    'items': current_l1_items
                })

            # Create new level 1 section
            current_l1_name = heading_text
            current_l1_items = []

            # Check if this level 1 section is too long
            is_too_long = content_line_count > TOO_LONG_THRESHOLD

            if is_too_long:
                # Long section: Don't create a file for this level 1 section
                # Level 2 items will be split into individual files
                current_l1_link = None
            else:
                # Short section: Create file for level 1 section
                # Level 2 items will NOT be split (items will be empty)
                file_name = heading_to_name(heading_text, used_names)
                file_path = base_dir / f'{file_name}.md'
                current_l1_link = f'/{name}/{file_name}'

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        elif level == 2:
            if current_l1_name is None:
                # If no level 1 heading yet, create a default one
                current_l1_name = 'Content'
                current_l1_items = []
                current_l1_link = None

            # Only split level 2 headings if parent level 1 section is "too long"
            # (i.e., current_l1_link is None, meaning no L1 file was created)
            if current_l1_link is None:
                # Parent is long: Create level 2 file (flat structure)
                file_name = heading_to_name(heading_text, used_names)
                file_path = base_dir / f'{file_name}.md'

                # Convert ## to # in level 2 files
                # Find the first line with ## and replace it with #
                content_lines = content.split('\n')
                for i, line in enumerate(content_lines):
                    if line.startswith('## '):
                        content_lines[i] = line[1:]  # Remove one # character to convert ## to #
                        break
                content = '\n'.join(content_lines)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                current_l1_items.append({
                    'text': heading_text,
                    'link': f'/{name}/{file_name}'
                })
            # else: Parent is short, don't split level 2 headings (keep items empty)

    # Add the last level 1 section
    if current_l1_name:
        sidebar_structure.append({
            'text': current_l1_name,
            'link': current_l1_link,
            'items': current_l1_items
        })

    return sidebar_structure


def generate_sidebar_config(structures: dict) -> str:
    """
    Generate VitePress sidebar configuration.
    
    Changes:
    - "引导页" entry removed from sidebar
    - Only add 'collapsed' and 'items' properties for sections that have items
    - Non-split sections (short sections) get simple format with just text and link
    
    Args:
        structures: Dictionary mapping name -> sidebar_structure
    
    Returns:
        JavaScript object string for sidebar configuration
    """
    sidebar_parts = []

    for name, structure in structures.items():
        # Create configuration for this document type
        # Note: Use /name without trailing slash to match /name/index.md and subdirectories
        sidebar_config = f"'/{name}': {{\n"
        sidebar_config += "        items: [\n"

        # Note: "引导页" entry removed from sidebar (index.md file is still created)

        # Add sections with links on headers
        # Only add collapsed and items for sections that have items (split sections)
        for section in structure:
            # Escape single quotes in text
            section_text = section['text'].replace("'", "\\'")
            sidebar_config += "            {\n"
            sidebar_config += f"                text: '{section_text}',\n"

            # Add link to the section header if available
            if section.get('link'):
                sidebar_config += f"                link: '{section['link']}',\n"

            # Only add collapsed and items if section has items (i.e., it's a split section)
            if section['items']:
                sidebar_config += "                collapsed: true,\n"
                sidebar_config += "                items: [\n"
                for sub_item in section['items']:
                    text = sub_item['text'].replace("'", "\\'")
                    sidebar_config += f"                    {{ text: '{text}', link: '{sub_item['link']}' }},\n"
                sidebar_config += "                ]\n"

            sidebar_config += "            },\n"

        # Note: Removed '完整文件' entry - no longer needed

        sidebar_config += "        ]\n"
        sidebar_config += "    }"

        sidebar_parts.append(sidebar_config)

    return ",\n        ".join(sidebar_parts)


def update_config_file(sidebar_config: str):
    """
    Update the config.mjs file with the generated sidebar configuration.
    
    Args:
        sidebar_config: JavaScript sidebar configuration string
    """
    # Read the template
    with open('config.templ.mjs', 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace the sidebar placeholder
    updated_config = template.replace(
        '// template: sidebar',
        sidebar_config
    )

    # Write to the actual config file
    with open('docs/.vitepress/config.mjs', 'w', encoding='utf-8') as f:
        f.write(updated_config)


def split(names: Iterable[str]):
    """
    Main function to cut markdown files into smaller pieces.
    
    Args:
        names: Set of document names to process (e.g., {'cf', 'oj'})
    """
    all_structures = {}

    for name in names:
        # Validate name to prevent path traversal
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            print(
                f"Error: Invalid name '{name}'. Only alphanumeric characters, underscore and hyphen are allowed. Skipping...")
            continue

        original_path = f'original/{name}.md'

        if not os.path.exists(original_path):
            print(f"Warning: {original_path} not found, skipping...")
            continue

        print(f"Processing {name} from original/{name}.md...")

        # Read the markdown file
        with open(original_path, 'r', encoding='utf-8') as f:
            content = f.read()

        sections = parse_markdown(content)
        print(f"  Found {len(sections)} sections")


        # Remove existing docs/{name}/ directory if it exists
        docs_dir = Path(f'docs/{name}')
        if docs_dir.exists():
            shutil.rmtree(docs_dir)
            print(f"  Removed existing docs/{name}/ directory")

        # Create file structure
        structure = create_file_structure(name, sections)
        all_structures[name] = structure
        print(f"  Created file structure in docs/{name}/")

        # Create index.md (guide page)
        base_dir = Path(f'docs/{name}')
        index_path = base_dir / 'index.md'

        # Determine the name for the guide page
        if name == 'oj':
            title = 'OpenJudge题库'
        elif name == 'cf':
            title = 'Codeforces题库'
        else:
            title = f'{name.upper()}题库'

        guide_content = f"# {title}\n\n欢迎来到{title}，点击左边目录选择题目。\n"

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        print(f"  Created index.md (guide page)")

    # Generate and update sidebar configuration
    if all_structures:
        print("Generating sidebar configuration...")
        sidebar_config = generate_sidebar_config(all_structures)
        update_config_file(sidebar_config)
        print("Updated docs/.vitepress/config.mjs")

    print("Done!")


if __name__ == "__main__":
    from config import ANSWERS
    split(answer.name for answer in ANSWERS)

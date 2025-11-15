#!/usr/bin/env python3
"""
Content linter for blog posts and study guides.
Checks for violations of writing standards defined in CLAUDE.md.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


class ContentViolation:
    def __init__(self, line_num: int, rule: str, text: str, suggestion: str = ""):
        self.line_num = line_num
        self.rule = rule
        self.text = text
        self.suggestion = suggestion

    def __str__(self):
        result = f"Line {self.line_num}: {self.rule}\n  \"{self.text}\""
        if self.suggestion:
            result += f"\n  → {self.suggestion}"
        return result


class ContentLinter:
    def __init__(self):
        self.violations: List[ContentViolation] = []

        # AI-tell phrases to avoid
        self.ai_tell_phrases = [
            r"\bthe key insight\b",
            r"\bthe insight\b(?! into)",  # "the insight" but not "the insight into"
            r"\bthe takeaway\b",
            r"\bit'?s important to note\b",
            r"\bit'?s worth noting\b",
            r"\bit should be noted\b",
            r"\bin conclusion\b",
            r"\bin summary\b",
            r"\bfinal version\b",
            r"\bfinal conclusion\b",
            r"\bultimately\b",
            r"\bessentially\b",
            r"\bfundamentally\b",
            r"\bat the end of the day\b",
            r"\bthe bottom line is\b",
        ]

        # AI-tell colon constructions
        self.ai_tell_colons = [
            r"What's converging:",
            r"A critical distinction:",
            r"The difference:",
            r"The key:",
            r"The point:",
            r"Here's why:",
        ]

        # Missing article patterns (common cases)
        self.missing_article_patterns = [
            (r"\bmasquerading as process\b", "masquerading as a process"),
            (r"\breconsolidate agreement\b", "reconsolidate the agreement"),
        ]

    def lint_file(self, filepath: Path) -> List[ContentViolation]:
        """Lint a markdown file and return list of violations."""
        self.violations = []

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        self._lint_lines(lines)
        return self.violations

    def lint_text(self, text: str) -> List[ContentViolation]:
        """Lint raw text and return list of violations."""
        self.violations = []
        lines = text.splitlines(keepends=True)
        self._lint_lines(lines)
        return self.violations

    def _lint_lines(self, lines: List[str]):
        """Internal method to lint a list of lines."""
        in_frontmatter = False
        frontmatter_ended = False
        in_code_block = False

        for line_num, line in enumerate(lines, start=1):
            # Skip YAML frontmatter (only at start of file)
            if line.strip() == '---':
                if line_num == 1:
                    # First line with --- starts frontmatter
                    in_frontmatter = True
                    continue
                elif in_frontmatter and not frontmatter_ended:
                    # Second --- ends frontmatter
                    in_frontmatter = False
                    frontmatter_ended = True
                    continue
                # Any other --- is just content (horizontal rule)

            if in_frontmatter:
                continue

            # Skip code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Skip bullet points and headers for some checks
            is_bullet = line.strip().startswith('-') or line.strip().startswith('*')
            is_header = line.strip().startswith('#')

            # Check for AI-tell phrases
            self._check_ai_tell_phrases(line_num, line)

            # Check for AI-tell colon constructions
            self._check_ai_tell_colons(line_num, line)

            # Check for em-dashes in sentences (not in bullets/headers)
            if not is_bullet and not is_header:
                self._check_em_dashes(line_num, line)

            # Check for missing articles
            self._check_missing_articles(line_num, line)

            # Check for run-on sentences
            if not is_bullet and not is_header:
                self._check_run_on_sentences(line_num, line)

            # Check for choppy sentence patterns
            if not is_bullet and not is_header:
                self._check_choppy_sentences(line_num, line)

    def _check_ai_tell_phrases(self, line_num: int, line: str):
        """Check for AI-tell phrases."""
        for phrase_pattern in self.ai_tell_phrases:
            if re.search(phrase_pattern, line, re.IGNORECASE):
                match = re.search(phrase_pattern, line, re.IGNORECASE)
                self.violations.append(ContentViolation(
                    line_num,
                    "AI-tell phrase detected",
                    line.strip(),
                    f"Remove '{match.group()}' and state directly"
                ))

    def _check_ai_tell_colons(self, line_num: int, line: str):
        """Check for AI-tell colon constructions."""
        for pattern in self.ai_tell_colons:
            if re.search(pattern, line, re.IGNORECASE):
                self.violations.append(ContentViolation(
                    line_num,
                    "AI-tell colon construction",
                    line.strip(),
                    "State the point directly without meta-commentary"
                ))

    def _check_em_dashes(self, line_num: int, line: str):
        """Check for em-dashes and hyphen-dash substitutes in prose sentences."""
        # Check for actual em-dash character
        if '—' in line:
            self.violations.append(ContentViolation(
                line_num,
                "Em-dash in sentence",
                line.strip(),
                "Use semicolon, comma, or period instead"
            ))

        # Check for hyphen used as em-dash substitute
        # Pattern: word/punctuation followed by space-hyphen-space followed by word
        # Exclude cases where it's clearly not a dash substitute:
        # - List items starting with "- "
        # - Markdown links with " - " as separator
        # - Short phrases like "a - b" comparisons
        if not line.strip().startswith('-'):  # Not a bullet point
            # Look for space-hyphen-space pattern with substantial text on both sides
            # Pattern allows for markdown formatting (**, *, `, etc.) before/after the hyphen
            # Must have at least 15 chars of context before the hyphen
            context_pattern = r'.{15,}\s+-\s+\w'
            if re.search(context_pattern, line):
                self.violations.append(ContentViolation(
                    line_num,
                    "Hyphen used as em-dash substitute",
                    line.strip(),
                    "Use semicolon, comma, or period instead of ' - '"
                ))

    def _check_missing_articles(self, line_num: int, line: str):
        """Check for common missing article patterns."""
        for pattern, suggestion in self.missing_article_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                self.violations.append(ContentViolation(
                    line_num,
                    "Missing article",
                    line.strip(),
                    f"Consider: '{suggestion}'"
                ))

    def _check_run_on_sentences(self, line_num: int, line: str):
        """Check for potential run-on sentences."""
        # Skip short lines
        if len(line.strip()) < 100:
            return

        # Count semicolons and commas in the sentence
        semicolons = line.count(';')
        commas = line.count(',')

        # Flag if sentence has 2+ semicolons or 3+ semicolons/commas combined
        if semicolons >= 2:
            self.violations.append(ContentViolation(
                line_num,
                "Possible run-on sentence (multiple semicolons)",
                line.strip()[:80] + "...",
                "Consider breaking into separate sentences"
            ))
        elif semicolons >= 1 and commas >= 3:
            # Check if it's excessively long with multiple clauses
            if len(line) > 150:
                self.violations.append(ContentViolation(
                    line_num,
                    "Possible run-on sentence (length + complexity)",
                    line.strip()[:80] + "...",
                    "Reader may need to buffer too much context; consider breaking up"
                ))

    def _check_choppy_sentences(self, line_num: int, line: str):
        """Check for choppy sentence patterns."""
        # Pattern: Telegraphic parallel structures (check first - more specific)
        # "X says Y. The other says Z." or "X does Y. Another does Z."
        parallel_patterns = [
            # Question followed by parallel structure (most specific)
            (r'[A-Z][^.?]{10,40}\?\s+One side [^.]{10,50}\.\s+The other [^.]{10,50}\.',
             "Combine parallel thoughts with conjunctions: 'One side says X and the other says Y'"),
            # One side... The other...
            (r'One side [^.]{10,50}\.\s+The other [^.]{10,50}\.',
             "Consider: 'One side X and the other Y' for better flow"),
            # Some... Others...
            (r'Some [^.]{10,50}\.\s+Others [^.]{10,50}\.',
             "Consider: 'Some X while others Y' for better flow"),
            # One... Another...
            (r'One [^.]{10,50}\.\s+Another [^.]{10,50}\.',
             "Consider using 'while' or 'whereas' to connect the thoughts"),
        ]

        # Track whether we've flagged this line to avoid duplicates
        flagged = False
        for pattern, suggestion in parallel_patterns:
            if re.search(pattern, line.strip()):
                self.violations.append(ContentViolation(
                    line_num,
                    "Telegraphic parallel structure",
                    line.strip()[:100] + ("..." if len(line.strip()) > 100 else ""),
                    suggestion
                ))
                flagged = True
                break

        # Pattern: General choppy sentences (only if not already flagged)
        # Looking for: "Word. Word" pattern where both are very short
        if not flagged:
            pattern = r'^([A-Z][^.!?]{5,30})\.(\s+)([A-Z][^.!?]{5,30})\.'
            if re.search(pattern, line.strip()):
                self.violations.append(ContentViolation(
                    line_num,
                    "Possibly choppy sentences",
                    line.strip()[:80],
                    "Consider combining with comma or semicolon for better flow"
                ))


def main():
    if len(sys.argv) < 2:
        print("Usage: python lint_content.py <markdown_file>")
        print("       python lint_content.py --text <text_content>")
        sys.exit(1)

    linter = ContentLinter()

    # Check if using --text flag for raw string input
    if sys.argv[1] == '--text':
        if len(sys.argv) < 3:
            print("Error: --text flag requires text content argument")
            sys.exit(1)

        text_content = sys.argv[2]
        violations = linter.lint_text(text_content)
        source_name = "provided text"
    else:
        filepath = Path(sys.argv[1])

        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            sys.exit(1)

        violations = linter.lint_file(filepath)
        source_name = filepath.name

    if not violations:
        print(f"OK: No violations found in {source_name}")
        sys.exit(0)

    # Use UTF-8 encoding for output
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print(f"VIOLATIONS FOUND in {source_name}:\n")
    for violation in violations:
        print(violation)
        print()

    print(f"Total violations: {len(violations)}")
    sys.exit(1)


if __name__ == "__main__":
    main()

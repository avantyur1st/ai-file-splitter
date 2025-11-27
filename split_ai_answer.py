#!/usr/bin/env python3
"""
AI Response File Splitter
Splits a structured AI response into multiple files and directories.
"""

import os
import sys
import argparse
import logging
from typing import List, Tuple, Dict


def parse_files(text: str) -> List[Tuple[str, str]]:
    """
    Parses AI response text into a list of (path, content) tuples.
    Expected format:

    FILE path/to/file.py
    ================================
    <content>
    ================================
    END FILE
    """
    lines = text.splitlines(keepends=True)

    idx = 0
    n = len(lines)
    result = []

    while idx < n:
        line = lines[idx].strip()

        # Look for block start
        if not line.startswith("FILE "):
            idx += 1
            continue

        path = line[len("FILE "):].strip()
        start_line = idx + 1
        idx += 1

        # Look for first separator line
        while idx < n and not is_separator(lines[idx].strip()):
            idx += 1
        if idx >= n:
            raise ValueError(
                f"Separator not found after FILE {path} (line {start_line})"
            )
        sep_line = lines[idx].strip()
        idx += 1

        # Collect content until next identical separator
        content_lines = []
        while idx < n and lines[idx].strip() != sep_line:
            content_lines.append(lines[idx])
            idx += 1
        if idx >= n:
            raise ValueError(
                f"Closing separator not found for file {path} (line {start_line})"
            )
        idx += 1  # skip closing separator

        # Expect END FILE
        if idx >= n or lines[idx].strip() != "END FILE":
            raise ValueError(
                f"Expected 'END FILE' after file {path} (line {idx + 1})"
            )
        idx += 1  # skip END FILE

        result.append((path, "".join(content_lines)))

    return result


def is_separator(line: str) -> bool:
    """
    Considers a line to be a separator if it consists of >=10
    identical '=' or '-' characters.
    """
    if len(line) < 10:
        return False
    chars = set(line)
    if len(chars) != 1:
        return False
    return line[0] in ("=", "-")


def validate_path(rel_path: str, output_dir: str) -> None:
    """
    Ensure the path doesn't escape output directory and is safe.
    
    Raises:
        ValueError: If path is invalid or potentially dangerous.
    """
    # Check for suspicious patterns
    if '..' in rel_path:
        raise ValueError(f"Path contains '..': {rel_path}")
    
    if rel_path.startswith('/') or rel_path.startswith('\\'):
        raise ValueError(f"Path is absolute: {rel_path}")
    
    # Verify the resolved path stays within output_dir
    full_path = os.path.abspath(os.path.join(output_dir, rel_path))
    base_path = os.path.abspath(output_dir)
    
    if not full_path.startswith(base_path + os.sep) and full_path != base_path:
        raise ValueError(f"Path escapes output directory: {rel_path}")


def write_files(
    blocks: List[Tuple[str, str]],
    output_dir: str,
    encoding: str = 'utf-8',
    dry_run: bool = False,
    force: bool = False
) -> Dict[str, int]:
    """
    Creates files from parsed blocks.
    
    Returns:
        Dictionary with statistics: created, skipped, errors.
    """
    stats = {'created': 0, 'skipped': 0, 'errors': 0}

    for rel_path, content in blocks:
        try:
            # Validate path
            validate_path(rel_path, output_dir)
            
            file_path = os.path.join(output_dir, rel_path)
            dir_name = os.path.dirname(file_path)

            # Check if file exists
            if os.path.exists(file_path) and not force and not dry_run:
                logging.warning(f"File exists: {file_path}")
                try:
                    response = input(f"Overwrite {rel_path}? [y/N]: ")
                    if response.lower() != 'y':
                        logging.info(f"Skipped: {file_path}")
                        stats['skipped'] += 1
                        continue
                except (EOFError, KeyboardInterrupt):
                    logging.info("\nSkipping file due to user input interruption")
                    stats['skipped'] += 1
                    continue

            if dry_run:
                logging.info(f"Would create: {file_path} ({len(content)} bytes)")
                stats['created'] += 1
            else:
                # Create directory if needed
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)
                
                # Write file
                with open(file_path, "w", encoding=encoding) as f:
                    f.write(content)
                
                logging.info(f"Created: {file_path}")
                stats['created'] += 1

        except ValueError as e:
            logging.error(f"Invalid path {rel_path}: {e}")
            stats['errors'] += 1
        except OSError as e:
            logging.error(f"Failed to create {rel_path}: {e}")
            stats['errors'] += 1
        except Exception as e:
            logging.error(f"Unexpected error with {rel_path}: {e}")
            stats['errors'] += 1

    return stats


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging based on verbosity flags."""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        stream=sys.stderr
    )


def main():
    parser = argparse.ArgumentParser(
        description='Splits a structured multi-file AI response into actual files.',
        epilog='Example: %(prog)s ai_response.txt -o ./project'
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        default='-',
        help='Path to the text file with AI response (use "-" for stdin)'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help='Directory where to place generated files (default: current directory)'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='Output file encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview files without creating them'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing files without prompting'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output (show debug information)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (only show errors)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose, args.quiet)
    
    try:
        # Read input
        if args.input == '-':
            logging.debug("Reading from stdin...")
            text = sys.stdin.read()
        else:
            logging.debug(f"Reading from file: {args.input}")
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        
        if not text.strip():
            logging.error("Input is empty")
            return 1
        
        # Parse blocks
        logging.debug("Parsing file blocks...")
        blocks = parse_files(text)
        
        if not blocks:
            logging.warning("No file blocks found in input")
            return 0
        
        logging.info(f"Found {len(blocks)} file(s) to process")
        
        # Create output directory if needed
        if args.output_dir != '.' and not args.dry_run:
            os.makedirs(args.output_dir, exist_ok=True)
            logging.debug(f"Ensured output directory exists: {args.output_dir}")
        
        # Write files
        stats = write_files(
            blocks,
            args.output_dir,
            encoding=args.encoding,
            dry_run=args.dry_run,
            force=args.force
        )
        
        # Print summary
        mode = "Would create" if args.dry_run else "Created"
        logging.info(
            f"\nSummary: {mode} {stats['created']} file(s), "
            f"skipped {stats['skipped']}, "
            f"errors {stats['errors']}"
        )
        
        return 1 if stats['errors'] > 0 else 0
        
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return 1
    except ValueError as e:
        logging.error(f"Parse error: {e}")
        return 1
    except KeyboardInterrupt:
        logging.info("\nOperation cancelled by user")
        return 130
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

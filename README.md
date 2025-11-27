🌍 **[Russian](README.ru.md)**

<div align="center">
  
# AI Response File Splitter

**Transform structured AI responses into complete project file structures**

</div>

***

## 📋 Overview

AI Response File Splitter is a zero-dependency Python command-line tool that automatically converts a single structured AI response into a multi-file project structure with proper directories and files.

Instead of manually copying code snippets from AI chat responses into separate files, this tool parses a specially formatted text file and creates your entire project structure in seconds.

### ✨ Key Features

- 🎯 **Human-readable format** - Simple text-based format, no JSON required
- 🚀 **Zero dependencies** - Uses only Python standard library
- 🔒 **Path validation** - Prevents directory traversal and malicious paths
- 👀 **Dry-run mode** - Preview files before creating them
- 🛡️ **Safe overwrites** - Interactive prompts before overwriting existing files
- 📊 **Detailed logging** - Verbose, normal, and quiet modes
- 📥 **Stdin support** - Works with pipes and redirects
- ⚡ **Fast** - Processes hundreds of files in seconds
- 🌍 **Cross-platform** - Works on Windows, macOS, and Linux

***

## 🔧 Requirements

- Python 3.8 or higher (no additional packages required)

All dependencies are part of Python's standard library:

- `os` - File system operations
- `sys` - System operations
- `argparse` - Command-line parsing
- `logging` - Logging functionality
- `typing` - Type hints

***

## 📥 Installation

### Quick Install

Simply download the script:

```bash
curl -O https://raw.githubusercontent.com/avantyur1st/ai-file-splitter/main/split_ai_answer.py
chmod +x split_ai_answer.py
```

Or clone the repository:

```bash
git clone https://github.com/avantyur1st/ai-file-splitter.git
cd ai-file-splitter
```

No `pip install` required!

***

## 🚀 Usage Scenarios

This tool supports **two workflows** depending on when you want to structure your code:

### Scenario 1: 📝 Start with Structure (Recommended)

Use this prompt **at the beginning** of your conversation with AI to generate properly structured code from the start.

### Scenario 2: 🔄 Refactor Later

Use this prompt **at the end** of your conversation to reorganize existing code into a multi-file project.

***

## 📝 Scenario 1: Generate Structured Code from Start

### 1. Use This AI Prompt

Copy this prompt and use it **at the beginning** of your conversation with any AI (ChatGPT, Claude, etc.):

```
You are a multi-file project generator.

Based on the technical requirements below, generate code split into multiple files.

Format (strictly follow):
- For each file use this block:
  FILE relative/path/to/file.py
  ========================================
  <full file content>
  ========================================
  END FILE

- The line starting with FILE contains the path relative to project root
- Lines of ==== serve as separators (minimum 10 identical characters)
- Between two separators is ONLY the file content without extra comments or Markdown
- After the second separator must be the line END FILE

Below is the user's technical requirements:
<your project description here>
```


### 2. Save AI Response

Save the AI's response to a text file (e.g., `ai_response.txt`)

### 3. Run the Script

```bash
python split_ai_answer.py ai_response.txt -o ./my_project
```

Done! Your project structure is created in `./my_project/`

***

## 🔄 Scenario 2: Refactor Existing Code

If you've already finished coding with AI and want to transform everything into a proper project structure, use this prompt **at the end** of your conversation:

### Refactoring Prompt

```
Please take all the code we've created in this chat and transform it into a multi-file project structure.

Output format (strictly follow):
- For each file use this block:
  FILE relative/path/to/file.py
  ========================================
  <full file content>
  ========================================
  END FILE

Requirements:
1. Split code into logical modules and files
2. Create proper directory structure (e.g., src/, tests/, config/, docs/)
3. Add requirements.txt (if dependencies are needed)
4. Add .gitignore for the project
5. Create README.md with brief project description
6. Each file should be self-contained (with all necessary imports)
7. Follow best practices for project structure in Python/JavaScript/other language

Do not add any explanations before or after file blocks — only the formatted code itself.
```


### Alternative (Shorter Version)

```
Reformat all code from this chat into a multi-file project.

Use format:
FILE path/to/file.ext
========================================
<content>
========================================
END FILE

Split into logical modules, add folder structure, README.md, .gitignore, and requirements.txt (if needed).
```


### Then Run the Script

```bash
python split_ai_answer.py ai_response.txt -o ./my_project
```
***

### Basic Syntax

```bash
python split_ai_answer.py [INPUT] [OPTIONS]
```
***

### Command-Line Options

| Option | Description |
| :-- | :-- |
| `INPUT` | Path to AI response file (use `-` for stdin) |
| `-o, --output-dir DIR` | Directory for generated files (default: current) |
| `--encoding ENCODING` | Output file encoding (default: utf-8) |
| `--dry-run` | Preview files without creating them |
| `--force` | Overwrite existing files without prompting |
| `-v, --verbose` | Show debug information |
| `-q, --quiet` | Only show errors |
| `--version` | Show version number |
| `-h, --help` | Show help message |


***

## 💡 Examples

### Example 1: Basic Usage

Create project from AI response:

```bash
python split_ai_answer.py response.txt -o ./myapp
```

**Output:**

```
INFO: Found 5 file(s) to process
INFO: Created: ./myapp/main.py
INFO: Created: ./myapp/config.py
INFO: Created: ./myapp/utils/helpers.py
INFO: Created: ./myapp/models/user.py
INFO: Created: ./myapp/tests/test_main.py

Summary: Created 5 file(s), skipped 0, errors 0
```


### Example 2: Preview Before Creating (Dry Run)

```bash
python split_ai_answer.py response.txt -o ./myapp --dry-run
```

**Output:**

```
INFO: Would create: ./myapp/main.py (1247 bytes)
INFO: Would create: ./myapp/config.py (523 bytes)
INFO: Would create: ./myapp/utils/helpers.py (892 bytes)

Summary: Would create 3 file(s), skipped 0, errors 0
```


### Example 3: From Stdin (Pipe Support)

```bash
cat ai_response.txt | python split_ai_answer.py - -o ./project
```

Or with clipboard:

```bash
pbpaste | python split_ai_answer.py - -o ./project  # macOS
xclip -o | python split_ai_answer.py - -o ./project  # Linux
```


### Example 4: Force Overwrite Existing Files

```bash
python split_ai_answer.py response.txt -o ./myapp --force
```


### Example 5: Verbose Mode for Debugging

```bash
python split_ai_answer.py response.txt -o ./myapp -v
```

**Output:**

```
DEBUG: Reading from file: response.txt
DEBUG: Parsing file blocks...
DEBUG: Ensured output directory exists: ./myapp
INFO: Found 3 file(s) to process
INFO: Created: ./myapp/main.py
DEBUG: Validated path: main.py
DEBUG: Created directory: ./myapp/utils
INFO: Created: ./myapp/utils/helpers.py
...
```


### Example 6: Quiet Mode (Errors Only)

```bash
python split_ai_answer.py response.txt -o ./myapp -q
```

Only shows output if there are errors.

***

## 📝 Input Format Specification

The AI response must contain file blocks in this exact format:

```text
FILE path/to/file.py
========================================
<full file content>
========================================
END FILE

FILE another/file.js
========================================
<full file content>
========================================
END FILE
```


### Format Rules

- **Header line:** `FILE <relative/path/to/file>`
- **Separator:** Line with ≥10 identical `=` or `-` characters
- **Content:** Everything between the two identical separators
- **Footer:** `END FILE` on its own line
- **Paths:** Must be relative (no `..` or absolute paths allowed)


### Valid Example

```text
FILE src/main.py
========================================
#!/usr/bin/env python3

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
========================================
END FILE

FILE src/utils/config.py
========================================
CONFIG = {
    "version": "1.0.0",
    "debug": True
}
========================================
END FILE
```


***

## 🔒 Security Features

The script includes several security validations:

- ✅ **Path traversal prevention** - Blocks paths containing `..`
- ✅ **Absolute path blocking** - Rejects paths starting with `/` or `\`
- ✅ **Directory escape detection** - Ensures files stay within output directory
- ✅ **Safe overwrites** - Prompts before overwriting (unless `--force`)

***

## 🐛 Troubleshooting

### "Separator not found after FILE"

**Cause:** Missing or invalid separator line after `FILE` declaration.

**Solution:** Ensure there's a line with at least 10 `=` or `-` characters after the `FILE` line.

### "Expected 'END FILE' after file"

**Cause:** Missing `END FILE` marker or wrong format.

**Solution:** Each file block must end with exactly `END FILE` on its own line.

### "Path escapes output directory"

**Cause:** File path tries to write outside the specified output directory.

**Solution:** Use only relative paths without `..` or leading `/`.

### "No file blocks found in input"

**Cause:** Input file doesn't contain properly formatted file blocks.

**Solution:** Check that your AI response follows the exact format specification above.

### Copy/paste indentation issues

**Cause:** Some chat apps (e.g., Perplexity) mangle indentation when you copy code fragments.

**Solution:** Ask the model to wrap every code block in a raw text fence, for example `text""" <code here> """`, so whitespace stays intact after pasting.
***

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints for new functions
- Update tests for new features
- Update documentation as needed

***

## 📄 License

Distributed under the MIT License. See `LICENSE` file for details.

***

## 👤 Author

[@avantyur1st](https://github.com/avantyur1st)

***

## 🙏 Acknowledgments

- Inspired by the need to quickly scaffold projects from AI-generated code
- Thanks to all AI models that help developers generate better code faster
- Built with Python's excellent standard library

***

## 📊 Project Statistics

- **Lines of Code:** ~250
- **Dependencies:** 0 (only stdlib)
- **Python Version:** 3.8+
- **License:** MIT
- **Status:** Production Ready

***

<div align="center">

**⭐ If this project helped you, please consider giving it a star!**

</div>

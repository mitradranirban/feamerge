# feamerge
## Merge Adobe feature files into a single variable feature file
`feamerge` is a tool designed to solve the challenge of compiling designspace files with varying OpenType features. It automates the preprocessing of UFO feature files—expanding kerning and positioning groups—before merging them into a valid variable font feature file.

### 🔄 New Workflow
Previously, this process required running three separate scripts manually. With version 0.1.1, these have been unified into a single command:

1. Break Kerning Groups: Expands @group definitions into individual glyph-to-glyph pairs.

2. Break Positioning Groups: Expands group references in mark, abvm, and blwm statements into single-glyph anchor rules.

3. Intelligent Merge: Combines the expanded features from all masters in the designspace into variable font syntax (e.g., pos A A (wght=400:10 wght=900:20)).

### 🚀 Installation
The package now supports standard Python installation, which automatically sets up the feamerge command in your environment.

```
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the package and dependencies
pip install .
```
### 💻 Usage
#### Command Line (Recommended)
You no longer need to call individual Python files. Simply use the feamerge command:

```
feamerge path/to/YourFont.ufo MyFont.designspace variable_features.fea
```
#### Programmatic Usage
If you still wish to use the combiner logic directly in a script:
```
from feamerge.combine_features import VariableFeatureCombiner

combiner = VariableFeatureCombiner("path/to/font.designspace")
combiner.save_combined_features("output/variable_features.fea")
```
### 📜 Changelog
**v0.1.2**

Package Restructuring: Moved all scripts into the feamerge/ package directory for proper bundling.

Unified CLI: Added a single feamerge entry point to run the entire preprocessing and merging sequence automatically.

Improved Metadata: Consolidated project configuration into pyproject.toml.

Version Bump: Updated version to 0.1.1.

**v0.1.0**

Initial release with separate scripts for kerning expansion and feature merging.

### Key Features
* _Designspace Integration_: Handles both absolute and relative paths for UFO source references.

* _Variable Font Syntax_: Generates coordinate:value pairs for positioning rules.

* _Intelligent Merging_: Deduplicates glyph classes and maintains OpenType features across masters.
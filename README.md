
# feamerge

## Python scripts to merge all feature fea file in a designspace in common variable feature.fea file

This is an attempt to vibe code a solution to problem that fontc can not compile designspace with varying Opettype features.

### Key Features
#### Designspace Integration
The script uses fontTools.designspaceLib.DesignSpaceDocument to read the designspace file and extract all UFO source references. It handles both absolute and relative paths correctly.

#### UFO Feature Reading
Using fontTools.ufoLib2.Font, the script opens each UFO and reads the features.fea content [1] [2]. This provides access to the complete feature definitions from each master.

#### Variable Font Syntax Generation
The script generates the variable font positioning syntax you requested:

* Combines glyph classes from all masters

* Creates positioning rules with coordinate:value pairs

* Supports both regular and enum positioning statements

* Formats output like: 

` pos A A (wdth=100,wght=400:10 wdth=100,wght=900:20)`

#### Intelligent Merging
* Glyph Classes: Merges and deduplicates glyph classes across masters

* Kerning Values: Collects kerning values from each master and formats them with proper axis coordinates

* Feature Preservation: Maintains other OpenType features beyond kerning

### Usage
#### Command Line
```
python3 combine_features.py MyFont.designspace variable_features.fea
```
#### Programmatic Usage
python
```
from combine_features import VariableFeatureCombiner

combiner = VariableFeatureCombiner("path/to/font.designspace")
combiner.save_combined_features("output/variable_features.fea")
```
### Installation Requirements
* Create a python virtual environmet and activate it
```
python3 -m venv venv
./venv/bin/activate
```
* Install the required fontTools components:

```
pip install fonttools[ufo]
```
This script provides a solid foundation for combining UFO feature files into variable font syntax. You may need to extend the parsing logic for more complex feature definitions or specific kerning patterns in your font sources. The feaLib module can also be used for more sophisticated feature file manipulation if needed.[3]

#### References
1. [Fonttools UFOlib Documentaion](https://fonttools.readthedocs.io/en/latest/ufoLib/index.html)
2. [Designspace specification](https://fonttools.readthedocs.io/en/latest/designspaceLib/python.html)
3. [Fonttools Fealib Documentation](https://fonttools.readthedocs.io/en/latest/feaLib/index.html)

## Preprocessing Python scripts

Two preprocesessing scripts are added to the repository for modifying feature.fea files before applying the features.

### A script to break kerning groups:

* Reads the feature.fea file from a UFO directory,

* Detects the kerning groups definitions,

* Expands groups in kerning pairs into individual glyph-to-glyph pairs,

* Outputs a new feature.fea file with only individual kerning pairs, no groups.

This will facilitate feamerge merging by having a consistent non-grouped kerning state in the UFO feature file.

To use the sript run

`python3 break_groups_in_fea.py path/to/YourFont.ufo`

### A script to break other positioning groups 

* Reads a UFO's feature.fea file,

* Parses groups defined as @GroupName = [...];

* Finds mark, abvm, blwm positioning statements containing group references,

* Replaces group references with all individual glyph references,

* Outputs a new feature.fea with expanded single-glyph anchor positioning rules (no group references) for these mark positioning tables.

It will write an expanded feature file (features_expanded_mark.fea) with all group references in mark positioning lines expanded to single glyphs, facilitating consistent merging or further processing.

To use the script run

`python3 break_groups_in_mark_pos.py path/to/font.ufo`

After the groups are broken into induvidual glyph entries they can be merged 
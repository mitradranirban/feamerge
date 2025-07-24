
# feamerge

## A python script to merge all feature fea file in a designspace in common variable feature.fea file

This is an attempt to vibe code a solution to problem that fontc can not compile designspace with varying Opettype features. 

### Key Features
#### Designspace Integration
The script uses fontTools.designspaceLib.DesignSpaceDocument to read the designspace file and extract all UFO source references. It handles both absolute and relative paths correctly.

#### UFO Feature Reading
Using fontTools.ufoLib2.Font, the script opens each UFO and reads the features.fea content ^1^ ^2^. This provides access to the complete feature definitions from each master.

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
This script provides a solid foundation for combining UFO feature files into variable font syntax. You may need to extend the parsing logic for more complex feature definitions or specific kerning patterns in your font sources. The feaLib module can also be used for more sophisticated feature file manipulation if needed.^3^

#### References 
1. [Fonttools UFOlib Documentaion](https://fonttools.readthedocs.io/en/latest/ufoLib/index.html)
2. [Designspace specification](https://fonttools.readthedocs.io/en/latest/designspaceLib/python.html)
3. [Fonttools Fealib Documentation](https://fonttools.readthedocs.io/en/latest/feaLib/index.html)
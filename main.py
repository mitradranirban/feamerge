#!/usr/bin/env python3
"""
Script to combine feature.fea files from UFOs referenced in a designspace
into a single variable features.fea file with proper variable font syntax.
"""

import os
import re
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib2 import Font
from collections import defaultdict, OrderedDict


class VariableFeatureCombiner:
    def __init__(self, designspace_path):
        self.designspace_path = designspace_path
        self.designspace = DesignSpaceDocument.fromfile(designspace_path)
        self.masters_data = {}
        self.combined_classes = {}
        self.combined_features = {}
        self.axis_mappings = {}
        
        # Extract axis information
        for axis in self.designspace.axes:
            self.axis_mappings[axis.tag] = {
                'name': axis.name,
                'min': axis.minimum,
                'default': axis.default,
                'max': axis.maximum
            }
    
    def load_ufo_features(self):
        """Load feature.fea content from all UFO masters"""
        for source in self.designspace.sources:
            if source.path:
                ufo_path = source.path
            elif source.filename:
                # Handle relative paths
                designspace_dir = os.path.dirname(self.designspace_path)
                ufo_path = os.path.normpath(os.path.join(designspace_dir, source.filename))
            else:
                continue
            
            if not os.path.exists(ufo_path):
                print(f"Warning: UFO not found at {ufo_path}")
                continue
            
            # Load UFO using fontTools
            try:
                font = Font.open(ufo_path)
                features_content = font.features.text if font.features.text else ""
                
                # Store master data with location coordinates
                location = source.location or {}
                self.masters_data[source.filename or source.path] = {
                    'location': location,
                    'features': features_content,
                    'font': font
                }
                
            except Exception as e:
                print(f"Error loading UFO {ufo_path}: {e}")
    
    def parse_glyph_classes(self, features_text):
        """Extract glyph class definitions from feature text"""
        classes = {}
        class_pattern = r'@([a-zA-Z0-9_.]+)\s*=\s*\[(.*?)\];'
        
        for match in re.finditer(class_pattern, features_text, re.DOTALL):
            class_name = match.group(1)
            glyph_list = [g.strip() for g in match.group(2).split() if g.strip()]
            classes[class_name] = glyph_list
        
        return classes
    
    def parse_kern_pairs(self, features_text):
        """Extract kerning pairs from feature text"""
        kern_pairs = []
        
        # Look for kern feature block
        kern_pattern = r'feature\s+kern\s*\{(.*?)\}\s*kern;'
        kern_match = re.search(kern_pattern, features_text, re.DOTALL)
        
        if kern_match:
            kern_block = kern_match.group(1)
            
            # Parse positioning statements
            pos_pattern = r'(enum\s+)?pos\s+([^(;]+?)(?:\s*\(([^)]*)\))?\s*:\s*([^;]+);'
            
            for match in re.finditer(pos_pattern, kern_block):
                is_enum = match.group(1) is not None
                glyphs = match.group(2).strip()
                conditions = match.group(3)
                value = match.group(4).strip()
                
                kern_pairs.append({
                    'enum': is_enum,
                    'glyphs': glyphs,
                    'conditions': conditions,
                    'value': value
                })
        
        return kern_pairs
    
    def merge_classes(self):
        """Merge glyph classes from all masters"""
        all_classes = defaultdict(set)
        
        for master_name, master_data in self.masters_data.items():
            classes = self.parse_glyph_classes(master_data['features'])
            for class_name, glyphs in classes.items():
                all_classes[class_name].update(glyphs)
        
        # Convert sets back to sorted lists
        self.combined_classes = {
            name: sorted(list(glyphs)) 
            for name, glyphs in all_classes.items()
        }
    
    def format_variable_value(self, master_values):
        """Format positioning values with variable font syntax"""
        if not master_values:
            return "0"
        
        # Build coordinate:value pairs
        coordinate_values = []
        for master_name, value in master_values.items():
            if master_name in self.masters_data:
                location = self.masters_data[master_name]['location']
                
                # Format location coordinates
                coords = []
                for axis_tag, axis_value in location.items():
                    coords.append(f"{axis_tag}={axis_value}")
                
                if coords:
                    coord_str = " ".join(coords)
                    coordinate_values.append(f"{coord_str}:{value}")
        
        return " ".join(coordinate_values) if coordinate_values else "0"
    
    def combine_kern_features(self):
        """Combine kerning features with variable font syntax"""
        # Collect all unique kern pairs across masters
        all_kern_pairs = defaultdict(dict)
        
        for master_name, master_data in self.masters_data.items():
            kern_pairs = self.parse_kern_pairs(master_data['features'])
            
            for pair in kern_pairs:
                pair_key = (pair['glyphs'], pair.get('enum', False))
                
                # Extract numeric value (simplified - you may need more robust parsing)
                value_match = re.search(r'(-?\d+)', pair['value'])
                if value_match:
                    numeric_value = int(value_match.group(1))
                    all_kern_pairs[pair_key][master_name] = numeric_value
        
        # Generate variable kern feature
        kern_statements = []
        for (glyphs, is_enum), master_values in all_kern_pairs.items():
            variable_value = self.format_variable_value(master_values)
            
            if variable_value != "0":
                enum_prefix = "enum " if is_enum else ""
                kern_statements.append(f"    {enum_prefix}pos {glyphs} ({variable_value});")
        
        return kern_statements
    
    def generate_variable_features(self):
        """Generate the complete variable features.fea content"""
        output_lines = []
        
        # Add header comment
        output_lines.append("# Variable features.fea generated from designspace masters")
        output_lines.append("# Combined from UFO sources in designspace")
        output_lines.append("")
        
        # Add glyph class definitions
        if self.combined_classes:
            output_lines.append("# Glyph class definitions")
            for class_name, glyphs in self.combined_classes.items():
                glyph_list = " ".join(glyphs)
                output_lines.append(f"@{class_name} = [{glyph_list}];")
            output_lines.append("")
        
        # Add kern feature with variable syntax
        kern_statements = self.combine_kern_features()
        if kern_statements:
            output_lines.append("feature kern {")
            output_lines.extend(kern_statements)
            output_lines.append("} kern;")
            output_lines.append("")
        
        # Add other features (simplified - you may want to handle these more carefully)
        other_features = set()
        for master_data in self.masters_data.values():
            features_text = master_data['features']
            
            # Extract other feature blocks (excluding kern)
            feature_pattern = r'feature\s+(\w+)\s*\{.*?\}\s*\1;'
            for match in re.finditer(feature_pattern, features_text, re.DOTALL):
                feature_name = match.group(1)
                if feature_name != 'kern':
                    other_features.add(match.group(0))
        
        # Add other features
        for feature in other_features:
            output_lines.append(feature)
            output_lines.append("")
        
        return "\n".join(output_lines)
    
    def save_combined_features(self, output_path):
        """Save the combined variable features.fea file"""
        self.load_ufo_features()
        self.merge_classes()
        
        variable_features_content = self.generate_variable_features()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(variable_features_content)
        
        print(f"Variable features.fea saved to: {output_path}")


def main():
    """Main function with example usage"""
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python combine_features.py <designspace_file> <output_features.fea>")
        print("\nExample:")
        print("python combine_features.py MyFont.designspace variable_features.fea")
        return
    
    designspace_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(designspace_path):
        print(f"Error: Designspace file not found: {designspace_path}")
        return
    
    try:
        combiner = VariableFeatureCombiner(designspace_path)
        combiner.save_combined_features(output_path)
        
        print("✓ Successfully combined features from all UFO masters")
        print(f"✓ Masters processed: {len(combiner.masters_data)}")
        print(f"✓ Classes combined: {len(combiner.combined_classes)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


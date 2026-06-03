import subprocess
import sys
import os
import argparse
from fontTools.designspaceLib import DesignSpaceDocument

def main():
    parser = argparse.ArgumentParser(description="Merge Adobe feature files sequentially.")
    parser.add_argument("ufo_path", help="Path to the UFO file")
    parser.add_argument("designspace", help="Path to the .designspace file")
    parser.add_argument("output_fea", help="Name of the output .fea file")
    
    args = parser.parse_args()

    designspace_path = args.designspace
    if not os.path.exists(designspace_path):
        print(f"Error: Designspace file not found: {designspace_path}")
        sys.exit(1)
        
    ds = DesignSpaceDocument.fromfile(designspace_path)
    ufo_paths = []
    designspace_dir = os.path.dirname(os.path.abspath(designspace_path))
    
    for source in ds.sources:
        if source.path:
            ufo_paths.append(os.path.abspath(source.path))
        elif source.filename:
            ufo_paths.append(os.path.abspath(os.path.join(designspace_dir, source.filename)))
            
    # Include args.ufo_path in the list if not already there
    abs_ufo_path = os.path.abspath(args.ufo_path)
    if abs_ufo_path not in [os.path.abspath(p) for p in ufo_paths]:
        ufo_paths.append(abs_ufo_path)

    for ufo in ufo_paths:
        # Step 1: break_groups_in_fea.py
        print(f"--- Step 1: Breaking groups in {ufo} ---")
        subprocess.run([sys.executable, "-m", "feamerge.break_groups_in_fea", ufo], check=True)

        # Step 2: break_groups_in_mark_pos.py
        print(f"--- Step 2: Breaking mark positioning in {ufo} ---")
        subprocess.run([
            sys.executable, "-m", "feamerge.break_groups_in_mark_pos", 
            ufo, "features_expanded.fea", "features_expanded_mark.fea"
        ], check=True)

    # Step 3: combine_features.py
    print(f"--- Step 3: Combining into {args.output_fea} ---")
    subprocess.run([sys.executable, "-m", "feamerge.combine_features", args.designspace, args.output_fea], check=True)

    print("\nDone! Variable features generated successfully.")


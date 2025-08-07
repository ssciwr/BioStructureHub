
#!/bin/bash
# AlphaFold 3 - Part 1: Alignment (CPU only)

# Load software module 
module load bio/alphafold/3.0.1

# Run with option --norun_inference to generate Multiple Sequence Alignments (MSAs) and templates
python $ALPHAFOLD_BIN_DIR/run_alphafold.py \
    --json_path=afold_test/input.json \
    --db_dir=$ALPHAFOLD_DATABASES \
    --model_dir=af3models  \
    --output_dir=afold_test/output  \
    --norun_inference

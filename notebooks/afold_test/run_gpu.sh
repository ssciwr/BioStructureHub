
#!/bin/bash
# AlphaFold 3 - Part 2: Inference (GPU required)

# Load software module 
module load bio/alphafold/3.0.1

# Run with option --norun_data_pipeline for featurisation and model inference
python $ALPHAFOLD_BIN_DIR/run_alphafold.py \
    --json_path=/home/christine/Sandbox/BioStructureHub/notebooks/afold_test/output/test/test_data.json \
    --db_dir=$ALPHAFOLD_DATABASES \
    --model_dir=/home/christine/Sandbox/BioStructureHub/notebooks/af3models \
    --output_dir=/home/christine/Sandbox/BioStructureHub/notebooks/afold_test/output_gpu \
    --norun_data_pipeline


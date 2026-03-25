
#!/bin/bash

# Load software module 
module load bio/rfdiffusion/1.1.0

# Create directories in your working directory
mkdir -p /home/hd/hd_hd/hd_aq354/protein_design_w_RFDiffusion/inputs
mkdir -p /home/hd/hd_hd/hd_aq354/protein_design_w_RFDiffusion/outputs
mkdir -p /home/hd/hd_hd/hd_aq354/protein_design_w_RFDiffusion/schedules

# Copy input PDB file to your working directory
cp $RFDIFFUSION_HOME/examples/input_pdbs/5TPN.pdb /home/hd/hd_hd/hd_aq354/protein_design_w_RFDiffusion/inputs/

# Run RFDiffusion 
HYDRA_FULL_ERROR=1  $RFDIFFUSION_HOME/scripts/run_inference.py \
  inference.input_pdb=/home/hd/hd_hd/hd_aq354/protein_design_w_RFDiffusion/inputs/5TPN.pdb \
  inference.output_prefix=/home/hd/hd_hd/hd_aq354/protein_design_w_RFDiffusion/outputs/motifscaffolding \
  inference.schedule_directory_path=/home/hd/hd_hd/hd_aq354/protein_design_w_RFDiffusion/schedules \
  inference.num_designs=3 \
  'contigmap.contigs=[10-40/A163-181/10-40]'

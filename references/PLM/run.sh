
#!/bin/bash

module load devel/miniforge/24.9.2
conda activate /mnt/sds-hd/sd25g005/PLMinteract

! torchrun --nproc_per_node=1 -m PLMinteract inference_PPI \
--seed 2 \
--batch_size_val 1 \
--test_filepath PLM_interact/test.csv \
--resume_from_checkpoint /mnt/sds-hd/sd25g005/PLMinteract/download_huggingface_folder/PLM-interact-650M-humanV11/pytorch_model.bin \
--output_filepath PLM_interact/output/ \
--offline_model_path /mnt/sds-hd/sd25g005/PLMinteract/download_huggingface_folder/offline/ \
--model_name esm2_t33_650M_UR50D \
--embedding_size 1280 --max_length 1520

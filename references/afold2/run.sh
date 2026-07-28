
#!/bin/bash
# AlphaFold 2 

# load software module 
module load bio/alphafold/2.3.2

# start program
run_alphafold.sh -d $ALPHAFOLD_DATABASES \
    -o /home/hd/hd_hd/hd_aq354/alphafold2/output  \
    -f /home/hd/hd_hd/hd_aq354/alphafold2/insulin.fasta  \
    -t 2020-05-14 \
    -c full_dbs \
    -m multimer
    

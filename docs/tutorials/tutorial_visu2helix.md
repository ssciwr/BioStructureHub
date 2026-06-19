# Transition from bwVisu to bwForCluster Helix

Welcome to the bwVisu to Helix transitioning tutorial! 
While this tutorial can be used for all of the methods covered in our bwVisu tutorial, we start with <a href="https://github.com/jwohlwend/boltz" target="_blank" rel="noopener">Boltz-2</a>

## Preparation: Get Access to Helix

The registration process to [bwForCluster Helix](https://wiki.bwhpc.de/e/Helix) is explained on the bwHPC website: [https://wiki.bwhpc.de/e/Registration/bwForCluster](https://wiki.bwhpc.de/e/Registration/bwForCluster)
Plan some time for the Rechenvorhaben to be processed before you start your calculations.

## Login to Helix

To login to the Helix cluster, you can follwo the [Login Tutorial](https://wiki.bwhpc.de/e/Registration/Login) on the bwHPC Wiki, and check the [extra information](https://wiki.bwhpc.de/e/Helix/Login) for Helix. You might find this [login example](https://wiki.bwhpc.de/e/Helix/Login#Login_Example) helpful.

Now you are in your `$HOME` directory, your space on the HPC cluster. To see which files and directories are in your `$HOME` directory you can use the [ls command](https://linuxize.com/post/how-to-list-files-in-linux-using-the-ls-command/). You will see the same files and directories as in the bwVisu file browser.

To change the directory from your home to any directory you see now, use the [cd command](https://linuxize.com/post/linux-cd-command/). Find your `$WORKDIR` that you created when following the [Boltz-2 tutorial](tutorial_Boltz_bwVisu.md). You can use the ls command again, to verify that all your previous files are here.

## Adapt the MSA Run File

In the tutorial, we first calculated the multi-sequence alignment (MSA) using MMseqs2 for each protein sequence. To do that, we wrote an input file, that we simply called `run_msa.sh`.
To look at the contents of the files, we need text editors. Choose your favourite from the [list](https://wvuhpc.github.io/2018-Lesson_1/03-text-editors/index.html) and look at the contents of `run_msa.sh`.

It should look like that:

```
#!/bin/bash

module load devel/miniforge/24.9.2
module load devel/cuda/12.8
conda activate /mnt/sds-hd/sd25g005/boltz

export PATH="/mnt/sds-hd/sd25g005/boltz/localcolabfold/colabfold-conda/bin:$PATH"

colabfold_search  \
    --db-load-mode 2 \
    --threads 96 \
    --use-env 0 \
    --gpu 1 \
    "{path to your input.fasta}" \
    "/mnt/sds-hd/sd25g005/boltz/localcolabfold" \
    "{path to your results}" \
```
This file loads relevant [modules](https://wiki.bwhpc.de/e/Environment_Modules) from the helix library. Then it activates the shared conda environment with all python packages provided by the Bio-Structure Hub. This shared environment is added to the `$PATH`, i.e. to the list of known directories to look for files to execute. Finally it runs the colabold search on your input file. This is the final program call, everything else is preparation so that this works flawlessly.

### Add Slurm Information

One thing that is missing here, is the information which GPU to use. In case of bwVisu, this is done by selecting a GPU when starting bwVisu (see [Boltz-2 tutorial, step 3](tutorial_Boltz_bwVisu.md#step-3-connect-to-bwvisu-and-start-jupyter)). That is because the Jupyter instance is started directly on the GPU you choose. 

Now with `ssh` acces to Helix, we have access to all the ressources that Helix has to offer (see list [here](https://wiki.bwhpc.de/e/Helix/Hardware)) the we need to add that information to our run file, so we end up using the ressources we want.

The ressoure allocation is done by [Slurm](https://wiki.bwhpc.de/e/Helix/Slurm). To use ressoures similar to bwVisu, we can change the start of our run file to:

```
#!/bin/bash
#SBATCH --partition=gpu-single
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --gres=gpu:A100:1,gpumem_per_gpu=40GB
#SBATCH --mem=8gb
```
This selects one GPU of type A100 with 40GB VRAM and 8GB RAM and allows your job to run for 20 minutes. Note that the calculation will be terminated once your allocated resources are exhausted. This is especially important for the time allocation.

### Add Workspace Information

The next thing we need to add to our file is a [workspace](https://wiki.bwhpc.de/e/Helix/Filesystems#Workspaces). In your home, you have 200 GB of space for your data, but your in a workspace you can store up to 10 TB of data. They provide structure to your projects, and once you are done you can store all the data on your group storage at [SDS@HD](https://www.urz.uni-heidelberg.de/en/service-catalogue/storage/sdshd-scientific-data-storage). 

Underneath the Slurm information, add the following to your file:
```
ws_allocate your_work_space 30
RESULTS_DIR=`ws_find your_work_space`
```
This creates a new workspace, called `your_work_space` (feel free to chose a more descriptive name) for 30 days. We can store the location of `your_work_space` in the variable `$RESULTS_DIR` to use it later when we call colabfold.

Now the final file should look like that:

```
#!/bin/bash
#SBATCH --partition=gpu-single
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --gres=gpu:A100:1,gpumem_per_gpu=40GB
#SBATCH --mem=8gb

ws_allocate your_work_space 30
RESULTS_DIR=`ws_find your_work_space`

module load devel/miniforge/24.9.2
module load devel/cuda/12.8
conda activate /mnt/sds-hd/sd25g005/boltz

export PATH="/mnt/sds-hd/sd25g005/boltz/localcolabfold/colabfold-conda/bin:$PATH"

colabfold_search  \
    --db-load-mode 2 \
    --threads 96 \
    --use-env 0 \
    --gpu 1 \
    "{path to your input.fasta}" \
    "/mnt/sds-hd/sd25g005/boltz/localcolabfold" \
    $RESULTS_DIR \
```
Now you can save it, and rename it to give it a `.slurm` ending, like `run_msa.slurm` to indicate that it is a run file with slurm information.

## Submit your Slurm Script

To start the calculation, type

``` sbatch run_msa.slurm ```

You should get a response telling you that the job was successfully submitted and the job id of your calculation. If it was not submitted successfully, you will get an error message that should tell you what is missing. Congratulations, you just submitted your first direct calculation!

You can check on your job by typing `squeue`, which shows you everything you submitted and whether it is running (`R`) or pending, i.e. waiting for ressources.

You also have a new log file in your directory, called `slurm-{job_id}.out`. This captures the output of the calculations, all progress and all errors that might occur. You can look at the log file and follow it as it is written by Slurm by typing `tail -f slurm-{job_id}.out`. Once you are done, press `Ctrl + C` to stop following the file.

Once the multisequence alignmemt is done, you should find the `.a3m` alignment file in the workspace. You can locate it by typing `ws_find your_work_space` and look at it by using `ls` or go there with `cd`. To get back to your home directory, you can use `cd` without a directory.

## Run Boltz

Now we will adapt the `run.sh` and `input.yaml` files that controls the Boltz inference calculations. Go to your `$WORKDIR` and look for the exact names of these files.

### Adapt the `.yaml` file

Open the `input.yaml` file from your bwVisu Tutorial calculation. It should look somewhat like this:

```
version: 1
sequences:
  - protein:
      id: [A] 
      sequence: {sequence}
      msa: {path to your a3m file}
```
Insert the path to your workspace and the name of your `.a3m` , as well as your sequence in the appropriate fields. Remember, all input options are documented in the [Boltz wiki](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md#input-format). Save and exit the `.yaml` file.

### Adapt the Boltz run file

Open the `run.sh` file

```
#!/bin/bash

module load devel/miniforge/24.9.2
module load devel/cuda/12.8
conda activate /mnt/sds-hd/sd25g005/boltz

boltz predict  {path to your .yaml } \
    --write_full_pae \
    --out_dir "{path to your results}"
```
Similar as before, we load relevant module, activate the conda environment, and finally run the calculation.
Now we need to add the same steps as before: the slurm control section and the workspace management.
Try following the same logic as before and compare to the full file below:

??? note "Click here to expand."
    ```
    #!/bin/bash
    #SBATCH --partition=gpu-single
    #SBATCH --ntasks=1
    #SBATCH --time=00:20:00
    #SBATCH --gres=gpu:A100:1,gpumem_per_gpu=40GB
    #SBATCH --mem=8gb

    RESULTS_DIR=`ws_find your_work_space`

    module load devel/miniforge/24.9.2
    module load devel/cuda/12.8
    conda activate /mnt/sds-hd/sd25g005/boltz

    boltz predict  {path to your .yaml } \
        --write_full_pae \
        --out_dir $RESULTS_DIR
    ```

    - note that we do not re-create the workspace, but just access it. You can fit multiple calculations in one workspace, no need to have multiples.

Save your run file and rename again to `.slurm`. Submit it using `sbatch`, and monitor using `squeue`.
The output files will again be in your workspace, which you can locate using `ws_find`.

To download the files, 

## After Your Calculation
Once you are done with your calculation(s) you need to store your output data. There are two options
- you can copy the files to your local computer using the scp command for blueprints check: [https://wiki.bwhpc.de/e/Data_Transfer/SCP](https://wiki.bwhpc.de/e/Data_Transfer/SCP).
- you can copy the files on a shared directory of the SDS@HD For more information see: [https://wiki.bwhpc.de/e/SDS@hd/Access#Access_from_a_bwHPC_Cluster](https://wiki.bwhpc.de/e/SDS@hd/Access#Access_from_a_bwHPC_Cluster)

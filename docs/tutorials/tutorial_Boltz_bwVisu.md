# Boltz2 on bwVisu

Welcome to the Boltz Tutorial for bwVisu! 

This tutorial will guide you through running Boltz on bwVisu. Please follow these steps carefully. Any feedback on the tutorial is welcome! Feel free to contact us!

### Step 1: Get access to bwVisu 

To start, get access to bwVisu via bwForCluster Helix or SDS. For more information, visit 

<a href="https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu" target="_blank" rel="noopener">https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu</a>

For technical questions regarding the high performance cluster, see <a href="https://bw-support.scc.kit.edu" target="_blank" rel="noopener">https://bw-support.scc.kit.edu</a>. Feel free to [contact us](../contact.md) for support.

### Step 2: Connect to bwVisu and Start Jupyter 

Go to <a href="https://bwvisu.bwservices.uni-heidelberg.de/" target="_blank" rel="noopener">https://bwvisu.bwservices.uni-heidelberg.de/</a> and log in with your credentials and one-time password. 

Choose Jupyter and start a new session. 

### Step 3: Prepare the Multisequence Alignment 

The first step of the structure prediction is a multi-sequence alignment (MSA). Boltz relies on external partner, such as the <a href="https://www.nature.com/articles/s41592-022-01488-1" target="_blank" rel="noopener">colabfold</a> server. To run Boltz on bwVisu, a precomputed MSA file for any given input sequence needs to be provided. 

![Screenshot](../images/tutorial/bwVisu_Boltz_MSA.png)
{: style="width:268px"} 

### Step 4: Prepare the Inference

Now we can use the Boltz model to run the inference and predict the structure.

For the inference step we need a GPU, so we need to request a GPU node on bwVisu. A list of available GPUs and their specifications is available at <a href="https://wiki.bwhpc.de/e/Helix/Hardware#Compute_Nodes" target="_blank" rel="noopener">https://wiki.bwhpc.de/e/Helix/Hardware#Compute_Nodes</a>, or in the table below.

![Screenshot](../images/tutorial/Helix_GPU.png)
<!--Cant I link this directly?-->

The GPU is selected byw "GPU Type". The memory of each GPU Type is specified in GPU Memory per GPU (GB). For this example we select one of the A40 GPUs. Larger jobs (= longer sequences, more chains) require more memory. To access these, it is suggested to run the job directly on the Helix cluster. We will prepare a tutorial for this shortly - feel free to contact us!

![Screenshot](../images/tutorial/bwVisu_GPU_Kernel.png)
<!--{: style="height:500px;width:750px"}-->

You also need to define the `Kernel Path` to the boltz kernel at `/mnt/sds-hd/sd25g005/boltzgen/share/jupyter/`. [Contact us](../contact.md) for access to this shared directory.

### Step 5: Set Up Your Diffusion Run Within the Notebook

 Open `Boltz_input.ipynb`. 

#### Set Environment Variables 

Link the output of the MSA prediction, and the project name given in the MSA input file 

    BOLTZ_WORKING_DIR = "boltz_test/"  

#### Write Input File 

First we prepare the `.yaml` input file that will be tell Boltz what to predict. 

More information and examples on how these files are structured can be found in the <a href="https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md#yaml-format" target="_blank" rel="noopener">Boltz github</a>.

Important parameters in the input file are the `name`, `sequence` and `id`, as well as the `msa` path that needs to point to the precalculated MSA. Upon executing this cell, the input file will be written to your working directory. 

Remember the name of your input file as it is needed for [the analysis](#step-6-analyze-your-results). 

#### Write Run File  

Next we need to write the `run file`, which loads all relevant modules and handles the Boltz `.yaml` file in a program call. You do not need to change these parameters. A full list is available <a href="https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md#options" target="_blank" rel="noopener">here</a>. Only change the parameters if you know what you are doing.

#### Run the Prediction

Run the prediction by executing the next cell:

    os.system(f'echo "Running file {BOLTZ_RUN_PATH}"')
    os.system(f"bash {BOLTZ_RUN_PATH}")

This may take a few minutes, but eventually, you should see (among other things)... 

![Screenshot](../images/tutorial/bwVisu_Boltz_done.png)

#### Verify Output 

In the output directory, there should be multiple files. The .cif file includes the structure, the other files are used to determine the quality of the prediction. 

![Screenshot](../images/tutorial/bwVisu_Boltz_output.png)
{: style="width:268px"}


### Step 6: Analyze your results

Open the second notebook called `Boltz_Confidence_Levels.ipynb` to get a summary of the models confidence levels. This notebook reads the confidence descriptions and renders its central information.

To find the files, you need the name of the input file of the Boltz run. In this example we used `input.yaml`, so the directory structure `input` are automatically created.

To visualize your predicted structures, download them to your computer and open the files with programs such as <a href="https://pymol.org/" target="_blank" rel="noopener">Pymol</a> or <a href="https://www.cgl.ucsf.edu/chimerax/" target="_blank" rel="noopener">ChimeraX</a>. To visualize the pIDDT in "classic" AlphaFold colors, use <a href="https://kpwulab.com/2023/03/09/color-alphafold2s-plddt/" target="_blank" rel="noopener">this</a> quick tutorial. This allows to visualize more and less confident areas of the predicted structure.
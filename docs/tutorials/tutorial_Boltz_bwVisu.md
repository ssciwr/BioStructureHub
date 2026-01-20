# Boltz2 on bwVisu

Welcome to the Boltz Tutorial for bwVisu! 

This tutorial will guide you through running Boltz on bwVisu. Please follow these steps carefully. Any feedback on the tutorial is welcome! Feel free to contact us!

### Step 1: Get access to bwVisu 

To start, get access to bwVisu via bwForCluster Helix or SDS. For more information, visit 

[https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu](https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu) 

For technical questions regarding the high performance cluster, see [https://bw-support.scc.kit.edu](https://bw-support.scc.kit.edu). Feel free to [contact us](/contact.md) for support.

### Step 2: Connect to bwVisu and Start Jupyter 

Go to [https://bwvisu.bwservices.uni-heidelberg.de/](https://bwvisu.bwservices.uni-heidelberg.de/ ) and log in with your credentials and one-time password. 

Choose Jupyter and start a new session. 

### Step 3: Prepare the Multisequence Alignment 

The first step of the structure prediction is a multi-sequence alignment (MSA). Boltz relies on external partner, such as the [colabfold](https://www.nature.com/articles/s41592-022-01488-1) server. To run Boltz on bwVisu, a precomputed MSA file for any given input sequence needs to be provided. 

![Screenshot](../images/tutorial/bwVisu_Boltz_MSA.png)
{: style="width:268px"} 

### Step 4: Prepare the Inference

Now we can use the Boltz model to run the inference and predict the structure.

For the inference step we need a GPU, so we need to request a GPU node on bwVisu. A list of available GPUs and their specifications is available at [https://wiki.bwhpc.de/e/Helix/Hardware#Compute_Nodes](https://wiki.bwhpc.de/e/Helix/Hardware#Compute_Nodes), or in the table below.

![Screenshot](../images/tutorial/Helix_GPU.png)
<!--Cant I link this directly?-->

The GPU is selected byw "GPU Type". The memory of each GPU Type is specified in GPU Memory per GPU (GB). For this example we select one of the A40 GPUs.

![Screenshot](../images/tutorial/bwVisu_GPU.png)
<!--{: style="height:500px;width:750px"}-->

Larger jobs (= longer sequences, more chains) require more memory. To access these, it is suggested to run the job directly on the Helix cluster. We will prepare a tutorial for this shortly - feel free to contact us!

### Step 5: Set Up Your Diffusion Run Within the Notebook

 Open `Boltz_input.ipynb`. 

#### Set Environment Variables 


Link the output of the MSA prediction, and the project name given in the MSA input file 

    BOLTZ_WORKING_DIR = "boltz_test/"  



#### Write Input File 

First we prepare the `.yaml` input file that will be tell Boltz what to predict. 

More information and examples on how these files are structured can be found in the [Boltz github](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md#yaml-format).

Important parameters in the input file are the `name`, `sequence` and `id`, as well as the `msa` path that needs to point to the precalculated MSA. Upon executing this cell, the input file will be written to your working directory. 

Remember the name of your input file as it is needed for [the analysis](#step-6-analyze-your-results). <!--the input file name directs the output folders!-->

#### Run Structure Prediction 

Run the structure prediction by executing the next cell: 

    ! CUDA_VISIBLE_DEVICES=0 boltz predict {BOLTZ_WORKING_DIR}/input.yaml --write_full_pae --out_dir {BOLTZ_WORKING_DIR}
		  

This may take a few minutes, but eventually, you should see... 

![Screenshot](../images/tutorial/bwVisu_Boltz_done.png)

#### Verify Output 

In the output directory, there should be multiple files. The .cif file includes the structure, the other files are used to determine the quality of the prediction. 

![Screenshot](../images/tutorial/bwVisu_Boltz_output.png)
{: style="width:268px"}


### Step 6: Analyze your results

Open the second notebook called `Boltz_Confidence_Levels.ipynb` to get a summary of the models confidence levels. This notebook reads the confidence descriptions and renders its central information.

To find the files, you need the name of the input file of the Boltz run. In this example we used `input.yaml`, so the directory structure `input` are automatically created.

To visualize your predicted structures, download them to your computer and open the files with programs such as [Pymol](https://pymol.org/) or [ChimeraX](https://www.cgl.ucsf.edu/chimerax/). To visualize the pIDDT in "classic" AlphaFold colors, use [this](https://kpwulab.com/2023/03/09/color-alphafold2s-plddt/) quick tutorial. This allows to visualize more and less confident areas of the predicted structure.
# Boltzgen on bwVisu

Welcome to the Boltzgen Tutorial for bwVisu!  

<a href="https://github.com/HannesStark/boltzgen" target="_blank" rel="noopener">Boltzgen</a> is an open-source model for structure generation of proteins, peptides and antibodies. This tutorial will guide you through running Boltzgen on bwVisu. Please follow these steps carefully. Any feedback on the tutorial is welcome! Feel free to [contact us](../contact.md)!


### Step 1: Get access to bwVisu 

To start, get access to bwVisu via bwForCluster Helix or SDS. For more information, visit 

<a href="https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu" target="_blank" rel="noopener">https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu</a> 

For technical questions regarding the high performance cluster, see <a href="https://bw-support.scc.kit.edu" target="_blank" rel="noopener">https://bw-support.scc.kit.edu</a>. Feel free to [contact us](../contact.md) for support.

### Step 2: Connect to bwVisu and Start Jupyter 

Go to <a href="https://bwvisu.bwservices.uni-heidelberg.de/" target="_blank" rel="noopener">https://bwvisu.bwservices.uni-heidelberg.de/</a> and log in with your credentials and one-time password. 

Choose Jupyter and start a new session. Now you can select the resources you need.

Boltzgen needs a GPU to run in the cluster. A list of available GPUs and their specifications is available at <a href="https://wiki.bwhpc.de/e/Helix/Hardware#Compute_Nodes" target="_blank" rel="noopener">https://wiki.bwhpc.de/e/Helix/Hardware#Compute_Nodes</a>, or in the table below.

![Screenshot](../images/tutorial/Helix_GPU.png)
<!--Cant I link this directly?-->

The GPU is selected byw "GPU Type". The memory of each GPU Type is specified in GPU Memory per GPU (GB). For this example we select one of the A40 GPUs. Larger jobs (= longer sequences, more chains) require more memory. To access these, it is suggested to run the job directly on the Helix cluster. Feel free to contact us, if you need assistance!

Choose the Kernel Path to Boltzen `/mnt/sds-hd/sd25g005/boltzgen/share/jupyter/`. [Contact us](../contact.md) for access to this shared directory.

![Screenshot](../images/tutorial/bwVisu_GPU_Kernel.png)
<!--{: style="height:500px;width:750px"}-->



Click on "Launch". This will bring you to a new screen showing your interactive sessions. Wait for your session to be ready, then click on "Connect to Jupyter". This brings you into a JupyterLab environment.


### Step 3: Set a Working Directory and Upload Files

Now we need to define a working directory. These will contain all files necessary for the tutorial. A new directory can be created using folder icon on the top left of the file browser:

![Screenshot](../images/tutorial/bwVisu_newDir.png){: style="height:111px;width:444px"}

Upload the notebooks from our <a href="https://github.com/ssciwr/BioStructureHub/tree/main/notebooks" target="_blank" rel="noopener">github</a> and the <a href="https://www.rcsb.org/structure/1G13" target="_blank" rel="noopener">1g13.cif</a> file by clicking on the upload button:

![Screenshot](../images/tutorial/bwVisu_upload.png){: style="height:111px;width:444px"}

After the upload, you can see the notebooks in the file browser on the left. 

![Screenshot](../images/tutorial/bwVisu_Boltzgen_files.png){: style="width:268px"} 

### Step 4: Open the Notebook and Start the Calculation

Open `Boltzgen.ipynb` and select the `boltzgen` kernel. You can verify the kernel in the top right corner of your JupyterLab instance:

![Screenshot](../images/tutorial/bwVisu_Boltzgen_kernel.png){: style="width:232px"} 

Now execute the cells in the notebook to start your Boltzgen run!


#### Verify Input

Before starting your Boltz prediction you should see the following files in your working directory:

![Screenshot](../images/tutorial/bwVisu_Boltzgen_input.png)
{: style="width:268px"}

#### Verify Output 

In the output directory, there should be multiple files. The intermediate directories will help you understand the reasoning. A detailed explanation can be found   <a href="https://github.com/HannesStark/boltzgen?tab=readme-ov-file#pipeline-output" target="_blank" rel="noopener">here</a>.

![Screenshot](../images/tutorial/bwVisu_Boltzgen_more_output.png)
{: style="width:268px"}

The best models are in`final_ranked_designs`:

![Screenshot](../images/tutorial/bwVisu_Boltzgen_output.png)
{: style="width:268px"}

To visualize your predicted structures, download them to your computer and open the files with programs such as <a href="https://pymol.org/" target="_blank" rel="noopener">Pymol</a> or <a href="https://www.cgl.ucsf.edu/chimerax/" target="_blank" rel="noopener">ChimeraX</a>. To visualize the pIDDT in "classic" AlphaFold colors, use <a href="https://kpwulab.com/2023/03/09/color-alphafold2s-plddt/" target="_blank" rel="noopener">this</a> quick tutorial. This allows to visualize more and less confident areas of the predicted structure.

If you need more assistance with the analysis, feel free to [contact us](../contact.md).

### References

<a href="https://www.biorxiv.org/content/10.1101/2025.11.20.689494v1" target="_blank" rel="noopener">https://www.biorxiv.org/content/10.1101/2025.11.20.689494v1</a>

<a href="https://github.com/HannesStark/boltzgen" target="_blank" rel="noopener">https://github.com/HannesStark/boltzgen</a>
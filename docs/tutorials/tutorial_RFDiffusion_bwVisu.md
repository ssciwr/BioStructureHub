# RFDiffusion on bwVisu

Welcome to the RFDiffusion Tutorial for bwVisu! 

### Step 1: Get access to bwVisu 

To start, get access to bwVisu via bwForCluster Helix or SDS. For more information, visit 

[https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu](https://www.urz.uni-heidelberg.de/en/service-catalogue/software-and-applications/bwvisu) 

For technical questions regarding the high performance cluster, see [https://bw-support.scc.kit.edu](https://bw-support.scc.kit.edu). Feel free to [contact us](/contact) for support.


### Step 2: Connect to bwVisu and Start Jupyter 

Go to [https://bwvisu.bwservices.uni-heidelberg.de/](https://bwvisu.bwservices.uni-heidelberg.de/ ) and log in with your credentials and one-time password. Please note that you need to be connected to Heidelberg University's VPN if you are connecting from outside the campus.

Choose Jupyter and start a new session. To use RFDiffusion, we need to request a GPU core of type A40 as shown below:

![Screenshot](../images/tutorial/bwVisu_GPU.png)
<!--{: style="height:500px;width:750px"}-->

Click on "Launch". This will bring you to a new screen showing your interactive sessions. Wait for your session to be ready, then click on "Connect to Jupyter". This brings you into a JupyterLab environment.

Upload the notebooks in (link) by clicking on the upload button:

![Screenshot](../images/tutorial/bwVisu_upload.png){: style="height:111px;width:444px"}

After the upload, you can see the notebooks in the file browser on the left.

Screenshot

### Step 3: Prepare Modules and Environments
Load the RFDiffusion module by clicking on the hexagon on the right and selecting rfdiffusion.
Open the notebook. Check if module list works by executing the first cells.
If the notebook was open before, restart the kernel.

![Screenshot](../images/tutorial/restart_kernel.png)
{: style="width:268px"}

### Step 4: Start the Calculation

Execute the steps in the notebook to start the calculation!
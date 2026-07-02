# Using Templates in Structure Prediction

Both AlphaFold3 and Boltz2 have the option to use an existing 3D structure as a template to guide the prediction. 

## Boltz2 
In the Boltz input, only a template `.cif` or `.pdb` file and a some information of the chain is needed. The program finds the residues cirectly. For more information see the [Boltz2 documentation on templates](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md#templates)


## AlphaFold3

For AlphaFold3 a list of incides in the query and template sequence is required, that defines maping from query resudyes to template residues. For more information see the [AlphaFold3 documentation on templates](https://github.com/google-deepmind/alphafold3/blob/main/docs/input.md#structural-templates).

If you want to use the template locally, only these lists are required. To use templates on the [AlphaFold3 server](https://alphafoldserver.com), a mapping file is required.

Both the list of indices and the mapping field can be created using our jupyter notebook : [AFold3_mapping.ipynb](../../notebooks/AFold3_mapping.ipynb).

This notebook does not need to be executed on bwVisu, but can run locally on your computer. Or conveniently in Google Colab.
<!--- add this link once tutorial goes live -->
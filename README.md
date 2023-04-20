# Scriptie_CoSEM
 
Here I present the Python model that I created during my thesis at the Delft University of Technology, in partial fullfillment of the requirements for the degree of MASTER OF SCIENCE in Complex Systems Engineering and Management.

The model provides an exhaustive search for the design of networks. The model was specifically cretaed for the design of networks in which a choice can be made between the conversion/reuse of existing infrastructure and the construction of new infrastructure. In my thesis, I applied my model to design hydrogen pipeline infrastructure in the Netherlands. My thesis can be found at: https://repository.tudelft.nl/islandora/search/W.%20Nijmeijer?collection=education 

In this Github folder, there are 2 seperate models and an example input file. The example input file provides an outline of what the necessary model inputs are and how these inputs can be fed into the model. The model titled "1. Determination reuse and capacities" can be used to determine on which routes the capapcity of the available existing infrastructure does not suffice and thus additional infrastructure needs to be realised to fullfill demand. In addition, this model can be used to determined the capacities of the different pipelines. These pipelines then are used as input for the model titled "2. Determination pareto fronts and analysis pareto fronts". This model calculates all the different possible variants for the realisation of the infrastructure on different supply and demand scenarios. Of these variants the pareto front is determined based on the principles of maximise the flow over the network and minimise the costs of the network.

More information about the model can be found in chapter 9 of my thesis. 

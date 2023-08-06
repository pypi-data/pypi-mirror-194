# Molecular Dynamics & Machine Learning (MDML)

This repository is for the graduation projrct for the Master in Data Science 
for Life Sciences at Hanze University of Applied Sciences.

Proteins play a vital role in many biological processes and are essential to the structure and function of cells. Dysfunctional proteins can lead to disease and studying them can aid in understanding the underlying cause of the disease and potentially developing treatments and medication. In this study, a custom Convolutional Neural Network (CNN) was used to analyze the active and inactive states of the EGFR protein, a key player in cancer. The CNN was able to identify key residues that define the active and inactive state of the protein, specifically the DFG-Asp motif, with 100% accuracy. Our methodology for image transformation represented the 3D coordinates of atoms in a protein as 2D images, which differs from existing methods in literature. The results of this study demonstrate the potential of using deep learning methods on MD simulation trajectories, but also highlight the need for careful evaluation of the used methods and their utility in order to ensure meaningful insights.

Student:          Stylianos Mavrianos, s.mavrianos@st.hanze.nl <br>
Supervisor:       Tsjerk Wassenaar,  t.a.wassenaar@pl.hanze.nl <br>
Daily supervisor: Vilacha Madeira R Santos, j.f.vilacha@rug.nl <br>

## Research questions
1. Assess whether a Convolutional Neural Networks (CNN) classification approach is useful and relevant in the field of MD.
2. Is it possible to predict long term simulations from sort term ones? 
3. How short is short enough? 

## Requirements

- Python 3.8.10
- Numpy
- MatplotLib
- PLotly
- Scikit-learn
- Tensorflow
- Keras
- MDAnalysis
- cv2
- yaml

## Setup

1. Clone the repository to your local machine:

```git clone https://github.com/StevetheGreek97/MD_ML.git```

2. Create a new environment:

``` virtualenv MD_ML```

3. Install the required packages:

```pip install -r requirments.txt```

4. Example tutorials for each module are in the Examples folder. There are all jupyter notebooks. 

## Usage

The pipeline consists of three modules: Preprocessing.py, Machinelearning.py and Mapping.py.

 To get started, simply configure a yaml configuration file (conf.yml) that includes:
1. the 'masterpath' to a folder containing subfolders for each classification state (e.g., active, inactive state) -> str

Each subfolder should contain a .pdb and .xtc file for the corresponding state.

```
< EGFR >
    |
    |--data 
    |    |  
    |    |
    |    |--active
    |    |     |
         |     |--topology file (.pdb)
         |     |
         |     |--coordinates file (.xtc)
         |
         |--inactive
               |
               |--topology file (.pdb)
               |
               |--coordinates file (.xtc)
```

2. a 'savingpath' that all the results with be saved. -> str

3. 'downsampled_to' how many image should be created for each state -> int

```
downsample_to: 1659
masterpath: /path/to/data/
savepath: /path/to/save

```
The final output includes a series of down-sampled images, a prefomance img, a confusion matrix, a saliency map, a .txt file listing important residues, and a .pdb file with b-factor information showing the important residues. 
```
< output >
    |
    |-- imgs 
    |     |
    |     |-- active
    |     |     |
    |     |     |-- active_X.jpg    # The down-sampled active trajectory transcribed in RGB values
    |     |
    |     |-- inactive
    |     |     |
    |           |-- inactive_X.jpg  # The down-sampled inactive trajectory transcribed in RGB values
    |     
    |-- models
    |     |
    |     |-- model.h5               # The trained model 
    |
    |-- performance
    |     |
    |     |-- peformancne.jpg        # An image of the model's performance (locc, accuracy)
    |     |-- confusion_matrix.jpg   # An image of the confusion matrix of the model 
    |
    |-- results
    |     |
    |     |-- inactive.txt           # The important residues for the inactive state
    |     |-- inactive.pdb           #  b-factor information showing the important residues for the inactive state
    |     |-- sal_map_inactive.jpg   # The saliency map of the inactive state
          |-- active.txt             # The important residues for the active state
          |-- active.pdb             #  b-factor information showing the important residues for the active state
          |-- sal_map_active.jpg     # The saliency map of the active state
          |   
    
```
In order to run the pipeline simply run this code:
```
python3 main.py -c path/to/confg.yml
```
Alternatevly you can run the three modules separately. They also serve as checkpoints.

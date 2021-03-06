# DynamicModels

## Libraries Required:
- igraph
- numpy
- matplotlib
- powerlaw.py

## Installations required:
### Igraph:
```
  pip install python-igraph
```
For more information please visit http://igraph.org/python/
 
### numpy:
Most of the recent python versions obtain numpy library. For more information please visit https://www.scipy.org/scipylib/download.html
  
### matplotlib:
 ```
    python -m pip install -U pip
    python -m pip install -U matplotlib
``` 
For more information please visit https://matplotlib.org/users/installing.html
    
### powerlaw.py
```
    easy_install powerlaw
```
or
```
    pip install powerlaw
```
You might need to install mpmath
```
    pip install mpmath
``` 
For more information please visit https://github.com/jeffalstott/powerlaw
    
## Running the code:
To run the code you can do either one:
- via terminal/shell by getting into the directory of the code then 
```
    python DynamicModel.py
```
watch it here (https://www.youtube.com/watch?v=PdDxDyJ1jAs)

- Open the code in a python IDE (like Pycharm, to download visit https://www.jetbrains.com/pycharm/download/)
then run the code. (whatch it here https://www.youtube.com/watch?v=OxoUVXRHVuI&feature=youtu.be)


Initially the number of steps are limited to 5000, you can change it by updating the variable "limit" on line 22.
(The execution time will be ~31 second 2.3 intel core i7, memory 16 GB), but this will be changed once the limit var is changed as well)

Once it finished the process it brings up another window including all 3 figures regarding the growth of number of nodes and edges plus the cumulative degree distribution.

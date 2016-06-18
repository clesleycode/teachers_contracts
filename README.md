# teachers contracts
This is the repo for code and documents related to the teachers unions project.

documents: drafts of slides and paper
code: includes code for merging data

Linkage.py
COMMAND LINE:

Linkage.py accepts four arguments, as follows:
Argument 0: Linkage.py Argument 1: Directory of files Argument 2: Education Data File Argument 3: Output filename

ALGORITHM:

The main begins by unzipping the given directory for data management later on, through the unzip() function. From there, the get-columns() function is called to retrieve the labels of each column for each file. This is to then find the most common labels across the files through the most-common() function. This result, set to the variable "result", will be used as the way of keeping track of the data.

After that, we go into the actual management of data. To begin, a dictionary (output) is initalized to keep track of all the data. From there, the code runs through every file, stripping all the relevant information and adding it to the dictionary as the relevant data is found.

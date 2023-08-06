## Statistical Distributions package

Distributions package functionality
Notes for beginners- the class has an init method for instantiating an object with 3 attributes- mean, standard devation (with default values) and an empty list for storing data.
* Read in the dataset
* Calculate mean
* Calculate standard deviation
* Plot normalized histogram using matplotlib
* Plot probability density function
* Add two distributions


### Files

The package consists of a subfolder called distributions, which is the name of the Python package.
Inside the distributions folder, you have:
* The Gaussiandistribution.py file.
* The Generaldistribution.py file.
* The Binomialdistribution.py file.
* The __init__.py file, importing the 2 distributions

Additional package files:
* A setup.py file, a file needed for building Python packages with pip
* A test.py file, contains unit tests that can be run to help determine if the code is working properly.
This file can be run using the command **python test.py** in terminal.
* numbers.txt and numbers_binomial.txt, which are data files used as part of the unit tests.


### Installation 

If you decide to install your package on your local computer, you'll want to create a virtual environment. A virtual environment is a silo-ed Python installation apart from your main Python installation. That way you can install packages and delete the virtual environment without affecting your main Python installation.

Enter the following command to create a virtual environment: 
**'python -m venv venv_name'** where **'venv_name'** is the name you want to give to your virtual environment. You'll see a new folder appear with the Python installation named 'venv_name'.
In the terminal, enter **'source venv_name/bin/activate'**. You'll notice that the command line now shows (venv_name) at the beginning of the line to indicate you are using the venv_name virtual environment.
Enter **'pip install python_package/'**. That should install your distributions Python package.
Try using the package in a program to see if everything works!

### Use Case
Once the package is downloaded, use your terminal window to navigate into the statistics_package folder.

Enter the following:

**cd statistics_package**
**pip install .**

If everything is set up correctly, pip installs the distributions package into the workspace. You can then start the Python interpreter from the terminal by entering:

**python**

Then, within the Python interpreter, you can use the gaussian distribution package by entering the following:

from distributions import Gaussian

gaussian_one = Gaussian(25, 2)

gaussian_one.mean

gaussian_one + gaussian_one

## Update

If any modification is made to the package, it needs to be reinstalled using the following command:
**pip install --upgrade .**
This command uninstalls the package and then reinstalls the updated version.



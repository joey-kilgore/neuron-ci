![example workflow](https://github.com/joey-kilgore/neuron-ci/actions/workflows/neuron.yml/badge.svg)
# neuron-ci
Testing Continuous Integration with NEURON  
Checkout the [pages](https://joey-kilgore.github.io/neuron-ci/)

# Setting up CI on a NEURON repo
This repo has continuous integration for the following tasks
- Python unit tests (see /test)
- Compiling models (see /mod)
- Running test hoc scripts (see /sim)

## Steps for setup
Obviously, you will need some hoc and mod files to start with (the sample ones in this repo were taken from the [NEURON source](https://github.com/neuronsimulator/nrn/tree/master/src))  
From there we can setup our automation by starting with a blank workflow and adding the following step that will install everything we need.
```
# Runs installation needed for neuron and multithreading
- name: Setup Neuron
  run: |
    sudo apt install build-essential gcc make perl dkms git vim lib32ncurses5-dev libreadline-dev libx11-dev cmake mpich
    pip install neuron
```

### Compiling NMODL
Assuming you already have some sample model files (and have ensured they compile on your machine) then we simply need to add an additional step to our workflow
```
# Attempt to transpile and compile the models
- name: Build Models
  run: nrnivmodl ./mod
```
Make sure that you have this step prior to any further testing/integration that requires the model files to be loaded.

### Python Unit Tests
The unit tests are located in the test directory. **Make sure you create an __init\_\_.py file so that python recognizes the directory as a module**  
The unit test code is written in the following form.
```
import unittest
# any additional imports>

class <className>(unittest.TestCase):
  def setUp(self):
    # initialize self with any variables you need

  def <testMethod>(self):
    # call/test some function
    # at the end of the test use an assert method like the following
    #  to mark the test case
    # self.assertEqual(result,8)
```
[Checkout the unittest docs for more info](https://docs.python.org/3/library/unittest.html)  

In our NEURON tests we will have the following script to setup everything, and then additional test methods can be added
```
import unittest
import neuron

class TestNeuron(unittest.TestCase):
  def setUp(self):
    self.h = neuron.h
    # load any additional *.hoc files
```

Once the script is written we can add the following step to our workflow
```
# Run the unit tests
- name: Unit Testing
  run: python3 -m unittest <path to python file e.g. test/testCalculator.py>
```

With that done all of your unittests should automatically on whatever commit/branch structure you specify.

### Testing NEURON with MPI
Finally, we might want to run a multithreaded simulation test with hoc files.   
To do this we add the following step to our workflow  
```
# Attempt running neuron with mpi
- name: NEURON and MPI test
  run: mpiexec -n 2 nrniv -mpi <relative path to hoc file e.g. ./sim/test0.hoc>
```  

Because I was unable to find any notes on the threading availability of the machine when running a job, I kept the number of threads to 2. You might be able to play around with this and find what numbers work best.

## Additional Resources
For notes on install requirements see [tjbanks/easy-nrn-install](https://github.com/tjbanks/easy-nrn-install)  

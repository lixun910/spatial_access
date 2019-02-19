

# spatial_access: Compute travel times and spatial access metrics at scale

<table>
<tr>
  <td>Version</td>
  <td>
    0.1.6.7
  </td>
</tr>    
<tr>
  <td>Latest Release</td>
  <td>
    <a href="https://travis-ci.org/GeoDaCenter/spatial_access">
    <img src="https://travis-ci.org/GeoDaCenter/spatial_access.svg?branch=master" alt="travis build status" />
  </td>
</tr>

<tr>
  <td>Supported Operating Systems</td>
  <td>
       *nix, macOS
  </td>
</tr>
</table>


## Components of spatial_access :
----
spatial_access has two submodules:
- p2p: Generate many to many matrices with travel times for sets of coordinates. Use `walk` ,`bike` or `drive` network types (import `transit` from other sources), or get the distance in meters.
- Models: Contains a suite of models for calculating spatial accessibility to amenities.
 
To use this service as a ReST API, see: https://github.com/GeoDaCenter/spatial_access_api 

If you are a Windows user, instructions for installing Ubuntu on a virtual machine are at the bottom of the Readme.


Installation 
----
1. `brew install spatialindex` (MacOS) 
or `sudo apt-get install libspatialindex-dev` (Ubuntu 16.04+)
2. `pip3 install spatial_access`


Usage
---
See the iPython notebooks in docs/ for example usage.


### Instructions for building locally (only for developers):

- If updating Cython or C++ code (anything in spatial_access/adapters/ or spatial_access/src/)
you must install cython
- To regenerate .pyx files, from repository root run: `cython --cplus spatial_access/adapters/*.pyx`
- To install locally, from repository root run: `sudo python3 setup.py install `

### PyPi Maintenance
The package lives at: `https://pypi.org/project/spatial-access/`

When a branch is pulled into Master and builds/passes all unit tests,
Travis CI will automatically deploy the build to PyPi. 

Note: The version number in setup.py must be incremented from the last published
version on PyPi, or it will be rejected.

To update PyPi access credentials, see .travis.yml and follow the instructions at https://docs.travis-ci.com/user/deployment/pypi/
to generate a new encrypted password.

### Installing Ubuntu 18 LTS with dependencies from scratch (recommended for Windows users)

1. Follow the instructions at this link: https://linus.nci.nih.gov/bdge/installUbuntu.html to set up a virtual machine
2. `sudo apt-get update`
3. `sudo add-apt-repository universe`
4. `sudo apt-get -y install python3-pip`
5. Continue with Installation Instructions (above)

### Questions/Feedback?

lnoel@uchicago.edu or spatial@uchicago.edu

### Acknowledgments

Developed by Logan Noel at the University of Chicago's Center for Spatial Data Science (CSDS) with support from the Public Health National Center for Innovations (PHNCI), the University of Chicago, and CSDS. 



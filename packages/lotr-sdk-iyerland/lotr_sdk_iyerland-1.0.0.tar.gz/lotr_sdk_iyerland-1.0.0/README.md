# narayan-sdk
Python SDK that makes the `Lord Of the Rings` API accessible to other developers. The SDK covers only the movie endpoints:  
```
/movie
/movie/{id}
/movie/{id}/quote
```
Details of the design can be found in `DESIGN.md`

The name of the package is `lotr-sdk-iyerland` and published to Python Package Index (PyPi).

## Assumptions
Python3 & Pip3 are already installed on the target machine where this 
repo will be cloned and tested.

## How to test the code
After checking out the code and while in project folder, run:
```
python3 -m unittest
```


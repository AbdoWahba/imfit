# IMFIT

A Workout tracker based on OpenCV and Openpose for human pose detection model.

---

## Installation

### Dependencies
- Puthon 3
- tensorflow==1.4.1
- OpenCV
- Clone this repo
- `cd` to `{repo-path}/`
- `pip install requirements.txt`
- Build C++ libraries `swig -python -c++ pafprocess.i && python setup.py build_ext --inplace`

## Running GUI
```
    python design.py
```

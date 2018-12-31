# SpliceTools

SpliceTools is a program that splices together
WAV files for use in synthesizers. It uses code
from SMS Tools to perform some of its functions. 
The intent of the program is to splice together
a consonant and a vowel from a recorded voice, 
which means that multiple consonants can be spliced 
a vowel, reducing recording time.

## Dependencies

Splice tools has a few dependencies, all pip installable:

```python
pip install numpy scipy matplotlib pysoundfile
```

## Running the UI

```bash
cd UI
python main.py
```
## An Example

```bash
cd UI/scripts
python batchSplice.py
```

Will run a default splice on audio files provided

In python:

```python
from batchSplice import spliceBatch
spliceBatch(<firstFolder>, <secondFolder>, <outputDestination>)
```

## Graphing and Visual Representations

```python
from soundOps import getInfo
getInfo(<soundFile>, <minimumFrequencyBound>, <maximumFrequencyBound>)
```
<img src="https://github.com/alcofrisbas/SpliceTools/blob/master/images/getInfo.png" width="400">

```python
from soundOps import graphError
graphError(<soundFile>, <minimumFrequencyBound>, <maximumFrequencyBound>)
```

<img src="https://github.com/alcofrisbas/SpliceTools/blob/master/images/graphError.png" width="400">

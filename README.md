# SpliceTools

SpliceTools is a program that splices together
WAV files for use in synthesizers. In it, there
is some code from SMS TOOLS Library. The intent
of the program is to splice together a consonant
and a vowel from a recorded voice, which means
that multiple consonants can be spliced a vowel,
reducing recording time.

## Dependencies

Splice tools has a few dependencies, all pip installable:

```python
pip install numpy scipy matplotlib pysoundfile
```
## An Example

```bash
cd scripts
python batchSplice.py
```

Will run a default splice on audio files provided

In python:


```python
from batchSplice import spliceBatch
spliceBatch(<firstSound.wav>, <secondSound.wav>, <outputDestination>)
```

## Graphing and Visual Representations

```python
from soundOps import getInfo
getInfo(<soundFile>, <minimumFrequencyBound>, <maximumFrequencyBound>)
```

```python
from soundOps import graphError
graphError(<soundFile>, <minimumFrequencyBound>, <maximumFrequencyBound>)
```

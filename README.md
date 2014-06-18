KDD 2013 - Author Paper Identification Challenge (Track 1)
==========================================================

# Licence
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# System requirements
Tested on a 2.3Ghz Intel Core i5 with 16GB memory.
Python 2.7.5+ with the following packages:
 - scikit-learn
 - numpy
 - scipy
 - jellyfish
 - nltk

Install all packages in one batch with:

```
pip install -r requirements.txt
```

# Using the script
Put the original contest data (Author.csv, Conference.csv, Journal.csv, Paper.csv, PaperAuthor.csv, Train.csv, Test.csv, Valid.csv, ValidSolution.csv) in the folder data/. Then run model.py to start.


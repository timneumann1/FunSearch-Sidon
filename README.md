# Senior Thesis: Using Google DeepMind's FunSearch algorithm for the search for large complete Sidon sets in AG(n,3)

This repository serves as a proof of concept that the FunSearch algorithm introduced by DeepMind can be used to search for Sidon sets / 4-general sets over AG(n,3). 
[The original paper considered capsets (3-general sets) over AG(n,3).] In order to achieve this, we make a change to the specification file, blocking more points than in the capset case.
The code in this repository stems largely from the implementation that @jonppe built on top of the publicly available code published by DeepMind. It has been altered in some minor aspects, but most notably it 
includes an implementation of querying Google's Large Language Model code-bison.

In the following, we provide an overview of how to use the code in this repository to search for large Sidon sets. (Note that especially in terms of the container environment, there are multiple ways to achieve this. The below items are based on a working implementation on a macOS device.)

1. In order to use the Google code-bison LLM, you need a Google Cloud console profile to access the Vertex AI API. You can use an ordinary @gmail.com address to open a new project in the Google Cloud Console. At the time of writing, private users receive credit to spend on experimenting with the Cloud services. Once the project is created, you need to add a service account and create a key for it. The key can be downloaded in .json format (this file should be kept private).
2. Download Docker Desktop and open it. You see a panel with containers and images (so far empty), which will be initialized later.
3. On a local machine, choose a working directory and clone this repository, using the terminal command
```
git clone https://github.com/timneumann1/FunSearch-Sidon.git
```
After the repository has been cloned, enter the folder using 
```
cd FunSearch-Sidon 
```
and create a "data" folder using 
```
mkdir data
```
Also, add the .json file downloaded from the Google Cloud Account to the (existing) "files" folder.
4. Your .json file has randomized name, e.g., "phonic-silo-417508-fc2829b1d7ce.json". In the file "funsearch/__main__.py" (line 98), insert the first three alphanumeric parts of this name into the aiplatform.init() function and add your location (available locations can be retrieved from the Google LLM documentation), e.g., 
```
aiplatform.init(project="phonic-silo-417508", location="us-east4", credentials=credential)
```
Make sure that your input in line 98 matches the name of your .json file in the "files" folder.
5. If you want to make changes to the FunSearch algorithm, open the "funsearch/config.py" file and set parameters like the reset period (in seconds) or the backup period (in number of programs in database).
For changes in hyperparameters, you can set a temperature and other parameters in the file "funsearch/sampler.py" (line 40). The current configuration here is 
```
response = self.model.predict(prompt, temperature = 0.7, max_output_tokens = 1024, candidate_count = 1) 
```
and more parameters, e.g., the "top_p" parameter for Large Language Models, might be added here.
6. For prompt engineering and other changes to the specification file(s), you can make changes to the .py files in the "files" folder.
6. Now it is time to build the container. In order to do this, verify that Docker Desktop is running and enter the Terminal command
```
docker build -t funsearch .
```
The build takes some time for the first time. Once successfully completed, enter the container by entering
```
docker run -it -v ./data:/workspace/data funsearch
```
Now you are in the container environment "funsearch".
7. To run the FunSearch algorithm, enter the Terminal command 
```
funsearch run files/sidon_set_spec.py 7 --sandbox_type ExternalProcessSandbox --authen files/<YOUR .JSON FILE NAME>.json
```
Here, place the name of your .json file in the --authen argument. Note that we only evaluate Sidon sets in one dimension (n = 7) with this command. In the "files" folder, there is also the capset specification file, which can replace the Sidon set specification file, if desired.

Now the FunSearch experiment will repeatedly query the LLM and update the programs database.

Here are some remarks on this architecture as added by @jonppe:

**Note that in the last command we use the ExternalProcessSandbox that is not fully safe
but makes it a bit less likely that invalid code from LLM would break the search.**

**Alternatively, you can run the main Python process on a host computer outside of any container and let
the process build and run separate sandbox containers (still requires Podman/Docker).
This variant could be also used, e.g., in Colab quite safely since the environment is some kind of container itself.**

```
pip install .

funsearch run examples/cap_set_spec.py 11
```

**Currently, the search is only using single thread with no asyncio and is somewhat slow
for challenging tasks.**



---

The repository contains a number of sample problems that can be solved with FunSearch.
Currently, only the cap set problem (examples/cap_set_spec.py) has been written in the form that can be directly
used with the 'funsearch' executable.

This repository accompanies the publication

> Romera-Paredes, B. et al. [Mathematical discoveries from program search with large language models](https://www.nature.com/articles/s41586-023-06924-6). *Nature* (2023)

There are 6 independent directories:

- `cap_set` contains functions discovered by FunSearch that construct large cap
sets, and we also provide those cap sets in a numerical format for convenience.

- `admissible_set` contains functions discovered by FunSearch that construct
large admissible sets, and we also provide those admissible sets in a numerical
format for convenience.

- `bin_packing` contains heuristics discovered by FunSearch for online 1D bin
packing problems, and an evaluation suite to reproduce the results reported in
the paper.

- `cyclic_graphs` contains functions discovered by FunSearch that construct
large independent sets in strong products of cyclic graphs, and we also provide
those sets in a numerical format for convenience.

- `corner_free_sets` contains the discovered sets of indices, in numerical
format, satisfying the combinatorial degeneration constraints described for the
corners-free problem in the Supplementary Information.

- `implementation` contains an implementation of the evolutionary algorithm,
code manipulation routines, and a single-threaded implementation of the
FunSearch pipeline. It does not contain language models for generating new
programs, the sandbox for executing untrusted code, nor the infrastructure for
running FunSearch on our distributed system. This directory is intended to be
useful for understanding the details of our method, and for adapting it for use
with any available language models, sandboxes, and distributed systems.

## Installation

No installation is required. All notebooks can be opened and run in Google
Colab.

## Usage

- `cap_set`: The notebook `cap_set.ipynb` can be opened via
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/google-deepmind/funsearch/blob/master/cap_set/cap_set.ipynb).

- `admissible_set`: The notebook `admissible_set.ipynb` can be opened
via
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/google-deepmind/funsearch/blob/master/admissible_set/admissible_set.ipynb).

- `bin_packing`: The notebook `bin_packing.ipynb` can be opened via
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/google-deepmind/funsearch/blob/master/bin_packing/bin_packing.ipynb).

- `cyclic_graphs`: The notebook `cyclic_graphs.ipynb` can be opened via
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/google-deepmind/funsearch/blob/master/cyclic_graphs/cyclic_graphs.ipynb).

## Citing this work

If you use the code or data in this package, please cite:

```bibtex
@Article{FunSearch2023,
  author  = {Romera-Paredes, Bernardino and Barekatain, Mohammadamin and Novikov, Alexander and Balog, Matej and Kumar, M. Pawan and Dupont, Emilien and Ruiz, Francisco J. R. and Ellenberg, Jordan and Wang, Pengming and Fawzi, Omar and Kohli, Pushmeet and Fawzi, Alhussein},
  journal = {Nature},
  title   = {Mathematical discoveries from program search with large language models},
  year    = {2023},
  doi     = {10.1038/s41586-023-06924-6}
}
```

## License and disclaimer

Copyright 2023 DeepMind Technologies Limited

All software is licensed under the Apache License, Version 2.0 (Apache 2.0);
you may not use this file except in compliance with the Apache 2.0 license.
You may obtain a copy of the Apache 2.0 license at:
https://www.apache.org/licenses/LICENSE-2.0

All other materials are licensed under the Creative Commons Attribution 4.0
International License (CC-BY). You may obtain a copy of the CC-BY license at:
https://creativecommons.org/licenses/by/4.0/legalcode

Unless required by applicable law or agreed to in writing, all software and
materials distributed here under the Apache 2.0 or CC-BY licenses are
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the licenses for the specific language governing
permissions and limitations under those licenses.

This is not an official Google product.

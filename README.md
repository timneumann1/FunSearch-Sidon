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
4. Your .json file has randomized name, e.g., "phonic-silo-417508-fc2829b1d7ce.json". 

has 

phonic-silo-417508 and phonic-silo-417508-fc2829b1d7ce.json











Usage:


You can run FunSearch in container using Podman or Docker

```
podman build . -t funsearch


# Create a folder to share with the container
mkdir data
podman run -it -v ./data:/workspace/data funsearch

# Set the environment variable OPENAI_API_KEY=sk-xxxx or create .env file.
# "gpt-3.5-turbo-instruct" model is used by default.
# Refer to 'llm' package docs to use other models.

funsearch run examples/cap_set_spec.py 11 --sandbox_type ExternalProcessSandbox
```
In here we are searching for the algorithm to find maximum cap sets for dimension 11.
You should see output something like
```
root@11c22cd7aeac:/workspace# funsearch run examples/cap_set_spec.py 11 --sandbox_type ExternalProcessSandbox
INFO:root:Writing logs to data/1704956206
INFO:absl:Best score of island 0 increased to 2048
INFO:absl:Best score of island 1 increased to 2048
INFO:absl:Best score of island 2 increased to 2048
INFO:absl:Best score of island 3 increased to 2048
INFO:absl:Best score of island 4 increased to 2048
INFO:absl:Best score of island 5 increased to 2048
INFO:absl:Best score of island 6 increased to 2048
INFO:absl:Best score of island 7 increased to 2048
INFO:absl:Best score of island 8 increased to 2048
INFO:absl:Best score of island 9 increased to 2048
INFO:absl:Best score of island 5 increased to 2053
INFO:absl:Best score of island 1 increased to 2049
INFO:absl:Best score of island 8 increased to 2684
^C^CINFO:root:Keyboard interrupt. Stopping.
INFO:absl:Saving backup to data/backups/program_db_priority_1704956206_0.pickle.
```

Note that in the last command we use the ExternalProcessSandbox that is not fully safe
but makes it a bit less likely that invalid code from LLM would break the search.


Alternatively, you can run the main Python process on a host computer outside of any container and let
the process build and run separate sandbox containers (still requires Podman/Docker).
This variant could be also used, e.g., in Colab quite safely since the environment is some kind of container itself.

```
pip install .

funsearch run examples/cap_set_spec.py 11
```

For more complex input data, you can provide the input also as a .json or .pickle file.

Currently, the search is only using single thread with no asyncio and is somewhat slow
for challenging tasks.  

## Alternative LLMs

The search uses gpt-3.5-turbo-instruct by default, but other models can be used with the --model_name argument
and possibly installing extensions to the llm package.
As an example of performance, with gpt-3.5-turbo-instruct on dimension 8 it usually around 20 tries to find a few
improvements to the naive algorithm.

On the other hand, using orca-mini-3b-gguf2-q4_0 doesn't seem to work quite well.
The latest version has a bit improved parsing to find the last priority_vX method from the LLM response
even if it contains other content like Markdown formatting. Anyway, the model seems to often
use strange indentation of 1 space and thus might require some customization to be useful at all.
Lastly, even with correct Python syntax, orca-mini-3b does not seem to find improvements (in 60 runs) and mostly
generates code that throws "IndexError: tuple index out of range". The situation changes a bit
if the search is started using a database generated by gpt-3.5-turbo prompts.

Overall, all models would probably require some prompt engineering, temperatures tuning, and such for the tool
to be useful at all except for very simple problems.
Also, the implementation is currently lacking good tools to analyze large amount of responses properly which
makes any prompt engineering more difficult.

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

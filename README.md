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

4. Your .json file has randomized name, e.g., "phonic-silo-417508-fc2829b1d7ce.json". In the file "funsearch/__main__.py" (line 98), insert the first three alphanumeric parts of this name into the aiplatform.init() function and add your location (available locations can be retrieved from the Google LLM documentation). That is, replace your randomized .json file name and location in the line
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
   
7. Now it is time to build the container. In order to do this, verify that Docker Desktop is running and enter the Terminal command
```
docker build -t funsearch .
```
The build takes some time for the first time. Once successfully completed, enter the container by entering
```
docker run -it -v ./data:/workspace/data funsearch
```
Now you are in the container environment "funsearch".

8. To run the FunSearch algorithm, enter the Terminal command 
```
funsearch run files/sidon_set_spec.py 7 --sandbox_type ExternalProcessSandbox --authen files/<YOUR .JSON FILE NAME>.json
```
Here, place the name of your .json file in the --authen argument. Note that we only evaluate Sidon sets in one dimension (n = 7) with this command. In the "files" folder, there is also the capset specification file, which can replace the Sidon set specification file, if desired.

Now the FunSearch experiment will repeatedly query the LLM and update the programs database.

---

Here are some remarks on this architecture as added by @jonppe:
```
Note that in the last command we use the ExternalProcessSandbox that is not fully safe
but makes it a bit less likely that invalid code from LLM would break the search. [...]
Currently, the search is only using single thread with no asyncio and is somewhat slow
for challenging tasks.
```

For alternative ways of running the algorithm safely, refer to @jonppe's GitHub page.

---


This repository accompanies the publication

> Romera-Paredes, B. et al. [Mathematical discoveries from program search with large language models](https://www.nature.com/articles/s41586-023-06924-6). *Nature* (2023)

The original code publication can be accesses at https://github.com/google-deepmind/funsearch.

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

# MSc Internship project: M.J. Posthuma 2023-2024

This project contains the code for the internship project of MSc student M.J. Posthuma. The project is supervised by Dr. Marijn Martens at Synaptica Ltd. The project is part of the MSc programme in Neurobiology at Radboud University Nijmegen. This README file contains the project description and the directory structure of the project.

For contact information, see the bottom of this file.

## Introduction to Epilepsy Research

Epilepsy is a complex neurological condition characterized by a variety of symptoms and disease progressions, stemming from dysfunctions in distinct brain regions which can be subdivided into microcircuits contain specific neuronal cell types. This document outlines the focus and goals of our research in understanding and managing temporal lobe epilepsy.

## Understanding Epilepsy Phenotypes

Epilepsy's diverse phenotypes of dysfunction are closely linked to a specific brain region:

- **Temporal Lobe Epilepsy**: Often originates from disrupted hippocampal function, leading to symptoms such as movement alterations, emotional and sensory changes, memory disturbances, and psychiatric symptoms. The hippocampus is a crucial brain region for memory and learning, and its dysfunction can lead to severe cognitive impairments. In our case the CA3 subfield of the hippocampus is of particular interest. The CA3 subfield is comprised of pyramidal, basket and OLM cells, which are interconnected in a complex network.

## The Role of Genetics in Epilepsy

The genetic factors influencing epilepsy are complex and not fully understood. The affected genes often code for ion channels and synaptic connectivity proteins, resulting in intricate non-linear interactions. Understanding these genetic influences is crucial for:

- Tailoring the prescription of anti-epileptic drugs (AEDs) or anti-seizure medications.
- Minimizing side-effects in patients.
- A lot of AEDs focus on sodium and potassium channels. The genetic factors influence the conductance of these channels in the individual cell types in the hippocampus which lead to ictal activity patterns in the network.

## Research Objectives

Our research aims to:

- Assess parameters linked to (inter)ictal activity in neural circuitries, particularly in the hippocampus.
- Investigate the functional consequences of genetic variants, such as SNPs or mutations known to induce epilepsy, by modeling their impact on ion channels and synaptic connectivity.

## Future Goals

The ultimate goal of this research is to help understand TLE and possible help to create a diagnostic tool for medical professionals in the future. This tool would be able to:

- Enable the implementation of specific patient gene profiles into an epilepsy model.
- Assist doctors in selecting appropriate medication to normalize neural circuit functioning.

These goals are ambitious and require a comprehensive understanding of the genetic and neural network dynamics underlying epilepsy.

## Research Questions and Hypotheses

During my internship, I will explore several key questions and hypotheses related to the impact of genetics on epileptic activity in simulated brain circuits. This exploration aims to deepen our understanding of epilepsy and its genetic underpinnings.

## Main Research Question

- **What is the impact of different genetic profiles on epileptic activity in simulated hippocampal brain circuits?**

## Main Hypothesis

- **It is hypothesized that by emulating specific genetic profiles within simulated CA3 hippocampal neural networks, we can replicate their impact on the networks' behavior. Furthermore, it is expected that inducing cellular dynamics that reduce seizure-like (ictal) activity will rescue normal network function.**

## Investigative Sub-Questions

1. **(Inter)Ictal Activity Parameters:**
   - What specific variables characterize (inter)-ictal activity in different neural cell types within temporal lobe epilepsy (TLE) networks?
   - How do these variables vary across different neural networks, and how can they be reliably measured and quantified in a NEURON model?

2. **Genetic Variance Implementation:**
   - How can genetic variations, such as single nucleotide polymorphisms (SNPs) or known epilepsy-inducing mutations, be successfully integrated into hippocampal neural network models to simulate the impact on ictal activity?
   - Are there specific network properties or cellular mechanisms that are particularly sensitive to different types of genetic variations associated with epilepsy?

3. **Combining the Outcomes of Step 1 and 2: Impact of Genetic Variance on Network Dynamics:**
   - What alterations in network dynamics and connectivity patterns are observed when introducing epilepsy-associated genetic variations into neural cell types?
   - Can the effects of specific genetic variants be correlated with the severity and frequency of seizures in the modeled networks?

4. **Rescuing the network: restoring normal brain function**
   - Can we identify specific targets for intervention that can restore normal network dynamics in the presence of epilepsy-associated genetic variations?
   - Are we able to reliable predict the effect of a specific drug on the network dynamics and emulate them in the model?

## Methods

To address these questions, I will leverage the capabilities of the NEURON simulator framework, using Python programming for a comprehensive exploration of genetically induced alterations in cellular dynamics. This research will primarily focus on constructing and analyzing computer models representing hippocampal and thalamocortical brain networks.

## Analysis Directory Structure Overview

This README provides an overview of the directory structure for the analysis project. Each directory and its contents are purposefully organized to support various aspects of the analysis, ranging from data storage to code execution.

### `data` Directory

- **Purpose**: Stores all the raw data collected per experiment. Not included in the repository due to size constraints.
- **Contents**:
  - Raw data files, each corresponding to a specific experiment.

### `Exercises` Directory

- **Purpose**: Includes Python files that contain exercises from a neuroscience tutorial.
- **Contents**:
  - Tutorial exercise scripts, tailored for neuroscience applications.

### `Experiments` Directory

- **Purpose**: Contains the primary experiment scripts used to generate new data.
- **Contents**:
  - A series of Python scripts designed for running various experiments and data generation.

### `imgs` Directory

- **Purpose**: Houses images and figures generated from data analysis.
- **Contents**:
  - Images of plots and visual data representations.

### `Math` Directory

- **Purpose**: Houses pdf files containing mathematical explanations of the models.
- **Contents**:
  - Document files containing mathematical explanations of the models.

### `Notebooks` Directory

- **Purpose**: Contains Jupyter notebooks for data analysis and visualization.
- **Contents**:
  - Jupyter notebooks detailing data analysis processes for each experiment.

### `SingleCell` Directory

- **Purpose**: Contains Python files for testing the single-cell models in the NEURON simulator.
- **Contents**:
  - Scripts for validating single-cell model functionalities.

### `src` Directory

- **Purpose**: Contains source code and modules for the project.
- **Contents**:
  - `FileManagement`: A subdirectory for verifying data folders and structures.
  - `SanjayCode`: Python files with functions for data structuring, plotting, and utilities.

### `Tutorials` Directory

- **Purpose**: Contains tutorial scripts and notebooks for learning NEURON and Python.
- **Contents**:
  - `NEURON_tut_*`: Notebooks containing the tutorials from the NEURON website.
  - `.py files`: Python files with functions related to the tutorials that explain NEURON simulator functionality.

**Note**: This README is intended to guide users and collaborators through the project's file structure, ensuring efficient navigation and understanding of the project's components. Each directory is crucial for the comprehensive analysis and has been organized for ease of use and clarity.

## Development

For a detailed list of upcoming enhancements and planned work for this project, please refer to the [TODO list](TODO.md).

## Thesis

For a copy of the master thesis document related to this project, email me to receive the final version: [email](marc.posthuma@ru.nl)

First reader: Prof. Dr. Paul Tiesinga
Second reader: Prof. Dr. Richard van Wezel

## Contributing

Thank you for considering contributing to this project! Guidelines are provided in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Authors

- **Marc J. Posthuma** - *MSc Student Research Project Intern @ Synaptica Ltd.* - [GitHub Profile](https://github.com/Marc-Mundo)

See also the list of [contributors](hhttps://github.com/users/Marc-Mundo/projects/1/contributors) who participated in this project.

See also the repository of my research project: [Msc Internship Project](https://github.com/Marc-Mundo/Synaptica_internship)

For more information about the project, please contact me at [email](marc.posthuma@ru.nl)

Company website: [Synaptica](https://www.synaptica.nl/)

## Acknowledgments

- **Marijn Martens** for his supervision and guidance during this project and allowing the opportunity to work at Synaptica for the duration of the internship.
- **Sean Gies** for his implementation of the Sanjay 2015 model in NEURON and general guidance in programming during this project.
- A.I. tools to help me brainstorm, analyse and write this project.

## Course information

This project was done as part of the Master's curriculum of the *Neurobiology* track of the **Radboud University**.

The internship was done externally and an internship agreement form was signed by all parties and sent to the internship coordinators of biosciences of the FNWI (2023-2024).

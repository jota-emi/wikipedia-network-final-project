# Directed Graph Generator with Wikipedia Links

This repository contains a Python project that generates a directed graph using Wikipedia's links pages. The project utilizes the `networkx`, `wikipedia`, `matplotlib`, and `seaborn` libraries. The pipeline is orchestrated by Apache Airflow and consists of three tasks: "getting_data", "cleaning_data", and "plotting_results".

## Project Overview

The Directed Graph Generator with Wikipedia Links project aims to create a directed graph based on Wikipedia's links pages. The graph represents the relationships between different Wikipedia articles, where each article is a node, and the links between them are the edges.

The project uses the following libraries:

- `networkx`: A Python library for creating, manipulating, and studying the structure, dynamics, and functions of complex networks.
- `wikipedia`: A Python library that makes it easy to access and parse data from Wikipedia.
- `matplotlib`: A plotting library for creating static, animated, and interactive visualizations in Python.
- `seaborn`: A Python data visualization library based on Matplotlib that provides a high-level interface for drawing informative and attractive statistical graphics.

## Component
- João Marcos Viana Silva

## Pipeline Tasks

The pipeline consists of the following three tasks:

### 1. Getting Data

The "getting_data" task is responsible for retrieving data from Wikipedia. It uses the `wikipedia` library to fetch Wikipedia articles and extract the links between them. The task collects the necessary data and prepares it for further processing.

### 2. Cleaning Data

The "cleaning_data" task performs data cleaning and preprocessing on the extracted Wikipedia data. It removes any irrelevant information, filters out unwanted links, and prepares the data for visualization.

### 3. Plotting Results

The "plotting_results" task generates a directed graph visualization using the cleaned data. It uses the `networkx`, `wikipedia`, `matplotlib`, and `seaborn` libraries to create an informative and visually appealing representation of the relationships between Wikipedia articles.

## Orchestration with Apache Airflow

The pipeline tasks are orchestrated using Apache Airflow, an open-source platform designed to programmatically author, schedule, and monitor workflows. Airflow allows you to define dependencies between tasks, schedule their execution, and track their progress.

The Directed Graph Generator with Wikipedia Links project leverages Apache Airflow to automate and manage the execution of the three pipeline tasks. You can customize the scheduling, dependencies, and other aspects of the workflow by modifying the Airflow DAG (Directed Acyclic Graph) associated with the project.

## Repository Structure

The repository has the following structure:

    .
    ├── dags
    │   └── wikipedia_graph_dag.py
    │   └── functions_pipeline.py
    ├── results
    │   ├── cdf_histograma.png
    │   ├── core_shell.png
    │   ├── metrics.png
    │   ├── pair_grid.png
    │   ├── pdf_histograma.png
    │   ├── wikipedia_network_raw.graphml
    │   └── wikipedia_network.graphml
    ├── README.md
    ├── docker-compose.yaml
    ├── wiki_net_analysis.ipynb
    ├── graph.png


- The `dags` directory contains the Apache Airflow DAG file `wikipedia_graph_dag.py`, which defines the pipeline workflow and task dependencies. And the python script `functions_pipeline.py` that contains the functions for each task: `getting_data`, `cleaning_data`, and `plotting_results`.
- The `results` directory contains the resulting figures and graph files.
- The `README.md` file (this file) provides an overview of the project and repository.
- The `docker-compose.yaml` file contains the configuration for running Apache Airflow using Docker.
- The `wiki_net_analysis.ipynb` file contains all the developing process and step-by-step.


## Getting Started

To run the Directed Graph Generator with Wikipedia Links project, follow these steps:

1. Clone this repository: `git clone https://github.com/your-username/directed-graph-wikipedia.git`.
2. Start Apache Airflow using Docker and the provided `docker-compose.yaml` file, with command `docker compose up --build`.
3. Trigger the DAG in the Apache Airflow UI or using the Airflow CLI.

Please refer to the specific documentation for each library (e.g., `networkx`, `wikipedia`, `matplotlib`, `seaborn`, and Apache Airflow) for further details on usage, customization, and advanced features.

## Explanation Video

For a detailed walkthrough of the Directed Graph Generator with Wikipedia Links project, you can watch the explanation video [here](https://youtu.be/Phn-5-Q0gG8m).



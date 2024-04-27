# Introduction
This Spark package is designed to process data from various sources, perform transformations, and write the results to different sinks. It follows the pipeline design pattern to provide a flexible and modular approach to data processing.

## Installation

Install this package using:

```bash
pip install pysparkify
```

## Usage

Run the library as a command line tool:

```bash
pysparkify your_recipe.yml
```

Or use it in your Python scripts:

```python
from pysparkify import run
run('your_recipe.yml')
```


## Design

The package is structured as follows:

### Source, Sink and Transformer Abstraction

The package defines abstract classes `Source`, `Sink` and `Transformer` to represent data sources, sinks and transformers. It also provides concrete classes, including `CsvSource`, `CsvSink` and `SQLTransformer`, which inherit from the abstract classes. This design allows you to add new source and sink types with ease.

### Configuration via `recipe.yml`

The package reads its configuration from a `recipe.yml` file. This YAML file specifies the source, sink, and transformation configurations. It allows you to define different data sources, sinks, and transformation queries.

### Transformation Queries

Transformations are performed by `SQLTransformer` using Spark SQL queries defined in the configuration. These queries are executed on the data from the source before writing it to the sink. New transformers can be implemented by extending `Transformer` abstract class that can take spark dataframes from sources to process and send dataframes to sinks to save.

### Pipeline Execution

The package reads data from the specified source, performs transformations based on the configured SQL queries, and then writes the results to the specified sink. You can configure multiple sources and sinks within the same package.

## Setup

The project is built using python-3.12.0, spark-3.5.0 (and other dependencies in requirements.txt).

## How to Contribute

1. Become a maintainer by requesting raohammad(at)gmail.com
2. Open a PR
3. Once the PR is reviewed and approved, included github actions will deploy the version directly to pypi repository


# Pysparkify Usage Example

This library abstracts Spark data processing workflows. Define your workflow in `recipe.yml`. Reads data from CSV source and writes data to CSV Sink (paths mentioned in config) after data transformation (SQL mentioned in config too)

```
source:
  - type: CsvSource
    config:
      name: csv
      path: "resources/data/input_data.csv"

transformer:
  - type: SQLTransformer
    config:
      name: transformer1
      source: 
        - name: csv
          as_name: t1
      statement: 
        - sql: "SELECT * from t1 limit 2"
          as_name: trx1
          to_sink: sink1
        - sql: "select AVG(age) from trx1"
          as_name: trx2
          to_sink: sink2

sink:
  - type: CsvSink
    config:
      name: sink1
      path: "output/output_data.csv"
  - type: CsvSink
    config:
      name: sink2
      path: "output/avgage_data.csv"
      
```

The sample from csv source file used in above transformation is as below;

```
name,age,city
Hayaan,10,Islamanad
Jibraan,8,ShahAlam
Allyan,3,Paris
John,35,San Francisco
Doe,22,Houston
Dane,30,Seattle
```
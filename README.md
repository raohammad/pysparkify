# Introduction
This Spark package is designed to process data from various sources, perform transformations, and write the results to different sinks. It follows the pipeline design pattern to provide a flexible and modular approach to data processing.

## Setup

Install this package using:

```bash
pip install pysparkify
```

Create spark_config.conf file of this format to enter all configurations related to spark in `config/spark_config.conf`

```bash
[SPARK]
spark.master=local[*]
spark.app.name=PysparkifyApp
spark.executor.memory=4g
spark.driver.memory=2g
```

This library abstracts Spark data processing workflows. For example you would like to;

- take first two rows of the data, save it as a separate output
- take an average and save it as a separate output

with below sample data

```
name,age,city
Hayaan,10,Islamanad
Jibraan,8,ShahAlam
Allyan,3,Paris
John,35,San Francisco
Doe,22,Houston
Dane,30,Seattle
```

Your recipe reads the csv data as source, transforms the data and optionally save the output of each transformation to sink. Below would be the recipe.yml for this operation.

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


### Usage

This library can be run as a command line tool:

```bash
pysparkify your_recipe.yml
```

Or use it in your Python scripts:

```python
from pysparkify.lib.app import run
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


## How to Contribute

1. There are plenty of ways, in which implementation of new Sources and Sinks top the list
2. Open a PR
3. PR is reviewed and approved, included `github actions` will deploy the version directly to pypi repository

# Introduction
The pysparkify library facilitates data processing from diverse sources, applying transformations, and writing outcomes to various destinations. It employs the pipeline design pattern, offering a flexible and modular approach to big data data processing.

Supported sources and sinks include:

- Amazon S3
- Amazon Redshift
- Postgres DB
- Local Files (for local spark)

## Setup

Install this package using:

```bash
pip install pysparkify
```

Create a spark_config.conf file following this format to input all Spark-related configurations. For instance:

```bash
[SPARK]
spark.master=local[*]
spark.app.name=PysparkifyApp
spark.executor.memory=4g
spark.driver.memory=2g
```

The library abstracts Spark data processing workflows. For example, you can:

- Extract the first two rows of data and save them as a separate output.
- Compute an average and save it as another output.

Here's a sample data set:

```
name,age,city
Hayaan,10,Islamanad
Jibraan,8,ShahAlam
Allyan,3,Paris
John,35,San Francisco
Doe,22,Houston
Dane,30,Seattle
```

Your recipe reads the CSV data as the source, transforms it, and optionally saves the output of each transformation to a sink. Below is a sample recipe.yml for this operation:

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

You can run this library as a command-line tool:

```bash
pysparkify 'path/to/recipe.yml' --spark-config 'path/to/spark-config.conf'
```

Or use it in your Python scripts:

```python

import pysparkify
pysparkify.run('path/to/recipe.yml') #this expects spark_config.conf file on path `config/spark_config.conf` path

# or with optional spark configuration file
pysparkify.run('path/to/recipe.yml', 'path/to/custom_spark_config.conf')

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


## Sponsors

The project is being sponsord by [Dataflick](https://www.dataflick.dev).
If you are considering using this library in your projects, [please consider becoming a sponsor for continued support](mailto:raohammad@gmail.com?subject=Become%20A%20Sponsor).
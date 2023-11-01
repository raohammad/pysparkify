# Introduction
This Spark package is designed to process data from various sources, perform transformations, and write the results to different sinks. It follows the pipeline design pattern to provide a flexible and modular approach to data processing.

## Design

The package is structured as follows:

### Source and Sink Abstraction

The package defines abstract classes `Source`, `Sink` and `Transformer` to represent data sources, sinks and transformers. It also provides concrete classes, including `CsvSource`, `CsvSink` and `SQLTransformer`, which inherit from the abstract classes. This design allows you to add new source and sink types with ease.

### Configuration via `recipe.yml`

The package reads its configuration from a `recipe.yml` file. This YAML file specifies the source, sink, and transformation configurations. It allows you to define different data sources, sinks, and transformation queries.

### Transformation Queries

Transformations are performed by `SQLTransformer` using Spark SQL queries defined in the configuration. These queries are executed on the data from the source before writing it to the sink. New transformers can be implemented by extending `Transformer` abstract class that can take spark dataframes from sources to process and send dataframes to sinks to save.

### Pipeline Execution

The package reads data from the specified source, performs transformations based on the configured SQL queries, and then writes the results to the specified sink. You can configure multiple sources and sinks within the same package.

## Setup

The project is built using python-3.12.0, spark-3.5.0 (and other dependencies in requirements.txt).

In your environment you should have spark and hadoop libraries added

    export SPARK_HOME=/path/to/your/spark
    export HADOOP_HOME=/path/to/your/hadoop (if applicable)
    export PATH=$SPARK_HOME/bin:$HADOOP_HOME/bin:$PATH


## Testing

Make sure that the required packages are installed in your python environemnt, listed in setup.py INSTALL_REQUIRES section. The package includes a testing framework using PyTest. Test cases are provided to ensure that each source, sink, and transformation works as expected. You can run the tests using the following command:

```bash
pytest test_app.py
```

or test run directly inside spark-transformer folder

```bash
python ./src/app.py --config ./config/recipe.yml 
```

## Deployment
... Environment specific documentation
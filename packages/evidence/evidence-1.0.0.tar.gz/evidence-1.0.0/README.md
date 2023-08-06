# Description

Differential analysis of DFXML idifference2.py output

# Installation

`pip install evidence`

# Usage

**From command line:**

`python -m evidence --path PATH [--output OUTPUT]`

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
|--path | -p | String | - | Path to idifference output dir |
|--output | -o | String | output | Path to result dir |


# Example

Given the following files, where the first placeholer describes
the action and the secon placeholder describes the number of execution.

```
ge/
    *.*.idiff
    noise.idiff
```


`python -m evidence -p path/to/idifference2result`

```
# The following directories will be created for each run of above command.
# Note: Content of this directories will be deleted 

output/
        ce/
            *.ce
        me/
            *.me
        pe/
            *.*.pe
```


# License

MIT
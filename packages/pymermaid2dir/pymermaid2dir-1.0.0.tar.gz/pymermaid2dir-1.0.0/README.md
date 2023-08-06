# pymermaid2dir

A Python package for converting directory structures to Markdown's Mermaid syntax.

pymermaid2dir is a Python package that allows you to convert directory structures into Markdown's Mermaid syntax, making it easy to visualize your file and folder hierarchy. With pymermaid2dir, you can easily generate diagrams and flowcharts that represent the structure of your project.

## Installation

You can install pymermaid2dir using pip:

```python
pip install pymermaid2dir
```

## Usage

To use pymermaid2dir, simply run the pymermaid2dir module on the command line to convert the directory structure to mermaid.

```shell
usage: pymermaid2dir [-h] --folder FOLDER --output OUTPUT [-v]

pymermaid2dir

options:
  -h, --help            show this help message and exit
  --folder FOLDER, -f FOLDER
                        Input Root Folder
  --output OUTPUT, -o OUTPUT
                        Output Mode
  -v, --version         show program's version number and exit
```

### Exsample

```shell
# command
python3 -m pymermaid2dir -f sample -o markdown

# result
\```mermaid
graph TD;
  28191270[sample]-->28191273[f1.txt];
  28191270[sample]-->28191278[f2.txt];
\```
```

> Currently, only markdown output is available, so be sure to run with `-o markdown`.

## License

pymermaid2dir is distributed under the MIT License. See the LICENSE file for more information.

We hope this helps you get started with your pymermaid2dir project on GitHub! Let us know if you have any other questions or if there's anything else we can do to assist you.

# gsheetnet
Neural Network implementation in Google Sheets

This script generates a feedforward neural network implementation as a CSV file that will
work in Google Sheets.

By default, all weight parameters are 0 and all biases are .5

## Requirements
* [fire](https://github.com/google/python-fire)

## Usage:
```
  python gsheetnet.py [layers] [args]
  Arguments:
    --layers: a list of comma separated layer sizes. no spaces
        (required)
    --bias: True or False, whether to add a bias term
        Default: True
    --activation: which activation function to use
        Default: 'sigmoid'
    --file: output filename
        Default: net.csv
```
## Examples:

  example.csv:

  `python gsheetnet.py [10,20,15,1] --file=example.csv`

  `python gsheetnet.py [5,10,10,1] --activation='relu' --file=mynet.csv`
 
  `python gsheetnet.py [28,50,10] False 'tanh' anotherfile.csv`

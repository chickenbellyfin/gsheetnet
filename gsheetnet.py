""" This script generates a feedforward neural network implementation as a CSV file that will
work in Google Sheets.

By default, all weight parameters are 0 and all biases are .5

Usage:
  python gsheetnet.py [layers] [args]

  Arguments:
    --layers: a list of comma separated layer sizes
        (required)
    --bias: True or False, whether to add a bias term
        Default: True
    --activation: which activation function to use
        Default: 'sigmoid'
    --file: output filename
        Default: net.csv

Examples:
  python gsheetnet.py [5, 10, 10, 1] --activation='relu' --file=mynet.csv
  python gsheetnet.py [28, 50, 10] False 'tanh' anotherfile.csv
"""
import fire

### formulas
RANGE = '$%s$%d:$%s$%d'
CELL = '$%s$%d'
activations = {
    'relu' : 'MAX(0, %s)',
    'tanh' : 'TANH(%s)',
    'sigmoid' : '1/(1 + EXP(-%s))'
}

weighted_sum_formula = 'SUM(ARRAYFORMULA(%s * %s))'
bias_term_formula = '(%s + %s)'


def column_name(n):
  """ Returns the Excel name for a column
  
  Args:
    n (int): column number, 0-based
  
  Returns:
    (str): column name, ex. 'J', 'AB', 'AAA'
  """

  A = ord('A')
  name = ''
  n += 1
  while n > 0:
    if n % 26:
      name = chr(A + (n % 26) - 1) + name
      n /= 26
    else:
      name = 'Z' + name
      n = n/26 - 1
  return name


def layer_range(layer_num, size):
  """ Returns the Excel range for a layer given it's index and size

  Args:
     layer_num (int): The layer number, 0-based
     size (int): number of nodes in the layer

  Returns:
    (str): Absolute range for the layer, ex. '$A$1:$A$5'
  """

  c = column_name(layer_num)
  return RANGE % (c, 1, c, size)


def write_csv(cells, file):
  """ Outputs the cells to a CSV file

  Args:
    cells (dict): A dict of cell contents
      keys (tuple): (column, row)
      values (str): cell value 
    file (str): File to output to
  """
  
  # find out number of rows and columns to use
  filled_cells = zip(*cells.keys())
  max_row = max(filled_cells[1]) + 1
  max_col = max(filled_cells[0]) + 1
  rows = []
  
  # find values for each row/column
  for row in range(max_row):
    row_elems = []
    for col in range(max_col):
      if cells.get((col, row)):
        row_elems.append(cells[(col, row)])
      else:
        row_elems.append('')
    rows.append(','.join(row_elems))

  csv = open(file, 'w')
  csv.write("\n".join(rows))
  csv.close()


def make_net(layers, bias=True, activation='sigmoid', file='net.csv'):
  """ Outputs a spreadsheet containing a neural network

  Args:
    layers (list): a list of layer sizes, with the first item being the input
                   and the last item being the output
    bias (boolean): Whether or not to include a bias term
    activation (str): Default: 'sigmoid'. which activation function to use. Possible values: 'relu', 'tanh', 'sigmoid'
    file (str): name of the file to output to
  """

  activation_formula = activations[activation]

  weight_start_row = max(layers)

  cells = {}

  for l in range(len(layers)):
    for n in range(layers[l]):
      if l == 0:
        # set inputs to 0
        cells[(l, n)] = '0'
      else:
        input_size = layers[l-1]
        
        # get sheet locations of inputs, weights, and bias
        input_range = layer_range(l - 1, input_size)

        weight_row = weight_start_row + sum(layers[1:l]) + n
        weight_range = RANGE % (column_name(0), weight_row + 1, column_name(input_size - 1), weight_row + 1)
        bias_cell = CELL % (column_name(input_size), weight_row + 1)
        
        # build cell formula
        layer_output = weighted_sum_formula % (input_range, weight_range)
        if(bias):
          layer_output = bias_term_formula % (layer_output, bias_cell)
        layer_output = activation_formula % layer_output
        
        # add to cell dict
        cells[(l, n)] = '=' + layer_output

        # set weight params to 0
        for w in range(input_size):
          cells[(w, weight_row)] = "0"

        # set bias to .5
        if bias:
          cells[(input_size, weight_row)] = ".5"

  # write cells to a CSV file
  write_csv(cells, file)

def main():
    fire.Fire(make_net)

if __name__ == '__main__':
    main()
'''
Print formated tabular data in different styles
'''

from collections import namedtuple
import textwrap
import os


#-----------------------------------------------------------------------
'''
CONSTANTS

Here all the constants for use are united.
The purpuse is to make cleaner, smaller, partitioned code.
fun names to easily remember.
'''

# Standard Invisible separator. This mark a standar
# of blank space for tables without visible vertical separators.
STINVISP = '  '

# Standar margin for cells is one space. More could look weird.
STAMA = 1

# Escape codes for a new line
ESCODES = ['\n', '\r']

# Minimum width of a column
MIWCOL = 2

#-----------------------------------------------------------------------
'''
UTILS
'''

class Utils():

    def getWIndowsSize():
        if os.name == "nt":
            mode = os.popen('mode').read().split()
            lines = "L¡neas:" if "L¡neas:" in mode else (
                "Líneas" if "Líneas" in mode else "Lines"
            )
            columns = "Columnas:" if "Columnas:" in mode else "Columns:"
            linesIndex = mode.index(lines)+1
            colsIndex = mode.index(columns)+1
            lines = mode[linesIndex]
            columns = mode[colsIndex]
        else:
            lines, columns = os.popen('stty size', 'r').read().split()
        
        return lines, columns
    
    def isarray(piece):
        return isinstance(piece, list)

#-----------------------------------------------------------------------
"""
COMPOSITION SETS - STYLES

A composition set is a named tuple  wich contain the characters
for each part of the table. Here are are the ones currently added.

*¡This part was based (mainly) in the "tabulate" package structure!
"""

tableComposition = namedtuple(
    'CompositionSet',
    [
        'horizontalComposition',
        'verticalComposition',
        'tableOptions'
    ]
)

HorizontalComposition = namedtuple(
    'HorizontalComposition',
    [
        'headerSuperior',
        'headerInferior',
        'startWithNoHeader',
        'tableBody',
        'tableEnd'
    ]
)

VerticalComposition = namedtuple(
    'VerticalComposition', 
    [
        'header',
        'tableBody'
    ]
)

SeparatorLine = namedtuple(
    'Separator',
    [
        'left',
        'middle',
        'intersection',
        'right'
    ]
)

TableOptions = namedtuple(
    'TableOptions',
    [
        'margin'
    ]
)

_styleCompositions = {
    'clean': tableComposition(
        horizontalComposition=HorizontalComposition(
            headerSuperior=None,
            headerInferior=SeparatorLine('', '─', STINVISP, ''),
            startWithNoHeader=None,
            tableBody=None,
            tableEnd=SeparatorLine('', '─', STINVISP, '')
        ),
        verticalComposition=VerticalComposition(
            header=SeparatorLine('', STINVISP, None, ''),
            tableBody=SeparatorLine('', STINVISP, None, '')
        ),
        tableOptions=TableOptions(
            margin=0
        )
    ),
    'plain': tableComposition(
        horizontalComposition=HorizontalComposition(
            headerSuperior=None,
            headerInferior=None,
            startWithNoHeader=None,
            tableBody=None,
            tableEnd=None
        ),
        verticalComposition=VerticalComposition(
            header=SeparatorLine('', STINVISP, None, ''),
            tableBody=SeparatorLine('', STINVISP, None, '')
        ),
        tableOptions=TableOptions(
            margin=0
        )
    ),
    'bold_borderline': tableComposition(
        horizontalComposition=HorizontalComposition(
            headerSuperior=SeparatorLine('╔', '═', '╤', '╗'),
            headerInferior=SeparatorLine('╠', '═', '╪', '╣'),
            startWithNoHeader=SeparatorLine('╔', '═', '╤', '╗'),
            tableBody=SeparatorLine('╟', '─', '┼', '╢'),
            tableEnd=SeparatorLine('╚', '═', '╧', '╝'),
        ),
        verticalComposition=VerticalComposition(
            header=SeparatorLine('║', '│', None, '║'),
            tableBody=SeparatorLine('║', '│', None, '║')
        ),
        tableOptions=TableOptions(
            margin=STAMA
        )
    ),
    'grid': tableComposition(
        horizontalComposition=HorizontalComposition(
            headerSuperior=SeparatorLine('+', '-', '+', '+'),
            headerInferior=SeparatorLine('+', '=', '+', '+'),
            startWithNoHeader=SeparatorLine('+', '-', '+', '+'),
            tableBody=SeparatorLine('+', '-', '+', '+'),
            tableEnd=SeparatorLine('+', '-', '+', '+')
        ),
        verticalComposition=VerticalComposition(
            header=SeparatorLine('|', '|', None, '|'),
            tableBody=SeparatorLine('|', '|', None, '|')
        ),
        tableOptions=TableOptions(
            margin=STAMA
        )
    ),
    'windows_alike': tableComposition(
        horizontalComposition=HorizontalComposition(
            headerSuperior=None,
            headerInferior=SeparatorLine('', '-', STINVISP, ''),
            startWithNoHeader=None,
            tableBody=None,
            tableEnd=None
        ),
        verticalComposition=VerticalComposition(
            header=SeparatorLine('', STINVISP, None, ''),
            tableBody=SeparatorLine('', STINVISP, None, '')
        ),
        tableOptions=TableOptions(
            margin=0
        )
    ),
    'thin_borderline': tableComposition(
        horizontalComposition=HorizontalComposition(
            headerSuperior=SeparatorLine('┌', '─', '─', '┐'),
            headerInferior=SeparatorLine('├', '─', '┬', '┤'),
            startWithNoHeader=SeparatorLine('┌', '─', '┬', '┐'),
            tableBody=SeparatorLine('├', '─', '┼', '┤'),
            tableEnd=SeparatorLine('└', '─', '┴', '┘')
        ),
        verticalComposition=VerticalComposition(
            header=SeparatorLine('│', ' ', None, '│'),
            tableBody=SeparatorLine('│', '│', None, '│')
        ),
        tableOptions=TableOptions(
            margin=STAMA
        )
    ),
    'bold_header': tableComposition(
        horizontalComposition=HorizontalComposition(
            headerSuperior=SeparatorLine('╔', '═', '╦', '╗'),
            headerInferior=SeparatorLine('╚', '═', '╩', '╝'),
            startWithNoHeader=SeparatorLine('┌', '─', '┬', '┐'),
            tableBody=SeparatorLine('├', '─', '┼', '┤'),
            tableEnd=SeparatorLine('└', '─', '┴', '┘')
        ),
        verticalComposition=VerticalComposition(
            header=SeparatorLine('║', '║', None, '║'),
            tableBody=SeparatorLine('│', '│', None, '│')
        ),
        tableOptions=TableOptions(
            margin=STAMA
        )
    ),

}

def getCompositions():
    return _styleCompositions

#-----------------------------------------------------------------------
""" 
FORMATION OF THE STYLE

Here the separators and data rows are formed
"""

class Separators(object):

    def __init__(
        self,
        headerIncluded: bool,
        alignments: list,
        cellMargin: int,
        composition: tuple,
        colsWidth: list,
        ):
        self.composition = composition
        self.headerIncluded = headerIncluded
        self.cellMargin = cellMargin
        self.colsWidths = colsWidth
        self.alignments = alignments
        
        # These are the composition of each type of separator, or
        # the characters that will conform them
        self.separatorsCompositions = self.composition.horizontalComposition

        # This is the named tuple with empty fields. Here the separators 
        # will be delivered
        self.separatorsPositions = HorizontalComposition
        
    def __str__(self):
        pass

    def makeMiddlePart(self, middle: str, singleColWidht: int, ):
        return f'{f"{middle}"*((singleColWidht)+(self.cellMargin*2))}'

    def makeOne(self, singleComposition: tuple):
        """
        Returns a single separator 
        """
        intersection = singleComposition.intersection
        middleChar = singleComposition.middle
        leftChar = singleComposition.left
        rightChar = singleComposition.right
        
        HorLines = map(
            self.makeMiddlePart,
            [middleChar for x in range(len(self.colsWidths))], #x is irrelevant
            self.colsWidths
            )

        # Here the separator is made joining al the horizontal lines of the
        # separator with the intersection as separator, resulting in a structure:
        #       line + separator + line + separator . . .
        #       ---- +   '  '    + ---  +   '  '    . . .
        # After that is the left char, and at the end the right char
        fullSeparator: str = leftChar + f'{intersection}'.join(HorLines) + rightChar

        return fullSeparator
    
    def makeAll(self) -> tuple:
        """ 
        Returns named tuple with the same structure that the horizontalComposition,
        but with the separator string or "None" if it isn´t used
        HorizontalComposition(  
            headerSuperior=None,
            headerInferior='───────  ──────  ───  ────  ─────  ───────',
            startWithNoHeader=None,
            tableBody=None, 
            tableEnd=None
            )   
        """

        separatorsCompositions = [
        sepcomp for sepcomp in self.separatorsCompositions
        ]

        madeSeparators = []
        current = 0
        for sepToDo in separatorsCompositions:

            if sepToDo != None:
                madeSeparator = self.makeOne(sepToDo)
                madeSeparators.append(madeSeparator)
            else:
                madeSeparators.append(None)

            current += 1

        # This part is to deliver a tuple with all the complete separators or None
        # statements, depending on the style. This is to distiguish easily for which
        # part of the table is each separator
        madeSeparators: tuple = self.separatorsPositions(
            headerSuperior=madeSeparators[0] if (
                self.headerIncluded == True
            ) else None,
            headerInferior=madeSeparators[1]if (
                self.headerIncluded == True
            ) else None,
            startWithNoHeader=madeSeparators[2] if (
                self.headerIncluded == False
            ) else None,
            tableBody=madeSeparators[3],
            tableEnd=madeSeparators[4],
        )

        return madeSeparators



class DataRows(object):

    def __init__(self, adjustedTableCells: list, composition: tuple, headers):
        self.headerCells = adjustedTableCells[0] if(
            (headers.lower() == 'first') if not Utils.isarray(headers) else False
            ) else headers
        self.rowCells = adjustedTableCells[1:]
        self.composition = composition 

        # These are the compositions of the divisions or vertical separators
        self.divisionsPositions = self.composition.verticalComposition

        # This is the named tuple with empty fields. Here the fully-formed 
        # dataRows will be delivered.
        self.rowsPositions = VerticalComposition

    def __str__(self):
        pass

    def makeOne(self, dataRow: list, isHeader: bool) -> str:
        divCompositionsKeys = {'header': 0, 'tableBody': 1}

        if isHeader:
            position = divCompositionsKeys['header']
        else:
            position = divCompositionsKeys['tableBody']

        leftChar = self.divisionsPositions[position].left
        rightChar = self.divisionsPositions[position].right
        middleChar = self.divisionsPositions[position].middle
        dataWithDivisions = f'{middleChar}'.join(dataRow)
        fullDataRow: str = leftChar + dataWithDivisions + rightChar

        return fullDataRow

    def makeAll(self)-> tuple:

        providedHeader = self.headerCells
        headerRow = None
        if providedHeader != None:
            headerRow = []
            for row in providedHeader:
                headerRow.append(self.makeOne(row, True) + '\n')

        bodyRows = []
        for multiline in self.rowCells:
            bodyRows.append([])
            for row in multiline:
                fullRow = self.makeOne(row, False)
                bodyRows[-1].append(fullRow + '\n')

        madeRows: tuple = self.rowsPositions(
            header=headerRow,
            tableBody=bodyRows
        )

        return madeRows
    
#-----------------------------------------------------------------------
'''
CELLS AND COLUNM FORMATING

Here the column widths are established, and the cells' spaces put.
'''

class TableMeasures(object):

    def __init__(self, expandToWindow, rawData,  cellMargin, composition, windowSize):
        self.verticalDivisions =  composition.verticalComposition.tableBody
        self.lenOfMidDiv = len(self.verticalDivisions.middle)
        self.lenOfRight = len(self.verticalDivisions.right)
        self.lenOfLeft = len(self.verticalDivisions.left)
        self.windowMeasures = windowSize
        self.windowWidht = int(self.windowMeasures[1])
        self.expandToWindow = expandToWindow # replace number for boolean
        self.cellMargin = cellMargin
        self.rawData = rawData

    def makeRowsEquals(self):
        '''
        Aqui se comprueba si todas las columnas tienen el mismo ancho.
        '''
        # falta completar comprobación del mismo ancho.

        pass
       
    def getRawDataCellsWidths(self):
        '''
        Here the widths of each cell are obtained iterating trough each
        row of the raw data.
        [[cell1, cell2],[cell3, cell4]] --> [[len1, len2],[len3, len4]]
        '''
        
        # Get len of each element in each row.
        cellsWidths = [
            [
                len(cell) for cell in row
            ] for row in self.rawData
            ]

        return cellsWidths

    def getFullColumnWidths(self, cellsWidths):
        '''
        Returns the Width of each column including the margin.
        '''

        # Each array in here is a column instead of a row.
        columnOrdenatedWidths = [] 
        for col in range(len(cellsWidths[0])):
            columnOrdenatedWidths.append([])
            for row in range(len(cellsWidths)):
                columnOrdenatedWidths[-1].append(cellsWidths[row][col])

        # Here the max of each array is obtained and appended in a
        # single array and are additioned with the product of the margin
        # by 2; it's important to add the margin at the beining, to ensure
        # that the space calculations include it.
        fullColumnWidths = [
            (
                max(singleCol) + (self.cellMargin*2)
            ) for singleCol in columnOrdenatedWidths
            ]
        
        return fullColumnWidths

    def getMaxWidth(self, columnWidths):        
        '''
        Returns:
            - maxWidhtPerCol: A list of the max widht of each column to
                fill the window, to be stretched or reduced.    
            - maxWidhtOfColumns: The max width of the columns, excluding
                the witdht of the vertical divisions of the table.
        '''

        # The widths of the vertical divisions are substracted of the
        # window width to ensure that the total width of the table, wich
        # includes the divisions, fit the window.
        maxWidhtOfColumns = (self.windowWidht - 1) - sum([
            self.lenOfLeft,
            ((self.lenOfMidDiv * len(columnWidths)) - 1),
            self.lenOfRight
        ])

        # The sum of column widths.
        WidhtOfColumns = sum(columnWidths)

        # What percentage of the sum represents each column.
        percentages = [column/WidhtOfColumns for column in columnWidths]

        # The maximun width per column, obtained multiplying the percentage
        # of each column by the maxWidhtOfColumns.
        maxWidhtPerCol = [
            (
                round(perc*maxWidhtOfColumns) 
            )for perc in percentages
            ]

        # sometimes the new size of the columns exceed the max width, 
        # so this substract that diference of the biggest column.
        newWidhtOfColumns = sum(maxWidhtPerCol)
        if newWidhtOfColumns > maxWidhtOfColumns:
            toReduce = maxWidhtPerCol.index(max(maxWidhtPerCol))
            if maxWidhtOfColumns > 0: 
                maxWidhtPerCol[toReduce] -= newWidhtOfColumns - maxWidhtOfColumns

        # Now the margin is substracted of the max widths per column, 
        # to avoid miscalculations in the wrapping of multilines in the
        # cells .
        maxWidhtPerColWithoutMargin = [width - (self.cellMargin*2) for width in maxWidhtPerCol]

        # Here each column is checked to see if there are 0 len columns 
        # (due to reduced space). If it is the case, the width is
        # incremented to fit the minimu width of a column (constant),
        # and the widest column gets decreased to keep to total width
        # the same 
        for current in range(len(maxWidhtPerColWithoutMargin)):

            # the biggest is re-calculated each time in case that the one
            # that was is no longer, because it will be reduced 
            biggestWidth = max(maxWidhtPerColWithoutMargin)
            biggestWidth = maxWidhtPerColWithoutMargin.index(biggestWidth)

            currentWidth = maxWidhtPerColWithoutMargin[current]
            if currentWidth < MIWCOL:
                incremented = 0
                while currentWidth <= MIWCOL:
                    currentWidth += 1
                    incremented += 1
                maxWidhtPerColWithoutMargin[current] = currentWidth
                maxWidhtPerColWithoutMargin[biggestWidth] -= incremented




        return maxWidhtPerColWithoutMargin, maxWidhtOfColumns

    def adjustWidthToWindow(self, columnWidths):
        '''
        Returns new columnWidths depending if the expandToWindow option is set to
        True and the size of the window.
        '''
        maxWidthOfTable = self.getMaxWidth(columnWidths=columnWidths)

        if self.expandToWindow == True:
            return maxWidthOfTable[0] # The max widths per column
        else:
            if maxWidthOfTable[1] < sum(columnWidths):
                return maxWidthOfTable[0]
            else:
                return columnWidths

    

class Cells(object):
    '''
    Recives the tabular data and the procesed column widths along with the
    margin to format (add spaces or make multilines) each cell.
    '''

    def __init__(self, tabularData, columnWidths, cellMargin, alignments):
        self.columnWidths = columnWidths
        self.tabularData = tabularData
        self.cellMargin = cellMargin
        self.alignments = alignments

    def wrapSingleCell(self, cell, maxWidth):
        '''
        Wrapes the string in the cell by adding a new line scape code
        with the max width as determinant.
        '''
        return textwrap.fill(cell, maxWidth)

    def wrapSingleRow(self, row):
        '''
        Creates a multiline array, being the number lines the number of
        new lines in the cell that contains the most.
        '''
        
        rows = [row]
        linesAdded = 0

        currentCol = 0
        for cell in row:
            parts = cell.splitlines()

            if len(parts)-1 > linesAdded:
                for x in range((len(parts)-1) - linesAdded):
                    linesAdded += 1
                    rows.append(['' for cell in row])
            
            if len(parts) > 1:
                for line in range(len(parts)):
                    rows[line][currentCol] = parts[line]
            
            currentCol += 1
        
        return rows

    # def getWrapInfo(self):
    #     '''
    #     Returns a list of lists. Each is a multiline, and contain the
    #     indexes of the rows that will conform the same line.
    #     '''
    #     multiLines = []

    #     currentLine = 0
    #     for multiline in self.tabularData:
    #         multiLines.append([])
    #         for row in multiline:
    #             multiLines[-1].append(currentLine)
    #             currentLine += 1

    #     return multiLines
    
    def wrapRows(self):
        '''
        Makes the tabularData a list of list's. Each list is a multiline,
        containing the rows that conforms it.
        Returns Nothing.
        '''

        maxWidhts = self.columnWidths

        currentRow = 0
        for row in self.tabularData:
            currentCell = 0
            for cell in row:
                currWidth = maxWidhts[currentCell]

                if len(cell) > currWidth:
                    cell = self.wrapSingleCell(cell, currWidth)
                    self.tabularData[currentRow][currentCell] = cell
            
                currentCell += 1

            rowToWrap = self.tabularData[currentRow]
            wrapedRow = self.wrapSingleRow(rowToWrap)
            self.tabularData[currentRow] = wrapedRow

            currentRow += 1
        
    def formatSingleCell(self, extraSpace):
        '''
        Calculates the blanks spaces in the left and right of the cell.
        Returns: leftPart, rightPart.
        '''

        mrg = self.cellMargin

        if self.alignments == 'left':
            leftPart = ' ' * mrg 
            rightPart = (' ' * extraSpace) + leftPart
        elif self.alignments == 'center':

            leftSpace = extraSpace // 2
            rightSpace = extraSpace - leftSpace
            leftPart = (' ' * mrg) + ' ' * leftSpace
            rightPart = (' ' * mrg) + ' ' * rightSpace

        elif self.alignments == 'right':
            rightPart = ' ' * mrg 
            leftPart = (' ' * extraSpace) + rightPart
        
        return leftPart, rightPart

            

    def format(self):
        '''
        Here the aligments of the text in the cells occurs by adding
        spaces.
        '''
        
        widths = self.columnWidths
        dataToFormat = self.tabularData

        # Get the len of the string in the current cell
        lenOfStr = lambda mtline, row, col: len(dataToFormat[mtline][row][col])

        currentMultiline = 0 # The actual multiline in wich rows to work
        for multiline in self.tabularData:
            currentRow = 0 # Current row of the tabularData iterated.
            for row in multiline:
                currentCol = 0 # It's the same that the curren cell.
                for cell in row:
                    extraSpace = widths[currentCol] - lenOfStr(currentMultiline, currentRow, currentCol)
                    formatForCel = self.formatSingleCell(extraSpace)
                    left = formatForCel[0]
                    right = formatForCel[1]
                    dataToFormat[currentMultiline][currentRow][currentCol] = left + cell + right 

                    currentCol += 1
                currentRow += 1
            currentMultiline += 1

        return dataToFormat
    
#-----------------------------------------------------------------------
""" 
FORMATION OF THE TABLE

Main Class.
Here the whole table is formed
"""

class Table(object):
    '''
    Makes table out of tabular like data:

    >>> tabularData: list[list[any]]
    >>> headers: 'first' | list[] 
    >>> style: str
    >>> strAlign: 'left' | 'center' | 'right'
    >>> expandToWindow: True | False
    '''  
    
    def __init__(
        self,
        tabularData,
        headers=None,
        style='clean',
        strAlign='left',
        expandToWindow=False
    ):
        self.data = tabularData
        self.headers = headers
        self.style = style
        self.strAlign = strAlign
        self.expandToWindow = expandToWindow
        self.formatedCells = []
        self.formatedSeparators = ()
        self.formatedDataRows = ()
    
    def sepExists(self, separator):
        """
        This checks if the separator is unused by checking if is None, in which case
        returns an empty ('') string.

        If the separator is used (exists), returns separator + '\\n'
        """

        if separator == None:
            return ''
        else:
            return separator + '\n'

    def compose(self):
        '''
        Joining of all the parts of the table
        '''
        
        # Finished string separators to put in the final table
        headSuperSep = self.sepExists(self.formatedSeparators.headerSuperior)
        headInferSep = self.sepExists(self.formatedSeparators.headerInferior)
        startWithNoHeadSep = self.sepExists(self.formatedSeparators.startWithNoHeader)
        bodySep = self.sepExists(self.formatedSeparators.tableBody)
        endSep = self.sepExists(self.formatedSeparators.tableEnd)

        # The data rows in arrays so wether or not is multi-line it will join all in 
        # each array with separators. If it is a multi line, it will result in
        # multiple rows betwin two separators, if not, only one, but the structure of 
        # "every table row in arrays" is the same.
        headerRows = self.formatedDataRows.header
        bodyRows = self.formatedDataRows.tableBody

        headerString = ''.join(headerRows)
        completeRows = [''.join(multiline) for multiline in bodyRows]
        bodyString = f'{bodySep}'.join(completeRows)

        # Yes! Here is the final product in a string. A fully formed table :).
        fullTableString = ''.join([
            headSuperSep,
            headerString,
            headInferSep,
            startWithNoHeadSep,
            bodyString,
            endSep
        ])

        return fullTableString
            
    def make(self):
        '''
        This crafts the separators and data rows of the table.

        Returns a table in the form of a string.
        '''
        composition = _styleCompositions[self.style]
        margin = composition.tableOptions.margin
        windowSize = Utils.getWIndowsSize()

        headerIncluded = True if (
            self.headers == 'first' or Utils.isarray(self.headers)
            ) else False
        
        if Utils.isarray(self.headers):
            self.headers = 'first'
            self.data.insert(0, self.headers)

        cellsData = TableMeasures(
            expandToWindow=self.expandToWindow,
            rawData=self.data,
            cellMargin=margin,
            composition=composition,
            windowSize=windowSize
            )
        cellsWidths = cellsData.getRawDataCellsWidths()
        columnWidths = cellsData.getFullColumnWidths(cellsWidths)
        adjustedColumnWidths = cellsData.adjustWidthToWindow(columnWidths)

        cellsAdjustment = Cells(
            tabularData=self.data,
            columnWidths=adjustedColumnWidths,
            cellMargin=margin,
            alignments=self.strAlign
            )

        # wrap the rows that exceed the width limit
        cellsAdjustment.wrapRows()

        formatedCells = cellsAdjustment.format()
        self.formatedCells = formatedCells
 
        obtainedSeparators = Separators(
            headerIncluded=headerIncluded,
            alignments=[],                              # Correct
            cellMargin=margin,
            composition=composition,
            colsWidth=adjustedColumnWidths
            )
        obtainedSeparators = obtainedSeparators.makeAll()
        self.formatedSeparators = obtainedSeparators


        obtainedRows = DataRows(
            adjustedTableCells=formatedCells,
            composition=composition,
            headers=self.headers
            )
        obtainedRows = obtainedRows.makeAll()
        self.formatedDataRows = obtainedRows
    
        return self.compose()

#-----------------------------------------------------------------------

if __name__ == '__main__':

    print('This is not supposed to be executed!')

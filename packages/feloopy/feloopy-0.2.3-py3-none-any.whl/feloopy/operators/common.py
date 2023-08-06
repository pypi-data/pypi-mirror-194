import pip
import timeit 
import os
import sys
import pandas as pd
import numpy as np
import itertools as it
import matplotlib.style as style
import matplotlib.pyplot as plt

from tabulate import tabulate as tb

sets = it.product

def install(package):
    '''
    Package Installer!
    ~~~~~~~~~~~~~~~~~~

    *package: enter a string representing the name of the package (e.g., 'numpy' or 'feloopy')

    '''

    if hasattr(pip, 'main'):
        pip.main(['install', package])
        pip.main(['install', '--upgrade', package])
    else:
        pip._internal.main(['install', package])
        pip._internal.main(['install', '--upgrade', package])

def uninstall(package):
    '''
    Package Uninstaller!
    ~~~~~~~~~~~~~~~~~~~~

    *package: enter a string representing the name of the package (e.g., 'numpy' or 'feloopy')

    '''

    if hasattr(pip, 'main'):
        pip.main(['uninstall', package])
    else:
        pip._internal.main(['unistall', package])

def begin_timer():
    '''
    Timer Starts Here!
    ~~~~~~~~~~~~~~~~~~
    '''
    global StartTime
    StartTime = timeit.default_timer()
    return StartTime

def end_timer(show=False):
    '''
    Timer Ends Here!
    ~~~~~~~~~~~~~~~~
    '''
    global EndTime
    EndTime = timeit.default_timer()
    sec = round((EndTime - StartTime), 3)% (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    if show:
        print("Elapsed time (microseconds):", (EndTime-StartTime)*10**6)
        print("Elapsed time (hour:min:sec):", "%02d:%02d:%02d" % (hour, min, sec))
    return EndTime

def load_from_excel(data_file: str, data_dimension: list, number_of_row_id_cols: int, number_of_col_id_rows: int, indices_list: list, sheet_name: str, path=None):
        
        '''
        Multi-Dimensional Excel Parameter Reader! 
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        *data_file: Name of the dataset file (e.g., data.xlsx)
        *data_dimension: data_dimension of the dataset
        *number_of_row_id_cols: Number of indices that exist in each row from left (e.g., 0, 1, 2, 3...)
        *number_of_col_id_rows: Number of indices that exist in each column from top (e.g., 0, 1, 2, 3...)
        *indices_list: The string which accompanies index counter (e.g., if row0, row1, ... and col0,col1, then index is ['row','col'])
        *sheet_name: Name of the excel sheet in which the corresponding parameter exists.
        *path: specify directory of the dataset file (if not provided, the dataset file should exist in the same directory as the code.)
        '''
        if path == None:
            data_file = os.path.join(sys.path[0], data_file)
        else:
            data_file = path

        parameter = pd.read_excel(data_file, header=[i for i in range(number_of_col_id_rows)], index_col=[i for i in range(number_of_row_id_cols)], sheet_name=sheet_name)

        if (number_of_row_id_cols == 1 and number_of_col_id_rows == 1) or (number_of_row_id_cols == 1 and number_of_col_id_rows == 0) or (number_of_row_id_cols == 0 and number_of_col_id_rows == 0) or (number_of_row_id_cols == 0 and number_of_col_id_rows == 1):

            return parameter.to_numpy()

        else:

            created_par = np.zeros(shape=([len(i) for i in data_dimension]))

            for keys in it.product(*data_dimension):

                try:

                    created_par[keys] = parameter.loc[tuple([indices_list[i]+str(keys[i]) for i in range(number_of_row_id_cols)]), tuple([indices_list[i]+str(keys[i]) for i in range(number_of_row_id_cols, len(indices_list))])]

                except:

                    created_par[keys] = None

            return created_par

def version(INPUT):

    print(INPUT.__version__)
    
    return(INPUT)

def sensitivity(model_function, params_list, range_of_change=[-10, 10], step_of_change=1, show_table=True, show_plot=False, save_plot=False, file_name='sensfig.png', plot_style='ggplot', legends_list=None, axis_names=['% Change', 'Objective Value'], size_of_fig=[[8, 6], 80]):
    '''

    Sensitivity Analyser
    ~~~~~~~~~~~~~~~~~~~~

    * model_function (Function): The function that contains the model, its corresponding solve command, and returns its object.
    * params_list (List): A list of parameters (e.g., [a], or [a,b])
    * range_of_change (List): A list of two values that specify the range of sensitivity analysis (e.g., [-10, 10] is between -10% and 10%)
    * step_of_change (Integer): A number which specifies the step of change.
    * show_table (Boolean): If a table of the results is required = True
    * show_plot (Boolean): If a plot of the results is required = True
    * save_plot (Boolean): If the plot should be saved = True (save directory is where the code is running)
    * file_name (String): The name and format of the file being saved (e.g., fig.png)
    * plot_style (String): Provide the style desired (e.g., 'seaborn-dark','seaborn-darkgrid','seaborn-ticks','fivethirtyeight','seaborn-whitegrid','classic','_classic_test','seaborn-talk', 'seaborn-dark-palette', 'seaborn-bright', 'seaborn-pastel', 'grayscale', 'seaborn-notebook', 'ggplot', 'seaborn-colorblind', 'seaborn-muted', 'seaborn', 'seaborn-paper', 'bmh', 'seaborn-white', 'dark_background', 'seaborn-poster', or 'seaborn-deep')
    * legends_list (List): Provide the legend Required (e.g., ['a','b'])
    * axis_names: Specify the x-axis and y-axis title
    * size_of_fig: Specify the size and dpi of the figure (e.g., [[8,6], 80] )
    '''

    OrigRange = range_of_change.copy()

    ObjVals = [[] for i in params_list]

    NewParamValues = params_list.copy()

    data = [dict() for i in params_list]

    if show_plot:
        plt.figure(figsize=(size_of_fig[0][0], size_of_fig[0][1]), dpi=size_of_fig[1])

    for i in range(0, len(params_list)):

        OriginalParameterValue = np.asarray(params_list[i])

        SensitivityPoints = []
        Percent = []

        range_of_change = OrigRange.copy()

        diff = np.copy(range_of_change[1]-range_of_change[0])

        for j in range(0, diff//step_of_change+1):

            Percent.append(range_of_change[0])

            SensitivityPoints.append(OriginalParameterValue*(1+range_of_change[0]/100))

            range_of_change[0] += step_of_change

        NewParamValues = params_list.copy()

        data[i]['points'] = SensitivityPoints

        for SensitivityPointofaParam in SensitivityPoints:

            NewParamValues[i] = SensitivityPointofaParam

            m = model_function(*tuple(NewParamValues))

            ObjVals[i].append(m.get_obj())

        x = Percent
        y = ObjVals[i]

        data[i]['change'] = x
        data[i]['objective'] = y

        if show_table:
            print()
            print(f"SENSITIVITY ANALYSIS (PARAM: {i+1})\n --------")
            print(
                tb({
                    "% change": x,
                    "objective value": y
                },
                    headers="keys", tablefmt="github"))
            print()

        if show_plot:

            style.use(plot_style)

            default_x_ticks = range(len(x))

            plt.xlabel(axis_names[0], size=12)

            plt.ylabel(axis_names[1], size=12)

            if legends_list == None:

                plt.plot(default_x_ticks, y,
                         label=f"Parameter {i}", linewidth=3.5)

            else:

                plt.plot(default_x_ticks, y, label=legends_list[i], linewidth=3.5)

            plt.scatter(default_x_ticks, y)

            plt.xticks(default_x_ticks, x)

    if show_plot and len(params_list) >= 2:

        plt.legend(loc="upper left")

    if show_plot and save_plot:

        plt.savefig(file_name, dpi=500)

    if show_plot:

        plt.show()

    return pd.DataFrame(data)
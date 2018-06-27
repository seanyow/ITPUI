from enum import Enum
import pandas as pd


class FileType(Enum):
    VLOG = 0
    VOMSII = 1
    V2PS = 2


class DataFrame:
    def __init__(self, data, file_type=FileType.VOMSII):
        self.__fileType = file_type  # 0 - VLOG, 1 - VOMSII, 2 - V2PS
        if type(data) is pd.DataFrame:
            self.__dataFrame = data
        else:
            self.__dataFrame = self.__readfile__(data)
        self.__columns = self.__get_columns()

    """
    Method to get DataFrame
    """

    def get_df(self):
        return self.__dataFrame

    """
    Method that returns a list containing column names
    """

    def get_columns(self):
        return self.__columns

    """
    Method to get the data type of each column
    """

    def get_column_datatypes(self):
        return self.__dataFrame.dtypes.astype(str).tolist()

    """
    Method to get data from a specific row based on index. Starts from 1
    """

    def get_row(self, row):
        # If row exists/is valid
        if 0 < row <= len(self.__dataFrame):
            return self.__dataFrame.iloc[row - 1]

        print("Invalid Row: No such row in DataFrame")
        return

    """
    Method to get number of rows
    """

    def len(self):
        return len(self.__dataFrame)

    """
    Methode to get filtered data
    """

    def get_filtered(self, conditions=[]):
        data_frame = self.__dataFrame

        con = ''
        for condition in conditions:
            if condition is not conditions[0]:
                con += " | "
            con += ('(data_frame["%s"] %s %s)' % condition)

        exec ('data_frame = (data_frame.loc[%s])' % con)

        return data_frame

    """
    Method to get data for a 2D Graph
    """

    def get_2D_data(self, x_axis, y_axis, conditions=None, clean=False):
        # If X-axis is not a column in DataFrame
        if not self.__does_column_exist(x_axis):
            print("Unknown column:'" + x_axis + "' does not exist")
            return
        # If Y-axis is not a column in DataFrame
        if not self.__does_column_exist(y_axis):
            print("Unknown column:'" + y_axis + "' does not exist")
            return

        # Filter Data is condition given
        if conditions is not None:
            data_frame = self.get_filtered(conditions)
        else:
            data_frame = self.__dataFrame
        # Get data based on given axis
        data_frame = data_frame[[x_axis, y_axis]]

        # Clean DataFrame
        if clean:
            data_frame = self.__clean_data(data_frame)

        return data_frame

    """
    Method to get data for a 3D Graph
    """

    def get_3D_data(self, x_axis, y_axis, z_axis):
        # If X-axis is not a column in DataFrame
        if not self.__does_column_exist(x_axis):
            print("Unknown column:'" + x_axis + "' does not exist")
            return
        # If Y-axis is not a column in DataFrame
        if not self.__does_column_exist(y_axis):
            print("Unknown column:'" + y_axis + "' does not exist")
            return
        # If Z-axis is not a column in DataFrame
        if not self.__does_column_exist(z_axis):
            print("Unknown column:'" + y_axis + "' does not exist")
            return

        # Get data based on given axis
        data_frame = self.__dataFrame[[x_axis, y_axis, z_axis]]

        # Clean DataFrame
        data_frame = self.__clean_data(data_frame)

        return data_frame

    """
    Method to read file and store file data as a DataFrame
    """

    def __readfile__(self, file):
        # If file is empty. -- REDUNDANT ERROR HANDLING --
        if file is None:
            print("Missing File: No file given")
            return

        # Reads VLOG    -- FOR FUTURE SCALABILITY --
        if self.__fileType is FileType.VLOG:
            return
        # Read VOSMII
        elif self.__fileType is FileType.VOMSII:
            # TODO: 'skiprows' should be customisable by user
            return pd.read_excel(file, skiprows=[])
        # Reads V2PS    -- FOR FUTURE SCALABILITY --
        elif self.__fileType is FileType.V2PS:
            return
        # Unknown FileType  TODO: Upgrade for better error handling
        else:
            print("Unknown FileType: File is not of VLOG, VOSMII or V2PS")
            return

    """
    Method to read file and obtain column names
    """

    def __get_columns(self):
        # If DataFrame is empty. -- REDUNDANT ERROR HANDLING --
        if self.__dataFrame is None:
            print("Missing Data: DataFrame is empty")
            return

        return self.__dataFrame.columns.astype(str).tolist()

    """
    Method to check if a given column name exists
    """

    def __does_column_exist(self, column):
        if column in self.__columns:
            return True
        return False

    """
    Method to remove 'Nan' data in DataFrame and convert data to appropriate file types. Returns cleaned DataFrame
    -- UPGRADE AND REEVALUATION REQUIRED --
    """

    def __clean_data(self, data_frame):
        # Remove rows containing 'Nan'
        df = data_frame.dropna()

        # TODO: Convert data to appropriate file types(eg. str to datetime)

        return df

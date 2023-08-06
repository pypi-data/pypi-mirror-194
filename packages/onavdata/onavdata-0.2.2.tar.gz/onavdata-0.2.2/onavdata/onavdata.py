import os
import toml
import pandas as pd
import numpy as np
from collections import OrderedDict
from onavdata.utils.dataframe_utils import read_from_ide
TIME_COL = 'TimeFromStart (s)'

# Load config information, pointing to data sets.
# Append private config, if available.
path_config = os.path.join(os.path.dirname(__file__), 'configs', 'config.toml')
path_private_config = os.path.join(os.path.dirname(__file__),
                                   'configs',
                                   'private-config.toml')
config = toml.load(path_config)
# Make path absolute
path_dataset = config['onavdata-data']['path_parentdir']
path_dataset = os.path.join(os.path.dirname(__file__),
                            path_dataset)
config['onavdata-data']['path_parentdir'] = path_dataset
if os.path.isfile(path_private_config):
    config.update(toml.load(path_private_config))
del path_config
del path_private_config


def add_dataset(name, path):
    """Add existing dataset with shornames

    Inputs
        name: Name of the dataset
        path: Path to dataset which includes the shortnames
    """
    config[name] = dict()
    config[name]['path_parentdir'] = path


def get_shortname_dict(config):
    """
    {key:shortname, value:
        {paths: {dict of paths},
         description: description string}
    }

    """
    shortname_dict = {}
    # print("Data Sets Found:")
    for dataset in config:
        # print('\t', dataset)
        path_dataset = config[dataset]['path_parentdir']
        path_shortnames = os.path.join(path_dataset, 'shortnames.txt')
        shortnames = toml.load(path_shortnames)

        while len(shortnames) > 0:
            sname, paths_dict = shortnames.popitem()

            # Append base path to relative paths inside dataset `shortnames`
            # file.
            for key in ['data', 'meta']:
                # Handle nested lists of paths
                if type(paths_dict[key]) == list:
                    for i in range(len(paths_dict[key])):
                        paths_dict[key][i] = os.path.join(path_dataset,
                                                          paths_dict[key][i])
                else:
                    paths_dict[key] = os.path.join(path_dataset,
                                                   paths_dict[key])
            shortname_dict[sname] = {}
            shortname_dict[sname]['paths'] = paths_dict
            if 'description' in paths_dict:
                shortname_dict[sname]['description'] = paths_dict[
                        'description']

    return shortname_dict


def print_shortnames(description=False):
    """
    Print all shortnames found.  Associated descriptions will be printed if
    `description` set to True.
    """
    shortname_dict = get_shortname_dict(config)
    for sname in sorted(shortname_dict):
        print('\t', sname)
        if description:
            if 'description' in shortname_dict[sname]:
                print(shortname_dict[sname]['description'])
            else:
                print("(No description available)")


def get_data(shortname=None):
    """
    If no shortname is specified, a sample data set will be returned.
    """
    # TODO: this shouldn't be reloaded everytime.  Or maybe it should?
    shortname_dict = get_shortname_dict(config)
    if shortname is None:
        shortname = list(shortname_dict.keys())[0]
        print('get_data(): No shortname specified so choice will be arbitrary.'
              '  Returning: %s' % shortname)

    assert shortname in shortname_dict, 'Requested `shortname` not found.'

    path_meta = shortname_dict[shortname]['paths']['meta']
    meta = toml.load(path_meta, _dict=OrderedDict)

    path_data_list = shortname_dict[shortname]['paths']['data']

    return get_data_direct(path_data_list, meta)


def get_data_direct(path_data_list, meta):
    """
    Load dataset (string or list of paths) using meta
    dictionary supplied.
    """
    if type(path_data_list) == str:
        path_data_list = [path_data_list]

    df_list = []
    for path_data in path_data_list:
        if path_data.upper().endswith('.IDE'):
            # Load IDE format
            df = read_from_ide(path_data)
        else:
            # Assuming CSV format supported by `pd.read_csv` method
            # Check if associated zip-file is available.  If so, use that.
            if os.path.isfile(path_data+'.zip'):
                path_data = path_data+'.zip'

            # Skip lines, if requested (e.g. multi-line header).
            skiprows = None
            if 'skip-lines' in meta:
                skiprows = meta['skip-lines']

            df = pd.read_csv(path_data, skipinitialspace=True, skiprows=skiprows)

        df = apply_meta(df, meta, path_data=path_data)
        df_list.append(df)
    df = pd.concat(df_list, axis=1)

    # Handle duplicate columns.
    cnt_dupcol = df.columns.duplicated().sum()
    if cnt_dupcol > 0:
        print(("Duplicate columns found (%d)."
               "  Taking non-NAN column values.") % cnt_dupcol)
        # For a given row, take the non-na value
        for col in df.columns[df.columns.duplicated()]:
            df[col] = df[col].bfill(axis=1).iloc[:, 0]
        # Drop duplicates
        df = df.loc[:, ~df.columns.duplicated(keep='first')]

    # Reorder columns using 'columns-rename', if specified,
    # while handling that not all columns are part of the rename meta.
    if 'columns-rename' in meta:
        cols = OrderedDict.fromkeys(meta['columns-rename'].values())
        if TIME_COL in cols:
            cols.pop(TIME_COL)
        # Columns not part of the rename are appended to the end.
        cols.update(OrderedDict.fromkeys(df.columns.copy()))
        cols = list(cols.keys())

        df = df[cols]

    return df

def apply_meta(dfin, meta, path_data='None Supplied'):
    """
    Returns a dataframe with meta parameters applied.
    The input dataframe `dfin` is unchanged working with a copy.

    If available, `path_data` is used to print useful status or
    warning messages.
    """
    df = dfin.copy(deep=True)
    # Strip lingering tabs from columns.
    df.columns = [c.lstrip('\t') for c in df.columns]
    df.columns = [c.strip('\t') for c in df.columns]

    # Optionally drop unnamed columns
    if ('drop-unnamed' in meta) and meta['drop-unnamed']:
        cols_unnamed = df.columns.str.contains('unnamed', case=False)
        df.drop(df.columns[cols_unnamed], axis=1, inplace=True)

    # Specify columns to be loaded.
    # Some columns specified to be used or dropped may not be present
    # in the current path_data.  This is handled.
    if ('columns-use' in meta) and ('columns-drop' in meta):
        raise AttributeError("%s meta cannot specify both 'columns-use' "
                             "and 'columns-drop'." % shortname)

    if 'columns-use' in meta:
        colsuse = meta['columns-use']
        if not isinstance(colsuse, list):
            colsuse = [colsuse]
        colsuse = list(set(df.columns) & set(colsuse))
        colsuse.sort()
        df = df[colsuse]

    if 'columns-drop' in meta:
        colsdrop = meta['columns-drop']
        if not isinstance(colsdrop, list):
            colsdrop = [colsdrop]
        colsdrop = list(set(df.columns) & set(colsdrop))
        df = df.drop(columns=colsdrop)

    # Drop rows based on specified value(s).
    if 'drop-rows-where' in meta:
        for key, value in meta['drop-rows-where'].items():
            # Handle both scalar or list of values.
            if not isinstance(value, list):
                value = [value]
            df = df[~df[key].isin(value)]

    # Keep rows based on specified value(s).
    if 'keep-rows-where' in meta:
        for key, value in meta['keep-rows-where'].items():
            # Handle both scalar or list of values.
            if not isinstance(value, list):
                value = [value]
            df = df[df[key].isin(value)]

    if 'keep-rows-gt' in meta:
        for key, value in meta['keep-rows-gt'].items():
            try:
                df = df[df[key].gt(value)]
            except Exception:
                raise ValueError('Unexpected `keep-rows-gt` entry '
                                 'encountered for `[%s]`' % key)

    if 'keep-rows-lt' in meta:
        for key, value in meta['keep-rows-lt'].items():
            try:
                df = df[df[key].lt(value)]
            except Exception:
                raise ValueError('Unexpected `keep-rows-lt` entry '
                                 'encountered for `[%s]`' % key)

    if 'keep-rows-between' in meta:
        for key, value in meta['keep-rows-between'].items():
            try:
                df = df[df[key].between(*value)]
            except Exception:
                raise ValueError('Unexpected `keep-rows-between` entry '
                                 'encountered for `[%s]`' % key)

    # Override default dtypes.
    # The dtype names must be acceptable to pd.DataFrame.astype() function.
    if 'columns-dtype' in meta:
        df = df.astype(dtype=meta['columns-dtype'])

    # Round columns to decimals specified.
    if 'columns-round-decimals' in meta:
        for key, value in meta['columns-round-decimals'].items():
            try:
                df[key] = df[key].round(value)
            except KeyError:
                print(('No matching `columns-round` entry '
                       'encountered for `[{}]`\n'
                       '\tFile: {}').format(
                                        key,
                                        path_data.split(os.path.sep)[-1]))
                continue

    # Subtract offset from columns, if present. Note, this can/should be skipped
    # for multiple-file datasets.
    if 'columns-subtract-offset' in meta:
        for key, value in meta['columns-subtract-offset'].items():
            try:
                df[key] -= float(value)
            except KeyError:
                print(("No matching `columns-subtract-offset` entry found in file.\n"
                       "\columns-subtract-offset.{}\n"
                       "\tFile: {}").format(
                                        key,
                                        path_data.split(os.path.sep)[-1]))
                continue


    # Scale columns, if present.  Note, this can/should be skipped
    # for multiple-file datasets.
    if 'columns-scale' in meta:
        for key, value in meta['columns-scale'].items():
            try:
                df[key] *= float(value)
            except KeyError:
                print(("No matching `columns-scale` entry found in file.\n"
                       "\columns-scale.{}\n"
                       "\tFile: {}").format(
                                        key,
                                        path_data.split(os.path.sep)[-1]))
                continue

    # Rename columns.
    if 'columns-rename' in meta:
        df = df.rename(columns=meta['columns-rename'])

    # Apply Rotations, if present.  Note, this can/should be skipped
    # for multiple-file datasets.
    # NOTE: The rotations are applied AFTER any column renaming.
    #       Hence, the key entries should refer to the renamed column
    #       names.
    if 'Rsensor2body' in meta:
        Rdict = meta['Rsensor2body']
        for key in Rdict:
            cols = [col for col in df if col.startswith(key)]
            if len(cols) == 0:
                print(("No matching Rsensor2body columns found in file.\n"
                       "\tRsensor2body.{}\n"
                       "\tFile: {}").format(
                                        key,
                                        path_data.split(os.path.sep)[-1]))
                continue
            # Sort the columns so that we end up with the order: X->Y->Z
            # where these are in the `sensor` frame.
            cols.sort()
            assert len(cols) == 3, ("Invalid number of matching columns "
                                    "found for Rsensor2body.{}:\n"
                                    "cols found: {}").format(key, cols)

            # Apply transformation:
            #   [x1, x2, ... xm]                   [x1, x2, ... xm]
            #   [y1, y2, ... ym]  =   Rsensor2body [y1, y2, ... ym]
            #   [z1, y3, ... ym]                   [z1, y3, ... ym]
            #                   body                               sensor
            # We transpose the entire expression in order to be able
            # to work with and store the Pandas DataFrame directly.
            Rsensor2body = np.array(Rdict[key], dtype=float)
            df[cols] = df[cols] @ Rsensor2body.transpose()

    # Check for time column and attempt to populate if it doesn't exist.
    if df.index.name != TIME_COL:
        if TIME_COL not in df:
            if 'SampleFreq (Hz)' in meta:
                dt_sec = 1.0/meta['SampleFreq (Hz)']

                df[TIME_COL] = df.index * dt_sec
            else:
                print("Unable to index time information.")
        df.set_index(TIME_COL, inplace=True)

    # Remove rows with duplicate index.
    cnt_dupind = df.index.duplicated().sum()
    if cnt_dupind > 0:
        print("Duplicate indices found (%d).  Keeping first." % cnt_dupind)
        df = df[~df.index.duplicated(keep='first')]

    # Add any columns specified via meta file.
    if 'add-columns' in meta:
        for key, value in meta['add-columns'].items():
            try:
                df[key] = df[value].copy()
            except KeyError:
                df[key] = value
            except Exception:
                raise ValueError('Unexpected `add-columns` entry '
                                 'encountered for `[%s]`' % key)
    return df


if __name__ == '__main__':
    print("Data Shortnames Found:")
    print_shortnames(description=True)

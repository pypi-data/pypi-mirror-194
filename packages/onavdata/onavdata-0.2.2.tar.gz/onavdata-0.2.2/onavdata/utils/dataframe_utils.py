import pandas as pd
import numpy as np
import idelib

mm_to_m = 1e-3


def get_columns(df, startswith_str):
    """
    Returns list of columns in data-frame `df` which begin with the
    `startswith_str` string.  The list is sorted prior to return.  This ensures
    the return order will be X->Y->Z for 3-axis sensors.
    """
    cols = [col for col in df if col.startswith(startswith_str)]
    cols.sort()
    return cols


def get_accel_cols(df, startswith_str='Accel', verbose=False):
    cols = get_columns(df, startswith_str)
    if verbose:
        print('Accel Columns Found:\n\t'+'\t'.join(['%s' % c for c in cols]))
    return cols


def get_gyro_cols(df, startswith_str='AngleRate', verbose=False):
    cols = get_columns(df, startswith_str)
    if verbose:
        print('Gyro Columns Found:\n\t'+'\t'.join(['%s' % c for c in cols]))
    return cols


def get_mag_cols(df, startswith_str='MagField', verbose=False):
    cols = get_columns(df, startswith_str)
    if verbose:
        print('Mag Columns Found:\n\t'+'\t'.join(['%s' % c for c in cols]))
    return cols


def convert_deg2rad(df, inplace=False):
    """ Convert any column units from (deg*) to (rad*)
    (e.g. Euler angles and/or gyro measurements)
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    for col in df_out.columns:
        if '(deg' in col:
            print("Converting '%s' readings from (deg*) to (rad*)." % col)
            df_out[col] = np.deg2rad(df_out[col])
            df_out.rename(columns={col: col.replace('(deg', '(rad')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def convert_rad2deg(df, inplace=False):
    """ Convert any column units from (rad*) to (deg*)
    (e.g. Euler angles and/or gyro measurements)
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    for col in df_out.columns:
        if '(rad' in col:
            print("Converting '%s' readings from (rad*) to (deg*)." % col)
            df_out[col] = np.rad2deg(df_out[col])
            df_out.rename(columns={col: col.replace('(rad', '(deg')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def convert_mm2m(df, inplace=False):
    """ Convert any column units from (mm*) to (m*)
    (e.g. Height in (mm) and/or speed (mm/s) measurements)
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    for col in df_out.columns:
        if '(mm' in col:
            print("Converting '%s' readings from (mm*) to (m*)." % col)
            df_out[col] = df_out[col] * mm_to_m
            df_out.rename(columns={col: col.replace('(mm', '(m')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def convert_mG2mps2(df, mG2mps2=9.80665e-3, inplace=False):
    """ Convert any accel columns from (mG) to (m/s^2).
    The accelerometer columns are retrieved using the `get_accel_cols`
    method.
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    cols_accel = get_accel_cols(df_out)
    for col in cols_accel:
        if '(mG)' in col:
            print("Converting '%s' readings from (mG) to (m/s^2)." % col)
            df_out[col] = mG2mps2*df_out[col]
            df_out.rename(columns={col: col.replace('(mG)', '(m/s^2)')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def convert_G2mps2(df, G2mps2=9.80665, inplace=False):
    """ Convert any accel columns from (G) to (m/s^2).
    The accelerometer columns are retrieved using the `get_accel_cols`
    method.
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    cols_accel = get_accel_cols(df_out)
    for col in cols_accel:
        if '(G)' in col:
            print("Converting '%s' readings from (G) to (m/s^2)." % col)
            df_out[col] = G2mps2*df_out[col]
            df_out.rename(columns={col: col.replace('(G)', '(m/s^2)')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def convert_mps2_to_G(df, G_mps2=9.80665, inplace=False):
    """ Convert any accel columns from (m/s^2) tp (G).
    The accelerometer columns are retrieved using the `get_accel_cols`
    method.
    """
    if inplace:
        df_out = df
    else:
        df_out = df.copy()

    cols_accel = get_accel_cols(df_out)
    for col in cols_accel:
        if '(m/s^2)' in col:
            print("Converting '%s' readings from (m/s^2) to (G)." % col)
            df_out[col] = (1.0/G_mps2)*df_out[col]
            df_out.rename(columns={col: col.replace('(m/s^2)', '(G)')},
                          inplace=True)

    if inplace:
        return None
    else:
        return df_out


def read_from_ide(filepath, update_col_names=True):
    """
    Load IDE-format datafile, as saved by enDAQ devices, into
    a dataframe where the column headers are composed of sensor
    axis, and units.

    Inputs
        filepath: string
            path to IDE file (e.g. 'dataset.IDE')
        update_col_names: bool (True)
            Updates column names to match syntax used by other
            default onavdata datasets

    Returns
        dataframe: pandas dataframe
            Dataframe composed of all channles and sub-channels
    """
    ds = idelib.importFile(filepath)

    df_list = []
    # At this point, merging only subset of channels
    # is supported until `ValueError` is investigated.
    for ch in [84, 80]:
        for sch in ds.channels[ch].subchannels:
            str_col = '{}{} ({})'.format(sch.units[0],
                                         sch.axisName,
                                         sch.units[1])
            events = sch.getSession()
            times_us, data = events.arraySlice()
            times_utc = events.session.utcStartTime + times_us/1e6
            # Optional: work with datetime objects
            # times_utc_obj = (
            #     np.datetime64(events.session.utcStartTime, 's')
            #     + times_us.astype('timedelta64[us]')
            # )
            df = pd.DataFrame({str_col: data}, index=times_utc)
            df_list.append(df)
    df = pd.concat(df_list, axis=1)
    ds.close()

    # Reset index and maintain two time columns:
    #   Absolute: UTC time
    #   Relative: `TimeFromStart (s)`
    df.index.name = 'TimeUTC'
    df['TimeFromStart (s)'] = (df.index - df.index[0])
    df.reset_index(inplace=True)

    if update_col_names:
        df.rename(columns={
                  'AccelerationX (g)': 'AccelX (G)',
                  'AccelerationY (g)': 'AccelY (G)',
                  'AccelerationZ (g)': 'AccelZ (G)',
                  'RotationX (deg/s)': 'AngleRateX (deg/s)',
                  'RotationY (deg/s)': 'AngleRateY (deg/s)',
                  'RotationZ (deg/s)': 'AngleRateZ (deg/s)',
                  # 'QuaternionW (q)': 'QuaternionNavToCaseS',
                  # 'QuaternionX (q)': 'QuaternionNavToCaseI',
                  # 'QuaternionY (q)': 'QuaternionNavToCaseJ',
                  # 'QuaternionZ (q)': 'QuaternionNavToCaseK',
                  # 'TemperatureNone (°C)': 'Temperature (C)',
                  # 'TemperatureControl (°C)': 'TemperatureControl (C)'
                  },
                  inplace=True)

    return df

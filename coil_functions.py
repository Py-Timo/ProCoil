
import os
import pandas as pd
import tzlocal  # Library to get the local timezone
from datetime import datetime
#

def File(selected_coil,rxe,voltage):
    #
    file_name = None
        #print("Selections are " ,selected_coil ,  selected_rxe ,selected_voltage )
    #print("Current working directory:", os.getcwd())
    #print("Directory contents:", os.listdir('.'))
    for file in os.listdir('.'):
        #print(f"Checking file: {file}")
        #if file.startswith(selected_coil) and selected_rxe in file and selected_voltage in file:
        if selected_coil in file and rxe in file and voltage in file:
            file_name = file
            break
    #print("the file is " , file_name)
    
    if file_name is None:
        return "No matching file found"
    print("Found file is = ", file_name)
    
    # Read the file and convert the data into a dataframe ignoring the header of 8 lines and using tab as separator
    file_path = os.path.join('.', file_name)
    
    print(" Compleate Path is = " , file_path)
    #"""
    df = pd.read_csv(file_path, skiprows=9, sep='\t', engine='python', on_bad_lines='skip')
    df.columns = ['date', 'time', 'voltage']
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
    # Drop rows with NaT values in datetime column (invalid parsing)
    df.dropna(subset=['datetime'], inplace=True)
    # Get the local timezone from the operating system
    local_timezone = tzlocal.get_localzone()
    # Set timezone to ensure consistency (local timezone)
    #df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert(local_timezone)
    # Extract hours and minutes from time column for x-axis 2
    df['time_hm'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f').dt.strftime('%H:%M')
    # Take the absolute value of voltage column
    df['voltage'] = df['voltage'].abs()
    
    ####
    return df
######################################################
def File_2(selected_coil, channel, parameter):
    file_name = None
    # Search for the file matching the selected coil, channel, and parameter
    for file in os.listdir('.'):
        if selected_coil in file and channel in file and parameter in file:
            file_name = file
            break

    if file_name is None:
        return "No matching file found"

    print("Found file is =", file_name)
    
    # Construct the full file path
    file_path = os.path.join('.', file_name)
    print("Complete Path is =", file_path)
    
    # Read the file and process its data
    try:
        df = pd.read_csv(file_path, skiprows=9, sep='\t', engine='python', on_bad_lines='skip', converters={'value': float})
        df.columns = ['date', 'time', 'parameter']
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
        # Drop rows with NaT values in the datetime column (invalid parsing)
        df.dropna(subset=['datetime'], inplace=True)
        # Extract hours and minutes from the time column for simplified time representation
        df['time_hm'] = pd.to_datetime(df['time'], format='%H:%M:%S.%f').dt.strftime('%H:%M')
        # Take the absolute value of the parameter column
        df['parameter'] = df['parameter'].abs()
        return df
    except Exception as e:
        print(f"Error reading or processing the file: {e}")
        return f"Error processing the file: {e}"

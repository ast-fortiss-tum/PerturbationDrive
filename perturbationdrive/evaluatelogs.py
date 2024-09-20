import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


def _is_misplaced_float(s):
    """
    Check if a string is a misplaced float with the pattern `^\d\.\d+$`.

    Returns:
        bool: True if the string is a misplaced float, False
    """
    return bool(re.match(r"^\d\.\d+$", s))


def fix_csv_logs(file_path):
    """
    Perform the following operations on the log file:
    1. Read the CSV file.
    2. Iterate over the rows and find misplaced floats.
    3. Append the misplaced float to the end of the previous row.
    4. Shift the row to the left.
    5. Drop the last column if it is all NaN.
    6. Save the fixed dataframe to a new csv file with the suffix "_fixed".

    Parameters:
        - file_path (str): The path to the log file.
    """
    # Read the csv file
    df = pd.read_csv(file_path, header=None, dtype=str)

    # Iterate over the dataframe rows
    for i in range(1, len(df)):
        # If the first element of the row matches the misplaced float pattern
        if _is_misplaced_float(df.iloc[i, 0]):
            # Append the misplaced value to the end of the previous row
            df.iloc[i - 1, df.shape[1] - 1] = df.iloc[i, 0]
            # Shift the row to the left
            df.iloc[i] = df.iloc[i].shift(-1)

    # Drop the last column if it is all NaN as a result of the shift
    if df.iloc[:, -1].isnull().all():
        df.drop(df.columns[-1], axis=1, inplace=True)

    # Save the fixed dataframe to a new csv file
    fixed_file_path = file_path.replace(".csv", "_fixed.csv")
    df.to_csv(fixed_file_path, index=False, header=False)

    return fixed_file_path


def plot_driven_distance(file_path):
    """
    Plot the driven distance for each perturbation in the log file.

    Parameters:
        - file_path (str): The path to the log file.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Ensure that 'x_pos' and 'y_pos' are numeric
    df["x_pos"] = pd.to_numeric(df["x_pos"], errors="coerce")
    df["y_pos"] = pd.to_numeric(df["y_pos"], errors="coerce")

    # Drop rows with NaN values in 'x_pos' or 'y_pos'
    df = df.dropna(subset=["x_pos", "y_pos"])

    # Get unique perturbation names
    perturbations = df["pertubation_name"].unique()
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Create a scatter plot for each perturbation
    for perturbation in perturbations:
        subset = df[df["pertubation_name"] == perturbation]
        ax = sns.scatterplot(data=subset, x="x_pos", y="y_pos", hue="pertubation_name")
        plt.title(f"Driven distance by {perturbation}")
        plt.legend(title=perturbation)
        plt.tight_layout()
        plt.show()

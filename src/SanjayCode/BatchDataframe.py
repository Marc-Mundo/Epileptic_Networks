import pandas as pd
import numpy as np


def create_dataframe_for_variant(variant_results):
    """
    Create a pandas DataFrame that lists all the results data for a given variant.

    Args:
        variant_results: A dictionary of datasets with their respective results.

    Returns:
        A pandas DataFrame containing all the results data for the variant.
    """
    # Initialize a list to store data from all conditions and datasets
    all_data = []

    # Iterate over each dataset in the variant
    for dataset_name, dataset in variant_results.items():
        for condition, results in dataset.items():
            # Extract the cell type from the dataset name
            if "Pyr" in dataset_name:
                cell_type = "Pyr"
            elif "Bwb" in dataset_name:
                cell_type = "Bwb"
            elif "OLM" in dataset_name:
                cell_type = "OLM"
            else:
                cell_type = (
                    "Unknown"  # Use a placeholder if the cell type is not recognized"
                )

            for run_name, run_data in results.items():
                # Prepare combined mean and std fields
                run_data[
                    "Pyr(Hz)+ Pyr (Std)"
                ] = f"{np.mean(run_data['pyr_mean']):.2f}+-{np.mean(run_data['pyr_std']):.2f}"
                run_data[
                    "BWB (Hz)+ BWB (Std)"
                ] = f"{np.mean(run_data['bwb_mean']):.2f}+-{np.mean(run_data['bwb_std']):.2f}"
                run_data[
                    "OLM (Hz)+ OLM (Std)"
                ] = f"{np.mean(run_data['olm_mean']):.2f}+-{np.mean(run_data['olm_std']):.2f}"

                # Format frequencies and power
                run_data[
                    "Theta Freq (Hz)"
                ] = f"{np.mean(run_data['theta_frequencies']):.1f}"
                run_data[
                    "Theta power (mV^2 Hz^-1)"
                ] = f"{np.mean(run_data['mean_theta_power']):.2f}"
                run_data[
                    "Gamma Freq (Hz)"
                ] = f"{np.mean(run_data['gamma_frequencies']):.1f}"
                run_data[
                    "Gamma power (mV^2 Hz^-1)"
                ] = f"{np.mean(run_data['mean_gamma_power']):.2f}"

                # Add metadata
                run_data["Modified Celltype"] = cell_type
                run_data["Condition"] = condition
                run_data["Run"] = run_name

                # Append the run data to the list
                all_data.append(run_data)

    # Create a DataFrame from the compiled data
    df = pd.DataFrame(all_data)

    # Select and order the columns as required
    column_order = [
        "Pyr(Hz)+ Pyr (Std)",
        "BWB (Hz)+ BWB (Std)",
        "OLM (Hz)+ OLM (Std)",
        "Theta Freq (Hz)",
        "Theta power (mV^2 Hz^-1)",
        "Gamma Freq (Hz)",
        "Gamma power (mV^2 Hz^-1)",
        "Modified Celltype",
        "Condition",
        "Run",
    ]
    df = df[column_order]

    return df


def create_dataframe_for_variant_averaged(variant_results):
    """
    Create a pandas DataFrame that lists the averaged results data for a given variant.

    Args:
        variant_results: A dictionary of datasets with their respective results.

    Returns:
        A pandas DataFrame containing the averaged results data for the variant.
    """
    # Initialize a list to store data from all conditions and datasets
    all_data = []

    # Iterate over each dataset in the variant
    for dataset_name, dataset in variant_results.items():
        # Extract the cell type from the dataset name
        if "Pyr" in dataset_name:
            cell_type = "Pyr"
        elif "Bwb" in dataset_name:
            cell_type = "Bwb"
        elif "OLM" in dataset_name:
            cell_type = "OLM"
        else:
            cell_type = (
                "Unknown"  # Use a placeholder if the cell type is not recognized
            )

        for condition, results in dataset.items():
            # Initialize a dictionary to accumulate run data
            condition_data = {
                "pyr_mean": [],
                "pyr_std": [],
                "bwb_mean": [],
                "bwb_std": [],
                "olm_mean": [],
                "olm_std": [],
                "theta_frequencies": [],
                "mean_theta_power": [],
                "gamma_frequencies": [],
                "mean_gamma_power": [],
            }
            for run_name, run_data in results.items():
                # Append the run data to the lists in the dictionary
                for key in condition_data.keys():
                    # Take the mean of the list if it's a list, otherwise just append the value
                    value = (
                        np.mean(run_data[key])
                        if isinstance(run_data[key], list)
                        else run_data[key]
                    )
                    condition_data[key].append(value)

            # Calculate the mean across all runs for the condition
            averaged_data = {
                key: np.mean(values) for key, values in condition_data.items()
            }
            averaged_data["Modified Celltype"] = cell_type
            averaged_data["Condition"] = condition

            # Append the averaged data to the list
            all_data.append(averaged_data)

    # Create a DataFrame from the compiled data
    df = pd.DataFrame(all_data)

    # Calculate combined mean and std for the aggregated data
    df["Pyr(Hz)+ Pyr (Std)"] = df.apply(
        lambda row: f"{row['pyr_mean']:.2f}+-{row['pyr_std']:.2f}", axis=1
    )
    df["BWB (Hz)+ BWB (Std)"] = df.apply(
        lambda row: f"{row['bwb_mean']:.2f}+-{row['bwb_std']:.2f}", axis=1
    )
    df["OLM (Hz)+ OLM (Std)"] = df.apply(
        lambda row: f"{row['olm_mean']:.2f}+-{row['olm_std']:.2f}", axis=1
    )

    # Format frequencies and power
    df["Theta Freq (Hz)"] = df["theta_frequencies"].apply(lambda freq: f"{freq:.1f}")
    df["Theta power (mV^2 Hz^-1)"] = df["mean_theta_power"].apply(
        lambda power: f"{power:.2f}"
    )
    df["Gamma Freq (Hz)"] = df["gamma_frequencies"].apply(lambda freq: f"{freq:.1f}")
    df["Gamma power (mV^2 Hz^-1)"] = df["mean_gamma_power"].apply(
        lambda power: f"{power:.2f}"
    )

    # Select and order the columns as required
    column_order = [
        "Pyr(Hz)+ Pyr (Std)",
        "BWB (Hz)+ BWB (Std)",
        "OLM (Hz)+ OLM (Std)",
        "Theta Freq (Hz)",
        "Theta power (mV^2 Hz^-1)",
        "Gamma Freq (Hz)",
        "Gamma power (mV^2 Hz^-1)",
        "Modified Celltype",
        "Condition",
    ]
    df = df[column_order]

    return df


def sort_and_group_dataframe(df):
    """
    Sort the DataFrame based on 'Condition' and group by 'Dataset'.

    Args:
        df: The DataFrame to sort and group.

    Returns:
        A sorted and grouped DataFrame.
    """
    # Convert 'Condition' to a float to sort numerically (assuming the condition is like 'NA_0.5')
    df["Condition"] = df["Condition"].str.extract(r"(\d+\.\d+)").astype(float)

    # Sort the DataFrame by 'Dataset' and then by 'Condition'
    df_sorted = df.sort_values(by=["Modified Celltype", "Condition"])

    # Reset the index of the DataFrame
    df_sorted.reset_index(drop=True, inplace=True)

    return df_sorted


def split_dataframe_by_celltype(df):
    """
    Split the DataFrame into separate DataFrames based on the 'Modified Celltype' column.

    Args:
        df: A pandas DataFrame that contains a 'Modified Celltype' column.

    Returns:
        A dictionary of DataFrames, where each key is a cell type and each value is the
        corresponding DataFrame with only data for that cell type.
    """
    # Get unique cell types
    cell_types = df["Modified Celltype"].unique()

    # Create a dictionary to hold the dataframes
    dfs_by_celltype = {}

    # Split the DataFrame by cell type
    for cell_type in cell_types:
        dfs_by_celltype[cell_type] = df[df["Modified Celltype"] == cell_type]

    return dfs_by_celltype

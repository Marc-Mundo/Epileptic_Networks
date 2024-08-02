import os
import pickle
import glob
import re
from src.SanjayCode import (
    process_data,
)
import gc  # Garbage collection module


def dataset_load(data_path):
    """
    Load data from a single simulation paths for different variants.

    :param data_paths: List of paths to the datasets.
    :return: Dictionary of datasets, with each key being a variant.
    """
    dataset_data = {}

    # Determine condition type based on dataset naming convention
    if "NA" in data_path:
        conditions = [
            "NA_0.5",
            "NA_0.6",
            "NA_0.7",
            "NA_0.8",
            "NA_0.9",
            "NA_1.0",
            "NA_1.1",
            "NA_1.2",
            "NA_1.3",
            "NA_1.4",
            "NA_1.5",
        ]
    elif "K" in data_path:
        conditions = [
            "K_0.5",
            "K_0.6",
            "K_0.7",
            "K_0.8",
            "K_0.9",
            "K_1.0",
            "K_1.1",
            "K_1.2",
            "K_1.3",
            "K_1.4",
            "K_1.5",
        ]
    else:
        # Handle error or unknown dataset type
        print(f"Unknown dataset type for path: {data_path}")
        return None

    for condition in conditions:
        condition_path = f"{data_path}/{condition}"
        files = glob.glob(f"{condition_path}/*.pkl")
        data = {}
        for file in files:
            pattern = r"(\d+)"
            match = re.search(pattern, file.split("/")[-1])
            if match:
                run = match.group(1)
                with open(file, "rb") as f:
                    data[run] = pickle.load(f)
                print("Loaded:", file)  # Debugging statement
        dataset_data[condition] = data
    return dataset_data


def process_dataset(dataset_data):
    """
    Process current dataset.

    :param dataset_data: Dictionary of current datasets.
    :return: Dictionary of processed results for current dataset.
    """
    dataset_results = {}
    for condition, runs in dataset_data.items():
        condition_results = {}
        for run, run_data in runs.items():
            print(f"Processing {condition}, run {run}")  # Debugging statement
            processed_data = process_data(run_data["simData"])
            condition_results[run] = processed_data
        dataset_results[condition] = condition_results
    return dataset_results


def extract_variant(data_path):
    """
    Extract variants from the data_path and create a dictionary.

    :param data_path: Path to the datasets.
    :return: Dictionary of variants.
    """
    # Determine the type of variant based on dataset naming convention
    if "NA" in data_path:
        variant_prefix = "NA"
    elif "K" in data_path:
        variant_prefix = "K"
    else:
        print(f"Unknown dataset type for path: {data_path}")
        return None

    # Define the range of values for the variants
    values = [round(x * 0.1, 1) for x in range(5, 16)]  # 0.5 to 1.5

    # Generate the dictionary with formatted string keys
    variant_dict = {f"{variant_prefix}_{value:.1f}": value for value in values}

    return variant_dict


def extract_variant_type(data_path):
    """
    Extract the variant type from the data path.

    :param data_path: Path to the dataset.
    :return: The variant type.
    """
    # Split the path and extract the part with the cell type and variant
    parts = data_path.strip("/").split("_")
    cell_type = parts[1]
    variant = parts[2]

    # Convert to full description based on cell type and variant
    if variant == "NA":
        variant_full = "Sodium conductance"
    elif variant == "K":
        variant_full = "Potassium conductance"

    return f"{cell_type} {variant_full} (times baseline)"


def main(data_paths):
    """
    Main function to process and plot data for multiple datasets, and return a dictionary
    of results keyed by data paths.

    :param data_paths: List of paths to the datasets.
    :return: Dictionary with data paths as keys and processed data as values.
    """
    results_dir = "../Results"
    os.makedirs(results_dir, exist_ok=True)  # Ensure the directory exists
    full_results_path = os.path.join(results_dir, "results_by_path.pkl")

    # Check if the full results file already exists
    if os.path.exists(full_results_path):
        print("Full results file already exists. Loading from file.")
        with open(full_results_path, "rb") as f:
            results_by_path = pickle.load(f)
    else:
        results_by_path = (
            {}
        )  # Initialize the dictionary to store results if not loading from file
        for path in data_paths:
            filename = os.path.basename(path).replace(
                ".data", "_results.pkl"
            )  # Adjust as necessary
            file_path = os.path.join(results_dir, filename)

            # Check if individual dataset results already exist
            if os.path.exists(file_path):
                print(f"Results for {path} already exist. Skipping processing.")
                with open(file_path, "rb") as f:
                    dataset_results = pickle.load(f)
            else:
                dataset_data = dataset_load(path)
                dataset_results = process_dataset(dataset_data)

                # Save processed results for the individual dataset
                with open(file_path, "wb") as f:
                    pickle.dump(dataset_results, f)

                # Optional: Clear processed data from memory
                del dataset_data
                gc.collect()

            results_by_path[path] = dataset_results

        # Save the full results after processing all datasets
        with open(full_results_path, "wb") as f:
            pickle.dump(results_by_path, f)

    return results_by_path


# if __name__ == "__main__":
#     # List of paths to your datasets
#     dataset_paths = ["path/to/dataset1", "path/to/dataset2", ...]

#     # Run the main function
#     main(dataset_paths)

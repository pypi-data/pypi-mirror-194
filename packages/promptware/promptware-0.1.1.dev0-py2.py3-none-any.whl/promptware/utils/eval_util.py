from datalabs import load_dataset


def generate_evaluated_data(dataset_name, sub_dataset, split_name, n_samples):

    test_data = load_dataset(dataset_name, sub_dataset, split=split_name)
    n_samples = n_samples if len(test_data) > n_samples else len(test_data)

    return test_data[:n_samples]

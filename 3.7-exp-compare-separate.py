import os
import pandas as pd
from algorithm import *
import time


def exp(data: list[int], useSeparate: bool) -> tuple[int, float, float]:
    result_path = "result.bin"
    result, encoding_time = period_encode_param(
        data, result_path, use_separate=useSeparate
    )
    start = time.time()
    data_new = period_decode(result_path, use_separate=useSeparate)
    end = time.time()
    decoding_time = end - start
    if data != data_new:
        raise ValueError("Decode fails.")
    return (result / (len(data) * 4), encoding_time, decoding_time)


if not os.path.exists("exp_result"):
    os.makedirs("exp_result")

exp_data = {
    "dataset": [],
    "name": [],
    "algorithm": [],
    "compress_ratio": [],
    "encoding_time": [],
    "decoding_time": [],
}

files = os.listdir("data")
for file in files:
    dataset = file.split("_")[0]
    file_pull = os.path.join("data", file)
    df = pd.read_csv(file_pull)
    data = df["value"].tolist()
    for useSeparate in [True, False]:
        (result, encoding_time, decoding_time) = exp(data, useSeparate)
        exp_data["dataset"].append(dataset)
        exp_data["name"].append(file)
        exp_data["algorithm"].append("separate" if useSeparate else "bit-packing")
        exp_data["compress_ratio"].append(result)
        exp_data["encoding_time"].append(encoding_time)
        exp_data["decoding_time"].append(decoding_time)
        print(
            dataset,
            file,
            "separate" if useSeparate else "bit-packing",
            result,
            encoding_time,
            decoding_time,
        )

exp_data_df = pd.DataFrame(data=exp_data)
exp_data_df.to_csv(os.path.join("exp_result", "exp_compare_separate.csv"), index=False)

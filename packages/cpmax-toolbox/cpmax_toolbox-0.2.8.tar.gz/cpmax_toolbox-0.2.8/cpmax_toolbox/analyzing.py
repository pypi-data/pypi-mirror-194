import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy import signal

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("pdf")

from rich.progress import track

from cpmax_toolbox.file_repair import repair_file, parse_path
from cpmax_toolbox.vib_measurement import wait_until

import time
import subprocess
import re
import typing


def _ping_nano():
    return b"NanoVib" in subprocess.check_output(
        "netsh wlan show interfaces", shell=True
    )


def _get_most_recent_measurement(
    folder_to_analyze: Path = (Path().home() / "Downloads"),
) -> Path:
    most_recent_measurement = folder_to_analyze / "CON" / "00010101_000000_combined.txt"
    for p0 in folder_to_analyze.iterdir():
        if not p0.is_dir():
            continue

        pattern = r"\d{8}_\d{6}_combined\.txt"
        matching_files = [p for p in p0.rglob("*") if re.search(pattern, p.name)]

        for p in matching_files:
            dt_exist = datetime.strptime(
                most_recent_measurement.stem, "%Y%m%d_%H%M%S_combined"
            )
            dt_p = datetime.strptime(p.stem, "%Y%m%d_%H%M%S_combined")
            if dt_p > dt_exist:
                most_recent_measurement = p

    return most_recent_measurement


def continuous_analyzing(
    folder_to_analyze: Path = (Path().home() / "Downloads"),
) -> None:
    tnow = 10 * int(time.time() // 10)
    delta = 1
    last_analyzing = [folder_to_analyze / "CON" / "00010101_000000_combined.txt", 0]
    while True:
        tnow = wait_until(tnow, delta)
        if not _ping_nano():
            delta = 15
            continue

        p_last_measurement = _get_most_recent_measurement()
        if not p_last_measurement.exists():
            delta = 30
            continue

        if last_analyzing[0] != p_last_measurement:
            last_analyzing = [p_last_measurement, 0]

        if p_last_measurement.stat().st_size == last_analyzing[1]:
            delta = 10
            continue

        if time.time() - p_last_measurement.stat().st_mtime < 5:
            delta = 5
            continue

        """ analyze... """
        try:
            df = pd.read_csv(p_last_measurement, skiprows=3, sep="\t")
        except:
            df = pd.read_csv(repair_file(p_last_measurement), skiprows=3, sep="\t")

        try:
            settings_nano = requests.get("http://192.168.4.1/settings").json()
        except:
            settings_nano = {
                "sensor": {"srd": 1},
                "measurement": {
                    "rpm_min": 0,
                    "rpm_max": 100,
                },
            }
        fs = int(1000 / (1 + settings_nano["sensor"]["srd"]))
        rpm_min = float(settings_nano["measurement"]["rpm_min"])
        rpm_max = float(settings_nano["measurement"]["rpm_max"])
        mins_measured = len(df) / (60 * fs)
        df = filter_measurement(df, fs, rpm_min, rpm_max, 1000)
        revs_filt = (df["Trigger"].diff() > 0).sum()

        df_ang = calculate_angle_dependency(df, show_track=False)

        output_pdf = (
            p_last_measurement.parent / "Spektren" / p_last_measurement.stem[:15]
        )
        output_pdf.mkdir(parents=True, exist_ok=True)

        prefix = (
            str(int(mins_measured)).zfill(5) + "__revs_" + str(int(revs_filt)).zfill(5)
        )

        if not any([p.stem.startswith(prefix) for p in output_pdf.iterdir()]):
            create_specs(df_ang, output_pdf, prefix=prefix)

        last_analyzing = [p_last_measurement, p_last_measurement.stat().st_size]
        del df, df_ang


def filter_measurement(
    df: pd.DataFrame, fs=500, n_min: float = 0, n_max: float = 100, thres: float = 5000
) -> pd.DataFrame:
    def filt_ax(df):
        hit_thres = False
        for col in df.columns:
            hit_thres = hit_thres or (
                ((df[col].max() - df[col].mean()) > thres)
                or ((df[col].mean() - df[col].min()) > thres)
            )

        n = 60 * fs / len(df)
        out_of_nrange = n < n_min or n > n_max

        df["okay"] = 1 - (hit_thres or out_of_nrange)
        return df

    df_temp = df.copy()

    """ remove rotations where any max > thres """
    df_temp["Revolutions"] = (df_temp["Trigger"].diff() < 0).cumsum()
    df_temp["okay"] = False

    dfs = df_temp.groupby("Revolutions", group_keys=True).apply(filt_ax)
    df_temp = dfs.reset_index(drop=True)

    return df_temp[df_temp["okay"].astype(bool)].reset_index(drop=True)[
        ["Axial", "Radial", "Torsional", "Trigger"]
    ]  # type:ignore - suppress type error from pylance


def calculate_angle_dependency(
    df: typing.Union[pd.DataFrame, Path, str],
    remove_mean: bool = True,
    angle_points=512,
    show_track=False,
) -> pd.DataFrame:
    if isinstance(df, str):
        df = parse_path(df)

    if isinstance(df, Path):
        try:
            df = pd.read_csv(df, skiprows=3, sep="\t")
        except:
            df = pd.read_csv(repair_file(df), skiprows=3, sep="\t")

    col_soll = {"Axial", "Radial", "Torsional", "Trigger"}
    col_ist = set(df.columns)
    if col_ist != col_soll:
        raise ValueError(f"columns in Dataframe not matching {{{', '.join(col_soll)}}}")

    df_temp = df.copy()
    if remove_mean:
        for ax in ["Axial", "Radial", "Torsional"]:
            df_temp[ax] = df_temp[ax] - df_temp[ax].mean()

    df_temp["Revolutions"] = (df_temp["Trigger"].diff() < 0).cumsum()
    dfs = []

    if show_track:
        gen = lambda x: track(x, "calculating angle dependency...")
    else:
        gen = lambda x: x

    for i in gen(range(df_temp["Revolutions"].max())):
        dfi = df_temp[df_temp["Revolutions"] == i]
        keys = ["Axial", "Radial", "Torsional", "Trigger"]
        data = {}
        for k in keys:
            if k == "Trigger":
                data[k] = ((angle_points - 1) * [0]) + [1]
            else:
                data[k] = signal.resample(dfi[k], angle_points)

        dfs.append(pd.DataFrame(data))
    df_temp = pd.concat(dfs, ignore_index=True)
    return df_temp


def create_specs(
    df_meas: pd.DataFrame,
    output_pdf: typing.Union[Path, None] = None,
    prefix="",
    fs=512,
    xmin=0,
    xmax=5,
) -> None:
    """fft calculation and plot -> vibA design"""
    # fft_freqs = np.fft.fftfreq(int(len(df_meas)), 1/fs)[: len(df_meas) // 2]
    data = {"f": np.fft.fftfreq(int(len(df_meas)), 1 / fs)[: len(df_meas) // 2]}
    for ax in ["Axial", "Radial"]:
        data[ax] = (
            2 * np.abs(np.fft.fft(df_meas[ax]))[: len(df_meas) // 2] / len(df_meas)
        )

    df_fft = pd.DataFrame(data=data)

    fig, axs = plt.subplots(2, 1, sharey=True)
    colors = ["#ffa500", "#9acd32"]
    for i, ax in enumerate(["Axial", "Radial"]):
        axs[i].plot(df_fft["f"], df_fft[ax], label=ax, color=colors[i])
        axs[i].axis(xmin=xmin, xmax=xmax, ymin=0)
        axs[i].set_xlabel("Order / Frequency [Hz]")
        axs[i].set_ylabel("Amplitude [mm/s²]")
        axs[i].grid()
        axs[i].legend(loc="upper right")

    if output_pdf:
        fig.set_size_inches(10, 10)
        if output_pdf.is_dir():
            r_max = df_fft[np.abs(df_fft["f"] - 1) < df_fft["f"][1]].max()
            output_pdf = output_pdf / (
                prefix
                + f"__res_{df_fft['f'][1]:.5f}P__Ax_{r_max['Axial']:.2f}mms2__Rad_{r_max['Radial']:.2f}mms2.pdf"
            )

        fig.savefig(
            output_pdf,  # type:ignore - suppress pylint warning message (Path -> str not compatible)
            bbox_inches="tight",
            dpi=600,
        )
    else:
        plt.show()


if __name__ == "__main__":
    continuous_analyzing()

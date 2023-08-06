#!/usr/bin/env python3

import itertools
import os
import re
from datetime import datetime
from typing import List, Optional, Tuple

import click
import numpy as np
import requests
import xarray as xr
from dask.diagnostics import ProgressBar
from pydap.net import HTTPError
from xarray.backends import PydapDataStore


def __parse_limit(message: str) -> Optional[float]:
    match = re.search(r", max=.+\";", message)
    if match:
        limit = match.group().strip(', max=";')
        return float(limit)
    else:
        return None


def split_by_chunks(dataset):
    chunk_slices = {}
    for dim, chunks in dataset.chunks.items():
        slices = []
        start = 0
        for chunk in chunks:
            if start >= dataset.sizes[dim]:
                break
            stop = start + chunk
            slices.append(slice(start, stop))
            start = stop
        chunk_slices[dim] = slices
    for slices in itertools.product(*chunk_slices.values()):
        selection = dict(zip(chunk_slices.keys(), slices))
        yield dataset[selection]


def find_chunk(ds: xr.Dataset, limit: float) -> Optional[int]:
    N = ds["time"].shape[0]
    for i in range(N, 0, -1):
        ds = ds.chunk({"time": i})
        ts = list(split_by_chunks(ds))
        if (ts[0].nbytes / (1000 * 1000)) < limit:
            return i
    return None


def subset(
    ds,
    variables: Optional[List[str]] = None,
    geographical_subset: Optional[Tuple[float, float, float, float]] = None,
    temporal_subset: Optional[Tuple[datetime, datetime]] = None,
    depth_range: Optional[Tuple[float, float]] = None,
):

    if variables:
        ds = ds[np.array(variables)]

    if geographical_subset:
        (
            minimal_latitude,
            maximal_latitude,
            minimal_longitude,
            maximal_longitude,
        ) = geographical_subset
        if "latitude" in ds.coords:
            ds = ds.sel(
                latitude=slice(minimal_latitude, maximal_latitude),
                longitude=slice(minimal_longitude, maximal_longitude),
            )
        elif "nav_lat" in ds.coords:
            mask = (
                (ds.nav_lon > minimal_longitude)
                & (ds.nav_lon < maximal_longitude)
                & (ds.nav_lat > minimal_latitude)
                & (ds.nav_lat < maximal_latitude)
            )
            geoindex = np.argwhere(mask.values)
            xmin = min(geoindex[:, 1])
            xmax = max(geoindex[:, 1])
            ymin = min(geoindex[:, 0])
            ymax = max(geoindex[:, 0])

            ds = ds.isel(
                x=slice(xmin, xmax),
                y=slice(ymin, ymax),
            )
        else:
            ds = ds.sel(
                lat=slice(minimal_latitude, maximal_latitude),
                lon=slice(minimal_longitude, maximal_longitude),
            )

    if temporal_subset:
        (start_datetime, end_datetime) = temporal_subset
        if "time_counter" in ds.coords:
            ds = ds.sel(time_counter=slice(start_datetime, end_datetime))
        else:
            ds = ds.sel(time=slice(start_datetime, end_datetime))

    if (("depth" in ds.dims) or ("deptht" in ds.dims)) and (
        depth_range is not None
    ):
        (
            minimal_depth,
            maximal_depth,
        ) = depth_range
        if "deptht" in ds.dims:
            ds = ds.sel(deptht=slice(minimal_depth, maximal_depth))
        else:
            ds = ds.sel(depth=slice(minimal_depth, maximal_depth))

    return ds


def download_dataset(
    login: str,
    password: str,
    dataset_url: str,
    output_path: str,
    output_file: Optional[str] = None,
    variables: Optional[List[str]] = None,
    geographical_subset: Optional[Tuple[float, float, float, float]] = None,
    temporal_subset: Optional[Tuple[datetime, datetime]] = None,
    depth_range: Optional[Tuple[float, float]] = None,
    limit: Optional[int] = None,
    confirmation: Optional[bool] = False,
):
    session = requests.Session()
    session.auth = (login, password)
    store = PydapDataStore.open(dataset_url, session=session, timeout=300)

    ds = xr.open_dataset(store)
    ds = subset(
        ds, variables, geographical_subset, temporal_subset, depth_range
    )

    if confirmation:
        print(ds)
        click.confirm("Do you want to continue?", abort=True, default=True)

    complete_dataset = os.path.join(
        output_path, dataset_url.rsplit("/", 1)[-1] + ".nc"
    )

    try:
        click.echo("Trying to download as one file...")
        ds.to_netcdf(complete_dataset)
    except HTTPError as e:
        if os.path.exists(complete_dataset):
            try:
                os.remove(complete_dataset)
            except OSError:
                click.echo("Error while deleting file: ", complete_dataset)

        click.echo("Dataset must be chunked.")
        if limit is None:
            size_limit = __parse_limit(str(e.comment))
        else:
            size_limit = limit

        if size_limit:
            click.echo(f"Server download limit is {size_limit} MB")
            i = find_chunk(ds, size_limit)
            ds = xr.open_dataset(
                store, mask_and_scale=True, chunks={"time": i}
            )

            ds = subset(
                ds,
                variables,
                geographical_subset,
                temporal_subset,
                depth_range,
            )

            ts = list(split_by_chunks(ds))

            p = [
                os.path.join(output_path, str(g) + ".nc")
                for g in range(len(ts))
            ]

            click.echo("Downloading " + str(len(ts)) + " files...")
            delayed = xr.save_mfdataset(datasets=ts, paths=p, compute=False)
            with ProgressBar():
                delayed.compute()
            click.echo("Files downloaded")

            if output_file is not None:
                click.echo(f"Concatenating files into {output_file}...")
                ds = xr.open_mfdataset(p)
                delayed = ds.to_netcdf(
                    os.path.join(output_path, output_file), compute=False
                )
                with ProgressBar():
                    delayed.compute()
                click.echo("Files concatenated")

                click.echo("Removing temporary files")
                for path in p:
                    try:
                        os.remove(path)
                    except OSError:
                        click.echo("Error while deleting file: ", path)
                click.echo("Done")

        else:
            click.echo("No limit found in the returned server error")


@click.command(
    help="""Downloads OPeNDAP dataset as NetCDF files taking into account the
server data query limit.

Example:

  opendap-downloader
--dataset-url
https://nrt.cmems-du.eu/thredds/dodsC/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
--variable analysed_sst --variable sea_ice_fraction
--temporal-subset 2021-01-01 2021-01-02
--geographical-subset 0.0 0.1 0.0 0.1

  opendap-downloader
-u https://nrt.cmems-du.eu/thredds/dodsC/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
-v analysed_sst -v sea_ice_fraction
-t 2021-01-01 2021-01-02
-g 0.0 0.1 0.0 0.1
"""
)
@click.option(
    "--dataset-url",
    "-u",
    type=str,
    required=True,
    help="The full OPeNDAP dataset URL",
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=str,
    help="Specify dataset variables",
    multiple=True,
)
@click.option(
    "--geographical-subset",
    "-g",
    type=(
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-180, max=180),
        click.FloatRange(min=-180, max=180),
    ),
    help="The geographical subset as "
    + "minimal latitude, maximal latitude, "
    + "minimal longitude and maximal longitude",
)
@click.option(
    "--temporal-subset",
    "-t",
    type=(
        click.DateTime(
            ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        ),
        click.DateTime(
            ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        ),
    ),
    help="The temporal subset as start datetime and end datetime",
)
@click.option(
    "--depth-range",
    "-d",
    type=(click.FloatRange(min=0), click.FloatRange(min=0)),
    help="The depth range in meters, if depth is a dataset coordinate",
)
@click.option(
    "--output-path",
    "-o",
    type=click.Path(),
    required=True,
    help="The destination path for the downloaded files."
    + " Default is the current directory",
    default="",
)
@click.option(
    "--output-file",
    "-f",
    type=click.Path(),
    help="Concatenate the downloaded data in the given file name"
    + " (under the output path)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    help="Specify the download size limit (in MB) of the Opendap server if it can't be provided by the message error",
)
@click.option(
    "--confirmation",
    is_flag=True,
    help="Print dataset metadata and ask for confirmation before download",
)
@click.option("--login", prompt="Your login please:")
@click.password_option(confirmation_prompt=False)
def download(
    dataset_url: str,
    variables: List[str],
    geographical_subset: Tuple[float, float, float, float],
    temporal_subset: Tuple[datetime, datetime],
    depth_range: Tuple[float, float],
    output_path: str,
    login: str,
    password: str,
    confirmation: bool,
    output_file: Optional[str],
    limit: Optional[int] = None,
):

    download_dataset(
        login,
        password,
        dataset_url,
        output_path,
        output_file,
        variables,
        geographical_subset,
        temporal_subset,
        depth_range,
        limit,
        confirmation,
    )


if __name__ == "__main__":
    download()

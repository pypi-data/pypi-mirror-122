import json
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from terality_serde import loads, dumps, SerializableEnum


class ArrayEncoding(SerializableEnum):
    MIXED = "MIXED"
    STRUCT = "STRUCT"


JSONABLE_TYPES = (float, int, bool, str, type(None))


def has_float_nan(array: Union[np.ndarray, pd.array]) -> bool:
    series = pd.Series(array)
    return series[series.isna()].apply(lambda x: isinstance(x, float)).any()


def has_only_jsonable_types(array: np.ndarray):
    series = pd.Series(array)
    return series.apply(lambda x: isinstance(x, JSONABLE_TYPES)).all()


def _endecode_json_indices_inplace(
    df: pd.DataFrame, indices_encoding: List[Optional[ArrayEncoding]], encode: bool
) -> pd.DataFrame:
    """
    Encode/Decode index levels which are either Mixed or Struct types.
    Mutates the input DataFrame.
    """

    assert len(indices_encoding) == df.index.nlevels

    new_arrays = []
    for level_num, index_encoding in enumerate(indices_encoding):
        index = df.index.get_level_values(level_num)
        array = index.array
        if index_encoding is not None:
            if index_encoding == ArrayEncoding.MIXED:
                array = encode_mixed_array(array) if encode else decode_mixed_array(array)
            elif index_encoding == ArrayEncoding.STRUCT:
                array = encode_struct_array(array) if encode else decode_struct_array(array)
            else:
                raise ValueError(f"Unknow encoding {index_encoding}")

        new_arrays.append(array)

    if isinstance(df.index, pd.MultiIndex):
        df.index = pd.MultiIndex.from_arrays(new_arrays, names=df.index.names)
    else:
        assert len(new_arrays) == 1
        df.index = pd.Index(new_arrays[0], name=df.index.name)
    return df


def _endecode_json_columns_inplace(
    df: pd.DataFrame, cols_encoding: List[Optional[ArrayEncoding]], encode: bool
) -> pd.DataFrame:
    """
    Encode/Decode columns which are either Mixed or Struct types.
    Mutates the input DataFrame.
    """

    assert len(cols_encoding) == len(df.columns)

    for col_num, col_need_encoding in enumerate(cols_encoding):
        array = df.iloc[:, col_num].array
        if col_need_encoding == ArrayEncoding.MIXED:
            array_encoded = encode_mixed_array(array) if encode else decode_mixed_array(array)
            df.iloc[:, col_num] = pd.Series(array_encoded, df.index)
        elif col_need_encoding == ArrayEncoding.STRUCT:
            array_encoded = encode_struct_array(array) if encode else decode_struct_array(array)
            df.iloc[:, col_num] = pd.Series(array_encoded, df.index)

    return df


def decode_json_indices_inplace(
    df: pd.DataFrame, indices_encoding: List[Optional[ArrayEncoding]]
) -> pd.DataFrame:
    return _endecode_json_indices_inplace(df, indices_encoding, encode=False)


def decode_json_columns_inplace(
    df: pd.DataFrame, cols_encoding: List[Optional[ArrayEncoding]]
) -> pd.DataFrame:
    return _endecode_json_columns_inplace(df, cols_encoding, encode=False)


def encode_json_indices_inplace(
    df: pd.DataFrame, indices_encoding: List[Optional[ArrayEncoding]]
) -> pd.DataFrame:
    return _endecode_json_indices_inplace(df, indices_encoding, encode=True)


def encode_json_columns_inplace(
    df: pd.DataFrame, cols_encoding: List[Optional[ArrayEncoding]]
) -> pd.DataFrame:
    return _endecode_json_columns_inplace(df, cols_encoding, encode=True)


def decode_struct_array(array: pd.array) -> pd.array:
    """
    - Can't use apply to avoid pandas auto-casting.
    - Can't use pd.array(data) because if data has tuples
      pandas thinks we want to build a 2D array.
    """
    data_decoded = [loads(val) for val in array]
    return pd.Series(data_decoded, dtype="object").array


def decode_mixed_array(array: pd.array) -> pd.array:
    """
    - Can't use apply to avoid pandas auto-casting.
    - Can't use pd.array(data) because if data has tuples
      pandas thinks we want to build a 2D array.
    """
    data_decoded = [json.loads(val) for val in array]
    return pd.Series(data_decoded, dtype="object").array


def encode_struct_array(array: pd.array) -> pd.array:
    return pd.Series(array).apply(dumps).array


def encode_mixed_array(array: pd.array) -> pd.array:
    return pd.Series(array).apply(json.dumps).array

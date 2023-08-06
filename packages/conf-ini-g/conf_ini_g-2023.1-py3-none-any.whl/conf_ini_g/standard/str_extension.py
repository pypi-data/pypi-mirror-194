# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import ast as ast_t
import textwrap as text
from conf_ini_g.standard.path_extension import path_t
from typing import Any, Tuple

from conf_ini_g.standard.type_extension import none_t


class _no_default_t:
    pass


def Flattened(string: str) -> str:
    """"""
    return text.dedent(string).replace("\n", " ")


def String2Value(string: str, /, *, expected_type: type = None) -> Tuple[Any, bool]:
    """
    expected_type: Must not be passed explicitly as None since None is interpreted as "no specific expected type". When
    expecting None, pass none_t.
    """
    if expected_type is None:
        return _String2Value(string)

    failed_conversion = None, False

    if expected_type is bool:
        if (lower := string.lower()) in ("true", "yes", "on"):
            return True, True
        elif lower in ("false", "no", "off"):
            return False, True
        #
    elif expected_type in (int, float):
        try:
            value = float(string)
        except ValueError:
            return failed_conversion

        if expected_type is int:
            if value.is_integer():
                value = int(value)
            else:
                return failed_conversion

        return value, True
        #
    elif expected_type is path_t:
        # An empty string becomes "." when converted to a pathlib Path while it should be interpreted as "no path
        # specified", which is closer to None. To avoid this confusion, an empty string is considered invalid.
        if string.__len__() > 0:
            return path_t(string), True
        #
    elif expected_type in (tuple, list):
        value, success = _String2Value(string)
        if success and isinstance(value, (tuple, list)):
            if (expected_type is tuple) and isinstance(value, list):
                value = tuple(value)
            elif (expected_type is list) and isinstance(value, tuple):
                value = list(value)

            return value, True
        #
    elif expected_type is none_t:
        if string.lower() == "none":
            return None, True
        #
    else:
        value, success = _String2Value(string)
        if success and isinstance(value, expected_type):
            return value, True

    return failed_conversion


def _String2Value(string: str, /) -> Tuple[Any, bool]:
    """"""
    if (lowered := string.lower()) == "none":
        return None, True
    elif lowered in ("true", "yes", "on"):
        return True, True
    elif lowered in ("false", "no", "off"):
        return False, True

    try:
        value = ast_t.literal_eval(string)
        success = True
    except (SyntaxError, ValueError):
        value = None
        success = False

    return value, success


def ValueFromStr(value: str, /) -> Any:
    """"""
    if (lowered := value.lower()) == "none":
        output = None
    elif lowered in ("true", "yes", "on"):
        output = True
    elif lowered in ("false", "no", "off"):
        output = False
    elif str.isdigit(value):
        output = int(value)
    elif (output := _AsFloat(value)) is not None:
        pass
    elif "," in value:
        top_level = []
        pieces = value.split(",")
        first_idx = 0
        status = 0
        for last_idx, piece in enumerate(pieces):
            if "(" in piece:
                status += 1
            elif ")" in piece:
                status -= 1
            if status == 0:
                stripped = ",".join(pieces[first_idx : (last_idx + 1)]).strip(" ()")
                top_level.append(stripped)
                first_idx = last_idx + 1
        output = tuple(ValueFromStr(_vle) for _vle in top_level)
    else:
        output = value

    return output


def _AsFloat(value: str, /) -> float | None:
    """"""
    try:
        output = float(value)
    except ValueError:
        output = None

    return output


def AlignedNameAndValue(unaligned: str, space: int, /) -> str:
    """"""
    name, value = unaligned.split("=", maxsplit=1)

    return f"{name:{space}}= {value}"

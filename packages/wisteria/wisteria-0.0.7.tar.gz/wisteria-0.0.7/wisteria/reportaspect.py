#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/reportaspect.py

    Define some 'aspects' (=some text attributes) for some excepts in report.

    ___________________________________________________________________________

    o  aspect_base100(bool_is_base100_reference, float_base100)
    o  aspect_boolsuccess(bool_success)
    o  aspect_data(data_objectname)
    o  aspect_list(listitems)
    o  aspect_nodata(string)
    o  aspect_percentage(percentage)
    o  aspect_ratio(inttotal_and_floatratio)
    o  aspect_serializer(serializer_name)
    o  aspect_stringlength(int_stringlength)
    o  aspect_time(floattime)
    o  aspect_title(title)
"""
import wisteria.globs


def aspect_base100(bool_is_base100_reference,
                   float_base100):
    """
        SerializationResults.aspect_base100()

        Format (float)<float_base100> and return this value as a string.
        If <bool_is_base100_reference> is True, it means that <float_base100>
        is the base100 reference value: its representation will therefore be
         slightly different.
        ___________________________________________________________________

        ARGUMENTS:
        o  (bool)bool_is_base100_reference : is <float_base100> a base100
                                             reference value ?
        o  (float)float_base100
    """
    if float_base100 is None:
        return aspect_nodata()

    prefix = " "
    suffix = ""
    if bool_is_base100_reference:
        prefix = "[italic]*"
        suffix = "[/italic]"

    return f"{prefix}{float_base100:.2f}{suffix}"


def aspect_boolsuccess(bool_success):
    """
        SerializationResults.aspect_boolsuccess()

        Format the input argument into a string. The input argument is a (bool)success.
            ex: False > "NOT OK"

        _______________________________________________________________

        ARGUMENT: (bool)bool_success

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if bool_success is None:
        return aspect_nodata()
    return "ok" if bool_success else "[red]NOT OK[/red]"


def aspect_data(data_objectname):
    """
        aspect_data()

        Modify the aspect of (str)data_objectname.

        _______________________________________________________________________

        ARGUMENT: (str)data_objectname

        RETURNED VALUE: (str)_objectname + some text attributes.
    """
    return f"[bold white]{data_objectname}[/bold white]"


def aspect_list(listitems):
    """
        aspect_list()

        Returns a list of (str)words written in good English, something
        like "a, b, and c" (no Oxford Comma here, confer
        https://www.grammar-monster.com/lessons/commas_the_Oxford_comma.htm)

        _______________________________________________________________________

        ARGUMENT: (str)data_objectname

        RETURNED VALUE: (str)_objectname + some text attributes.
    """
    if len(listitems) == 0:
        return ""
    if len(listitems) == 1:
        return listitems[0]
    if len(listitems) == 2:
        return f"{listitems[0]} and {listitems[1]}"
    return f"{', '.join(listitem for listitem in listitems[:-1])} and {listitems[-1]}"


def aspect_nodata(string=None):
    """
        aspect_percentage()

        Return a string with rich text attribute saying that no data is available.

        _______________________________________________________________________

        RETURNED VALUE: (str)"no data" string + some text attributes.
    """
    if not string:
        string = "(no data)"

    return f"[red]{string}[/red]"


def aspect_percentage(percentage):
    """
        aspect_percentage()

        Modify the aspect of (float)percentage.

        _______________________________________________________________________

        ARGUMENT: (float)percentage

        RETURNED VALUE: (str)percentage + some text attributes.
    """
    return f"{percentage:.2f}%"


def aspect_ratio(inttotal_and_floatratio):
    """
        SerializationResults.aspect_ratio()

        Format the input argument into a string. The input argument is an absolute
        (int)number and a (float)fraction, its ratio.
            ex: (3, 0.5) > "3 (50 %)"

        _______________________________________________________________

        ARGUMENT: (None|(int, float))inttotal_and_floatratio

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if inttotal_and_floatratio != (None, None):
        return f"{inttotal_and_floatratio[0]} " \
            f"({aspect_percentage(100*inttotal_and_floatratio[1])})"
    return aspect_nodata()


def aspect_serializer(serializer_name):
    """
        aspect_serializer()

        Modify the aspect of (str)serializer_name, replace it by its
        .human_name.

        _______________________________________________________________________

        ARGUMENT: (str)serializer_name

        RETURNED VALUE: (str)serializer_name + some text attributes.
    """
    return "[yellow]" \
        f"{wisteria.globs.SERIALIZERS[serializer_name].human_name}" \
        "[/yellow]"


def aspect_stringlength(int_stringlength):
    """
        SerializationResults.aspect_stringlength()

        Format the input argument into a string. The input argument is a (int)number
        of characters
            ex: 3 > "3 chars"

        Please note that the unit has deliberately not been added to the end of the string.
        _______________________________________________________________

        ARGUMENT: (None|int)int_stringlength, a string number.

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if int_stringlength is None:
        return aspect_nodata()
    return f"{int_stringlength}"


def aspect_time(floattime):
    """
        SerializationResults.aspect_time()

        Format the input argument into a string. The input argument is a (float)time laps.
            ex: 0.333345677 > "0.333345"

        Please note that the unit has deliberately not been added to the end of the string.
        _______________________________________________________________

        ARGUMENT: (None|float)floattime

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if floattime is None:
        return aspect_nodata()
    return f"{floattime:.6f}"


def aspect_title(title):
    """
        aspect_title()

        Modify the aspect of (str)title.

        _______________________________________________________________________

        ARGUMENT: (str)title

        RETURNED VALUE: (str)title + some text attributes.
    """
    return f"[bold white on blue]{title}[/bold white on blue]"

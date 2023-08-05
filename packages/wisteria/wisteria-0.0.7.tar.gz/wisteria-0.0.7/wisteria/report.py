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
    Wisteria project : wisteria/report.py

    Functions that print the report, especially report().

    ___________________________________________________________________________

    o  humanratio(ratio)
    o  cmpdata2phrase(cmpdata)
    o  ratio2phrase(ratio, base_string)

    o  report_section_a1(results, s1s2d)
    o  report_section_a2(results, s1s2d)
    o  report_section_a3(results, s1s2d)
    o  report_section_b1a(results, s1s2d)
    o  report_section_b1b(results, s1s2d)
    o  report_section_b1c(results, s1s2d)
    o  report_section_b1d(results, s1s2d)
    o  report_section_b2a(results, s1s2d)
    o  report_section_b2b(results, s1s2d)
    o  report_section_c1a(results, s1s2d)
    o  report_section_c1b(results, s1s2d)
    o  report_section_c2a(results, s1s2d)
    o  report_section_c2b(results, s1s2d)
    o  report_section_d1a(results, s1s2d)
    o  report_section_d1b(results, s1s2d)
    o  report_section_d2a(results, s1s2d)
    o  report_section_d2b(results, s1s2d)
    o  report_section_d2c(results, s1s2d)

    o  report(results, s1s2d)
"""
import rich.table

import wisteria.globs
from wisteria.globs import UNITS
from wisteria.globs import REPORT_SHORTCUTS
from wisteria.wisteriaerror import WisteriaError
from wisteria.utils import shortenedstr
from wisteria.msg import msgreport, msgreporttitle
from wisteria.reportaspect import aspect_serializer, aspect_data, aspect_percentage, aspect_list
from wisteria.reportaspect import aspect_nodata
from wisteria.cmdline_mymachine import mymachine
from wisteria.textandnotes import TextAndNotes


def humanratio(ratio,
               explanations=None):
    """
        humanratio()

        Since ratio are difficult to understand when being smaller than 1, this function
        computes, if necessary, the inverse of <ratio> and returns it.

        - if <explanations> is None, return the (float)ratio value;
        - if <explanations> is not None, return an (str)explanation describing the
        (float)ratio value.

        _______________________________________________________________________

        ARGUMENTS:
        o  (float)ratio, the ratio to be returned
        o  (None|list of str)explanations:
                (str)ratio1_str, (float)ratio1, (str)ratio2_str, (float)ratio2,
                (None if no unit or str)unit_name

        RETURNED VALUE: (float)ratio or (float)1/ratio.
    """
    # ---- explanations is None > let's return a (float)value -----------------
    if explanations is None:
        if ratio < 1:
            return 1/ratio
        return ratio

    # ---- explanations is not None > let's return a (str)explanation ---------
    ratio1_str, ratio1, ratio2_str, ratio2, unit_name = explanations
    unit_str = "" if unit_name is None else UNITS[unit_name]
    if ratio < 1:
        ratio = 1/ratio
        res = f"factor {ratio:.3f} = {ratio2_str} / {ratio1_str} " \
            f"= {ratio2:.3f} {unit_str} / {ratio1:.3f} {unit_str}" \
            "\n" \
            f"{ratio1_str} * {ratio:.3f} = {ratio1:.3f} {unit_str} * {ratio:.3f} = " \
            f"{ratio2_str} = {ratio2:.3f} {unit_str}"
    else:
        res = f"factor {ratio:.3f} = {ratio1_str} / {ratio2_str} " \
            f"= {ratio1:.3f} {unit_str} / {ratio2:.3f} {unit_str}" \
            "\n" \
            f"{ratio2_str} * {ratio:.3f} = {ratio2:.3f} {unit_str} * {ratio:.3f} " \
            f"= {ratio1_str} = {ratio1:.3f} {unit_str}"
    return res


def cmpdata2phrase(cmpdata):
    """
        cmpdata2phrase()

        Convert <cmpdata> to a phrase describing <cmpdata>.

        _______________________________________________________________________

        ARGUMENT: (str)<cmpdata>: 'all', 'ini', 'cwc'

        RETURNED VALUE: (str)a string describing <cmpdata>
    """
    assert cmpdata in ('all', 'ini', 'cwc')

    if cmpdata == "all":
        return "According to the tests " \
            "carried out on all data, "
    if cmpdata == "ini":
        return "According to the tests " \
            "carried out on the data defined in the configuration file, "
    # cmpdata == "cwc"
    return "According to the tests " \
        "conducted on data of the 'comparing what is comparable' type, "


def ratio2phrase(ratio,
                 base_string):
    """
        ratio2phrase()

        Convert a (float)<ratio> (e.g. 0.5, 2, 4...) to an adverbial phrase
        like "much slower".

        _______________________________________________________________________

        ARGUMENTS:
        o  (float)ratio
        o  (str)base_string: "slow/fast" or "long/short"

        RETURNED VALUE: (str)an adverbial phrase
    """
    assert base_string in ('slow/fast', 'long/short', 'good/bad')

    if base_string == "slow/fast":
        if ratio > 10:
            expression = "extremly slower"
        elif ratio > 2:
            expression = "much slower"
        elif ratio > 1.4:
            expression = "slower"
        elif ratio > 1.1:
            expression = "slightly slower"
        elif ratio > 0.9:
            expression = "slightly faster"
        elif ratio > 0.5:
            expression = "faster"
        elif ratio > 0.1:
            expression = "much faster"
        else:
            expression = "extremly faster"

    elif base_string == "long/short":
        if ratio > 10:
            expression = "extremly longer"
        elif ratio > 2:
            expression = "much longer"
        elif ratio > 1.4:
            expression = "longer"
        elif ratio > 1.1:
            expression = "slightly longer"
        elif ratio > 0.9:
            expression = "slightly shorter"
        elif ratio > 0.5:
            expression = "shorter"
        elif ratio > 0.1:
            expression = "much shorter"
        else:
            expression = "extremly shorter"

    elif base_string == "good/bad":
        if ratio > 10:
            expression = "much, much better"
        elif ratio > 2:
            expression = "much better"
        elif ratio > 1.4:
            expression = "better"
        elif ratio > 1.1:
            expression = "slightly better"
        elif ratio > 0.9:
            expression = "slightly worse"
        elif ratio > 0.5:
            expression = "worse"
        elif ratio > 0.1:
            expression = "much worse"
        else:
            expression = "much, much worse"

    return expression


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_a1(results,
                      s1s2d):
    """
        report_section_a1()

        Sub-function of report() for report section "A1"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle(
            "(A1) Report (--cmp = "
            f"'[italic]{wisteria.globs.ARGS.cmp}[/italic]')")
        msgreport()


def report_section_a2(results,
                      s1s2d):
    """
        report_section_a2()

        Sub-function of report() for report section "A2"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(A2) List of Serializers to Be Used")
        msgreport()

    for serializer in wisteria.globs.SERIALIZERS.values():
        msgreport(f"  - {serializer.simple_repr()}")
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_a3(results,
                      s1s2d):
    """
        report_section_a3()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    data = wisteria.globs.DATA

    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(A3) List of Data Objects to Be Used")
        msgreport()

    for dataobj_name, dataobj_value in data.items():
        msgreport(f"  - {dataobj_name:>30} : {shortenedstr(repr(dataobj_value))}")
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1a(results,
                       s1s2d):
    """
        report_section_b1a()

        Sub-function of report() for report section "B1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1a) Full Details: Serializer * Data Object")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer > Data Object", width=24)
    table.add_column("Encod. Ok ?", width=11)
    table.add_column(f"Encod. Time ({UNITS['time']})", width=11)
    table.add_column(f"Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column("Decod. Ok ?", width=11)
    table.add_column(f"Decod. Time ({UNITS['time']})", width=11)
    table.add_column("Encod.<>Decod. ?", width=16)

    for serializer in results.serializers:
        table.add_row(f"{aspect_serializer(serializer)} :")
        for dataobj in results.dataobjs:
            table.add_row(
                "> " + f"{aspect_data(dataobj)}",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time"),
                results.repr_attr(serializer, dataobj, "encoding_strlen"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time"),
                results.repr_attr(serializer, dataobj, "similarity"))
    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1b(results,
                       s1s2d):
    """
        report_section_b1b()

        Sub-function of report() for report section "B1b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1b) Full Details: Serializers")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer", width=24)
    table.add_column(f"Encod. Ok ? (Max={results.dataobjs_number})", width=11)
    table.add_column(f"Σ Encoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column(f"Decod. Ok ? (Max={results.dataobjs_number})", width=11)
    table.add_column(f"Σ Decoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Encod.<>Decod. ? (Max={results.dataobjs_number})", width=16)

    for serializer in results.serializers:
        table.add_row(
            f"{aspect_serializer(serializer)}",
            f"{results.ratio_encoding_success(serializer=serializer)}",
            f"{results.total_encoding_time(serializer=serializer)}",
            f"{results.total_encoding_strlen(serializer=serializer)}",
            f"{results.ratio_decoding_success(serializer=serializer)}",
            f"{results.total_decoding_time(serializer=serializer)}",
            f"{results.ratio_similarity(serializer=serializer)}",
        )
    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1c(results,
                       s1s2d):
    """
        report_section_b1c()

        Sub-function of report() for report section "B1c"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1c) Full Details: Serializers, Hall of Fame")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("#", width=2)
    table.add_column(f"Encod. Ok ? (Max={results.dataobjs_number})", width=11)
    table.add_column(f"Σ Encoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column(f"Decod. Ok ? (Max={results.dataobjs_number})", width=11)
    table.add_column(f"Σ Decoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Encod.<>Decod. ? (Max={results.dataobjs_number})", width=16)

    for index in range(results.serializers_number):
        table.add_row(
            f"{index+1}",
            f"{results.get_halloffame('encoding_success', index)}",
            f"{results.get_halloffame('encoding_time', index)}",
            f"{results.get_halloffame('encoding_strlen', index)}",
            f"{results.get_halloffame('decoding_success', index)}",
            f"{results.get_halloffame('decoding_time', index)}",
            f"{results.get_halloffame('similarity', index)}",
        )

    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b1d(results,
                       s1s2d):
    """
        report_section_b1d()

        Sub-function of report() for report section "B1d"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B1d) Full Details: Which Serializer(s) Can't Handle Data Objects ?")

    for serializer in results.serializers:
        _list = tuple(dataobj for dataobj in results[serializer]
                      if not results[serializer][dataobj].similarity)
        if not _list:
            msgreport(f"* ({aspect_serializer(serializer)}) "
                      "There's no data object that serializer "
                      f"{aspect_serializer(serializer)} can't handle.")
        else:
            msgreport(f"* ({aspect_serializer(serializer)}) "
                      f"Serializer {aspect_serializer(serializer)} "
                      "can't handle following data objects:")
            for dataobj in _list:
                msgreport(f"  - {aspect_data(dataobj)}")
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b2a(results,
                       s1s2d):
    """
        report_section_b2a()

        Sub-function of report() for report section "B2a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B2a) full details: data object * serializer")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Data Object > Serializer", width=24)
    table.add_column("Encod. Ok ?", width=11)
    table.add_column(f"Encod. Time ({UNITS['time']})", width=11)
    table.add_column(f"Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column("Decod. Ok ?", width=11)
    table.add_column(f"Decod. Time ({UNITS['time']})", width=11)
    table.add_column("Encod.<>Decod. ?", width=16)

    for dataobj in results.dataobjs:
        table.add_row(f"{aspect_data(dataobj)} :")
        for serializer in results.serializers:
            table.add_row(
                "> " + f"{aspect_serializer(serializer)}",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time"),
                results.repr_attr(serializer, dataobj, "encoding_strlen"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time"),
                results.repr_attr(serializer, dataobj, "similarity")
            )
    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_b2b(results,
                       s1s2d):
    """
        report_section_b2b()

        Sub-function of report() for report section "B2b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(B2b) Full Details: Data Objects")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Data Object", width=24)
    table.add_column(f"Encod. Ok ? (Max={results.serializers_number})", width=11)
    table.add_column(f"Σ Encoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})", width=13)
    table.add_column(f"Decod. Ok ? (Max={results.serializers_number})", width=11)
    table.add_column(f"Σ Decoded Time ({UNITS['time']})", width=11)
    table.add_column(f"Encod.<>Decod. ? (Max={results.serializers_number})", width=16)

    for dataobj in results.dataobjs:
        table.add_row(
            f"{aspect_data(dataobj)}",
            f"{results.ratio_encoding_success(dataobj=dataobj)}",
            f"{results.total_encoding_time(dataobj=dataobj)}",
            f"{results.total_encoding_strlen(dataobj=dataobj)}",
            f"{results.ratio_decoding_success(dataobj=dataobj)}",
            f"{results.total_decoding_time(dataobj=dataobj)}",
            f"{results.ratio_similarity(dataobj=dataobj)}",
        )
    msgreport(table)
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_c1a(results,
                       s1s2d):
    """
        report_section_c1a()

        Sub-function of report() for report section "C1a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C1a) Full Details: Serializer * Data Object (base 100)")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer > Data Object", width=24)
    table.add_column("Encod. Ok ?", width=11)

    if base100 := results.get_base('encoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_time')
        table.add_column(f"Encod. Time (Base 100 = {result} {UNITS['time']})", width=11)
    else:
        table.add_column(f"Encod. Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    if base100 := results.get_base('encoding_strlen'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_strlen')
        table.add_column(
            f"Encoded Str. Length (Base 100 = {result} {UNITS['string length']})", width=13)
    else:
        table.add_column(f"Encoded Str. {aspect_nodata('(NO BASE 100)')}",
                         width=13)

    table.add_column("Decod. Ok ?", width=11)

    if base100 := results.get_base('decoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='decoding_time')
        table.add_column(f"Decod. Time (Base 100 = {result} {UNITS['time']})", width=11)
    else:
        table.add_column(f"Decod. Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    table.add_column("Encod.<>Decod. ?", width=16)

    for serializer in results.serializers:
        table.add_row(f"{aspect_serializer(serializer)} :")
        for dataobj in results.dataobjs:
            table.add_row(
                "> " + f"{aspect_data(dataobj)}",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time", output="base100"),
                results.repr_attr(serializer, dataobj, "encoding_strlen", output="base100"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time", output="base100"),
                results.repr_attr(serializer, dataobj, "similarity"))
    msgreport(table)
    msgreport()


def report_section_c1b(results,
                       s1s2d):
    """
        report_section_c1b()

        Sub-function of report() for report section "C1b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C1b) Full Details: Serializers (base 100)")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer", width=24)
    table.add_column(f"Encod. Ok ? (Max={results.dataobjs_number})", width=11)
    if base100 := results.get_serializers_base('encoding_time'):
        table.add_column(
            "Σ Encoded Time "
            f"(Base 100 = {results.total_encoding_time(serializer=base100)} {UNITS['time']})",
            width=11)
    else:
        table.add_column(f"Σ Encoded Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    if base100 := results.get_serializers_base('encoding_strlen'):
        table.add_column(
            "Σ Encoded Str. Length "
            f"(Base 100 = {results.total_encoding_strlen(serializer=base100)} "
            f"{UNITS['string length']})",
            width=13)
    else:
        table.add_column(f"Σ Encoded Str. {aspect_nodata('(NO BASE 100)')}", width=11)

    table.add_column(f"Decod. Ok ? (Max={results.dataobjs_number})", width=11)

    if base100 := results.get_serializers_base('decoding_time'):
        table.add_column(
            "Σ Decoded Time "
            f"(Base 100 = {results.total_decoding_time(serializer=base100)} {UNITS['time']})",
            width=11)
    else:
        table.add_column(f"Σ Decoded Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    table.add_column(f"Encod.<>Decod. ? (Max={results.dataobjs_number})", width=16)

    for serializer in results.serializers:
        table.add_row(
            f"{aspect_serializer(serializer)}",
            f"{results.ratio_encoding_success(serializer=serializer)}",
            f"{results.total_encoding_time(serializer=serializer, output='base100')}",
            f"{results.total_encoding_strlen(serializer=serializer, output='base100')}",
            f"{results.ratio_decoding_success(serializer=serializer)}",
            f"{results.total_decoding_time(serializer=serializer, output='base100')}",
            f"{results.ratio_similarity(serializer=serializer)}",
        )
    msgreport(table)
    msgreport()


def report_section_c2a(results,
                       s1s2d):
    """
        report_section_c2a()

        Sub-function of report() for report section "C2a"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C2a) Full Details: Data Object * Serializer (base 100)")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Data Object > Serializer", width=24)

    table.add_column("Encod. Ok ?", width=11)

    if base100 := results.get_base('encoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_time')
        table.add_column(f"Encod. Time (Base 100 = {result} {UNITS['time']})", width=11)
    else:
        table.add_column(f"Encod. Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    if base100 := results.get_base('encoding_strlen'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='encoding_strlen')
        table.add_column(
            f"Encoded Str. Length (Base 100 = {result} {UNITS['string length']})", width=13)
    else:
        table.add_column(f"Encoded Str. Length {aspect_nodata('(NO BASE 100)')}",
                         width=13)

    table.add_column("Decod. Ok ?", width=11)

    if base100 := results.get_base('decoding_time'):
        result = results.repr_attr(serializer=base100.serializer,
                                   dataobj=base100.dataobj,
                                   attribute_name='decoding_time')
        table.add_column(f"Decod. Time (Base 100 = {result} {UNITS['time']})", width=11)
    else:
        table.add_column(f"Decod. Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    table.add_column("Encod.<>Decod. ?", width=16)

    for dataobj in results.dataobjs:
        table.add_row(f"{aspect_data(dataobj)} :")
        for serializer in results.serializers:
            table.add_row(
                "> " + f"{aspect_serializer(serializer)}",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time", output='base100'),
                results.repr_attr(serializer, dataobj, "encoding_strlen", output='base100'),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time", output='base100'),
                results.repr_attr(serializer, dataobj, "similarity")
            )
    msgreport(table)
    msgreport()


def report_section_c2b(results,
                       s1s2d):
    """
        report_section_c2b()

        Sub-function of report() for report section "C2b"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(C2b) Full Details: Data Objects (base 100)")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Data Object", width=24)
    table.add_column(f"Encod. Ok ? (Max={results.serializers_number})", width=11)

    if base100 := results.get_dataobjs_base('encoding_time'):
        table.add_column(
            "Σ Encoded Time "
            f"(Base 100 = {results.total_encoding_time(dataobj=base100)} {UNITS['time']})",
            width=11)
    else:
        table.add_column(f"Σ Encoded Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    if base100 := results.get_dataobjs_base('encoding_strlen'):
        table.add_column(
            "Σ Encoded Str. Length "
            f"(Base 100 = {results.total_encoding_strlen(dataobj=base100)} "
            f"{UNITS['string length']})",
            width=13)
    else:
        table.add_column(f"Σ Encoded Str. Length {aspect_nodata('(NO BASE 100)')}", width=13)

    table.add_column(f"Decod. Ok ? (Max={results.serializers_number})", width=11)

    if base100 := results.get_dataobjs_base('decoding_time'):
        table.add_column(
            "Σ Decoded Time "
            f"(Base 100 = {results.total_decoding_time(dataobj=base100)} "
            f"{UNITS['time']})",
            width=11)
    else:
        table.add_column(f"Σ Decoded Time {aspect_nodata('(NO BASE 100)')}",
                         width=11)

    table.add_column(f"Encod.<>Decod. ? (Max={results.serializers_number})", width=16)

    for dataobj in results.dataobjs:
        table.add_row(
            f"{aspect_data(dataobj)}",
            f"{results.ratio_encoding_success(dataobj=dataobj)}",
            f"{results.total_encoding_time(dataobj=dataobj, output='base100')}",
            f"{results.total_encoding_strlen(dataobj=dataobj, output='base100')}",
            f"{results.ratio_decoding_success(dataobj=dataobj)}",
            f"{results.total_decoding_time(dataobj=dataobj, output='base100')}",
            f"{results.ratio_similarity(dataobj=dataobj)}",
        )
    msgreport(table)
    msgreport()


def report_section_d1a(results,
                       s1s2d):
    """
        report_section_d1a()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    def show(serializer,
             cmpdata):
        """
            show()

            Print the message for serializer (str)<serializer> and for <cmpdata>.

            ___________________________________________________________________

            ARGUMENTS:
            o  (str)serializer
            o  (str)cmpdata              -> "all" or "ini" or "cwc", cf read_cmpstring()
        """
        data = wisteria.globs.DATA

        _list = []
        for dataobj_name in results.dataobjs:
            if results[serializer][dataobj_name].similarity:
                _list.append(dataobj_name)

        if not data:
            msgreport(
                f"{aspect_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                "no data objects may be used: therefore there's no conclusion about the objects "
                f"data serializer {aspect_serializer(serializer)} can handle.")
        elif not _list:
            msgreport(
                f"{aspect_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                "there's no data object "
                f"among the {len(results.dataobjs)} used data objects "
                f"that serializer {aspect_serializer(serializer)} can handle (0%).")
        elif len(_list) == 1:
            msgreport(
                f"{aspect_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{aspect_serializer(serializer)} can handle one data object "
                f"among {len(results.dataobjs)} "
                f"({aspect_percentage(100*len(_list)/len(results.dataobjs))}), namely "
                f"{aspect_list(tuple(f'{aspect_data(dataobj)}' for dataobj in _list))} .")
        else:
            msgreport(
                f"{aspect_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{aspect_serializer(serializer)} can handle {len(_list)} data objects "
                f"among {len(results.dataobjs)} "
                f"({aspect_percentage(100*len(_list)/len(results.dataobjs))}), namely "
                f"{aspect_list(tuple(f'{aspect_data(dataobj)}' for dataobj in _list))} .")

    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(D1a) Conclusion: Data Objects Handled by the Serializer(s)")
        msgreport()

    serializer1, serializer2, cmpdata = s1s2d
    if serializer1 != "all":
        show(serializer1, cmpdata)
        msgreport()
    if serializer2 != "all":
        show(serializer2, cmpdata)
        msgreport()

    # Other serializers, leaving apart <serializer1> and <serializer2> ?
    _serializers = list(wisteria.globs.SERIALIZERS.keys())
    if serializer1 != "all":
        _serializers.remove(serializer1)
    if serializer2 != "all":
        _serializers.remove(serializer2)
    if _serializers and (serializer1 == "all" or serializer2 == "all"):
        if serializer1 != "all" or serializer2 != "all":
            msgreport("[bold]Other serializers:[/bold]")
        for __serializer in _serializers:
            show(__serializer, cmpdata)
        msgreport()


def report_section_d1b(results,
                       s1s2d):
    """
        report_section_d1b()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    def show(serializer,
             cmpdata):
        """
            show()

            Print the message for serializer (str)<serializer> and for <cmpdata>.

            ___________________________________________________________________

            ARGUMENTS:
            o  (str)serializer
            o  (str)cmpdata              -> "all" or "ini" or "cwc", cf read_cmpstring()
        """
        data = wisteria.globs.DATA

        _list = []
        for dataobj_name in results.dataobjs:
            if not results[serializer][dataobj_name].similarity:
                _list.append(dataobj_name)

        if not data:
            msgreport(
                f"{aspect_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                "no data objects may be used: therefore there's no conclusion about the objects "
                f"data serializer {aspect_serializer(serializer)} can't handle.")
        elif not _list:
            msgreport(f"{aspect_serializer(serializer)}: "
                      f"{cmpdata2phrase(cmpdata)}"
                      "there's no data object "
                      f"among the {len(results.dataobjs)} used data objects "
                      f"that serializer {aspect_serializer(serializer)} can't handle (0%).")
        elif len(_list) == 1:
            msgreport(
                f"{aspect_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{aspect_serializer(serializer)} can't handle one data object "
                f"among {len(results.dataobjs)} "
                f"({aspect_percentage(100*len(_list)/len(results.dataobjs))}), namely "
                f"{aspect_list(tuple(f'{aspect_data(dataobj)}' for dataobj in _list))} .")
        else:
            msgreport(
                f"{aspect_serializer(serializer)}: "
                f"{cmpdata2phrase(cmpdata)}"
                f"{aspect_serializer(serializer)} can't handle {len(_list)} data objects "
                f"among {len(results.dataobjs)} "
                f"({aspect_percentage(100*len(_list)/len(results.dataobjs))}), namely "
                f"{aspect_list(tuple(f'{aspect_data(dataobj)}' for dataobj in _list))} .")

    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(D1b) Conclusion: "
                       "Data Objects [italic]NOT[/italic] Handled by the Serializer(s)")
        msgreport()

    serializer1, serializer2, cmpdata = s1s2d
    if serializer1 != "all":
        show(serializer1, cmpdata)
        msgreport()
    if serializer2 != "all":
        show(serializer2, cmpdata)
        msgreport()

    # Other serializers, leaving apart <serializer1> and <serializer2> ?
    _serializers = list(wisteria.globs.SERIALIZERS.keys())
    if serializer1 != "all":
        _serializers.remove(serializer1)
    if serializer2 != "all":
        _serializers.remove(serializer2)
    if _serializers and (serializer1 == "all" or serializer2 == "all"):
        if serializer1 != "all" or serializer2 != "all":
            msgreport("[bold]Other serializers:[/bold]")
        for __serializer in _serializers:
            show(__serializer, cmpdata)
        msgreport()


def report_section_d2a(results,
                       s1s2d):
    """
        report_section_d2a()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(D2a) Conclusion: Serializers ([italic]Not Sorted[/italic])")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer", width=25)
    table.add_column(f"Σ Encoded Str. Length ({UNITS['string length']})", width=16)
    table.add_column(f"Σ Encod.+Decod. Time ({UNITS['time']})", width=16)
    table.add_column(f"Encod.<>Decod. ? (Max={results.dataobjs_number})", width=16)

    serializer1, serializer2, _ = s1s2d
    _serializers = []
    if serializer1 != "all":
        _serializers.append(serializer1)
    if serializer2 != "all":
        _serializers.append(serializer2)
    _serializers.append("-")
    for serializer in results.serializers:
        if serializer not in _serializers:
            _serializers.append(serializer)
    if _serializers[-1] == "-":
        # let's remove this useless '-' since there's no more serializer(s) after.
        _serializers.pop()

    for serializer in _serializers:
        if serializer != "-":
            table.add_row(
                f"{aspect_serializer(serializer)}",
                f"{results.total_encoding_strlen(serializer=serializer)}",
                f"{results.total_encoding_plus_decoding_time(serializer=serializer)}",
                f"{results.ratio_similarity(serializer=serializer)}")
        else:
            table.add_row(
                "-",
                "-",
                "-",
                "-")

    msgreport(table)
    msgreport()


def report_section_d2b(results,
                       s1s2d):
    """
        report_section_d2b()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(D2b) "
                       "Conclusion: Overall Score Based on 3 Points "
                       "(Σ Encoded Str./Σ Encod.+Decod. Time/Encod.<>Decod.)")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("Serializer", width=25)
    table.add_column("Overall Score", width=13)

    serializer1, serializer2, _ = s1s2d
    _serializers = []
    if serializer1 != "all":
        _serializers.append(serializer1)
    if serializer2 != "all":
        _serializers.append(serializer2)
    _serializers.append("-")
    for serializer in results.serializers:
        if serializer not in _serializers:
            _serializers.append(serializer)
    if _serializers[-1] == "-":
        # let's remove this useless '-' since there's no more serializer(s) after.
        _serializers.pop()

    for serializer in _serializers:
        if serializer != "-":
            table.add_row(
                f"{aspect_serializer(serializer)}",
                f"{results.overallscores[serializer]}")
        else:
            table.add_row(
                "-",
                "-")

    msgreport(table)
    msgreport()


def report_section_d2c(results,
                       s1s2d):
    """
        report_section_d2c()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(D2c) Conclusion")

    serializer1, serializer2, cmpdata = s1s2d

    text = TextAndNotes()
    text.append(cmpdata2phrase(cmpdata))

    if serializer1 == "all" and serializer2 == "all":
        # ========================================================
        # (CASE 1/3) serializer1 and serializer2 are both == "all"
        # ========================================================
        text.append(f"{aspect_serializer(results.halloffame['encoding_plus_decoding_time'][0][1])} "
                    "is the quickest to encode/decode, ")
        text.append(f"{aspect_serializer(results.halloffame['encoding_strlen'][0][1])} "
                    "produces the shortest strings, ")
        text.append(f"and {aspect_serializer(results.halloffame['similarity'][0][1])} "
                    "has the best coverage. ")

        bests = results.get_overallscore_bestrank()
        if len(bests) == 1:
            text.append(f"{aspect_list(bests)} is ranked #1 "
                        f"among {results.serializers_number} serializers, "
                        "according to the overall scores (__note:overallscore__).")
        else:
            text.append(f"{aspect_list(bests)} "
                        f"are ranked #1 among {results.serializers_number} serializers, "
                        "according to the overall scores (__note:overallscore__).")

        text.append("\nConversely, ")
        text.append(
            f"{aspect_serializer(results.halloffame['encoding_plus_decoding_time'][-1][1])} "
            "is the slowest to encode/decode, ")
        text.append(f"{aspect_serializer(results.halloffame['encoding_strlen'][-1][1])} "
                    "produces the longest strings, ")
        text.append(f"and {aspect_serializer(results.halloffame['similarity'][-1][1])} "
                    "has the worst coverage. ")

        worsts = results.get_overallscore_worstrank()
        if len(worsts) == 1:
            text.append(f"{aspect_serializer(worsts[0])} is ranked #{results.serializers_number} "
                        f"among {results.serializers_number} serializers, "
                        "according to the overall scores (__note:overallscore__).")
        else:
            text.append(
                f"{aspect_list(worsts)} "
                f"are ranked #{results.serializers_number} among "
                f"{results.serializers_number} serializers, "
                "according to the overall scores (__note:overallscore__).")

        text.notes.append(
            ("overallscore"
             "a rank based on 3 points: Σ encoded str./Σ encod.+decod. time/encod.<>decod."))

    elif serializer1 != "all" and serializer2 != "all":
        # ========================================================
        # (CASE 2/3) serializer1 and serializer2 are both != "all"
        # ========================================================

        # ---- encoding/decoding time -----------------------------------------
        total_encoding_time_ratio = \
            results.total_encoding_plus_decoding_time(serializer=serializer1, output='value') \
            / results.total_encoding_plus_decoding_time(serializer=serializer2,
                                                        output='value')

        if total_encoding_time_ratio == 1:
            text.append(
                f"{aspect_serializer(serializer1)} "
                f"and {aspect_serializer(serializer2)} "
                "seem to require exactly the same time to encode and decode; ")
        else:
            text.append(
                f"{aspect_serializer(serializer1)} "
                f"is {ratio2phrase(total_encoding_time_ratio, 'slow/fast')} "
                f"- by a factor of {humanratio(total_encoding_time_ratio):.3f} "
                "(__note:total_encoding_time_ratio__) - "
                "than "
                f"{aspect_serializer(serializer2)} "
                "to encode and decode; ")

            text.notes.append(
                ("total_encoding_time_ratio",
                 humanratio(
                     total_encoding_time_ratio,
                     explanations=(
                         f"{aspect_serializer(serializer1)}'s Σ encod.+decod. time",
                         results.total_encoding_plus_decoding_time(serializer=serializer1,
                                                                   output='value'),
                         f"{aspect_serializer(serializer2)}'s Σ encod.+decod. time",
                         results.total_encoding_plus_decoding_time(serializer=serializer2,
                                                                   output='value'),
                         'time',
                     ))))

        # ---- total_encoding_strlen -----------------------------------------
        total_encoding_strlen_ratio = \
            results.total_encoding_strlen(serializer=serializer1, output='value') \
            / results.total_encoding_strlen(serializer=serializer2,
                                            output='value')

        if total_encoding_strlen_ratio == 1:
            text.append(f"{aspect_serializer(serializer1)} "
                        f"and {aspect_serializer(serializer2)} "
                        "seem to produce strings that have exactly the same size; ")
        else:
            text.append("strings produced by "
                        f"{aspect_serializer(serializer1)} "
                        f"are {ratio2phrase(total_encoding_strlen_ratio, 'long/short')} "
                        f"- by a factor of {humanratio(total_encoding_strlen_ratio):.3f} "
                        f"(__note:total_encoding_strlen_ratio__) - "
                        "than "
                        f"strings produced by {aspect_serializer(serializer2)}; ")

            text.notes.append(
                ("total_encoding_strlen_ratio",
                 humanratio(
                     total_encoding_strlen_ratio,
                     explanations=(
                         f"{aspect_serializer(serializer1)}'s jsonstring strlen",
                         results.total_encoding_strlen(serializer=serializer1,
                                                       output='value'),
                         f"{aspect_serializer(serializer2)}'s jsonstring strlen",
                         results.total_encoding_strlen(serializer=serializer2,
                                                       output='value'),
                         'string length',
                     ))))

        # ---- ratio_similarity -----------------------------------------------
        ratio_similarity = \
            results.ratio_similarity(serializer=serializer1, output='value') \
            / results.ratio_similarity(serializer=serializer2,
                                       output='value')

        if ratio_similarity == 1:
            text.append(f"{aspect_serializer(serializer1)} "
                        f"and {aspect_serializer(serializer2)} "
                        "seem to have exactly the same data coverage.")
        else:
            text.append(f"{aspect_serializer(serializer1)}'s coverage "
                        f"is {ratio2phrase(ratio_similarity, 'good/bad')} "
                        f"- by a factor of {humanratio(ratio_similarity):.3f} "
                        f"(__note:ratio_similarity__) - "
                        "than "
                        f"{aspect_serializer(serializer2)}'s coverage.")

            text.notes.append(
                ("ratio_similarity",
                 humanratio(
                     ratio_similarity,
                     explanations=(
                         f"{aspect_serializer(serializer1)}'s similarity ratio",
                         results.ratio_similarity(serializer=serializer1,
                                                  output='value'),
                         f"{aspect_serializer(serializer2)}'s similarity ratio",
                         results.ratio_similarity(serializer=serializer2,
                                                  output='value'),
                         None,
                     ))))

    else:
        # =====================================================================
        # (CASE 3/3) One of the two {serializer1|serializer2} is equal to "all"
        # =====================================================================

        # <serializer> is the reference serializer againt all others.
        if serializer1 != "all":
            serializer = serializer1
        else:
            serializer = serializer2
        rank = results.get_overallscore_rank(serializer)
        text.append(f"{aspect_serializer(serializer)} "
                    f"is ranked #{rank} among {len(results.serializers)} serializers "
                    f"(__note:overallscore__)")
        text.append(". ")

        text.notes.append(
            ("overallscore",
             "a rank based on 3 points: Σ jsonstr.len./Σ encod.+decod. time/encod.<>decod."))

        for attribute in ("encoding_strlen",
                          "encoding_plus_decoding_time",
                          "similarity",
                          ):
            subtext = []
            _less, _more = results.comparison_inside_halloffame(serializer, attribute)

            if attribute == "encoding_strlen":
                if not _less:
                    subtext.append(
                        "There's no serializer that produces longer strings than "
                        f"{aspect_serializer(serializer)} ")
                elif len(_less) == 1:
                    subtext.append(
                        f"Only {aspect_serializer(_less[0])} produces longer string than "
                        f"{aspect_serializer(serializer)} ")
                else:
                    subtext.append(
                        f"There are {len(_less)} serializers"
                        ", namely "
                        f"{aspect_list(tuple(f'{aspect_serializer(_seria)}' for _seria in _less))} "
                        f"that produce longer strings than {aspect_serializer(serializer)} ")

                subtext.append("and ")

                if not _more:
                    subtext.append(
                        "there's no serializer that produces shorter strings than "
                        f"{aspect_serializer(serializer)}")
                elif len(_more) == 1:
                    subtext.append(
                        f"only {aspect_serializer(_more[0])} produces shorter string than "
                        f"{aspect_serializer(serializer)}")
                else:
                    subtext.append(
                        f"there are {len(_more)} serializers"
                        ", namely "
                        f"{aspect_list(tuple(f'{aspect_serializer(_seria)}' for _seria in _more))} "
                        f"that produce shorter strings than {aspect_serializer(serializer)}")

                subtext.append(". ")

            elif attribute == "encoding_plus_decoding_time":
                if not _less:
                    subtext.append(
                        "There's no serializer slower than "
                        f"{aspect_serializer(serializer)} ")
                elif len(_less) == 1:
                    subtext.append(
                        f"Only {aspect_serializer(_less[0])} is slower than "
                        f"{aspect_serializer(serializer)} ")
                else:
                    subtext.append(
                        f"There are {len(_less)} serializers"
                        ", namely "
                        f"{aspect_list(tuple(f'{aspect_serializer(_seria)}' for _seria in _less))}"
                        f"that are slower than {aspect_serializer(serializer)} ")

                subtext.append("and ")

                if not _more:
                    subtext.append(
                        "there's no serializer that is faster than "
                        f"{aspect_serializer(serializer)}")
                elif len(_more) == 1:
                    subtext.append(
                        f"only {aspect_serializer(_more[0])} is faster than "
                        f"{aspect_serializer(serializer)}")
                else:
                    subtext.append(
                        f"there are {len(_more)} serializers"
                        ", namely "
                        f"{aspect_list(tuple(f'{aspect_serializer(_seria)}' for _seria in _more))} "
                        f"that are faster than {aspect_serializer(serializer)}")

                subtext.append(". ")

            elif attribute == "similarity":
                if not _less:
                    subtext.append(
                        "There's no serializer is worse than "
                        f"{aspect_serializer(serializer)} "
                        "when it comes to data coverage ")
                elif len(_less) == 1:
                    subtext.append(
                        f"Only {aspect_serializer(_less[0])} is worse than "
                        f"{aspect_serializer(serializer)} "
                        "when it comes to data coverage ")
                else:
                    subtext.append(
                        f"There are {len(_less)} serializers"
                        ", namely "
                        f"{aspect_list(tuple(f'{aspect_serializer(_seria)}' for _seria in _less))} "
                        f"that are worse than {aspect_serializer(serializer)} "
                        "when it comes to data coverage ")

                subtext.append("and ")

                if not _more:
                    subtext.append(
                        "there's no serializer is better than "
                        f"{aspect_serializer(serializer)} "
                        "when it comes to data coverage")
                elif len(_more) == 1:
                    subtext.append(
                        f"only {aspect_serializer(_more[0])} is better than "
                        f"{aspect_serializer(serializer)} "
                        "when it comes to data coverage")
                else:
                    subtext.append(
                        f"there are {len(_more)} serializers"
                        ", namely "
                        f"{aspect_list(tuple(f'{aspect_serializer(_seria)}' for _seria in _more))} "
                        f"that are better than {aspect_serializer(serializer)} "
                        "when it comes to data coverage")

                subtext.append(". ")

            text.append("".join(subtext))

    msgreport(text.output())
    msgreport()


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_e1a(results,
                       s1s2d):
    """
        report_section_e1a()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(E1a) Informations About The Machine ([italic]No Details[/italic])")

    mymachine(fulldetails=False)


# Since all report_() functions have the same signature, it may happen that
# some arguments passed to the function are not used.
# pylint: disable=unused-argument
def report_section_e1b(results,
                       s1s2d):
    """
        report_section_e1b()

        Sub-function of report() for report section "A3"
        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult

        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if "titles;" in wisteria.globs.ARGS.report:
        msgreporttitle("(E1b) Informations About The Machine ([italic]Full Details[/italic])")

    mymachine(fulldetails=True)


# STR2REPORTSECTION has two goals:
# (1) translate a (str)report section name > list of corresponding functions
# (2) store all known keys accepted in --report.
STR2REPORTSECTION = {
        "titles": None,
        "A": (report_section_a1,
              report_section_a2,
              report_section_a3,),
        "A1": (report_section_a1,),
        "A2": (report_section_a2,),
        "A3": (report_section_a3,),
        "B": (report_section_b1a,
              report_section_b1b,
              report_section_b1c,
              report_section_b1d,
              report_section_b2a,
              report_section_b2b,),
        "B1": (report_section_b1a,
               report_section_b1b,
               report_section_b1c,
               report_section_b1d,),
        "B1a": (report_section_b1a,),
        "B1b": (report_section_b1b,),
        "B1c": (report_section_b1c,),
        "B1d": (report_section_b1d,),
        "B2": (report_section_b2a,
               report_section_b2b,),
        "B2a": (report_section_b2a,),
        "B2b": (report_section_b2b,),
        "C": (report_section_c1a,
              report_section_c1b,
              report_section_c2a,
              report_section_c2b,),
        "C1": (report_section_c1a,
               report_section_c1b,),
        "C1a": (report_section_c1a,),
        "C1b": (report_section_c1b,),
        "C2": (report_section_c2b,),
        "C2a": (report_section_c2a,),
        "C2b": (report_section_c2b,),
        "D": (report_section_d1a,
              report_section_d1b,
              report_section_d2a,
              report_section_d2b,
              report_section_d2c,),
        "D1": (report_section_d1a,
               report_section_d1b,),
        "D1a": (report_section_d1a,),
        "D1b": (report_section_d1b,),
        "D2": (report_section_d2a,
               report_section_d2b,
               report_section_d2c),
        "D2a": (report_section_d2a,),
        "D2b": (report_section_d2b,),
        "D2c": (report_section_d2c,),
        "E": (report_section_e1a,
              report_section_e1b,),
        "E1": (report_section_e1a,
               report_section_e1b),
        "E1a": (report_section_e1a,),
        "E1b": (report_section_e1b,),
}


def report(results,
           s1s2d):
    """
        report()

        Print an analyze of <results>.

        (pimydoc)report sections
        ⋅* A         : main informations
        ⋅  - A1      : main title
        ⋅  - A2      : list of the serializers to be used
        ⋅  - A3      : list of the data objects to be used
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: serializers, hall of fame
        ⋅    . B1d   : full details: full details: <S> serializer can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C         : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        ⋅* D         : conclusions
        ⋅  - D1      : conclusion: data objects handled/not handled by the serializer(s)
        ⋅    . D1a   : conclusion: data objects handled by the serializer(s)
        ⋅    . D1b   : conclusion: data objects NOT handled by the serializer(s)
        ⋅  - D2      : conclusion: final text and data
        ⋅    . D2a   : conclusion: serializers (not sorted)
        ⋅    . D2b   : conclusion: overall score (based on: Σ strlen./Σ enc+dec time/enc⇆dec)
        ⋅    . D2c   : conclusion
        ⋅* E         : various informations
        ⋅  - E1      : informations about the machine
        ⋅    . E1a   : informations about the machine (no details)
        ⋅    . E1b   : informations about the machine (full details)
        _______________________________________________________________________

        ARGUMENTS:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
        o  s1s2d: ( (str)serializer1,
                    (str)serializer2,
                    (str)cmpdata         -> "all" or "ini" or "cwc", cf read_cmpstring()
                  )
    """
    if wisteria.globs.ARGS.report.strip() == ";":
        raise WisteriaError(
            f"(ERRORID018) Can't interpret report section which is empty. "
            f"Accepted keywords are {tuple(STR2REPORTSECTION.keys())}. "
            f"You may simply use shortcuts ({tuple(REPORT_SHORTCUTS.keys())}) "
            "but be sure to use this shortcut alone, with nothing else in the --report string. "
            "More informations in the documentation.")

    for report_section in wisteria.globs.ARGS.report.split(";"):
        report_section = report_section.strip()

        if report_section == "":
            pass
        elif report_section in STR2REPORTSECTION and STR2REPORTSECTION[report_section] is not None:
            for func in STR2REPORTSECTION[report_section]:
                func(results, s1s2d)
        elif report_section in STR2REPORTSECTION and STR2REPORTSECTION[report_section] is None:
            # special keywords (like 'titles') that don't match any function in <STR2REPORTSECTION>.
            pass
        elif report_section.strip() != "":
            raise WisteriaError(
                f"(ERRORID017) Can't interpret report section; "
                f"what is '{report_section}' ? args.report is '{wisteria.globs.ARGS.report}' . "
                f"Accepted keywords are {tuple(STR2REPORTSECTION.keys())}. "
                f"You may simply use shortcuts ({tuple(REPORT_SHORTCUTS.keys())}) "
                "but be sure to use this shortcut alone, with nothing else in the --report string. "
                "More informations in the documentation.")

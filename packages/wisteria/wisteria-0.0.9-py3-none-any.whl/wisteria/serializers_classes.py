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
    Wisteria project : wisteria/serializers_classes.py

    All classes required to handle serializers.

    ___________________________________________________________________________

    o  SerializerData class
    o  SerializerDataObj class
    o  SerializationResult class
    o  SerializationResults class
"""
from dataclasses import dataclass

from wisteria.wisteriaerror import WisteriaError
from wisteria.reportaspect import aspect_serializer, aspect_ratio, aspect_time, aspect_nodata
from wisteria.reportaspect import aspect_base100, aspect_stringlength, aspect_boolsuccess
from wisteria.msg import msgerror


class SerializerData:
    """
        SerializerData class

        SerializerData are used to store infos. about serializers in the SERIALIZERS dict.

        _______________________________________________________________________

        instance attributes:

        o  (str)name
        o  (str)human_name
        o  (str)internet
        o  (str)version
        o  (callable)func   : function to be called to use this serializer


        methods:

        o  __init__(self, name, module_name, human_name, internet, func)
        o  __repr__(self)
        o  checkup_repr(self)
        o  simple_repr(self)
    """
    def __init__(self,
                 name,
                 module_name,
                 human_name,
                 internet,
                 func):
        """
            SerializerData.__init__()

            ___________________________________________________________________

            ARGUMENTS:
            o  (str)name
            o  (str)module_name
            o  (str)human_name
            o  (str)internet
            o  (str)version
            o  (callable)func   : function to be called to use this serializer
        """
        self.name = name
        self.module_name = module_name
        self.human_name = human_name
        self.internet = internet
        self.version = None
        self.func = func

    def __repr__(self):
        """
            SerializerData.__repr__()

            For the check up output, see .checkup_repr().

            ___________________________________________________________________

            RETURNED VALUE: (str)a basic representation of <self>.
                            See also .checkup_repr() and .simple_repr()
        """
        return f"{self.name=}; {self.module_name=}; {self.human_name=}; {self.internet=}; " \
            f"{self.version=}; {self.func=}"

    def checkup_repr(self):
        """
            SerializerData.checkup_repr()

            Does the same as .__repr__() but for the check up output.

            ___________________________________________________________________

            RETURNED VALUE: (str)a basic representation of <self>.
                            See also .__repr__() and .simple_repr()
        """
        return f"{aspect_serializer(self.name)} ({self.version}), see {self.internet} ."

    def simple_repr(self):
        """
            SerializerData.simple_repr()

            Does the same as .__repr__() but for a simple output.

            ___________________________________________________________________

            RETURNED VALUE: (str)a basic representation of <self>.
                            See also .checkup_repr() and .__repr__()
        """
        return f"{aspect_serializer(self.name)} ({self.version})"


@dataclass
class SerializerDataObj:
    """
        SerializerDataObj class

        Nothing but an easy way to store (serializer, dataobj)

        _______________________________________________________________________

        methods:

        o  serializer: (str)
        o  dataobj:    (str)
    """
    serializer: str = None
    dataobj: str = None


# No useless public methods to add, indeed!
# pylint: disable=too-few-public-methods
class SerializationResult:
    """
        SerializationResult class

        Class used to store tests results in a SerializationResults object.

        _______________________________________________________________________

        instance attributes:
        o  (bool)encoding_success
        o  (bool)encoding_time
        o  (bool)encoding_strlen
        o  (bool)decoding_success
        o  (bool)decoding_time
        o  (bool)similarity


        methods:

        o  __init__(self)
        o  __repr__(self)
    """
    def __init__(self):
        """
            SerializationResult.__init__()

            ___________________________________________________________________

            ARGUMENTS:

            o  (bool)encoding_success
            o  (bool)encoding_time
            o  (bool)encoding_strlen
            o  (bool)decoding_success
            o  (bool)decoding_time
            o  (bool)similarity
        """
        self.encoding_success = False
        self.encoding_time = None
        self.encoding_strlen = None
        self.decoding_success = False
        self.decoding_time = None
        self.similarity = False

    def __repr__(self):
        """
            SerializationResult.__repr__()
        """
        return f"{self.encoding_success=}; {self.encoding_time=}; {self.encoding_strlen=}; " \
            f"{self.decoding_success=}; {self.decoding_time=}; {self.similarity=}"


class SerializationResults(dict):
    """
        SerializationResults class

        SerializationResults objects are used to store all results created during the tests.

        A SerializationResults object has the following structure:
                SerializationResults[(str)serializer][(str)dataobj] = SerializationResult object

        Do not forget to call .finish_initialization() once you have finished initializing <self>.

        _______________________________________________________________________

        instance attributes:

        o  (list)serializers        : list of str
        o  (list)dataobjs           : list of str
        o  (int) serializers_number : =len(self.serializers)
        o  (int) dataobjs_number    : =len(self.dataobjs)
        o  (dict)halloffame         : e.g. {'encoding_success' = [(0.24, 'marshal'),
                                                                  (0.22, 'pickle')],
                                            ...

                                      keys are: 'encoding_success', 'encoding_time',
                                                'encoding_strlen',
                                                'decoding_success', 'decoding_time',
                                                'similarity',
                                                'encoding_plus_decoding_time'
        o  (dict)overallscores      : overallscores[serializer] = (int)overallscore


        methods:

        o  __init__(self)
        o  comparison_inside_halloffame(self, serializer, attribute)
        o  finish_initialization(self)
        o  get_base(self, attribute)
        o  get_dataobjs_base(self, attribute)
        o  get_halloffame(self, attribute, index)
        o  get_overallscore_rank(self, serializer)
        o  get_overallscore_bestrank(self)
        o  get_overallscore_worstrank(self)
        o  get_serializers_base(self, attribute)
        o  ratio_decoding_success(self, serializer=None, dataobj=None, output="fmtstr")
        o  ratio_encoding_success(self, serializer=None, dataobj=None, output="fmtstr")
        o  ratio_similarity(self, serializer=None, dataobj=None, output="fmtstr")
        o  repr_attr(self, serializer, dataobj, attribute_name, output="fmtstr")
        o  total_decoding_time(self, serializer=None, dataobj=None, output="fmtstr")
        o  total_encoding_plus_decoding_time(self, serializer=None, dataobj=None, output="fmtstr")
        o  total_encoding_strlen(self, serializer=None, dataobj=None, output="fmtstr")
        o  total_encoding_time(self, serializer=None, dataobj=None, output="fmtstr")
    """
    def __init__(self):
        """
            SerializationResults.__init__()

            ___________________________________________________________________

            ARGUMENTS:
            o  (list)serializers        : list of str
            o  (list)dataobjs           : list of str
            o  (int) serializers_number : =len(self.serializers)
            o  (int) dataobjs_number    : =len(self.dataobjs)
            o  (dict)halloffame         : e.g. {'encoding_success' = [(0.24, 'marshal'),
                                                                      (0.22, 'pickle')],
                                                ...

                                          keys are: 'encoding_success', 'encoding_time',
                                                    'encoding_strlen',
                                                    'decoding_success', 'decoding_time',
                                                    'similarity',
                                                    'encoding_plus_decoding_time'
            o  (dict)overallscores      : overallscores[serializer] = (int)overallscore
        """
        dict.__init__(self)
        self.serializers = []
        self.dataobjs = []
        self.serializers_number = None
        self.dataobjs_number = None
        self.halloffame = None
        self.overallscores = None

    def comparison_inside_halloffame(self,
                                     serializer,
                                     attribute):
        """
            SerializationResults.comparison_inside_halloffame()

            Returns the serializers better placed than <serializer>
            (=placed before <serializer>) and the less well placed
            serializers than <serializer> (=placed after <serializer>)
            in relation to <attribute>.

            ___________________________________________________________________

            ARGUMENTS:
            o  (str)serializer
            o  (str)attribute

            RETURNED VALUE: (list of better placed serializers than <serializer>,
                             list of less well placed serializers than <serializer>)
        """
        _less = []
        _more = []

        before_serializer = False  # will be True when <serializer> will be read in the loop.
        for index in range(self.serializers_number):
            if self.halloffame[attribute][index][1] == serializer:
                before_serializer = True
            elif before_serializer:
                _less.append(self.halloffame[attribute][index][1])
            else:
                _more.append(self.halloffame[attribute][index][1])

        return _less, _more

    def finish_initialization(self):
        """
            SerializationResults.finish_initialization()

            Once the initialization of <self> is over, this method must be called to
            set self.self.serializers, self.dataobjs, self.serializers_number
            self.dataobjs_number, self.halloffame and self.overallscores

            ___________________________________________________________________

            RETURNED VALUE: (bool)success
        """
        self.serializers = sorted(self.keys())
        self.serializers_number = len(self.serializers)

        if self.serializers_number == 0:
            msgerror("(ERRORID016) Incorrect data, there's no serializer.")
            return False

        first_serializer = tuple(self.serializers)[0]
        self.dataobjs = sorted(self[first_serializer].keys())
        self.dataobjs_number = len(self.dataobjs)

        self.halloffame = {
            "encoding_success": sorted(((self.ratio_encoding_success(serializer=serializer,
                                                                     output="value"),
                                         serializer) for serializer in self.serializers),
                                       reverse=True),
            "encoding_time": sorted(((self.total_encoding_time(serializer=serializer,
                                                               output="value"),
                                      serializer) for serializer in self.serializers),
                                    reverse=False),
            "decoding_success": sorted(((self.ratio_decoding_success(serializer=serializer,
                                                                     output="value"),
                                         serializer) for serializer in self.serializers),
                                       reverse=True),
            "decoding_time": sorted(((self.total_decoding_time(serializer=serializer,
                                                               output="value"),
                                      serializer) for serializer in self.serializers),
                                    reverse=False),
            "encoding_strlen": sorted(((self.total_encoding_strlen(serializer=serializer,
                                                                   output="value"),
                                        serializer) for serializer in self.serializers),
                                      reverse=False),
            "similarity": sorted(((self.ratio_similarity(serializer=serializer,
                                                         output="value"),
                                   serializer) for serializer in self.serializers),
                                 reverse=True),
            "encoding_plus_decoding_time": sorted(((self.total_encoding_time(serializer=serializer,
                                                                             output="value") +
                                                    self.total_decoding_time(serializer=serializer,
                                                                             output="value"),
                                                    serializer) for serializer in self.serializers),
                                                  reverse=False),
            }

        # overall score computing:
        # * if a serializer is #0 (first rank) for a certain attribute,
        #   its score increases by results.serializers_number-0.
        # * if a serializer is #1 (first rank) for a certain attribute,
        #   its score increases by results.serializers_number-1.
        # * ...
        self.overallscores = {}
        for serializer in self.serializers:
            self.overallscores[serializer] = 0

            for attribute in ('encoding_plus_decoding_time',
                              'encoding_strlen',
                              'similarity',
                              ):
                for index in range(self.serializers_number):
                    if self.halloffame[attribute][index][1] == serializer:
                        self.overallscores[serializer] += self.serializers_number-index

        return True

    def get_base(self,
                 attribute):
        """
            SerializationResults.get_base()

            Return <serializer, base data object> for attribute <attribute>.

            In other words, get_base() searches the first available couple
            of <serializer, base data object> which is initialized so that
            this couple could be a base for the <attribute>.

            ___________________________________________________________________

            ARGUMENT:
            o  (str)attribute, with only 3 values, namely "encoding_time",
               "decoding_time" and "encoding_strlen".

            RETURNED VALUE: (SerializerDataObj), i.e. serializer + dataobj
        """
        assert attribute in ("encoding_time", "decoding_time", "encoding_strlen")

        if attribute == "encoding_time":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj] is not None and \
                       self[serializer][dataobj].encoding_time:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        if attribute == "decoding_time":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj] is not None and \
                       self[serializer][dataobj].decoding_time:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        if attribute == "encoding_strlen":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj] is not None and \
                       self[serializer][dataobj].encoding_strlen:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        return None  # this line should never be executed.

    def get_dataobjs_base(self,
                          attribute):
        """
            SerializationResults.get_dataobjs_base()

            Return a data object that may be a reference data object, for
            the attribute <attribute>.

            In other words, get_dataobjs_base() answers the question:
                Among all data objects, what's the first that could be a
            reference data object ? The serializers have no importance here,
            we just have to look at the data objects, the first one being
            often the right one.
            The selected data object must have its .encoding_success set
            to True for all serializers.

            ___________________________________________________________________

            ARGUMENT:
            o  (str)attribute, with only 3 values, namely "encoding_time",
               "decoding_time" and "encoding_strlen".

            RETURNED VALUE: (str)dataobject name or None if no data object
                            is adequate.
        """
        assert attribute in ("encoding_time", "decoding_time", "encoding_strlen")

        if attribute == "encoding_time":
            for dataobj in self.dataobjs:
                found = True
                for serializer in self.serializers:
                    if self[serializer][dataobj] is not None and \
                       not self[serializer][dataobj].encoding_success:
                        found = False
                        break
                if found:
                    return dataobj
            return None

        if attribute == "encoding_strlen":
            for dataobj in self.dataobjs:
                found = True
                for serializer in self.serializers:
                    if self[serializer][dataobj] is not None and \
                       not self[serializer][dataobj].encoding_strlen:
                        found = False
                        break
                if found:
                    return dataobj
            return None

        if attribute == "decoding_time":
            for dataobj in self.dataobjs:
                found = True
                for serializer in self.serializers:
                    if self[serializer][dataobj] is not None and \
                       not self[serializer][dataobj].decoding_time:
                        found = False
                        break
                if found:
                    return dataobj
            return None

        return None  # this line should never be executed.

    def get_halloffame(self,
                       attribute,
                       index):
        """
            SerializationResults.get_halloffame()

            Return the formatted string result of the 'hall of fame'
            for a given <attribute> and an <index>.
            In other words, answer the question: which serializer is number
            #<index> for a given <attribute> ?

            ___________________________________________________________________

            ARGUMENT:
            o  (str)attribute: 'encoding_success' or
                               'encoding_time' or
                               'decoding_success' or
                               'decoding_time' or
                               'encoding_strlen' or
                               'similarity'
            o  (int)index: 0 <= index < len(self.serializers_numbers-1)

            RETURNED VALUE: (str)a formatted string describing the result.
        """
        assert attribute in ('encoding_success',
                             'encoding_time',
                             'decoding_success',
                             'decoding_time',
                             'encoding_strlen',
                             'similarity')

        serializer = self.halloffame[attribute][index][1]
        value = self.halloffame[attribute][index][0]

        if attribute == 'encoding_success':
            return f"{aspect_serializer(serializer)} " \
                f"[{self.ratio_encoding_success(serializer=serializer)}]"

        if attribute == 'encoding_time':
            return f"{aspect_serializer(serializer)} " \
                f"[{aspect_time(value)}]"

        if attribute == 'decoding_success':
            return f"{aspect_serializer(serializer)} " \
                f"[{self.ratio_decoding_success(serializer=serializer)}]"

        if attribute == 'decoding_time':
            serializer = self.halloffame[attribute][index][1]
            return f"{aspect_serializer(serializer)} " \
                f"[{aspect_time(value)}]"

        if attribute == 'similarity':
            serializer = self.halloffame[attribute][index][1]
            return f"{aspect_serializer(serializer)} " \
                f"[{self.ratio_similarity(serializer=serializer)}]"

        if attribute == 'encoding_strlen':
            serializer = self.halloffame[attribute][index][1]
            return f"{aspect_serializer(serializer)} " \
                f"[{aspect_stringlength(value)}]"

        return None  # this line should never be executed.

    def get_overallscore_rank(self,
                              serializer):
        """
            SerializationResults.get_overallscore_rank()

            Return the (int)rank of <serializer> among 'overall scores'.

            ___________________________________________________________________

            ARGUMENT:
            o  (str)serializer

            RETURNED VALUE: (int)rank, 0 <= rank < len(self.serializers_numbers)
        """
        _rank = None

        # for rank, (score, _serializer) ...
        for rank, (_, _serializer) in enumerate(sorted(
                ((self.overallscores[serializer],
                  serializer) for serializer in self.serializers), reverse=True)):
            if serializer == _serializer:
                _rank = rank

        return _rank

    def get_overallscore_bestrank(self):
        """
            SerializationResults.get_overallscore_bestrank()

            Return the list of the serializers with the best score
            among "overall scores". There's maybe more than one serializer
            having the highest score, hence the returned list.

            ___________________________________________________________________

            RETURNED VALUE: (list)list of (str)serializers
        """
        highestscore = sorted(
            ((self.overallscores[serializer],
              serializer) for serializer in self.serializers))[-1][0]
        res = []
        for serializer in self.serializers:
            if self.overallscores[serializer] == highestscore:
                res.append(serializer)
        return res

    def get_overallscore_worstrank(self):
        """
            SerializationResults.get_overallscore_worstrank()

            Return the list of the serializers with the worst score
            among "overall scores". There's maybe more than one serializer
            having the worst score, hence the returned list.

            ___________________________________________________________________

            RETURNED VALUE: (list)list of (str)serializers
        """
        worstscore = sorted(
            ((self.overallscores[serializer],
              serializer) for serializer in self.serializers))[0][0]
        res = []
        for serializer in self.serializers:
            if self.overallscores[serializer] == worstscore:
                res.append(serializer)
        return res

    def get_serializers_base(self,
                             attribute):
        """
            SerializationResults.get_serializers_base()

            Return a serializer that may be a reference serializer, for
            the attribute <attribute>.

            In other words, get_serializers_base() answers the question:
                Among all serializers, what's the first that could be a
            reference serializer ? The data objects have no importance here,
            we just have to look at the serializers, the first one being
            often the right one.
            The selected serializer must have its .encoding_success set
            to True for all data objects.

            ___________________________________________________________________

            ARGUMENT:
            o  (str)attribute, with only 3 values, namely "encoding_time",
               "decoding_time" and "encoding_strlen".

            RETURNED VALUE: (str)serializer or None if no serializer
                            is adequate.
        """
        assert attribute in ("encoding_time", "decoding_time", "encoding_strlen")

        if attribute == "encoding_time":
            for serializer in self.serializers:
                found = True
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj] is not None and \
                       not self[serializer][dataobj].encoding_success:
                        found = False
                        break
                if found:
                    return serializer
            return None

        if attribute == "encoding_strlen":
            for serializer in self.serializers:
                found = True
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj] is not None and \
                       not self[serializer][dataobj].encoding_strlen:
                        found = False
                        break
                if found:
                    return serializer
            return None

        if attribute == "decoding_time":
            for serializer in self.serializers:
                found = True
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj] is not None and \
                       not self[serializer][dataobj].decoding_time:
                        found = False
                        break
                if found:
                    return serializer
            return None

        return None  # this line should never be executed.

    def ratio_decoding_success(self,
                               serializer=None,
                               dataobj=None,
                               output="fmtstr"):
        """
            SerializationResults.ratio_decoding_success()

            Compute and format the ratio of decoding success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  <output>(str): "fmtstr" for a formatted returned string or "value"
               for the (float)raw value

            RETURNED VALUE:
                (output=='fmtstr')a formatted string representing the input argument.
                (output=='value')a float
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value')

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return aspect_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj] is not None and \
                   self[serializer][_dataobj].decoding_success:
                    count += 1
            if output == "fmtstr":
                return aspect_ratio((count, count/self.dataobjs_number))
            if output == "value":
                return count/self.dataobjs_number

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return aspect_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj] is not None and \
               self[_serializer][dataobj].decoding_success:
                count += 1
        if output == "fmtstr":
            return aspect_ratio((count, count/self.serializers_number))
        if output == "value":
            return count/self.serializers_number

        return None  # this line should never be executed.

    def ratio_encoding_success(self,
                               serializer=None,
                               dataobj=None,
                               output="fmtstr"):
        """
            SerializationResults.ratio_encoding_success()

            Compute and format the ratio of encoding success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  <output>(str): "fmtstr" for a formatted returned string or "value"
               for the (float)raw value

            RETURNED VALUE:
                (output=='fmtstr')a formatted string representing the input argument.
                (output=='value')a float
        """
        assert serializer is None or dataobj is None
        assert output in ("fmtstr", "value")

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return aspect_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj] is not None and \
                   self[serializer][_dataobj].encoding_success:
                    count += 1
            if output == "fmtstr":
                return aspect_ratio((count, count/self.dataobjs_number))
            if output == "value":
                return count/self.dataobjs_number

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return aspect_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj] is not None and \
               self[_serializer][dataobj].encoding_success:
                count += 1
        if output == "fmtstr":
            return aspect_ratio((count, count/self.serializers_number))
        if output == "value":
            return count/self.serializers_number

        return None  # this line should never be executed.

    def ratio_similarity(self,
                         serializer=None,
                         dataobj=None,
                         output="fmtstr"):
        """
            SerializationResults.ratio_similarity()

            Compute and/or format the ratio of similarity success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  <output>(str): "fmtstr" for a formatted returned string or "value"
               for the (float)raw value

            RETURNED VALUE:
                (output=='fmtstr')a formatted string representing the input argument.
                (output=='value')a float
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value')

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return aspect_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj] is not None and \
                   self[serializer][_dataobj].similarity:
                    count += 1
            if output == "fmtstr":
                return aspect_ratio((count, count/self.dataobjs_number))
            if output == "value":
                return count/self.dataobjs_number

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return aspect_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj] is not None and \
               self[_serializer][dataobj].similarity:
                count += 1

        if output == "fmtstr":
            return aspect_ratio((count, count/self.serializers_number))
        if output == "value":
            return count/self.serializers_number

        return None  # this line should never be executed.

    def repr_attr(self,
                  serializer,
                  dataobj,
                  attribute_name,
                  output="fmtstr"):
        """
            SerializationResults.repr_attr()

            Format the value stored into self[serializer][dataobj].<attribute_name>.

            _______________________________________________________________

            o  <str>serializer: name of the serializer to be used.
            o  <str>dataobj: name of the data object to be used.
            o  <output>(str): "fmtstr" for a formatted returned string, "base100"
               for a special formatted string

            RETURNED VALUE: a formatted string representing
                            self[serializer][dataobj].<attribute_name>
                (output=='fmtstr')a formatted string representing the input argument.
                (output=='base100')a special string considering
                                   self[serializer][dataobj].<attribute_name>
                                   as a base100 reference.
        """
        assert serializer is not None
        assert dataobj is not None
        assert output in ('fmtstr', 'base100')

        res = None  # unexpected result !

        if output == "base100":
            base100_serializerdataobj = self.get_base(attribute=attribute_name)
            base100 = self[base100_serializerdataobj.serializer][base100_serializerdataobj.dataobj]

        if attribute_name == "decoding_success":
            if output == "fmtstr":
                if self[serializer][dataobj] is None:
                    res = aspect_nodata()
                else:
                    res = aspect_boolsuccess(
                        self[serializer][dataobj].decoding_success)
            else:
                raise WisteriaError(
                    "(ERRORID022) Internal error. "
                    f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if attribute_name == "decoding_time":
            if output == "fmtstr":
                if self[serializer][dataobj] is None:
                    res = aspect_nodata()
                else:
                    res = aspect_time(
                        self[serializer][dataobj].decoding_time)
            else:
                # output == "base100"
                if self[serializer][dataobj] is None or \
                   self[serializer][dataobj].decoding_time is None:
                    res = aspect_nodata()
                else:
                    res = aspect_base100(
                        serializer == base100_serializerdataobj.serializer and
                        dataobj == base100_serializerdataobj.dataobj,
                        100*self[serializer][dataobj].decoding_time/base100.decoding_time)

        if attribute_name == "encoding_strlen":
            if output == "fmtstr":
                if self[serializer][dataobj] is None or \
                   self[serializer][dataobj].encoding_strlen is None:
                    res = aspect_nodata()
                else:
                    res = aspect_stringlength(
                        self[serializer][dataobj].encoding_strlen)
            else:
                # output == "base100"
                if self[serializer][dataobj] is None or \
                   self[serializer][dataobj].encoding_strlen is None:
                    res = aspect_nodata()
                else:
                    res = aspect_base100(
                        serializer == base100_serializerdataobj.serializer and
                        dataobj == base100_serializerdataobj.dataobj,
                        100*self[serializer][dataobj].encoding_strlen/base100.encoding_strlen)

        if attribute_name == "encoding_time":
            if output == "fmtstr":
                if self[serializer][dataobj] is None or \
                   self[serializer][dataobj].encoding_time is None:
                    res = aspect_nodata()
                else:
                    res = aspect_time(
                        self[serializer][dataobj].encoding_time)
            else:
                # output == "base100"
                if self[serializer][dataobj] is None:
                    res = aspect_nodata()
                elif self[serializer][dataobj].encoding_time is None:
                    res = aspect_nodata()
                else:
                    res = aspect_base100(
                        serializer == base100_serializerdataobj.serializer and
                        dataobj == base100_serializerdataobj.dataobj,
                        100*self[serializer][dataobj].encoding_time/base100.encoding_time)

        if attribute_name == "encoding_success":
            if output == "fmtstr":
                if self[serializer][dataobj] is None or \
                   self[serializer][dataobj].encoding_success is None:
                    res = aspect_nodata()
                else:
                    res = aspect_boolsuccess(
                        self[serializer][dataobj].encoding_success)
            else:
                raise WisteriaError(
                    "(ERRORID023) Internal error. "
                    f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if attribute_name == "similarity":
            if output == "fmtstr":
                if self[serializer][dataobj] is None or \
                   self[serializer][dataobj].similarity is None:
                    res = aspect_nodata()
                else:
                    res = aspect_boolsuccess(
                        self[serializer][dataobj].similarity)
            else:
                raise WisteriaError(
                    "(ERRORID024) Internal error. "
                    f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if res is None:
            raise WisteriaError("(ERRORID025) "
                                "Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {attribute_name=};")
        return res

    def total_decoding_time(self,
                            serializer=None,
                            dataobj=None,
                            output="fmtstr"):
        """
            SerializationResults.total_decoding_time()

            Compute and format the total decoding time used by a <serializer>
            OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)

            RETURNED VALUE: a formatted string representing the input arguments.
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value', 'base100')

        if output == "base100" and self.get_serializers_base('encoding_time') is None:
            # no base 100 reference available:
            return aspect_nodata()

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return aspect_time(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj] is not None and \
                   self[serializer][_dataobj].decoding_success:
                    total += self[serializer][_dataobj].decoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = aspect_time(total)
            if output == "base100":
                res = aspect_base100(
                    serializer == self.get_serializers_base('decoding_time'),
                    100*total/self.total_decoding_time(
                        serializer=self.get_serializers_base('decoding_time'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                return aspect_time(None)

            for _serializer in self:
                if self[_serializer][dataobj] is not None and \
                   self[_serializer][dataobj].decoding_success:
                    total += self[_serializer][dataobj].decoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = aspect_time(total)
            if output == "base100":
                res = aspect_base100(
                    dataobj == self.get_dataobjs_base('decoding_time'),
                    100*total/self.total_decoding_time(
                        dataobj=self.get_dataobjs_base('decoding_time'),
                        output="value"))

        if res is None:
            raise WisteriaError("(ERRORID026) Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {output=};")
        return res

    def total_encoding_plus_decoding_time(self,
                                          serializer=None,
                                          dataobj=None,
                                          output="fmtstr"):
        """
            SerializationResults.total_encoding_plus_decoding_time()

            Compute and format the total encoding + decoding time used by a
            <serializer> OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    NOT "base100": no formatted string based on a "base 100" value (str)

            RETURNED VALUE: a formatted string representing the input arguments.
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value',)

        if output == "value":
            return self.total_encoding_time(serializer, dataobj, output) + \
                self.total_decoding_time(serializer, dataobj, output)
        if output == "fmtstr":
            return aspect_time(
                self.total_encoding_time(serializer, dataobj, output='value') +
                self.total_decoding_time(serializer, dataobj, output='value'))

        raise WisteriaError("(ERRORID027) Internal error: the result could not be computed. "
                            f"{serializer=}; {dataobj=}; {output=};")

    def total_encoding_strlen(self,
                              serializer=None,
                              dataobj=None,
                              output="fmtstr"):
        """
            SerializationResults.total_encoding_strlen()

            Compute and format the total encoding string length created by a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)

            RETURNED VALUE: a formatted string representing the input arguments.
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value', 'base100')

        if output == "base100" and self.get_serializers_base('encoding_time') is None:
            # no base 100 reference available:
            return aspect_nodata()

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return aspect_stringlength(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj] is not None and \
                   self[serializer][_dataobj].encoding_strlen:
                    total += self[serializer][_dataobj].encoding_strlen
            if output == "value":
                res = total
            if output == "fmtstr":
                res = aspect_stringlength(total)
            if output == "base100":
                res = aspect_base100(
                    serializer == self.get_serializers_base('encoding_strlen'),
                    100*total/self.total_encoding_strlen(
                        serializer=self.get_serializers_base('encoding_strlen'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                return aspect_stringlength(None)

            for _serializer in self:
                if self[_serializer][dataobj] is not None and \
                   self[_serializer][dataobj].encoding_strlen:
                    total += self[_serializer][dataobj].encoding_strlen
            if output == "value":
                res = total
            if output == "fmtstr":
                res = aspect_stringlength(total)
            if output == "base100":
                res = aspect_base100(
                    dataobj == self.get_dataobjs_base('encoding_strlen'),
                    100*total/self.total_encoding_strlen(
                        dataobj=self.get_dataobjs_base('encoding_strlen'),
                        output="value"))

        if res is None:
            raise WisteriaError("(ERRORID028) Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {output=};")
        return res

    def total_encoding_time(self,
                            serializer=None,
                            dataobj=None,
                            output="fmtstr"):
        """
            SerializationResults.total_encoding_time()

            Compute and format the total decoding time used by a <serializer>
            OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and only one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "fmtstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None
        assert output in ('fmtstr', 'value', 'base100')

        if output == "base100" and self.get_serializers_base('encoding_time') is None:
            # no base 100 reference available:
            return aspect_nodata()

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return aspect_time(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj] is not None and \
                   self[serializer][_dataobj].encoding_success:
                    total += self[serializer][_dataobj].encoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = aspect_time(total)
            if output == "base100":
                res = aspect_base100(
                    serializer == self.get_serializers_base('encoding_time'),
                    100*total/self.total_encoding_time(
                        serializer=self.get_serializers_base('encoding_time'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                res = aspect_time(None)

            for _serializer in self:
                if self[_serializer][dataobj] is not None and \
                   self[_serializer][dataobj].encoding_success:
                    total += self[_serializer][dataobj].encoding_time
            if output == "value":
                res = total
            if output == "fmtstr":
                res = aspect_time(total)
            if output == "base100":
                res = aspect_base100(
                    dataobj == self.get_dataobjs_base('encoding_time'),
                    100*total/self.total_encoding_time(
                        dataobj=self.get_dataobjs_base('encoding_time'),
                        output="value"))

        if res is None:
            raise WisteriaError("(ERRORID029) Internal error: the result could not be computed. "
                                f"{serializer=}; {dataobj=}; {output=};")
        return res

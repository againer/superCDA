"""
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

__author__ = "Alex Gainer (superrawr@gmail.com)"
__copyright__ = "Copyright 2014, Health Records For Everyone (HR4E)"

import cPickle as pickle
import datetime
import os


class PickleNotFoundException(Exception):
    """Missing Pickle Exception"""


class ClinicPickle(object):
    """Word dictionary utilities for pickling GRE words."""
    _PICKLE_FOLDER = os.path.join('data', 'clinics')
    _MISSING_PICKLE = 'Pickle {0} File Missing.'

    def __init__(self, name):
        self.name = name
        self.date_created = datetime.datetime.now()

    @classmethod
    def create(cls, name):
        """Creates a clinic object and pickles it."""
        try:
            pickle_file_name = '{0}.pkl'.format(name)
            path_to_pickle = os.path.join(cls._PICKLE_FOLDER,
                                          pickle_file_name)
            path = os.path.isfile(path_to_pickle)
            if not path:
                pickle.dump(cls(name).__dict__, file(path_to_pickle, 'wb'))
        except IOError:
            raise PickleNotFoundException, self._MISSING_PICKLE.format(name)

    def delete(self):
        """Deletes a Clinic Pickle File."""
        try:
            pickle_file_name = '{0}.pkl'.format(self.name)
            path_to_pickle = os.path.join(self._PICKLE_FOLDER,
                                          pickle_file_name)
            os.remove(path_to_pickle)
        except IOError:
            missing_pickle_error = self._MISSING_PICKLE.format(self.name)
            raise PickleNotFoundException, missing_pickle_error

    @classmethod
    def get_all(cls):
        return filter(lambda x: x != None,
                      [cls.load(name) for name in cls.GetAllClinicNames()])

    @classmethod
    def get_all_clinic_names(cls):
        pkl_files = [f for f in os.listdir(cls._PICKLE_FOLDER)
                     if os.path.isfile(os.path.join(cls._PICKLE_FOLDER,f))]
        return [_.strip('.pkl') for _ in pkl_files]

    @classmethod
    def load(cls, name):
        """Loads up a pickled clinic as a clinic object."""
        try:
            pickle_file_name = '{0}.pkl'.format(name)
            path_to_pickle = os.path.join(cls._PICKLE_FOLDER,
                                          pickle_file_name)
            if os.path.isfile(path_to_pickle):
                clinic = cls(name)
                clinic.__dict__ = pickle.load(file(path_to_pickle, 'r+b'))
            else:
                clinic = None
            return clinic
        except IOError:
            return None

    def update(self, post_data):
        """Updates a clinic given the post_data dictionary."""
        self.__dict__.update({})
        try:
            pickle_file_name = '{0}.pkl'.format(self.name)
            path_to_pickle = os.path.join(self._PICKLE_FOLDER,
                                          pickle_file_name)
            if os.path.isfile(path_to_pickle):
                pickle.dump(self.__dict__, file(path_to_pickle), 'wb')
        except IOError:
            raise PickleNotFoundException, self._MISSING_PICKLE.format(name)

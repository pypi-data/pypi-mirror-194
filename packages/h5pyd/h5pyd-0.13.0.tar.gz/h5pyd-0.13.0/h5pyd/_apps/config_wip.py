##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of HSDS (HDF5 Scalable Data Service), Libraries and      #
# Utilities.  The full HSDS copyright notice, including                      #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################
import os
import json

default_cfg = {
    "hs_endpoint": {
        "default": None,
        "flags": ["--endpoint", "-e"],
        "help": "server endpoint, e.g. http://hsdshdflab.hdfgroup.org",
        "nargs": 1
    },
    "hs_username": {
        "default": None,
        "flags": ["--user", "-u"],
        "help": "User name credential",
        "nargs": 1
    },
    "hs_password": {
        "default": None,
        "flags": ["--password", "-p"],
        "help": "Password credential",
        "nargs": 1
    },
    "hs_api_key": {
        "default": None,
        "flags": ["--api_key",],
        "help": "User api key",
        "nargs": 1
    },
    "loglevel": {
        "default": "error",
        "flags": ["--loglevel",],
        "help": ["logging verbosity"],
        "nargs": 1
    }
}

class Config:
    """
    User Config state
    """
    def __init__(self, config_file=None, custom_entries=[], **kwargs):
        self._names = []
        self._values = {}
        self._flags = {}
        self._help = {}
        self._nargs = {}
        self._choices = {}

        # set default entries
        for defaults in (default_cfg, custom_entries):
            for name in defaults:
                if name in self._names:
                    raise ValueError(f"config {name} already set")
                entry = defaults[name]
                self._names.append(name)
                if "default" in entry:
                    self._values[name] = entry["default"]
                if "flags" in entry:
                    self._flags[name] = entry["flags"]
                if "help" in entry:
                    self._help[name] = entry["help"]
                if "nargs" in entry:
                    self._nargs[name] = entry["nargs"]

        if config_file:
            self._config_file = config_file
        elif os.path.isfile(".hscfg"):
            self._config_file = ".hscfg"
        else:
            self._config_file = os.path.expanduser("~/.hscfg")
        # process config file if found
        if os.path.isfile(self._config_file):
            line_number = 0
            with open(self._config_file) as f:
                for line in f:
                    line_number += 1
                    s = line.strip()
                    if not s:
                        continue
                    if s[0] == '#':
                        # comment line
                        continue
                    fields = s.split('=')
                    if len(fields) < 2:
                        print("config file: {} line: {} is not valid".format(self._config_file, line_number))
                        continue
                    k = fields[0].strip()
                    v = fields[1].strip()
                    if k not in self._names:
                        raise ValueError(f"undefined option: {name}")
                    if name in self._choices:
                        choices = self._choices[name]
                        if v not in self._choices:
                            raise ValueError(f"option {name} must be one of {choices}")
                    self._values[k] = v
        # override any config values with environment variable if found
        for k in self._names:
            if k.upper() in os.environ:
                v = os.environ[k.upper()]
                if name in self._choices:
                    choices = self._choices[name]
                    if v not in self._choices:
                        raise ValueError(f"option {name} must be one of {choices}")
                self._values[name] = v

        # finally update any values that are passed in to the constructor
        for name in kwargs.keys():
            if name in self._names:
                v = kwargs[name]
                if name in self._choices:
                    choices = self._choices[name]
                    if v not in self._choices:
                        raise ValueError(f"option {name} must be one of {choices}")
                self._values[name] = kwargs[name]

    def __getitem__(self, name):
        """ Get a config item  """
        if name not in self._names:
            return None
        return self._values[name]

     
    def __len__(self):
        return len(self._names)

    def __iter__(self):
        """ Iterate over config names """
        for name in self._names:
            yield name

    def __contains__(self, name):
        return name in self._names

    def __repr__(self):
        return json.dumps(self._values)

    def keys(self):
        return self._names

    def get_flags(self, name):
        if name in self._flags:
            return self._flags[name]
        else:
            return None

    def get_help(self, name):
        if name in self._help:
            return self._help[name]
        else:
            return None

    def get_nargs(self, name):
        if name in self._nargs:
            return self._nargs[name]
        else:
            return 0

    def get_choices(self, name):
        if name in self._choices:
            return self._choices[name]
        else:
            return 0
    









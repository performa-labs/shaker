# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random

from oslo_config import cfg
from oslo_log import log as logging
import six


LOG = logging.getLogger(__name__)


def env(*_vars, **kwargs):
    """Returns the first environment variable set.

    If none are non-empty, defaults to '' or keyword arg default.
    """
    for v in _vars:
        value = os.environ.get(v)
        if value:
            return value
    return kwargs.get('default', None)


def validate_required_opts(conf, opts):
    # all config parameters default to ENV values, that's why standard
    # check of required options doesn't work and needs to be done manually
    for opt in opts:
        if opt.required and not conf[opt.dest]:
            raise cfg.RequiredOptError(opt.name)


def read_file(file_name):
    with open(file_name) as fd:
        return fd.read()


def split_address(address):
    try:
        host, port = address.split(':')
    except ValueError:
        raise ValueError('Invalid address: %s, "host:port" expected', address)
    return host, port


def read_uri(uri):
    try:
        req = six.moves.urllib.request.Request(url=uri)
        fd = six.moves.urllib.request.urlopen(req)
        raw = fd.read()
        fd.close()
        return raw
    except Exception as e:
        LOG.warn('Error "%(error)s" while reading uri %(uri)s',
                 {'error': e, 'uri': uri})


def random_string(length=6):
    return ''.join(random.sample('adefikmoprstuz', length))


def copy_dict_kv(source):
    return dict((k, v) for k, v in source.items())

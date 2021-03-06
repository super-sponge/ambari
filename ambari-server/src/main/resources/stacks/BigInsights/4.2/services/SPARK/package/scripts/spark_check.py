#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import socket
import params

from resource_management.core.exceptions import Fail
from resource_management.core.resources import Execute
from resource_management.libraries.functions import format

from resource_management.core import Logger


def check_thrift_port_sasl(address, port, hive_auth="NOSASL", key=None, kinitcmd=None, smokeuser='ambari-qa',
                           transport_mode="binary", http_endpoint="cliservice", ssl=False, ssl_keystore=None,
                           ssl_password=None):
    """
    Hive thrift SASL port check
    """

    # check params to be correctly passed, if not - try to cast them
    if isinstance(port, str):
        port = int(port)

    if isinstance(ssl, str):
        if str(ssl).lower() == str("true"):
            ssl = bool(True)
        else:
            ssl = bool(False)

    # to pass as beeline argument
    ssl_str = str(ssl).lower()
    beeline_check_timeout = 60
    beeline_url = ['jdbc:hive2://{address}:{port}/', "transportMode={transport_mode}"]

    # append url according to used transport
    if transport_mode == "http":
        beeline_url.append('httpPath={http_endpoint}')

    # append url according to used auth
    if hive_auth == "NOSASL":
        beeline_url.append('auth=noSasl')

    # append url according to ssl configuration
    if ssl and ssl_keystore is not None and ssl_password is not None:
        beeline_url.extend(['ssl={ssl_str}', 'sslTrustStore={ssl_keystore}', 'trustStorePassword={ssl_password!p}'])

    # append url according to kerberos setting
    if kinitcmd:
        beeline_url.append('principal={key}')
        Execute(kinitcmd, user=smokeuser)

    cmd = "! beeline -u '%s' -e '' 2>&1| awk '{print}'|grep -i -e 'Connection refused' -e 'Invalid URL' -e 'Error'" % \
          format(";".join(beeline_url))
    Execute(cmd,
            user=smokeuser,
            path=["/usr/iop/"+params.iop_full_version+"/spark/bin"],
            timeout=beeline_check_timeout
            )

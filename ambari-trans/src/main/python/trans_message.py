# -- coding: utf-8 --
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

import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def trans_data(jsfile):
    with open(jsfile) as f:
        data = json.load(f,encoding="utf-8")
        return  data
def trans_message(data, infile, outfile) :
    with open(infile, 'r') as fin:
        with open(outfile, 'w') as fout:
            for line in fin:
                splits = line.split(":")
                if len(splits) > 1 and line.endswith(",\n"):
                    key = splits[0].replace(" ","").replace("\'","")
                    if key in data:
                        fout.write(splits[0] + ": \'" +  data[key].replace("\n","\\n") + "\',\n" )
                    else:
                        fout.write(line)
                else:
                    fout.write(line)

if __name__ == '__main__':
    trans_zh = trans_data("../resources/zh.json")
    # trans_message(trans_zh, "../resources/messages.js", "../resources/zk_message.js")
    trans_message(trans_zh, "../resources/messages.js", "../../../../ambari-web/app/locales/zh/messages.js")

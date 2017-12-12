# -- coding: utf-8 --
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def trans_data(jsfile):
    with open(jsfile) as f:
        data = json.load(f,encoding="utf-8")
        return  data
def save_jsondata(data, ofile) :
    with open(ofile, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")

if __name__ == '__main__':
    trans_zh = trans_data("E:\\tmp\\trans.js")
    print trans_zh
    save_jsondata(trans_zh, 'E:\\tmp\\zh_new.json')
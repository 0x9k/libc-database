# -*-coding:utf-8-*-
__author__ = 'joker'

from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
import sys
import commands

app = Flask(__name__)
bootstrap = Bootstrap(app)


def get_libc_single_by_funtion(function_name,function_address_last_3):
    _, libc_id_str = commands.getstatusoutput('''grep -i -e "^{0} .*{1}$" db/*.symbols | perl -n -e '/db\/(.*)\.symbols/ && print "$1\n"' | sort '''.format(function_name,function_address_last_3))
    return libc_id_str

def dump_function(libc_id):
    dump_str_list = ["str_bin_sh", "system"]
    _, lib_version = commands.getstatusoutput('''cat db/{0}.info'''.format(libc_id))
    libc_version = lib_version.split("/")[-1]
    functions_result = ""
    for dump_str in dump_str_list:
        _, offset = commands.getstatusoutput('''cat db/{0}.symbols | grep "^{1} " | cut -d' ' -f2'''.format(libc_id, dump_str))
        #print "offset_{0} = 0x{1}".format(dump_str, offset)
        functions_result += dump_str + "_address = " + "0x{0}".format(offset) +"\t\t"
    return libc_version,functions_result


@app.route('/')
def index():
    return render_template('index.html',name='index')

@app.route('/query/',methods=['GET'])
def query():
    if request.method == 'GET':
        try:
            q = request.args.get('q')
            find_args = q.split(" ")
            libc_id_set = set([])
            for i in range(0,len(find_args),2):
                function_name = find_args[i]
                function_address_last_3 = find_args[i+1][-3]
                libc_id_str = get_libc_single_by_funtion(function_name,function_address_last_3)
                libc_id_list = libc_id_str.split(" ")
                if libc_id_set == set([]):
                    libc_id_set = libc_id_set | set(libc_id_list)
                else:
                    libc_id_set = libc_id_set & set(libc_id_list)

            libc_id = libc_id_set.pop()
            search_info = "About libc resluts..."
            libc_version_result,functions_result = dump_function(libc_id)
            print libc_version_result
            print functions_result
            return render_template('index.html',
                                   libc_version_result = libc_version_result,
                                   functions_result = functions_result,
                                   search_info=search_info)
        except :
            return render_template('index.html',
                                   error=sys.exc_info())


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug = True)

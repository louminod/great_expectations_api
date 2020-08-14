import pip
import subprocess
import sys
import os
import json
import shutil

def boolify(data):
    if data == 'True':
        return True
    if data == 'False':
        return False
    raise ValueError("")


def autoconverter(data):
    for fn in (boolify, int, float):
        try:
            return fn(data)
        except ValueError:
            pass
    return data

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def uninstall(package):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package])


for arg in sys.argv:
    if arg == 'init':
        print('- Installation of sub-required packages -')
        install('flask')
        install('sqlalchemy')
        install('jsonpickle')

        # POSTGRESQL
        install('psycopg2-binary')
        print('- Installation of great expectations -')
        install('great_expectations')
        print('- Initialize great expectations -')
        os.system("great_expectations init")
        if os.path.isfile('./great_expectations/expectations/config.json'):
            data = {
                "data_asset_type": "Dataset",
                "expectation_suite_name": "config",
                "meta": {
                    "BasicSuiteBuilderProfiler": {
                        "created_at": 1597322401.136341,
                        "created_by": "BasicSuiteBuilderProfiler"
                    }
                }
            }
            with open('./great_expectations/expectations/config.json', 'w') as config_file:
                json.dump(data, config_file)
            print('Initialization done !')
        else:
            print('expectation config error')
    if arg == 'start':
        import great_expectations as ge
        from flask import Flask, request
        import jsonpickle

        context = ge.data_context.DataContext()
        expectation_suite_name = "config"
        suite = context.get_expectation_suite(expectation_suite_name)
        suite.expectations = []

        api = Flask(__name__)

        @api.route('/<data_source>/<schema>/<table>/<great_request>')
        def great(data_source, schema, table, great_request):
            batch_kwargs = {
                "datasource": data_source,
                "schema": schema,
                "table": table,
            }

            if "limit" in request.args:
                limit = autoconverter(request.args.get("limit"))
                batch_kwargs.update({"limit": limit})

            batch = context.get_batch(batch_kwargs, suite)
            batch.head()

            arguments = []
            for arg in request.args:
                if arg not in ["limit"]:
                    arguments.append(autoconverter(request.args.get(arg)))

            return jsonpickle.encode(getattr(batch, great_request)(*arguments), unpicklable=False)

        ip = input("IP: ")
        port = input("PORT: ")
        api.run(host=ip, port=port, debug=False)
    if arg == 'delete':
        shutil.rmtree('./great_expectations/')
        uninstall('flask')
        uninstall('sqlalchemy')
        uninstall('psycopg2-binary')
        uninstall('jsonpickle')
        uninstall('great_expectations')

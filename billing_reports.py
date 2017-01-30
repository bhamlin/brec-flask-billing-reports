#!/usr/bin/python3

import os
import sys

# os.environ['ORACLE_HOME'] = '/usr/lib/oracle/11.2/client64'
# os.environ['TNS_ADMIN'] = '/usr/lib/oracle/11.2/client64'
# os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'

os.environ['FLASK_BILLING_CONFIG'] = '/etc/flask_billing_reports/config'

from flask import Flask, Response, render_template, request, url_for
# import cx_Oracle
import pymssql
# import postgresql

app = Flask(__name__)
app.config.from_envvar('FLASK_BILLING_CONFIG')
app.configdebug=1

# ORADB_DSN = (
#     '''{0[ORADB_USERNAME]}/{0[ORADB_PASSWORD]}@ats'''
#         .format(app.config))
# PGSQL_DSN = (
#     '''pq://{0[PGSQL_USERNAME]}:{0[PGSQL_PASSWORD]}@warehouse.brec.local/Black River?[sslmode]=require'''
#         .format(app.config))

@app.route('/')
def index():
    data = dict()
    isInputMeter = isInputAccount = ''
    if not data:
        isInputAccount = ' selected'
        data['inputIdentifier'] = ''
        data['inputDateStart'] = '2016-12-30'
        data['inputDateEnd'] = '2017-01-30'
    else:
        if data['inputIdType'] == 'meter':
            isInputMeter = ' selected'
        else:
            isInputAccount = ' selected'
    return render_template('base.html',
                           inputIdentifier=data['inputIdentifier'],
                           inputDateStart=data['inputDateStart'],
                           inputDateEnd=data['inputDateEnd'],
                           inputMeter=isInputMeter,
                           inputAccount=isInputAccount)

@app.route('/chart/<idtype>/<id>/from/<startDate>/to/<endDate>')
def chart(idtype, id, startDate, endDate):
    if idtype.lower() == 'meter': # Meter lookup
        pass
    return 'doop'

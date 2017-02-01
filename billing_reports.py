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
import postgresql

COLOR_WEEKDAY = 'rgba(65, 126, 188, 0.8)'
COLOR_WEEKEND = 'rgba(126, 64, 188, 0.8)'
COLOR_DAYLIST = (COLOR_WEEKDAY, COLOR_WEEKEND)

BASE_URL = 'http://10.50.10.208:5001/'

app = Flask(__name__)
app.config.from_envvar('FLASK_BILLING_CONFIG')
app.configdebug=1

# ORADB_DSN = (
#     '''{0[ORADB_USERNAME]}/{0[ORADB_PASSWORD]}@ats'''
#         .format(app.config))
PGSQL_DSN = (
    '''pq://{0[PGSQL_USERNAME]}:{0[PGSQL_PASSWORD]}@warehouse.brec.local/Black River?[sslmode]=require'''
        .format(app.config))

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
    return render_template('blank.html',
                           inputIdentifier=data['inputIdentifier'],
                           inputDateStart=data['inputDateStart'],
                           inputDateEnd=data['inputDateEnd'],
                           inputMeter=isInputMeter,
                           inputAccount=isInputAccount)

@app.route('/chart/<idtype>/<id>/from/<startDate>/to/<endDate>')
def chart(idtype, id, startDate, endDate):
    if idtype.lower() == 'meter': # Meter lookup
        with pymssql.connect(*[app.config[x] for x in
            ('MSSQL_HOST', 'MSSQL_USERNAME', 'MSSQL_PASSWORD', 'MSSQL_DATABASE')]) as conn:
            with conn.cursor() as cursor:
                query = '''

SELECT DateDimension.dateId AS UsageDate, UsageFact.dailyUsage AS usage,
    DateDimension.Day_DOWName AS dayOfTheWeek 
FROM UsageFact 
    INNER JOIN DateDimension ON UsageFact.dateDimensionId = DateDimension.dateDimensionId 
    INNER JOIN MeterDimension ON UsageFact.meterDimensionId = MeterDimension.meterDimensionId 
WHERE (MeterDimension.meterNumber = %s) and ((dateID >= %s) and (dateID <= %s))
ORDER BY DateDimension.dateId

                '''
                # app.logger.debug(query)
                
                cursor.execute(query, (id, startDate, endDate))
                
                dateList, readingList, dowList = list(), list(), list()
                for row in cursor:
                    dateList.append(str(row[0])[:10])
                    readingList.append(row[1])
                    dowList.append(row[2])
        db = postgresql.open(PGSQL_DSN)
        tempData = db.prepare('''

select left(measurement_time::character varying, 10) as day,
  min(temperature),
  avg(temperature),
  max(temperature)
from weather.sumter_data
where 1=1
  and measurement_time  > $1::text::timestamp with time zone
  and measurement_time <= $2::text::timestamp with time zone
group by left(measurement_time::character varying, 10)
order by left(measurement_time::character varying, 10)

                    '''.strip())(startDate, endDate)
        db.close()
        tempsDate, tempMin, tempAvg, tempMax = zip(*tempData)
        
        return render_template('data.html',
            base_url=BASE_URL,
            inputIdentifier=id,
            inputDateStart=startDate,
            inputDateEnd=endDate,
            inputMeter=' selected',
            inputAccount='',
            entryCount=len(dateList),
            dateList="|".join(dateList),
            readingList="|".join(map(str, readingList)),
            tempMin="|".join(map(str, tempMin)),
            tempAvg="|".join(map(str, tempAvg)),
            tempMax="|".join(map(str, tempMax)),
            colorList="|".join([COLOR_DAYLIST[x in ('Saturday', 'Sunday')] for x in dowList]))
    else:
        return 'doorp'

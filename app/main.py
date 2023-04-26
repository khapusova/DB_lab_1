import csv
import sys
import pandas as pd
import psycopg2
import requests #для завантаження архівів з даними про ЗНО/НМТ
import py7zr #для розпакування архівів
import time
import os


#docker-compose build --no-cache && docker-compose up -d --force-recreate
def main():
    start_time = time.time()
    print("Start time: ", time.strftime("%H:%M:%S"))

    # Підключаємось до БД
    conn = create_conn()

    #завантажуємо та розархівовуємо дані про ЗНО з сайту за допомогою ліби requests, csv та py7zr
    save_data()

    #створюємо pandas Dataframe для завантаження даних в БД
    df19, df21 = create_df()

    if isTable():
        print("Table exists")
    else:
        createTable()
        print("Table doesn't exist. Creating table...")

    #Вставляємо дані в таблицю
    conn = create_conn()
    insert_data_to_db(df19, conn, 2019)
    conn = create_conn()
    insert_data_to_db(df21, conn, 2021)

    #Виконуємо запит згідно 13-го варіанту
    get_data_by_region()

    #Записуємо час виконання програми в текстовий файл
    txt_timer(start_time)
    conn.close()
    print("--- %s seconds ---" % round(time.time() - start_time, 2))


def txt_timer(start_time):
    with open('timer.txt', 'w', encoding='UTF-32') as f:
        mins = int((time.time() - start_time)/60)
        secs = int((time.time() - start_time) - mins*60)
        f.write("Time of executing: {0}:{1}".format(mins, secs))
        f.close()


def create_df():
    data21 = pd.read_csv('Odata2021File.csv', sep=";", decimal=",", low_memory=False)
    data19 = pd.read_csv('Odata2019File.csv', sep=";", decimal=",", encoding="Windows-1251", low_memory=False)
    df19 = pd.DataFrame(data19, columns=['OUTID', 'Birth', 'SEXTYPENAME', 'REGNAME', 'AREANAME',
                                         'TERNAME', 'REGTYPENAME', 'TerTypeName', 'EONAME', 'EOTYPENAME', 'EORegName',
                                         'UkrTestStatus',
                                         'UkrBall100',
                                         'UkrBall12',
                                         'UkrBall',
                                         'histTestStatus',
                                         'histBall100',
                                         'histBall12',
                                         'histBall',
                                         'mathTestStatus',
                                         'mathBall100',
                                         'mathBall12',
                                         'mathBall',
                                         'physTestStatus',
                                         'physBall100',
                                         'physBall12',
                                         'physBall',
                                         'chemTestStatus',
                                         'chemBall100',
                                         'chemBall12',
                                         'chemBall',
                                         'bioTestStatus',
                                         'bioBall100',
                                         'bioBall12',
                                         'bioBall',
                                         'geoTestStatus',
                                         'geoBall100',
                                         'geoBall12',
                                         'geoBall',
                                         'engTestStatus',
                                         'engBall100',
                                         'engBall12',
                                         'engBall',
                                         'frTestStatus',
                                         'frBall100',
                                         'frBall12',
                                         'frBall',
                                         'deuTestStatus',
                                         'deuBall100',
                                         'deuBall12',
                                         'deuBall',
                                         'spTestStatus',
                                         'spBall100',
                                         'spBall12',
                                         'spBall',
                                         ])
    df21 = pd.DataFrame(data21, columns=['OUTID', 'Birth', 'SexTypeName', 'RegName', 'AREANAME',
                                         'TERNAME', 'RegTypeName', 'TerTypeName', 'EONAME', 'EOTypeName', 'EORegName',
                                         'UMLTestStatus',
                                         'UMLBall100',
                                         'UMLBall12',
                                         'UMLBall',
                                         'UkrTestStatus',
                                         'UkrBall100',
                                         'UkrBall12',
                                         'UkrBall',
                                         'HistTestStatus',
                                         'HistBall100',
                                         'HistBall12',
                                         'HistBall',
                                         'MathTestStatus',
                                         'MathBall100',
                                         'MathBall12',
                                         'MathBall',
                                         'PhysTestStatus',
                                         'PhysBall100',
                                         'PhysBall12',
                                         'PhysBall',
                                         'ChemTestStatus',
                                         'ChemBall100',
                                         'ChemBall12',
                                         'ChemBall',
                                         'BioTestStatus',
                                         'BioBall100',
                                         'BioBall12',
                                         'BioBall',
                                         'GeoTestStatus',
                                         'GeoBall100',
                                         'GeoBall12',
                                         'GeoBall',
                                         'EngTestStatus',
                                         'EngBall100',
                                         'EngBall12',
                                         'EngBall',
                                         'FrTestStatus',
                                         'FrBall100',
                                         'FrBall12',
                                         'FrBall',
                                         'DeuTestStatus',
                                         'DeuBall100',
                                         'DeuBall12',
                                         'DeuBall',
                                         'SpTestStatus',
                                         'SpBall100',
                                         'SpBall12',
                                         'SpBall',
                                         ])

    for col in df19.columns:
        if "Ball100" in col:
            df19[col] = df19[col].apply(pd.to_numeric)

    for col in df19.columns:
        if "Ball100" in col:
            df19[col] = df19[col].apply(pd.to_numeric)

    return df19, df21


def create_conn():
    for i in range(10):
        try:
            conn = psycopg2.connect(dbname='student01_DB', user='postgres', password='root1', host='db')
            print("Connection to database is successful")
            return conn
        except psycopg2.OperationalError:
            print("Connection failed. Restarting in 5 seconds...")
            time.sleep(5)

    print("Failed to connect. Try later :(")
    sys.exit()


def save_data():
    years = ["2019", "2021"]
    url19 = "https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO2019.7z"
    url21 = "https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO2021.7z"
    urls = [url19, url21]

    for num in range(len(urls)):
        req = requests.get(urls[num], stream=True)
        if req.status_code == 200:
            filename = "ZNO" + years[num]
            with open(filename, 'wb') as out:
                out.write(req.content)
            with py7zr.SevenZipFile(filename, 'r') as archive:
                archive.extractall()

            if os.path.isfile("ZNO" + str(years[num])):
                os.remove("ZNO" + str(years[num]))
        else:
            print('Request failed: %d' % req.status_code)


def isTable():
    conn = create_conn()
    cur = conn.cursor()
    query = """SELECT COUNT(table_name) FROM information_schema.tables
            WHERE table_schema LIKE 'public' AND table_type LIKE 'BASE TABLE' AND table_name = 'zno_records'"""
    cur.execute(query)
    result = cur.fetchall()[0][0]
    if result == 1:
        return True
    return False



def createTable():
    conn = create_conn()
    with conn:
        cur = conn.cursor()

        query1 = """
        CREATE TABLE zno_records(
            Year INT,
            OutID VARCHAR(1000) NOT NULL,
            Birth CHAR(4) NOT NULL,
            SexTypeName CHAR(8) NOT NULL,
            Regname VARCHAR(1000) NOT NULL,
            AreaName VARCHAR(1000) NOT NULL,
            TerName VARCHAR(1000) NOT NULL,
            RegTypeName VARCHAR(1000) NOT NULL,
            TerTypeName VARCHAR(1000) NOT NULL,
            EOName VARCHAR(1000),
            EOTypeName VARCHAR(1000),
            EORegName VARCHAR(1000),
            UMLTestStatus VARCHAR(25),
            UMLBall100 DECIMAL,
            UMLBall12 DECIMAL,
            UMLBall DECIMAL,
            UkrTestStatus VARCHAR(25),
            UkrBall100 DECIMAL,
            UkrBall12 DECIMAL,
            UkrBall DECIMAL,
            HistTestStatus VARCHAR(25),
            HistBall100 DECIMAL,
            HistBall12 DECIMAL,
            HistBall DECIMAL,
            MathTestStatus VARCHAR(25),
            MathBall100 DECIMAL,
            MathBall12 DECIMAL,
            MathBall DECIMAL,
            PhysTestStatus VARCHAR(25),
            PhysBall100 DECIMAL,
            PhysBall12 DECIMAL,
            PhysBall DECIMAL,
            ChemTestStatus VARCHAR(25),
            ChemBall100 DECIMAL,
            ChemBall12 DECIMAL,
            ChemBall DECIMAL,
            BioTestStatus VARCHAR(25),
            BioBall100 DECIMAL,
            BioBall12 DECIMAL,
            BioBall DECIMAL,
            GeoTestStatus VARCHAR(25),
            GeoBall100 DECIMAL,
            GeoBall12 DECIMAL,
            GeoBall DECIMAL,
            EngTestStatus VARCHAR(25),
            EngBall100 DECIMAL,
            EngBall12 DECIMAL,
            EngBall DECIMAL,
            FrTestStaTus VARCHAR(25),
            FrBall100 DECIMAL,
            FrBall12 DECIMAL,
            FrBall DECIMAL,
            DeuTestStaTus VARCHAR(25),
            DeuBall100 DECIMAL,
            DeuBall12 DECIMAL,
            DeuBall DECIMAL,
            SpTestStaTus VARCHAR(25),
            SpBall100 DECIMAL,
            SpBall12 DECIMAL,
            SpBall DECIMAL 
        );
        """
        cur.execute(query1)


def insert_data_to_db(df, conn, year):
    columns = [i for i in df.columns]
    values_string = '%s, ' * (len(columns)+1)
    values_string = values_string[:-2]
    columns = "year, " + ', '.join(columns)
    cash = []

    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM zno_records WHERE year=" + str(year))
        num_of_records_to_ignore = cur.fetchall()[0][0]

    except psycopg2.OperationalError:
        conn = create_conn()
        insert_data_to_db(df, conn, year)

    counter = 0
    for row in df.values:
        row = list(row)
        row.insert(0, year)
        cash.append(row)
        query1 = "INSERT INTO zno_records(" + columns + ") VALUES( " + values_string + ");"
        if counter > num_of_records_to_ignore:
            try:
                cur = conn.cursor()
                cur.execute(query1, row)
                if counter % 1000 == 0:
                    conn.commit()
                    cash = []
                    print("{0} rows inserted, time: {1}".format(counter, time.strftime("%H:%M:%S")))

            except psycopg2.OperationalError:
                print("Restoring connection...")
                conn = create_conn()
                cur = conn.cursor()
                for el in cash:
                    cur.execute(query1, el)
                cur.execute(query1, row)
                if counter % 1000 == 0:
                    conn.commit()
                    cash = []
                    print("{0} rows inserted, time: {1}".format(counter, time.strftime("%H:%M:%S")))

        counter += 1

    conn.commit()
    print("{0} rows inserted, time: {1}".format(counter, time.strftime("%H:%M:%S")))
    print("Data of {0} year is successfully inserted.".format(year))


def get_data_by_region():
    query = "SELECT year, regname, MAX(EngBall100) FROM zno_records WHERE engteststatus='Зараховано' GROUP BY regname, year;"
    conn = create_conn()
    cur = conn.cursor()
    cur.execute(query)
    records = cur.fetchall()
    field_names = ['Year', 'Region', "EngBall100"]
    rows = []

    for record in records:
        d = {
            'Year': record[0],
            'Region': record[1],
            "EngBall100": record[2]
        }

        rows.append(d)

    with open('records.csv', 'w', encoding='UTF-32') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)
        f.close()


main()

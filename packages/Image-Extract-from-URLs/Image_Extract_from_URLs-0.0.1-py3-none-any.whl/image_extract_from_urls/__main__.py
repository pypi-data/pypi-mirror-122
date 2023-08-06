import argparse
import requests
import shutil
import pandas as pd
import csv
import os

dic = {}
succ = []
unsucc = []


def extract_image(i, url, filePath):
    fileName = 'image{}.jpg'.format(i)
    print("===================={}====================".format(fileName))
    print("==================================================\n")
    print(url)
    fullPath = '{}{}'.format(filePath, fileName)
    print(fullPath)
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(fullPath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print('{} sucessfully Downloaded: '.format(fileName))
            succ.append(fileName)
        else:
            unsucc.append(fileName)
            print('{} Couldn\'t be retreived'.format(fileName))
    except:
        pass
    print("\n==================================================")
    return None


def main():
    parser = argparse.ArgumentParser(description="Downloading Images from list of URLs")
    parser.add_argument("Name", help="Name of the Food")
    parser.add_argument("URLs", help="URLs Text file")
    parser.add_argument("Path", help="Destination Path")
    args = parser.parse_args()
    urlTxt = args.URLs
    Name = args.Name
    destPath = args.Path
    path = destPath + Name + "/"

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    df = pd.read_csv(urlTxt, delimiter=',', header=0, error_bad_lines=False, quoting=csv.QUOTE_NONE)
    csvName = Name + ".csv"
    csvDest = path + "/" +csvName
    df.to_csv(csvDest)
    csvdf = pd.read_csv(csvDest, quoting=csv.QUOTE_NONE)
    for i, url in enumerate(csvdf.values):
        extract_image(i + 1, url[1], path)
    reportPath = path + 'report.txt'
    with open(reportPath, 'w+') as f:
        f.write("====================Success====================\n")
        for items in succ:
            f.write('%s\n' % items)
        f.write("===================UnSuccess===================\n")
        for items in unsucc:
            f.write('%s\n' % items)
        print("File written successfully")
    f.close()
    return None

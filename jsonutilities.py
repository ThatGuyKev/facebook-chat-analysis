import json # We will be working with json files
from datetime import datetime # To format ms to datetime

def handleFile(filename):
    with open(filename) as f:
        data = json.load(f)

    row_data =[]
    hours  =[]

    # To loop in json file and only return the message and the hour and fetch them in row_data, hours
    for item in data['messages']:
        try:
            content = item['content']
            timestamp = item['timestamp_ms']
        except:
            content = 'None'
            timestamp = item['timestamp_ms']
            pass
        item_datetime = datetime.fromtimestamp(timestamp/1000)
        hour = item_datetime.strftime("%H")
        row_data.append(str(content).strip())
        hours.append(str(hour).strip())

    return row_data, hours

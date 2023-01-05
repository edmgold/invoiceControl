from io import BytesIO
import pandas as pd
import json
from fastapi import HTTPException

from functools import wraps

def csv_to_json(file):
    contents = file.file.read()
    buffer = BytesIO(contents)

    try:
        df = pd.read_csv(buffer, delimiter=';', index_col=False)
    except pd.errors.ParserError:
        raise HTTPException(status_code=404, detail="Invalid file")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=404, detail="Empty file")  

    buffer.close()
    file.file.close()

    result = df.to_json(orient = "records", lines = True, date_format = "iso", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)
 
    result = result[:-2].replace( "}", "},")
    result = '{ "detail" : [' + result + "}]}"

    return json.loads(result)



import pandas as pd
from io import BytesIO
from datetime import datetime
import bz2


with bz2.open("datasets//compressed_backup.bz2","rb") as input:
    dataset_binary = input.read()
    
dataframe = pd.read_csv(BytesIO(dataset_binary),index_col=0)

temp = [int(datetime.timestamp(datetime.fromisoformat(x))) for x  in dataframe.loc[:,"D_time"]]

dataframe.loc[:,"D_time"] = pd.Series(temp,name="D_time")

print(dataframe)
with bz2.open(f"datasets//compressed.bz2","wb") as output:
    output.write(dataframe.to_csv().encode())
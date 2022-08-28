import pandas as pd
a = pd.Series([1,2,4,6])
b = pd.Series([3,5,7,9])

df = pd.DataFrame([a,b])
df.loc[df.shape[0],:] = a
print(df)
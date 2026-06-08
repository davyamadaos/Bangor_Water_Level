import io, json, zipfile, requests, pandas as pd
import os

os.makedirs("data", exist_ok=True)
URL='https://epawebapp.epa.ie/Hydronet/output/internet/stations/CAS/33008/Q/3_months.zip'
z=zipfile.ZipFile(io.BytesIO(requests.get(URL,timeout=60).content))
csv=[n for n in z.namelist() if n.endswith('.csv')][0]
lines=z.read(csv).decode('utf-8').splitlines()
rows=[l for l in lines if not l.startswith('#') and l.strip()]
from io import StringIO
df=pd.read_csv(StringIO('\n'.join(rows)),sep=';',header=None,
 names=['timestamp','value','absolute','quality'])
out={'rows':[{'timestamp':str(r.timestamp),'absolute':float(r.absolute)}
 for _,r in df.iterrows()]}
open('data/latest.json','w').write(json.dumps(out))
print('updated')

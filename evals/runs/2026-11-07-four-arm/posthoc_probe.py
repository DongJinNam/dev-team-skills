import importlib.util,json,sys
spec=importlib.util.spec_from_file_location('candidate',sys.argv[1]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
results=[]
for sep in ('\u2028','\u0085'):
    text=json.dumps({'id':'a'+sep+'b','category':'x','amount':1},ensure_ascii=False)
    try: good=m.summarize(text)=={'x':1}
    except Exception: good=False
    results.append({'case':'unicode_'+hex(ord(sep)), 'passed':good})
for constant in ('NaN','Infinity','-Infinity'):
    text='{"id":"a","category":"x","amount":1,"extra":'+constant+'}'
    try: m.summarize(text); good=False
    except ValueError: good=True
    except Exception: good=False
    results.append({'case':'invalid_constant_'+constant,'passed':good})
print(json.dumps(results))

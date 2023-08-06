import glob

from pyraf import cl2py

for f in glob.glob('/usr/lib/iraf/**/*.cl', recursive=True):
    #print(f)
    try:
        pcode = cl2py.cl2py(f)
        #print(pcode.code)
    except (SyntaxError, KeyError) as e:
        print('-'*80)
        print(f, str(e))
        with open(f) as fp:
            print(fp.read())

import requests
# create a small dummy pdf-like file
with open('test_dummy.pdf','wb') as f:
    f.write(b'%PDF-1.4\n%Dummy\n')

with open('test_dummy.pdf','rb') as fh:
    files = {'file': ('test.pdf', fh, 'application/pdf')}
    r = requests.post('http://127.0.0.1:5000/upload', files=files)
    print(r.status_code)
    print(r.text)

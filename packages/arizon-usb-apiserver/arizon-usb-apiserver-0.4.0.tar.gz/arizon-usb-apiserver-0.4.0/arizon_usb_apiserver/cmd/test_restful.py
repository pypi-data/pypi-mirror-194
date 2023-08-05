import requests
import tqdm
import urllib.parse as urlparse

from py_cli_interaction import must_parse_cli_string

def test_restful():
    endpoint = must_parse_cli_string("endpoint", "http://127.0.0.1:8080")
    requests.put(urlparse.urljoin(endpoint, 'v1/arizon/force?flag=true'))
    
    force_endpoint = str(urlparse.urljoin(endpoint, 'v1/arizon/force'))
    try:
        with tqdm.tqdm() as pbar:
            while True:
                resp = requests.get(force_endpoint)
                data = resp.json()['data']
                if data is not None:
                    pbar.set_description("Index: {} Force: {}, Timestamp: {}".format(data['index'], data['f'], data['sys_ts_ns']))
                    pbar.update(len(data))
                    # Force: 0.0, Timestamp: 1675831264.3972561: : 5817it [00:15, 368.32it/s]  
    except KeyboardInterrupt as e:
        requests.put(urlparse.urljoin(endpoint, 'v1/arizon/force?flag=false'))

if __name__ == '__main__':
   test_restful()
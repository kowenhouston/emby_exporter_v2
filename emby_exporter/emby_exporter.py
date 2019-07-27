import argparse
import time
import asyncio

from prometheus_client import start_wsgi_server, Gauge
from embypysessionextender import EmbySessionExtender as Emby

# Create an emby_exporter class
class emby_exporter:
    def __init__(self, url, api_key, user_id):
        self.emby = Emby(
            url,
            api_key=api_key,
            userid=user_id,
        )

    def get_session_data(self):
        return(self.emby.sessions_sync)

def main():
    parser = argparse.ArgumentParser(description='emby_exporter')
    parser.add_argument(
        '-e', '--emby', help='emby address', default='localhost:8096')
    parser.add_argument(
        '-p',
        '--port',
        help='port we is listening on',
        default=9123,
        type=int)
    parser.add_argument(
        '-i',
        '--interface',
        help='interface will listen on',
        default='0.0.0.0')
    parser.add_argument('-a', '--auth', help='emby api token')
    parser.add_argument('-u', '--userid', help='emby user id')
    parser.add_argument(
        '-s',
        '--interval',
        help='scraping interval in seconds',
        default=15,
        type=int)
    args = parser.parse_args()

    # Started threaded wsgi server
    print(f"* Listening on {args.interface}:{args.port}")
    start_wsgi_server(args.port)

    # Connect to emby
    print(f'Connecting to emby: {args.emby}')
    emby_ex = emby_exporter(f'http://{args.emby}', args.auth, args.userid)

    # Make a guage
    g = Gauge('emby_sessions', 'Provides an output of sessions')
    
    # Update the metrics every interval
    while True:
        print('Updating metrics...')
        items = emby_ex.get_session_data()
        g.set(len(items))
        time.sleep(args.interval)


if __name__ == '__main__':
    main()

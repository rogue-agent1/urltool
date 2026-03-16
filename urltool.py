#!/usr/bin/env python3
"""urltool - Parse, build, encode/decode URLs."""
import argparse, sys
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs, quote, unquote, urljoin

def main():
    p = argparse.ArgumentParser(description='URL utility')
    sub = p.add_subparsers(dest='cmd')

    par = sub.add_parser('parse', help='Parse URL into components')
    par.add_argument('url')
    par.add_argument('-j', '--json', action='store_true')

    enc = sub.add_parser('encode', help='URL-encode a string')
    enc.add_argument('text')

    dec = sub.add_parser('decode', help='URL-decode a string')
    dec.add_argument('text')

    bld = sub.add_parser('build', help='Build URL from components')
    bld.add_argument('--scheme', default='https')
    bld.add_argument('--host', required=True)
    bld.add_argument('--path', default='/')
    bld.add_argument('--port', type=int)
    bld.add_argument('-q', '--query', nargs='*', help='key=value pairs')

    jn = sub.add_parser('join', help='Join base URL with relative path')
    jn.add_argument('base')
    jn.add_argument('path')

    qry = sub.add_parser('query', help='Extract/modify query params')
    qry.add_argument('url')
    qry.add_argument('--get', help='Get param value')
    qry.add_argument('--set', nargs=2, action='append', metavar=('KEY','VAL'))
    qry.add_argument('--remove', nargs='*')

    args = p.parse_args()
    if not args.cmd:
        p.print_help(); return

    if args.cmd == 'parse':
        u = urlparse(args.url)
        if args.json:
            import json
            print(json.dumps({'scheme':u.scheme,'netloc':u.netloc,'hostname':u.hostname,
                'port':u.port,'path':u.path,'query':u.query,'fragment':u.fragment,
                'params':parse_qs(u.query)}, indent=2))
        else:
            print(f"Scheme:   {u.scheme}\nHost:     {u.hostname}\nPort:     {u.port or 'default'}")
            print(f"Path:     {u.path}\nQuery:    {u.query}\nFragment: {u.fragment}")
            if u.query:
                print("Params:")
                for k, v in parse_qs(u.query).items():
                    print(f"  {k} = {', '.join(v)}")
    elif args.cmd == 'encode':
        print(quote(args.text, safe=''))
    elif args.cmd == 'decode':
        print(unquote(args.text))
    elif args.cmd == 'build':
        netloc = args.host + (f":{args.port}" if args.port else "")
        query = urlencode(dict(kv.split('=',1) for kv in (args.query or [])))
        print(urlunparse((args.scheme, netloc, args.path, '', query, '')))
    elif args.cmd == 'join':
        print(urljoin(args.base, args.path))
    elif args.cmd == 'query':
        u = urlparse(args.url)
        params = parse_qs(u.query, keep_blank_values=True)
        if args.get:
            vals = params.get(args.get, [])
            print('\n'.join(vals) if vals else f"(not found)")
        else:
            if args.set:
                for k, v in args.set:
                    params[k] = [v]
            if args.remove:
                for k in args.remove:
                    params.pop(k, None)
            flat = {k: v[0] if len(v)==1 else v for k, v in params.items()}
            new_q = urlencode(flat, doseq=True)
            print(urlunparse((u.scheme, u.netloc, u.path, u.params, new_q, u.fragment)))

if __name__ == '__main__':
    main()

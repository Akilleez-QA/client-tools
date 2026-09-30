"""Verify first; execute only when separately requested. No device/config setup here."""
import argparse
import json
import subprocess
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from receipt import verify_pair

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', required=True)
    parser.add_argument('--receipt-sha256', required=True, help='external trusted pin, not a mutable sibling file')
    parser.add_argument('--configuration', required=True, choices=['Debug', 'Release'])
    parser.add_argument('--host', required=True)
    parser.add_argument('--controller', required=True)
    parser.add_argument('--execute', action='store_true', help='requires separately authorized vendor runtime')
    parser.add_argument('--media', help='private fixture media, required only for explicit execution')
    parser.add_argument('--record', required=True)
    args = parser.parse_args()
    result = verify_pair(args.receipt, args.receipt_sha256, args.configuration, args.host, args.controller)
    if args.execute and not args.media:
        parser.error('--execute requires private --media')
    # Exclusive record prevents silently overwriting a prior attempt.
    with Path(args.record).open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    if not args.execute:
        print('VERIFIED ONLY: no process launched')
        return 0
    command = [result['outputs'][1]['path'], result['outputs'][0]['path'], args.media]
    completed = subprocess.run(command, check=False)
    return completed.returncode

if __name__ == '__main__':
    raise SystemExit(main())

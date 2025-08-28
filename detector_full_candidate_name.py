#!/usr/bin/env python3

import csv
import json
import re
import sys

def mask_phone(val):
   
    digits = re.sub(r'\D', '', val)
    if len(digits) != 10:
        return '[REDACTED_PII]'
    return digits[:2] + 'X' * 6 + digits[-2:]

def mask_aadhar(val):
    digits = re.sub(r'\D', '', val)
    if len(digits) != 12:
        return '[REDACTED_PII]'
    return digits[:4] + 'X' * 4 + digits[-4:]

def mask_passport(val):
    if not re.match(r'^[A-Z]\d{7}$', val):
        return '[REDACTED_PII]'
    return val[0] + 'X' * (len(val) - 2) + val[-1]

def mask_upi(val):
    if '@' not in val:
        return '[REDACTED_PII]'
    local, domain = val.split('@', 1)
    if len(local) <= 4:
        m = 'X' * len(local)
    else:
        m = local[:2] + 'X' * (len(local) - 4) + local[-2:]
    return m + '@' + domain

def mask_name(val):
    parts = val.split()
    masked = []
    for w in parts:
        if len(w) <= 1:
            masked.append('X')
        else:
            masked.append(w[0] + 'X' * (len(w) - 1))
    return ' '.join(masked)

def mask_email(val):
    if '@' not in val:
        return '[REDACTED_PII]'
    local, domain = val.split('@', 1)
    if len(local) <= 2:
        m = 'X' * len(local)
    else:
        m = local[:2] + 'X' * (len(local) - 2)
    return m + '@' + domain

def mask_address(val):
    return '[REDACTED_PII]'

def mask_device_or_ip(val):
  
    parts = val.split('.')
    if len(parts) == 4 and all(p.isdigit() for p in parts):
        return '.'.join(parts[:3] + ['X'])
    return '[REDACTED_PII]'

def detect_and_redact(record):
    data = record.copy()
    pii_found = False

    
    standalone = {
        'phone': mask_phone,
        'aadhar': mask_aadhar,
        'passport': mask_passport,
        'upi_id': mask_upi,
    }
    for key, masker in standalone.items():
        v = data.get(key)
        if v:
            masked = masker(str(v))
            data[key] = masked
            pii_found = True

   
    comb_keys = ['name', 'email', 'address', 'device_id', 'ip_address']
    comb_present = [k for k in comb_keys if data.get(k)]
    if len(comb_present) >= 2:
        pii_found = True
        for k in comb_present:
            v = str(data[k])
            if k == 'name':
                data[k] = mask_name(v)
            elif k == 'email':
                data[k] = mask_email(v)
            elif k == 'address':
                data[k] = mask_address(v)
            elif k in ('device_id', 'ip_address'):
                data[k] = mask_device_or_ip(v)

    return data, pii_found

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 detector_full_candidate_name.py iscp_pii_dataset.csv")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = 'redacted_output_candidate_full_name.csv'

    with open(infile, newline='', encoding='utf-8') as fin,\
         open(outfile, 'w', newline='', encoding='utf-8') as fout:

        reader = csv.DictReader(fin)
        writer = csv.writer(fout)
        writer.writerow(['record_id', 'redacted_data_json', 'is_pii'])

        for row in reader:
            rid = row['record_id']
            try:
                data = json.loads(row['data_json'])
            except json.JSONDecodeError:
                
                writer.writerow([rid, '{}', 'False'])
                continue

            redacted, pii_flag = detect_and_redact(data)
            # dump JSON without extra spaces
            redacted_json = json.dumps(redacted, separators=(',', ':'))
            writer.writerow([rid, redacted_json, str(pii_flag)])

    print(f"Redacted output written to {outfile}")

if __name__ == '__main__':
    main()

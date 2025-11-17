#!/usr/bin/env python3
"""
Descarga el catálogo NGC/IC desde OpenNGC y guarda como catalogo_completo.json
Uso: python download_catalog.py
"""
import requests, json, sys

urls = [
    'https://raw.githubusercontent.com/mattiaverga/OpenNGC/master/database_files/ngc_ic.json',
    'https://raw.githubusercontent.com/mattiaverga/OpenNGC/master/database_files/ngc_ic.csv'
]

for url in urls:
    try:
        print('Intentando', url)
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        txt = r.text
        try:
            data = json.loads(txt)
            with open('catalogo_completo.json','w',encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print('Guardado catalogo_completo.json (JSON) desde', url)
            sys.exit(0)
        except Exception:
            print('No JSON, intentando CSV parse...')
            lines = [l for l in txt.split('\\n') if l.strip()]
            headers = [h.strip().strip('\"\\'') for h in lines[0].split(',')]
            objs = []
            for line in lines[1:]:
                cols = line.split(',')
                obj = {}
                for i,h in enumerate(headers):
                    obj[h]= cols[i] if i < len(cols) else ''
                if 'ra' in obj and 'dec' in obj:
                    try:
                        objs.append({'id': obj.get('ID') or obj.get('NGC') or obj.get('IC') or '', 'nombre': obj.get('Name') or obj.get('name') or '', 'ra': float(obj.get('ra')), 'dec': float(obj.get('dec')), 'mag': float(obj.get('mag') or obj.get('mag_v') or 0)})
                    except:
                        pass
            if objs:
                with open('catalogo_completo.json','w',encoding='utf-8') as f:
                    json.dump(objs, f, ensure_ascii=False, indent=2)
                print('Guardado catalogo_completo.json (CSV parsed) desde', url)
                sys.exit(0)
    except Exception as e:
        print('Fallo descarga desde', url, e)
print('No se pudo descargar catálogo. Revisa conexión o descarga manual desde https://github.com/mattiaverga/OpenNGC')

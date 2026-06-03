#__author__ = 'jblukach'

import sqlite3
from morphs.BaseMorph import BaseMorph

class filenamesNSRL(BaseMorph):
    
    name = 'NSRLFilename'
    displayname = 'NSRL Filename Morph'
    helptext = 'Shows filenames that do not match the NSRL list'
    plugins = ['pslist','psxview']
    config = {
        'NSRLdb':{
            'name':'NSRL Name Database',
            'description':'Database of names in NSRL fileset',
            'type':'path',
            'required':True
        }
    }

    def morph(self, data):
        if data['name'] == 'pslist' or data['name'] == 'psxview':
            colnum = data['columns'].index('Name')
            con = sqlite3.connect(self.config['NSRLdb']['value'])
            cur = con.cursor()
            try:
                for idx, row in enumerate(data['data']):
                    cur.execute(
                        "SELECT filename FROM NSRL WHERE filename=:filename",
                        {"filename": row[colnum].lower()},
                    )
                    match = cur.fetchone()
                    if match is None:
                        new_row = list(row)
                        new_row[colnum] = {'value': row[colnum], 'style': 'background-color:yellow;'}
                        data['data'][idx] = new_row
            finally:
                cur.close()
                con.close()

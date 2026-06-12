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
            for idx,row in enumerate(data['data']):
                
                con = sqlite3.connect('NSRL_RDS_2-48_File_Names.SQLite')
                cur = con.cursor()
                cur.execute("SELECT filename FROM NSRL WHERE filename=:filename", {"filename":row[colnum].lower()})
                match = cur.fetchone()
                
                try:
                    if match is None:
                        row = list(row)
                        row[colnum] = {'value':row[colnum],'style':'background-color:yellow;'}
                        data['data'][idx] = row
                except (IndexError, TypeError, ValueError):
                    # IndexError: colnum is computed from
                    # data['columns'].index('Name') and the row tuple
                    # may have been hand-trimmed by an upstream plugin
                    # (pslist, psxview) to fewer columns than
                    # data['columns'] reports.
                    # TypeError: row[colnum] can raise if the column
                    # value is not subscriptable (e.g. a pre-flattened
                    # record from a custom pslist plugin).
                    # ValueError: list(row) can raise on malformed
                    # numpy record rows with non-uniform dtypes.
                    # The bare except: also caught KeyboardInterrupt
                    # and SystemExit, which should propagate, and
                    # silently swallowed any future bug introduced
                    # into the row-mutate path. The narrow tuple
                    # keeps the documented 'highlight unmatched
                    # names' behavior for the three real row-shape
                    # failure modes while letting real bugs surface.
                    pass
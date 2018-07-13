# -*- mode: python -*-

block_cipher = None


a = Analysis(['GUI.py'],
             pathex=['.\\modules\\'],
             binaries=[],
             datas=[],
             hiddenimports=['frameworkAPI', 'platform', 'json', 'ssl', 'xmlrpclib', 'SocketServer', 'SimpleXMLRPCServer', 'ldap3', 'passlib.hash', 'psycopg2', 'code'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='server',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='.\\build.ico')
coll = COLLECT(exe,
               a.binaries,
               Tree('.\\windows', prefix='windows\\'),
               Tree('.\\plugins', prefix='plugins\\'),
               Tree('.\\icons', prefix='icons\\'),
               Tree('.\\locale', prefix='locale\\'),
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='.')

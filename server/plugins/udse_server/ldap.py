# -*- coding: utf-8 -*-

from ldap3 import Server, Connection, NTLM
from passlib.hash import lmhash, nthash
from settings import domains

class LDAP:
    def __init__(self, adLogin, adPwdHash, adDomain):
        self.adUser = adDomain+'\\'+adLogin
        self.adPwdHash = adPwdHash
        self.adHost = domains[adDomain.lower()]
    def connect(self):
        result = None
        try:
            connection = Connection(Server(self.adHost),
                                user=self.adUser,
                                password=self.adPwdHash,
                                authentication=NTLM,
                                auto_bind=True)
            result = connection
            #connection.unbind()
        except Exception as error:
            raise
        return result

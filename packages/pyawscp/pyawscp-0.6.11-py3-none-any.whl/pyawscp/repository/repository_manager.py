import os
from os.path import expanduser
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage

class RepositoryManager:

    CREDENTIALS         = "CREDENTIALS"
    ROLE                = "ROLE"
    MFA                 = "MFA"
    DB_CREDENTIALS_FILE = os.path.join(expanduser("~"),".pyawscp","credentials")
    DB_ROLE_FILE        = os.path.join(expanduser("~"),".pyawscp","role")
    DB_MFA_FILE         = os.path.join(expanduser("~"),".pyawscp","mfa")

    def __init__(self, _dbFile):
        self.database = TinyDB(_dbFile, indent=4)
    
    def isEmpty(self):
        return not len(self.database.all()) > 0
    
    def insert(self, record):
        self.database.insert(record)
    
    def remove(self, query):
        self.database.remove(query)

    def findByProfile(self, profile):
        return self.database.get(Query().profile == profile)
    
    def searchByQuery(self, query):
        return self.database.search(query)
    
    def update(self, record, profile):
        self.database.update(record, Query().profile == profile)
    
    def all(self):
        return self.database.all()
    
    def purge(self):
        self.database.truncate()
    
    def databaseConnection(self):
        return self.database

class CredentialsRepository(RepositoryManager):
     def __init__(self):
         super().__init__(RepositoryManager.DB_CREDENTIALS_FILE)

class RoleRepository(RepositoryManager):
     def __init__(self):
         super().__init__(RepositoryManager.DB_ROLE_FILE)

class MfaRepository(RepositoryManager):
     def __init__(self):
         super().__init__(RepositoryManager.DB_MFA_FILE)





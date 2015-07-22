import os
import math
import Parallel
import DBManager

if __name__ == "__main__":
    #p = Parallel.Parallel('E:\\Python Projects\\Parallel\\Parallel\\test.sys')
    #p.GetFileOutput('E:\\Python Projects\\Parallel\\Parallel\\out.sys')
    dbm = DBManager.DBManager('E:\\Python Projects\\Parallel\\Parallel\\share.db')
    dbm.InitializeDB()
    #dbm.InsertNewSharedFile('E:\\Python Projects\\Parallel\\Parallel\\test.sys', 'share_0x0000000000000001');
    dbm.InsertNewSharedFile('pippo', 'pluto');
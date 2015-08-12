import os
import math
import Parallel
import DBManager

if __name__ == "__main__":
    #p = Parallel.Parallel('E:\\Python Projects\\Parallel\\Parallel\\test.sys')
    #p.GetFileOutput('E:\\Python Projects\\Parallel\\Parallel\\out.sys')
    dbm = DBManager.DBManager('E:\\Python Projects\\Parallel\\Parallel\\share.db')
    dbm.InitializeDB()
    dbm.InsertNewSharedFile('E:\\Python Projects\\Parallel\\test\\test.txt', '0x0000000000000001');
    dbm.InsertNewSharedFile('E:\\Python Projects\\Parallel\\test\\test_2.txt', '0x0000000000000002');
    dbm.InsertNewSharedFile('E:\\Python Projects\\Parallel\\test\\test.sys', '0x0000000000000003');
    dbm.InsertNewSharedFile('E:\\Python Projects\\Parallel\\test\\mp3.mp3', '0x0000000000000004');
    dbm.InsertNewSharedFile('E:\\Python Projects\\Parallel\\test\\flv.flv', '0x0000000000000005');
    dbm.RecoveryFileFromDB('E:\\Python Projects\\Parallel\\test\\test_exit.txt', '0x0000000000000001');
    dbm.RecoveryFileFromDB('E:\\Python Projects\\Parallel\\test\\test_2_exit.txt', '0x0000000000000002');
    dbm.RecoveryFileFromDB('E:\\Python Projects\\Parallel\\test\\test_exit.sys', '0x0000000000000003');
    dbm.RecoveryFileFromDB('E:\\Python Projects\\Parallel\\test\\mp3_exit.mp3', '0x0000000000000004');
    dbm.RecoveryFileFromDB('E:\\Python Projects\\Parallel\\test\\flv_exit.mp3', '0x0000000000000005');
    #dbm.DeleteShareFile('0x0000000000000004');
    dbm.CloseConnection();
    #dbm.InsertNewSharedFile('pippo', 'pluto');
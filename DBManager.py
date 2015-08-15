import Parallel
import sqlite3

# variables name definition:
# G_ : global variables
# P_ : parameter varaibales
# L_ : local variables
# O_ : output variables

class DBManager:

    def __init__(self, P_DB_Name):
        try:
            global G_Con
            global G_Cur
            G_Con = sqlite3.connect(P_DB_Name)
            G_Cur = G_Con.cursor()
        except:
            print("Error DBManager.Init.001 - i can't create DB File (" + P_DB_Name + ")")

    def InitializeDB(self):
        #try query on indexes table. if this query is impossible, i need to create table indexes
        try:
            L_SqlQuery = "select Indexes_File_Name from indexes"
            G_Cur.execute(L_SqlQuery)
        except:
            # creation of indexes table
            try:
                G_Cur.execute("""create table indexes(
                                Indexes_Primary_Key INTEGER PRIMARY KEY,
                                Indexes_File_Name TEXT,
                                Indexes_Index TEXT,
                                Indexes_Pkg_Count INTEGER
                            )""")
                return True
            except:
                print("Error DBManager.InitializeDB.001 - i can't create table 'indexes'")
                return False

    def InsertNewSharedFile(self, P_File_Name, P_File_Index):
        #try to find current shared file.
        try:
            L_SqlQuery = "select Indexes_File_Name from indexes where Indexes_Index = '" + P_File_Index + "'"
            G_Cur.execute(L_SqlQuery)
        except:
            print("""Error DBManager.InsertNewSharedFile.001 - i can't execute \"""" + L_SqlQuery + """\"""")
        try:
            # if i can't find it, i need to create.
            L_Index_Value = 1
            if G_Cur.fetchone() == None:
                L_SqlQuery = "select MAX(Indexes_Primary_Key) from indexes"
                G_Cur.execute(L_SqlQuery)
                for c in G_Cur.fetchone():
                    if c == None:
                        L_Index_Value = 1
                    else:
                        L_Index_Value += c
                # loop file and insert bynary packages
                p = Parallel.Parallel(P_File_Name)
                L_count = p.FilePackageCount()
                G_Cur.execute("""insert into indexes(Indexes_Primary_Key, Indexes_File_Name, Indexes_Index, Indexes_Pkg_Count)
                            values (
                                """ + str(L_Index_Value) + """,
                                '""" + P_File_Name + """',
                                '""" + P_File_Index + """',
                                '""" + str(L_count) + """'
                            )""")
                G_Con.commit()
                try:
                    G_Cur.execute("""create table share_""" + P_File_Index + """(
                                    Share_Primary_Key INTEGER PRIMARY KEY ASC,
                                    Share_Value BLOB
                                )""")
                    G_Con.commit()
                except:
                    print("""Error DBManager.InsertNewSharedFile.004 - i can't creatre 'share_""" + P_File_Index + """' table""")
                try:
                    G_Cur.execute("""create table pkgshared_""" + P_File_Index + """(
                                    Pkgshared_Primary_Key INTEGER PRIMARY KEY ASC,
                                    Pkgshared_Package_No INTEGER,
                                    Pkgshared_Count INTEGER
                                )""")
                    G_Con.commit()
                except:
                    print("""Error DBManager.InsertNewSharedFile.006 - i can't creatre 'pkgshared_""" + P_File_Index + """' table""")
                try:
                    i = 0
                    while i < (L_count):
                        out = []
                        for c in p.GetReadPackage(i):
                            out.append(c)
                        blob = bytearray(out)
                        G_Cur.execute("""insert into share_""" + P_File_Index + """ (Share_Primary_Key, Share_Value)
                                            values (""" + str(i+1) + """, ?)""", (blob,))
                        G_Cur.execute("""insert into pkgshared_""" + P_File_Index + """ (Pkgshared_Primary_Key, Pkgshared_Package_No, 
                                        Pkgshared_Count) values (""" + str(i+1) + """, """ + str(i+1) + """, 0)""")
                        i += 1
                    G_Con.commit()
                    print("file '" + P_File_Name + "' with index '" + P_File_Index + "' insert into 'share_" + P_File_Index + "'' table")
                except:
                    #print("""Error DBManager.InsertNewSharedFile.005 - i can't insert """ + blob.tostring() + """ into 'share_""" + P_File_Index + """' table""")
                    print("""Error DBManager.InsertNewSharedFile.005 - i can't insert 'something' into 'share_""" + P_File_Index + """' table""")
            else:
                print("""Error DBManager.InsertNewSharedFile.003 - file '""" + P_File_Name + """' with index '""" 
                    + P_File_Index + """' already exists into 'indexes' table""")
        except:
            print("""Error DBManager.InsertNewSharedFile.002 - i can't insert file '""" + P_File_Name + """' with index '""" 
                + P_File_Index + """' into 'indexes' table""")

    def RecoveryFileFromDB(self, P_File_Name, P_File_Index):
        #recovery file from DB and save it into path specified in P_File_Name variable with specified name        
        L_SqlQuery = "select COUNT(*) from share_" + P_File_Index
        G_Cur.execute(L_SqlQuery)
        for c in G_Cur.fetchone():
            if c == None:
                L_count = 0
            else:
                L_count = int(c)

        i = 0
        exit_bytearray = bytearray([])
        while i < (L_count):
            exit_bytearray += self.ReturnPackageValue(P_File_Index, i+1)
            i += 1

        f = open(P_File_Name,'wb')
        f.write(exit_bytearray)
        f.close()

    def ReturnPackageValue(self, P_File_Index, P_Pkg_Count):
        #return specified package from specified file index
        L_SqlQuery = """select Share_Value from share_""" + P_File_Index + """ 
                        where Share_Primary_Key = """ + str(P_Pkg_Count) + """ order by Share_Primary_Key"""
        G_Cur.execute(L_SqlQuery)
        try:            
            exit_bytearray = bytearray([])
            for c in G_Cur.fetchone():
                exit_bytearray += c
            return exit_bytearray
        except:
            print("Error DBManager.ReturnPackageValue.001 - i can't read " + str(P_Pkg_Count) + " package")

    def DeleteShareFile(self, P_File_Index):
        #delete a file into DB. This function delete index and tables linked to shared file.
        try:
            L_SqlQuery = "delete from indexes where Indexes_Index = '" + P_File_Index + "'"
            G_Cur.execute(L_SqlQuery)
            try:
                L_SqlQuery = "drop table share_" + P_File_Index
                G_Cur.execute(L_SqlQuery)
                L_SqlQuery = "drop table pkgshared_" + P_File_Index
                G_Cur.execute(L_SqlQuery)
                G_Con.commit()
                try:
                    #this query empty free space from DB
                    L_SqlQuery = "VACUUM"
                    G_Cur.execute(L_SqlQuery)
                    G_Con.commit()
                except sqlite3.Error as e:
                    print("Error DBManager.DeleteShareFile.003 - " + e)
            except sqlite3.Error as e:
                print("Error DBManager.DeleteShareFile.002 - " + e)
        except sqlite3.Error as e:
            print("Error DBManager.DeleteShareFile.001 - " + e)

    def CloseConnection(self):
        #close connection
        G_Con.close()
import platform
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
                                Indexes_Index TEXT
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
                G_Cur.execute("""insert into indexes(Indexes_Primary_Key, Indexes_File_Name, Indexes_Index)
                            values (
                                """ + str(L_Index_Value) + """,
                                '""" + P_File_Name + """',
                                '""" + P_File_Index + """'
                            )""")
                try:
                    G_Cur.execute("""create table share_""" + P_File_Index + """(
                                    Share_Primary_Key INTEGER PRIMARY KEY ASC,
                                    Share_Value BLOB
                                )""")
                except:
                    print("""Error DBManager.InsertNewSharedFile.004 - i can't creatre 'share_""" + P_File_Index + """' table""")
                try:
                    # loop file and insert bynary packages here....
                    p = Parallel.Parallel(P_File_Name)
                    L_count = p.FilePackageCount()
                    i = 0
                    while i < (L_count):
                        out = []
                        for c in p.GetReadPackage(i):
                            out.append(c)
                        blob = bytearray(out)
                        G_Cur.execute("""insert into share_""" + P_File_Index + """ (Share_Primary_Key, Share_Value)
                                            values (""" + str(i+1) + """, ?)""", (blob,))
                        i += 1
                    G_Con.commit()
                except:
                    #print("""Error DBManager.InsertNewSharedFile.005 - i can't insert """ + blob.tostring() + """ into 'share_""" + P_File_Index + """' table""")
                    print("""Error DBManager.InsertNewSharedFile.005 - i can't insert 'something' into 'share_""" + P_File_Index + """' table""")
            else:
                print("""Error DBManager.InsertNewSharedFile.003 - file '""" + P_File_Name + """' with index '""" 
                    + P_File_Index + """' already exists into 'indexes' table""")
        except:
            print("""Error DBManager.InsertNewSharedFile.002 - i can't insert file '""" + P_File_Name + """' with index '""" 
                + P_File_Index + """' into 'indexes' table""")
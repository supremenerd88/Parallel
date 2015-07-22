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
        try:
            L_SqlQuery = "select Indexes_File_Name from indexes where Indexes_Index = '" + P_File_Index + "'";
            G_Cur.execute(L_SqlQuery);
        except:
            print("""Error DBManager.InsertNewSharedFile.001 - i can't execute \"""" + L_SqlQuery + """\"""")
        try:
            if G_Cur.fetchone() == None:
                G_Cur.execute("""insert into indexes(Indexes_Primary_Key, Indexes_File_Name, Indexes_Index
                            values (
                                1,
                                '""" + P_File_Name + """',
                                '""" + P_File_Index + """'
                            )""")
                try:
                    G_Cur.execute("""create table share_""" + P_File_Index + """(
                                    Share_Primary_Key INTEGER PRIMARY KEY ASC,
                                    Share_Value BLOB
                                )""")
                except:
                    print("""Error DBManager.InsertNewSharedFile.001 - i can't creatre 'share_""" + P_File_Index + """' table""")
            else:
                print("already exist!!!")
        except:
            print("""Error DBManager.InsertNewSharedFile.002 - i can't insert file '""" + P_File_Name + """' with index '""" 
                + P_File_Index + """' into 'indexes' table""")
        
'''
#print(cur.fetchall())
for result in cur.fetchall():
    for value in result:
        print(value)
    print('############')
'''
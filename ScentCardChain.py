import datetime
import hashlib
import pymysql
 
"""Hi there! 
In ScentCardChain.py, I generate a Block-chain functionality in my Scent Card app (please check ScentCard.rp, which sumbits together).
Here is the details of ScentCardChain program:
""" 

class ScentCard:
    """Store information input of a scent card,
    including Owner name, Scent Card name, Fragrance, Top note, Middle note, Low note
    also the information of a block, including blockNo, timestamp, hash code, previous block's hash code,
    nonce and reference of the next block
    """
    # information of a block
    blockNo = 0
    next = None
    Hash = None
    data = None
    nonce = 0
    previous_hash = 0x0 # read in hexadecimal
    timestamp = datetime.datetime.now() # current time that a block generated

    def __init__(self,data=None):
        self.data = data

    # information of a scent card
    def sc_input(self):
        self.owner = input("Owner's name: ")
        self.Name = input("your Scent card name: ")
        self.Fragrance = input("your Scent card fragrance(weak/medium/strong): ")
        self.Top_note = input("Scent Card Top note: ")
        self.Middle_note = input("Scent Card Middle note: ")
        self.Low_note = input("Scent Card Low note: ")
        self.data = "Owner: " + self.owner + "\nFragrance: " + self.Fragrance +"\nTop note: " + self.Top_note + "\nMiddle note: " + self.Middle_note + "\nLow note: " + self.Low_note
        return self
    
    # generate hash code, containing all messages of a scent card, nonce
    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest() 
 
    def __str__(self):
        # when print a block, it will print like this:
        output = ("--------------\n"+"Scent Card No : " + str(self.blockNo) + "\nHash code: " + str(self.nonce) +
        "\n" + str(self.data) + "\nBlock Hash: " + str(self.hash()) +
        "\nCreate time: " + str(self.timestamp)+"\n--------------")
        # hash code acts as a password of your scent card, so it should be printed as first
        return output

class ScentCard_dbs:
    """basic operation: including input/check your dbs info"""
    def input_dbs_info(self):
        #input information of your own database, including host, user,password, port
        self.host = input("your MySQL database host(default=localhost): ")
        self.user = input("your MySQL user's name: ")
        self.password = input("your MySQL password: ")
        self.port = input("your MySQL port(default = 3306): ")
        # default value of port
        if len(self.host) == 0:
            self.host = "localhost"
        if len(self.port) == 0:
            self.port = "3306"

        #check the information of your database if necessary
        changemode = 0
        while changemode == 0:
            print("host: "+self.host,"user: "+self.user,"password: "+self.password,"port: "+self.port,sep="\n")
            changemode = int(input("are these information correct?(1:Yes,0:No) "))
            if changemode == 1:
                break
            msg_changes = input("what information you'd like to change(host,user,password,port)? " +
                                "use \",\" to seperate your input if more than 2 information you want to change: ")
            msg_changes_list = msg_changes.split(",")
            for each in msg_changes_list:
                if each == "host":
                    self.host = input("your MySQL database host(default=localhost): ")
                if each == "user":
                    self.user = input("your MySQL user's name: ")
                if each == "password":
                    self.password = input("your MySQL password: ")
                if each == "port":
                    self.port = input("your MySQL port(default = 3306): ")
        # when all information of database is recorded and correct return true
        return True
    """transactions of databases: including create dbs, table, add(insert), select operation
    (block in blockchain cannot update of delete)
    the use of each transaction will connect the database and close it as the transaction ends.
    do check the information of your own database when using the following method"""

    def create_dbs(self)->bool:
        # create or recreate a database: ScentCard, return true if database is create
        db = pymysql.connect(host=self.host,
                             user=self.user,
                             password=self.password,
                             port=int(self.port))
        cursor = db.cursor()
        try:
            cursor.execute("CREATE DATABASE ScentCard")
            print("database ScentCard has created!!")
            return True
        except pymysql.ProgrammingError as pe:
            print("error occurs when creating database: ",pe)
        finally:
            db.close()

    def create_table(self)->bool:
        #create or recreate table: ScentCardChain
        db = pymysql.connect(host=self.host,
                             user=self.user,
                             password=self.password,
                             port=int(self.port))
        cursor = db.cursor()
        #sql code for CREATE operation
        cursor.execute("USE scentcard;") #every time we should verify what database is going to use
        sql = """CREATE TABLE IF NOT EXISTS ScentCardChain(
            ScentCardNo INT PRIMARY KEY,
            Owner VARCHAR(50) NOT NULL,
            Name VARCHAR(50),
            Fragrance VARCHAR(30),
            Top_note VARCHAR(30),  
            Middle_note VARCHAR(30), 
            Low_note VARCHAR(30), 
            Hashcode VARCHAR(50),
            Create_time VARCHAR(100)
            );"""
        try:
            cursor.execute(sql)
            print("table ScentCardChain has created!!")
            return True
        except pymysql.ProgrammingError as pe:
            print("error occurs when creating table: ",pe)
        finally:
            db.close()
    
    def add_to_table(self,scentCard:ScentCard)->bool:
        #add information of blockChain to table:
        db = pymysql.connect(host=self.host,
                             user=self.user,
                             password=self.password,
                             port=int(self.port))
        cursor = db.cursor()
        cursor.execute("USE scentcard;") #every time we should verify what database is going to use
        #sql code for INSERT operation
        sql = """INSERT INTO ScentCardChain VALUES
        (%s,'%s','%s','%s','%s','%s','%s','%s','%s');""" % (scentCard.blockNo,scentCard.owner,scentCard.Name,
                                                        scentCard.Fragrance,scentCard.Top_note,scentCard.Middle_note,scentCard.Low_note,
                                                        str(scentCard.nonce),str(scentCard.timestamp))
        try:
            #transaction:INSERT
            cursor.execute(sql)
            db.commit()
        except pymysql.ProgrammingError as pe:
            db.rollback()
            print("error occurs when add something to table: ",pe)
        finally:
            db.close()

    def select_sc(self,mode = None):
        #user can check information of his scent card by input the hash code.
        db = pymysql.connect(host=self.host,
                             user=self.user,
                             password=self.password,
                             port=int(self.port))
        cursor = db.cursor()
        cursor.execute("USE scentcard;") #every time we should verify what database is going to use
        #sql code for SELECT operation
        if mode == None:
            code = input("input your hash code of scent card: ")
            sql = """SELECT * FROM ScentCardChain WHERE Hashcode = %s;""" %(code) # return exactly one customer's scent card
        elif mode == "*":
            sql = """SELECT * FROM ScentCardChain""" # return whole ScentCardChain
        try:
            #transaction:SELECT
            cursor.execute(sql)
            # get the result of SELECT operation:
            results = cursor.fetchall()
            for row in results:
                blockno = row[0]
                owner = row[1]
                name = row[2]
                fragrance = row[3]
                top_note = row[4]
                middle_note = row[5]
                low_note = row[6]
                hashcode = row[7]
                create_time = row[8]
                print ("ScentCardno: %s\nHash code: %s\nOwner: %s\nName: %s\nFragrance: %s\nTop note: %s\nMiddle note: %s\nLow note: %s\nCreate time: %s"
                       % (blockno,hashcode,owner,name,fragrance,top_note,middle_note,low_note,create_time))
            db.commit()
        except pymysql.ProgrammingError as pe:
            db.rollback()
            print("error occurs when add something to table: ",pe)
        finally:
            db.close()


class ScentCardchain:
    #set the difference that create a block, here the value "diff" = 20
    diff = 20
    maxNonce = 2**32
    target = 2 ** (256-diff)
 
    block = ScentCard("Genesis") #original block
    dummy = head = block
 
    def add_sc_db(self,db_info=None):
        self.db = db_info # db:attribute to record database information
           
    
    def add(self, block:ScentCard):
        #add a block in form of Linked list, where the number of block increase simutaneously
        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        #create single linked list
        self.block.next = block
        self.block = self.block.next 

        #add a scent card to table:
        if self.db != None:
            self.db.add_to_table(block)

    def find_in_table(self):
        # find a specific scent card from database through find method
        self.db.select_sc()
    
    #Block mining: to find a proper nounce, so that to find a proper hash value 
    # only the valid hash value can be added
    def mine(self, block:ScentCard,db=None):
        self.add_sc_db(db)
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target: # convert the hash value from hexadecimal to decimal first
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1 

# specific input / output functions

def create_sc(n:int,db:ScentCard_dbs = None)->ScentCardchain:
    """create a block for scent card and add to blockchain"""
    scentcardchain = ScentCardchain()
    for i in range(n):
        sc = ScentCard().sc_input()
        print("Generating Scent card "+ str(i+1) + " please wait...")
        scentcardchain.mine(sc,db)
    return scentcardchain

def get_sc_chain(scentcardchain:ScentCardchain):
    """return blockchain of scent card, including the original block"""
    while scentcardchain.head != None:
        print(scentcardchain.head) 
        scentcardchain.head = scentcardchain.head.next

def create_sc_table():
    db_info = ScentCard_dbs()
    has_input = db_info.input_dbs_info()
    if has_input == 1:
        has_db = db_info.create_dbs()
        if has_db == 1:
            has_table = db_info.create_table()
            if has_table == 1:
                db = db_info # db:attribute to record database information
                return db

 
# main() function
# create 3 scent card
sc_num = 3
# #get scent card chain
# sc_chain1 = create_sc(sc_num)

#add one's scent card to MySQL:
db = create_sc_table()
sc_chain2=create_sc(sc_num,db)
sc_chain2.find_in_table()
#get_sc_chain(sc_chain1)

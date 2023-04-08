import sqlite3

class DataBase:
    def __init__(self):

        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()

        # Создание базы данных
        self.cur.execute(
            """
			CREATE TABLE IF NOT EXISTS users(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				userid BIGINT,
                status INT,
                balance FLOAT,
                logsLoad INT,
                profits FLOAT,
                referalsProfits FLOAT,
                linked_qiwi TEXT,
                linked_lzt TEXT,
                linked_btc TEXT,
                linked_eth TEXT,
                linked_usdt TEXT,
                linked_ltc TEXT,
                ban INT,
                username TEXT
            )
            """
        )

        self.cur.execute(
            """
			CREATE TABLE IF NOT EXISTS work_requests(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				userid BIGINT,
				username TEXT,
                profile TEXT,
                feedback TEXT,
                online TEXT,
                query TEXT
            )
            """
        )

        self.cur.execute(
            """
			CREATE TABLE IF NOT EXISTS referals(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				userid BIGINT,
				referid BIGINT
            )
            """
        )

        self.cur.execute(
            """
			CREATE TABLE IF NOT EXISTS withdraws(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				userid BIGINT,
				types TEXT,
                sum FLOAT,
                status INT
            )
            """
        )

        self.cur.execute(
            """
			CREATE TABLE IF NOT EXISTS logs(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				userid BIGINT,
				fromSite TEXT,
                logsType INT,
                them INT,
                srevices TEXT,
                checkedQuery TEXT,
                linkshop TEXT,
                isInstal INT,
                is3Person INT,
                username TEXT,
                logLink TEXT
            )
            """
        )

    def change(self, query, values):
        """Изменение базы данных (Insert, Update, Alert)"""
        self.cur.execute(query, values)
        self.con.commit()

    def get(self, query, values=None, fetchone=True):
        """Получение данных из базы данных"""
        self.cur.execute(query, values)
        if fetchone:
            return self.cur.fetchone()
        else:
            return self.cur.fetchall()
        
    def createUser(self, userid, username, refer=None):
        if(self.get("SELECT * FROM users WHERE userid = ?", (userid, )) == None):
            self.change("INSERT INTO users VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (userid, 0, 0, 0, 0, 0, "", "", "", "", "", "", 0, username))
            print(f"Создание новой пользователь - {userid}")

            if refer != None:
                self.change("INSERT INTO referals VALUES (NULL, ?, ?)", (userid, refer))
                
    def createWorkQuest(self, userid, username, profile, feedback, online, query):
        print(f"Создание новой заявки на работу - {userid} - {username}")
        self.change("INSERT INTO work_requests VALUES(NULL,?,?,?,?,?,?)", (userid, username, profile, feedback, online, query))

    def createLogs(self, userid, fromSite, typeLogs, typeSubLogs, howCheck, howQueryWork, takeLinks, isInstal, is3Person, username, sendLinkLog):
        print(f"Создание новой заявки на отработку - {userid} - {sendLinkLog}")
        typeSubLogs = typeSubLogs if typeSubLogs != None else ""
        takeLinks = takeLinks if takeLinks != None else ""
        self.change("INSERT INTO logs VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)", (userid, fromSite, typeLogs, typeSubLogs, f"{howCheck}", howQueryWork, takeLinks, isInstal, is3Person, username, sendLinkLog))
        
        logsLoaded = self.getUser(userid)["logsLoad"] + 1
        self.change("UPDATE users SET logsLoad = ? WHERE userid = ?", (logsLoaded, userid))

        if logsLoaded == 50:
            self.givePrefix(userid, 3)
        if logsLoaded == 100:
            self.givePrefix(userid, 4)
        if logsLoaded == 500:
            self.givePrefix(userid, 5)

    def getStatus(self, status):

        return {
            "-1": "Заблокирован",
            "0": "Новокек",
            "1": "Дроповод",
            "2": "V.I.P",
            "3": "Постоялец",
            "4": "Траффер",
            "5": "Логовод",
            "6": "Админ"
        }[str(status)]

    def getUser(self, userid):
        user = self.get("SELECT * FROM users WHERE userid = ?", (userid, ))
        return {
            "id": user[0],
            "userid": user[1],
            "status": self.getStatus(user[2]),
            "balance": round(user[3],2),
            "logsLoad": user[4],
            "profits": round(user[5],2),
            "referalsProfits": round(user[6],2),
            "linked_qiwi": user[7] if user[7] != "" else "Не привязан",
            "linked_lzt": user[8] if user[8] != "" else "Не привязан",
            "linked_btc": user[9] if user[9] != "" else "Не привязан",
            "linked_eth": user[10] if user[10] != "" else "Не привязан",
            "linked_usdt": user[11] if user[11] != "" else "Не привязан",
            "linked_ltc": user[12] if user[12] != "" else "Не привязан",
            "linked_qiwi_clear": user[7],
            "linked_lzt_clear": user[8],
            "linked_btc_clear": user[9],
            "linked_eth_clear": user[10],
            "linked_usdt_clear": user[11],
            "linked_ltc_clear": user[12],
            "referals": self.get("SELECT COUNT(id) FROM referals WHERE referid = ?", (userid, ))[0]
        }
    
    def changeWallet(self, wallet, text, userid):
        self.change(f"UPDATE users SET linked_{wallet.lower()} = ? WHERE userid = ?", (text, userid))

    def createWithdraw(self, userid, types, sum):
        print(f"Создание новой заявки на вывод - {userid} - {types} - {sum}")
        self.change("INSERT INTO withdraws VALUES(NULL,?,?,?,?)", (userid, types, sum, 0))
        self.change("UPDATE users SET balance = 0 WHERE userid = ?", (userid, ))

    def givePrefix(self, userid, prefix):
        self.change("UPDATE users SET status = ? WHERE userid = ?", (prefix, userid))
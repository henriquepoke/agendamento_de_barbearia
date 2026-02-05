import sqlite3

class AgendamentoDB:
    def __init__(self, path, horarios):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.horarios = horarios
        self.init_db()

    def init_db(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS horarios_agendamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                horario TEXT UNIQUE NOT NULL,
                cliente TEXT
            )
        """)

        for h in self.horarios:
            self.cur.execute("""
                INSERT OR IGNORE INTO horarios_agendamento (horario, cliente)
                VALUES (?, NULL)
            """, (h,))

        self.con.commit()

    def adicionar_cliente(self, nome):
        self.cur.execute("""
            UPDATE horarios_agendamento
            SET cliente = ?
            WHERE id = (
                SELECT id FROM horarios_agendamento
                WHERE cliente IS NULL
                ORDER BY horario
                LIMIT 1
            )
        """, (nome,))
        self.con.commit()

        return self.cur.rowcount > 0

    def listar(self):
        self.cur.execute("""
            SELECT horario, cliente
            FROM horarios_agendamento
            ORDER BY horario
        """)
        return self.cur.fetchall()
    
    def remover_cliente(self, nome):
        self.cur.execute("""
            UPDATE horarios_agendamento
            SET cliente = NULL
            WHERE cliente = ?
        """, (nome,))

        self.con.commit()

        return self.cur.rowcount > 0

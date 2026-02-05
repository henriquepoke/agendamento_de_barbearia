from modules.database import AgendamentoDB
from modules.barbearia_modulos import gerar_horarios

horarios = gerar_horarios()
db = AgendamentoDB('db/dadosAgendamentos.db', horarios)

db.remover_cliente('Jadson')

while True:
    nome = input('Nome do cliente: ')
    if not db.adicionar_cliente(nome):
        print('Nenhum horário disponível')
        break

    op = input('Deseja continuar? [S/N]')
    if op.upper() == 'N':
        break

print('\n📋 Agenda:')
for horario, cliente in db.listar():
    print(f'{horario} → {cliente or 'Disponível'}')

db.listar()
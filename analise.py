import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import yfinance as yf


def get_ticket_data(ticker):
    ticker_completo = ticker + '.SA'
    start = datetime.now() - timedelta(days=365 * 3)
    data = yf.download(ticker_completo, start=start, progress=False, interval="1wk")
    data['12 meses'] = data['Close'].rolling(window=12).mean()
    data['3 meses'] = data['Close'].rolling(window=4).mean()
    return data


def generate_graph(show_or_save, data, ticket):
    plt.figure(figsize=(19.20, 10.80))
    plt.plot(data['Close'], label=f'{ticket}')
    plt.plot(data['12 meses'], label='12 meses', linestyle='--')
    plt.plot(data['3 meses'], label='3 meses', linestyle='--')
    plt.title(f'Preço de Fechamento do Ativo {ticket} com Médias Móveis nos Últimos 3 Anos')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento')
    plt.legend()
    plt.grid(True)

    if show_or_save == '1':
        plt.show()
    else:
        graph_path = f"graphs/{datetime.now().strftime('%Y')}/{datetime.now().strftime('%m')}/{datetime.now().strftime('%d')}"
        os.makedirs(graph_path, exist_ok=True)
        file_path = f'{graph_path}/{ticket} {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.png'
        plt.savefig(file_path, dpi=100)


def get_tickets_by_file(file_path):
    tickets = []
    with open(file_path, 'r') as file:
        for line in file:
            ticker = line.strip().upper()
            if ticker:
                tickets.append(ticker)
    return tickets


def main():
    tickets = []

    # Seleção de visualização ou salvamento
    while True:
        show_or_save = input("O que você deseja fazer? "
                             "\n\t1 - Visualizar os gráficos"
                             "\n\t2 - Salvar os gráficos no meu computador"
                             "\nOpção: ")
        if show_or_save in ['1', '2']:
            break
        else:
            print("\n\033[91mOpção inválida.\033[0m\n")

    # Seleção de tipo seleção de ticket e caso necessário caminho do arquivo.
    while True:
        insertion_type = input("\nComo você prefere inserir as ações para analisar?"
                               "\n\t 1 - Manual, vou digitar os tickets"
                               "\n\t 2 - Arquivo, vou selecionar um arquivo que contém todas as ações"
                               "\nOpção: ")
        if insertion_type in ['1', '2']:
            if insertion_type == '1':
                while True:
                    ticker = input("\nDigite o ticket da ação."
                                   "\n\tExemplo: ABEV3, B3SA3, ITUB4, PETR4, VALE3, WEGE3..."
                                   "\n\tPressione \033[93mEnter\033[0m para prosseguir"
                                   "\nTicket: ").upper()
                    if ticker == '/CONTINUE':
                        break
                    tickets.append(ticker)
            elif insertion_type == '2':
                while True:
                    file_path = input("\nQual é o caminho até o arquivo?"
                                      "\n\tPressione enter se o caminho for \033[93m./acoes.csv\033[0m"
                                      "\nCaminho: ")
                    file_path = file_path if file_path else './acoes.csv'

                    if os.path.exists(file_path):
                        tickets = get_tickets_by_file(file_path)
                        break
                    else:
                        print("\n\033[91mArquivo não encontrado.\033[0m")
            break
        else:
            print("\n\033[91mOpção inválida.\033[0m")

    while True:
        averages = input("\nVocê deseja inserir médias? "
                         "\n\t1 - Sim"
                         "\n\t2 - Não"
                         "\nOpção: ")

        if averages in ['1', '2']:
            if averages == '1':
                count = 1
                list_average = []
                while True:
                    average = input(f"\nInforme a {count}° média em dias: "
                                    "\n\tPressione \033[93mEnter\033[0m para prosseguir"
                                    "\nMédia: ")

                    if len(list_average) == 0 and average == '':
                        print("\n\033[91m\nVocê deve informar ao menos uma média.\033[0m")
                    elif len(list_average) > 0 and average == '':
                        break
                    else:
                        try:
                            list_average.append(int(average))
                            count += 1
                        except ValueError:
                            print("\n\033[91m\nVocê deve informar um número inteiro.\033[0m")

                # Seleciona se deseja apenas tickets em tendência de alta
                while True:
                    just_uptrend = input(
                        f"\nExibir apenas ações com tendência de alta? Média {min(list_average)} dias maior que a "
                        f"média de {max(list_average)} dias."
                        "\n\t1 - Sim"
                        "\n\t2 - Não"
                        "\nOpção: ")
                    if just_uptrend in ['1', '2']:
                        break
                    else:
                        print("\n\033[91mOpção inválida.\033[0m")
                break
            else:
                break
        else:
            print("\n\033[91mOpção inválida.\033[0m")

    for ticket in tickets:
        data = get_ticket_data(ticket)

        if data.empty:
            print(f"Sem informações para {ticket}")
        else:
            try:
                if just_uptrend == '1':
                    if (data['3 meses'].iloc[-1] > data['12 meses'].iloc[-1]) and (
                            data['Close'].iloc[-1] > data['Close'].iloc[-3]):
                        print(f"\033[92mMontando gráfico do ticket {ticket}, em tendência de alta.\033[0m")
                        generate_graph(show_or_save, data, ticket)
                    else:
                        print(f"\033[91mIgnorando o ticket {ticket}, em tendência de baixa.\033[0m")
            except UnboundLocalError:
                print(f"\033[92mMontando gráfico do ticket {ticket}\033[0m")
                generate_graph(show_or_save, data, ticket)


if __name__ == "__main__":
    main()

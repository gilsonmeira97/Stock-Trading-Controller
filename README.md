# Stock-Trading-Controller
Projeto para obter as cotações diárias da B3 através do software de negociação MetaTrader 5.  
As cotação são obtidas através da lib **"Metatrader5"** e são gravadas em uma base de dados mongoDB.
O objetivo principal dessa aplicação é poder armazenar as cotações localmente possibilitando fazer testes estatísticos para buscar padrões.

## Como utilizar o projeto:
Primeiramente faça a instalação dos seguintes programas: [**mongoDB**](https://www.mongodb.com/try/download/community), [**Metatrader 5**](https://www.metatrader5.com/es/download), [**Git**](https://git-scm.com/downloads), [**Python 3**](https://www.python.org/downloads/).

<br>

Clone o repositório com o comando:
```
git clone https://github.com/gilsonmeira97/Stock-Trading-Controller.git
```

<br>

Entre na pasta do projeto com o comando: 
```
cd ./Stock-Trading-Controller
```

<br>

Faça a instalação dos requerimentos com o comando: 
```
pip install -r ./requirements.txt
```

<br>

Crie um arquivo na raiz do projeto com o nome ***.env*** com a seguinte estrutura:
>LOGIN='Login na corretora - Ex: 5748754'<br>
>SERVER='Nome do servidor da corretora - Ex: HPXT5-DEMO'<br>
>PASSWORD='Senha na corretora - Ex: ABC123456'

<br>

Faça o download do histórico de cotação diária **(Mais recente de preferência)** através do link abaixo, salve o arquivo na pasta raiz do projeto com o nome ***'COTAHIST_Reference.txt'***:
>https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/

<br>

Após isso, basta rodar o comando: 
```
python ./mt5UpdateRates.py
```

<br>

O comando acima criará o registro de todos os ativos na primeira vez que for executado, nas vezes subsequentes irá apenas atualiza-los.

<br>

O database terá diversas collections, onde cada uma representará um ativo e cada document dessa collection representará o tick de um horário determinado.
### A estrutura do banco de dados será:
```
Stocks(Database) {
	PETR3(Collection): {
		{'date', 'open', 'close', 'high', 'low', 'real_volume', 'tick_volume' },
		{'date', 'open', 'close', 'high', 'low', 'real_volume', 'tick_volume' },
		...
	},
	VALE3(Collection): {
		{'date', 'open', 'close', 'high', 'low', 'real_volume', 'tick_volume' },
		{'date', 'open', 'close', 'high', 'low', 'real_volume', 'tick_volume' },
		...
	}
}
```

<br>

## Observações:
- A lib ***Metatrader5*** só está disponível para plataforma Windows, logo, não será possível obter as cotações através de uma plataforma linux.
- csvExtract tem como função exportar as cotações de um determinado ativo.
- A pasta tempTest contem arquivos com funcionalidades em teste, a mesma não é referenciada por nenhum outro arquivo podendo até mesmo ser excluída.
- o arquivo ***\_\_sub\_\_.py*** é utilizado apenas para referenciar o diretório raiz nos subdiretórios, o que permite utilizar módulos do diretório raiz em arquivos que estão em subdiretórios.
- A pasta ***strategies*** é destinada a armazenar as estratégias que serão testadas, nela há algumas estratégias já testadas, utilize um dos arquivos para melhor orientar-se na criação de suas estratégias.

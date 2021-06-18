# fast-circuit-breaker

> Circuit breakers existem para permitir que uma parte do seu sistema falhe sem destruir todo seu ecossistema de serviços. Michael Nygard

Nesse exemplo vamos executar o serviço de oferta (fria) que se comunica com o serviço de oferta do parceiro (quente). Depois vamos provocar uma indisponibilidade no serviço de oferta do parceiro, retornando uma oferta fria (fallback) do serviço de oferta.

![Fluxo de oferta!](/imgs/offer-flow.png "Fluxo de oferta")

Veremos que em certo momento o serviço de oferta deixará de se comunicar com o serviço de oferta do parceiro, abrindo o circuito (open), após um determinado tempo o serviço de oferta continuará tentando restabelecer a comunicação com serviço de oferta do parceiro.

Quando a comunicação entre os serviços for restabelecida, o circuito será fechado (close).

![Estados do circuit breaker!](/imgs/circuit-breaker-states.png "Estados do circuit breaker")

## Instalação

Crie um ambiente virtual.

`python3 -m venv venv`

Ative o ambiente virtual.

`source venv/bin/activate`

Instale as pendencias do projeto.

`pip install -r requirements.txt`

## Uso

Execute o serviço de oferta do parceiro, responsável por retornar uma oferta quente (hot).

`python partner_offer_service.py`

Execute o serviço de oferta, responsável por buscar oferta no serviço de oferta parceiro (hot), em caso de indisponibilidade do serviço de oferta do parceiro retorna oferta fria (cold).

`HTTPX_LOG_LEVEL=debug python offer_service.py`

Execute o [monitoror](https://monitoror.com) para monitorar as aplicações através de um dashboard.

`./monitoror`

![Dashboard Monitoror!](/imgs/monitoror1.png "Dashboard Monitoror")

O arquivo `config.json` tem as configurações do monitoror.

## Circuit break

Pare a execução do serviço de oferta do parceiro, observe que o serviço de oferta deve retornar uma oferta fria (cold).

![Dashboard Monitoror!](/imgs/monitoror2.png "Dashboard Monitoror")

Observe também o número de tentativas falhas do servico de oferta de se comunicar com o servico de oferta do parceiro aumentar.

Após 3 tentativas (`fail_max`) de comunicação com o serviço de oferta do parceiro, o circuito do serviço de oferta mudará seu estado para aberto (open).

![Dashboard Monitoror!](/imgs/monitoror3.png "Dashboard Monitoror")

**No estado aberto o serviço de oferta deixa de se comunicar com o serviço de oferta do parceiro.**

Há cada 15 segundos (`reset_timeout`) o servico de oferta tentará restabelecer uma comunicação com o de oferta do parceiro.

Caso a comunicação seja restabelecida o circuito irá mudar o estado para fechado.

![Dashboard Monitoror!](/imgs/monitoror4.png "Dashboard Monitoror")

O arquivo `circuit_breaker.py` configura o [pybreaker](https://github.com/danielfm/pybreaker) (implementação do padrão circuit break do python).

# fast-circuit-breaker

> Circuit breakers existem para permitir que uma parte do seu sistema falhe sem destruir todo seu ecossistema de serviços. Michael Nygard

Nesse exemplo vamos executar o serviço de oferta (fria) que se comunica com o serviço de oferta do parceiro (quente). Depois vamos provocar uma indisponibilidade no serviço de oferta do parceiro, retornando uma oferta fria (fallback) do serviço de oferta.

![Fluxo de oferta!](/imgs/offer-flow.png "Fluxo de oferta")

Veremos que em certo momento o serviço de oferta deixará de se comunicar com o serviço de oferta do parceiro, abrindo o circuito (open), após um determinado tempo o serviço de oferta continuará tentando restabelecer a comunicação com serviço de oferta do parceiro, circuito meio-aberto (half-open).

Quando a comunicação entre os serviços for restabelecida, o circuito será fechado (close).

Observe abaixo o fluxo de mudança de estado do padrão circuit breaker.

![Estados do circuit breaker!](/imgs/circuit-breaker-states.png "Estados do circuit breaker")

## Instalação

Crie um ambiente virtual.

`python3 -m venv venv`

Ative o ambiente virtual.

`source venv/bin/activate`

Instale as dependências do projeto.

`pip install -r requirements.txt`

## Uso

Execute o serviço de oferta do parceiro, responsável por retornar uma oferta quente (hot).

`python partner_offer_service.py`

Execute o serviço de oferta responsável por buscar oferta quente no serviço de oferta do parceiro.

`HTTPX_LOG_LEVEL=debug python offer_service.py`

Vamos testar a busca de oferta, através de uma chamada HTTP do qualquer cliente (browser, curl, [httpie](https://github.com/httpie/httpie)), o exemplo abaixo usa o httpie.

`http ":8001/offer"`

A resposta deve ser uma oferta quente do serviço de oferta do parceiro.

`"Hot offer 24:48"`

Veja nos logs do serviço de oferta, a resposta OK do serviço de oferta do parceiro.

```bash
DEBUG [2021-06-19 11:03:03] httpx._client - HTTP Request: GET http://127.0.0.1:8000/offer/hot "HTTP/1.1 200 OK"
```

## Circuit breaker

Vamos alterar o arquivo `partner_offer_service.py` na linha 13 para retornar o código de erro 500 na resposta do recurso `GET /offer/hot`, conforme exemplo abaixo.

`return Response(content=body, status_code=500)`

> Atenção: os serviços tem a configuração de recarregar (reload) a aplicação toda vez que um arquivo é alterado.

Vamos chamar o serviço de busca de oferta novamente.

`http ":8001/offer"`

A resposta agora deve ser uma oferta fria, retornada através de uma função (fallback) do serviço de oferta.

`"Cold offer fallback 47:32"`

Veja nos logs do serviço de oferta um erro na comunicação com o serviço de oferta do parceiro.

`DEBUG [2021-06-19 20:44:27] httpx._client - HTTP Request: GET http://127.0.0.1:8000/offer/hot "HTTP/1.1 500 Internal Server Error"`

Vamos verificar o estado do circuito do serviço de oferta.

`http ":8001/offer/circuit"`

A resposta mostra que o circuito está com o estado fechado (`current_state`) e 1 falha `fail_counter`.

```json
{
  "current_state": "closed",
  "fail_counter": 1
}
```

Antes de prosseguirmos vamos analisar a configuração do circuito no arquivo `circuit_breaker.py`, para mais informações consulte a documentação da biblioteca [pybreaker](https://github.com/danielfm/pybreaker).

1. `fail_max`: Quantidade máxima de falhas.
2. `reset_timeout`: Limite de tempo (segundos) para redefinição do estado do circuito.
3. `state_storage`: Onde o estado será armazenado (Memória, Redis, etc).
4. `listeners`: Ouvintes que serão notificados em cada evento do circuito

```python
circuit_breaker = CircuitBreaker(
    fail_max=3,
    reset_timeout=15,
    state_storage=state_storage,
    listeners=[LogListener()]
)
```

Vamos chamar o recurso de buscar oferta mais 3 vezes.

`http ":8001/offer"`

Após 3 falhas (`fail_max`) na comunicação com o serviço de oferta do parceiro, o circuito é aberto (open).

Vamos verificar o estado do circuito mais uma vez.

`http ":8001/offer/circuit"`

Na resposta o circuito está aberto (`current_state`) com 3 falhas `fail_counter`.

```json
{
  "current_state": "open",
  "fail_counter": 3
}
```

**Observe que no estado aberto, não há registro de log de comunicação, pois o circuito protege o serviço de oferta do parceiro de receber chamadas por um determinado período de tempo.**

No estado aberto (open), há cada 15 segundos (`reset_timeout`) o circuito entrará no estado meio-aberto (half-open) para tentar restabelecer a comunicação com o serviço de oferta do parceiro.

Podemos acompanhar (terminal) os eventos do circuito através dos logs da classe `LogListener` registrada como ouvinte na instancia do circuito.

```bash
Antes do circuito invocar a função.
Quando uma invocação de função levanta uma exceção.
Quando o estado do circuito mudou (open).
Quando o estado do circuito mudou (half-open).
Quando o estado do circuito mudou (open).
```

Caso alteremos o código da resposta do serviço de oferta do parceiro para 200, então o circuito será fechado (close), ou caso a resposta continue com código de erro 500 o circuito continuará aberto.

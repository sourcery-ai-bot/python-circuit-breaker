from pybreaker import (
    CircuitBreaker, CircuitMemoryStorage, CircuitBreakerListener, STATE_CLOSED)


class LogListener(CircuitBreakerListener):

    def before_call(self, cb, func, *args, **kwargs):
        print("Antes do circuito invocar a função.")

    def state_change(self, cb, old_state, new_state):
        print(f"Quando o estado do circuito mudou ({new_state.name}).")

    def failure(self, cb, exc):
        print("Quando uma invocação de função levanta uma exceção.")

    def success(self, cb):
        print("Quando uma invocação de função é bem-sucedida.")


state_storage = CircuitMemoryStorage(STATE_CLOSED)
circuit_breaker = CircuitBreaker(
    fail_max=3,
    reset_timeout=15,
    state_storage=state_storage,
    listeners=[LogListener()]
)

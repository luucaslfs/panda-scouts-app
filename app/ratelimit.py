from ratelimit import limits, RateLimitException, sleep_and_retry

# Define o limite global de taxa (por exemplo, 1000 requisições por dia)
GLOBAL_RATE_LIMIT = (1000, 24 * 60 * 60)  # 1000 requisições por dia


def global_rate_limited(func):
    @sleep_and_retry
    @limits(calls=GLOBAL_RATE_LIMIT[0], period=GLOBAL_RATE_LIMIT[1])
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RateLimitException as e:
            # Lidar com exceção de limite de taxa, como registrar ou esperar
            # Você pode personalizar isso de acordo com suas necessidades
            raise Exception(
                "Limite de taxa global atingido. Aguarde e tente novamente mais tarde.")

    return wrapper

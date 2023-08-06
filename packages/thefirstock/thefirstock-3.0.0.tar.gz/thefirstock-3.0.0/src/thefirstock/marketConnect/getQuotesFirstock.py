def firstock_getQuote(exchange, token):
    try:
        getQuotes = FirstockGetQuotes(
            exch=exchange,
            token=token
        ).firstockGetQuotes()

        return getQuotes

    except Exception as e:
        print(e)

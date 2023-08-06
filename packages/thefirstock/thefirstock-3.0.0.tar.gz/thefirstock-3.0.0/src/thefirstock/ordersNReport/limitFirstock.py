def firstock_Limits():
    try:

        limits = FirstockLimits().firstockLimits()

        return limits

    except Exception as e:
        print(e)

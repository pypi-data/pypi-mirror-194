def firstock_PositionBook():
    try:

        positionBook = FirstockPositionBook().firstockPositionBook()

        return positionBook

    except Exception as e:
        print(e)
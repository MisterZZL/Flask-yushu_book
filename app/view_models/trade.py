class TradeInfo():
    def __init__(self,goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self,goods):
        print(type(goods))
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self,single):
        create_datetime = single.create_datetime
        time = create_datetime.strftime('%Y-%m-%d')if create_datetime else '未知时间'
        return dict(
            user_name = single.user.nickname,
            time = time,
            id = single.id
        )


"""
优化代码：由于赠送清单和心愿清单的逻辑类似，也就是MyGift类和MyWish类的是基本一样
，这里就将这两个类合并成一个基类为MyTrade"""
class MyTrade():
    def __init__(self,trade_of_mine,trade_count_dict):
        self.__trade_of_mine = trade_of_mine
        self.__trade_count_dict = trade_count_dict
        self.trade = self.__parse()

    def __parse(self):
        temp_trade = []
        for gift in self.__trade_of_mine:
            count = self.__trade_count_dict.get(gift.isbn,0)
            gift = {
                'trade_count':count,
                'book':gift.books,
                'id' :gift.id
            }
            temp_trade.append(gift)

        return temp_trade
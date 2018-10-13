# class MyWish():
#     def __init__(self,gifts_of_mine,wish_count_dict):
#         self.__gifts_of_mine = gifts_of_mine
#         self.__wish_count_dict = wish_count_dict
#         self.gifts = self.__parse()
#
#     def __parse(self):
#         temp_gifts = []
#         for gift in self.__gifts_of_mine:
#             count = self.__wish_count_dict.get(gift.isbn,0)
#             gift = {
#                 'wishes_count':count,
#                 'book':gift.books,
#                 'id' :gift.id
#             }
#             temp_gifts.append(gift)
#
#         return temp_gifts
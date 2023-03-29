import Bot.admin.Command
import Bot.admin.CallBack
import Bot.admin.WaitEvent
from aiogram import Dispatcher
from Bot import Command, Message, CallBack
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType

class Handler():
    def __init__(self, dp: Dispatcher):
        self.dp = dp

    def RegisterAdminEvent(self):
        self.dp.register_message_handler(Bot.admin.Command.admin, commands=['admin'], is_admin=True, state="*")
        self.dp.register_callback_query_handler(Bot.admin.Command.admin, lambda c: c.data == 'AShowAdminPanel', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.get_category, lambda c: c.data == 'AShowCategory', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.create_category, lambda c: c.data == 'ACreateNewCategory', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.open_category, lambda c: c.data.split('&')[0] == 'AOpenCategory', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.get_product, lambda c: c.data.split('&')[0] == 'AShowProduct', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.create_product, lambda c: c.data.split('&')[0] == 'ACreateNewProduct', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.edit_title_category, lambda c: c.data.split('&')[0] == 'AEditCategoryTitle', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.delete_category, lambda c: c.data.split('&')[0] == 'ADeleteCategory', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.open_product, lambda c: c.data.split('&')[0] == 'AOpenProduct', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.add_item, lambda c: c.data.split('&')[0] == 'AAddItemInProduct', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.set_image, lambda c: c.data.split('&')[0] == 'ASetImageProduct', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.delete_product, lambda c: c.data.split('&')[0] == 'ADeleteProduct', is_admin=True, state='*')
        self.dp.register_callback_query_handler(Bot.admin.CallBack.choose_content_type, lambda c: c.data.split('&')[0] == 'ACreateItemChooseContent', is_admin=True, state='*')

    def RegisterWaitEvent(self):
        self.dp.register_message_handler(Bot.admin.WaitEvent.create_category, state="WaitInputTitleNewCategory", content_types=[ContentType.TEXT])
        self.dp.register_message_handler(Bot.admin.WaitEvent.create_product, state="WaitInputTitleNewProduct", content_types=[ContentType.TEXT])
        self.dp.register_message_handler(Bot.admin.WaitEvent.input_description_product, state="WaitInputDescriptionNewProduct", content_types=[ContentType.TEXT])
        self.dp.register_message_handler(Bot.admin.WaitEvent.input_price_product, state="WaitInputPriceNewProduct", content_types=[ContentType.TEXT])
        self.dp.register_message_handler(Bot.admin.WaitEvent.edit_title_category, state="WaitInputEditTitleCategory", content_types=[ContentType.TEXT])
        self.dp.register_message_handler(Bot.admin.WaitEvent.upload_item, state="WaitUploadFileItem", content_types=[ContentType.DOCUMENT])
        self.dp.register_message_handler(Bot.admin.WaitEvent.upload_image, state="WaitUploadImageItem", content_types=[ContentType.PHOTO])
        self.dp.register_message_handler(Bot.admin.WaitEvent.input_amount_refill, state="WaitInputAmountRefill", content_types=[ContentType.TEXT])
        self.dp.register_message_handler(Bot.admin.WaitEvent.upload_item_text, state="WaitUploadTextItem", content_types=[ContentType.TEXT])

    def RegisterCommands(self):
        self.dp.register_message_handler(Command.start, commands=['start'], state="*")

    def RegisterTextMessage(self):
        self.dp.register_message_handler(Message.show_catalog, Text(equals=["📦 Купить"]), state="*")
        self.dp.register_message_handler(Message.show_profile, Text(equals=["🔒Профиль"]), state="*")

    def RegisterCallBack(self):
        self.dp.register_callback_query_handler(CallBack.open_category, lambda c: c.data.split('&')[0] == 'OpenCategory', state='*')
        self.dp.register_callback_query_handler(CallBack.open_product, lambda c: c.data.split('&')[0] == 'OpenProduct', state='*')
        self.dp.register_callback_query_handler(CallBack.buy_product, lambda c: c.data.split('&')[0] == 'BuyProduct', state='*')
        self.dp.register_callback_query_handler(CallBack.check_payment_, lambda c: c.data.split('&')[0] == 'CheckPayment', state='*')
        self.dp.register_callback_query_handler(CallBack.not_have_product, lambda c: c.data == 'NotHaveProduct', state='*')
        self.dp.register_callback_query_handler(CallBack.refill_balance, lambda c: c.data == 'RefillBalance', state='*')
        self.dp.register_callback_query_handler(Message.show_profile, lambda c: c.data == 'ShowProfile', state='*')
        self.dp.register_callback_query_handler(CallBack.ping, state="*")

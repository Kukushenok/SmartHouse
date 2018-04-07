# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters , CommandHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup , ReplyKeyboardRemove
import watson_developer_cloud
import os
import objects.Manager
import pygame
messager = {}
calling = {}

def main():
    print("Запускаем программу...")
    users = 0
    assistant = watson_developer_cloud.ConversationV1(
        username='d9a6b2ae-44fd-4cb4-9602-95a3cc357363',
        password='Rxs5YCzznkbY',
        version='2018-02-16'
    )
    def starting(bot, updater,user_data):
        if user_data.get("getted_started"):
            updater.message.reply_text('Не... Лень рассказывать заного функционал дома... Ааах, ну ладно, уговорил.\n'
                                       'Функционал дома:\n'
                                       'Всего 6 комнат: коридор, зал (кухня), бойлерная, ванная,большая и малая спальни.\n'
                                       'В них можно либо включить/выключить свет, либо установить температуру.\n')
        if not objects.Manager.Manager.getPassHandler().CheckOnWhitelist(updater["message"]["chat"]["username"]):
            updater.message.reply_text("Вас нет в белом списке, Вы не можете войти")
            return None
        user_data["attempts"] = int(objects.Manager.Manager.getConfig().get("maxAttemps"))
        user_data["getted_started"] = True
        user_data["pass_input"] = True
        print(updater["message"]["chat"]["username"] + " пытается войти в систему")
        updater.message.reply_text('Добро пожаловать в систему "Умный дом"! \n'
                                   'Мне можно задавать команды на "человеческом" языке! \n'
                                   'Функционал дома\n'
                                   'В доме 6 зон: коридор, зал (гостиная),спальня, детская, бойлерная и ванная.\n'
                                   'В них можно включить/выключить свет, установить температуру, поставить дом на охрану (включить сигнализацию).\n'
                                   'Для доступа к системе "Умный дом" необходимо иметь пароль. Если у Вас его нет - обратитесь к владельцу дома.\n'
                                   '\n'
                                   'Давайте начнём! Скажите мне пароль, и я впущу Вас :D')

    def chat_handler(bot, updater,user_data):
        global messager, context
        user_data["getted_started"] = True
        #print("Получаем из телеграмма: " + updater.message.text)
        if not objects.Manager.Manager.getPassHandler().CheckOnWhitelist(updater["message"]["chat"]["username"]):
            updater.message.reply_text("Вас нет в белом списке, Вы не можете войти")
            return None
        print("Отправляем Ватсону: " + updater.message.text)
        response = assistant.message(
            workspace_id='adcfa951-1a99-4127-bfbc-e09101075716',
            input={
                'text': updater.message.text
            },
            context=user_data.get("context",{})
        )
        print("Получаем из Ватсона: " + str(response))
        user_data["context"] = response['context']
        if response["intents"] and response["intents"][0]["intent"] == "cancel":
            updater.message.reply_text("Отменено.")
            user_data["calling"] = {}
            return None

        calling = user_data.get("calling",{})
        if user_data.get("logged_in"):
            calling["ready"] = False
            for output in response["output"]["text"]:
                #print("Отправляем телеграмму: "+output)
                updater.message.reply_text(output)
                if output[:3] == "Поп":
                    calling["ready"] = True
            if response["intents"]:
                if not calling.get("intent") or calling["intent"]["conf"]<response["intents"][0]["confidence"]:
                    calling["intent"] = {"type":response["intents"][0]["intent"],"conf":response["intents"][0]["confidence"]}
            if response["entities"] and calling.get("intent"):
                if not calling.get("params"):
                    calling["params"] = {}
                    for entity in response["entities"]:
                        calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
                else:
                    for entity in response["entities"]:
                        if not calling["params"].get(entity["entity"]):
                            calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
                        elif calling["params"][entity["entity"]]["conf"]<entity["confidence"]:
                            calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
            if calling["intent"]["type"] == "show_state":
                bot.send_photo(chat_id=updater.message.chat.id,
                               photo=open(os.path.join(os.getcwd(), "house.png"), 'rb'))
            if calling["intent"]["type"] == "log_out":
                user_data["logged_in"] = False
                objects.Manager.Manager.getUsers().remove_user(updater["message"]["chat"]["username"])
                user_data["context"] = {}
                return None
            print(response)
            fast_callback = objects.Manager.Manager.getHouse().call(calling,updater["message"]["chat"]["username"])
            if fast_callback == "Busy": updater.message.reply_text("Простите, но данный запрос был отклонён из-за посторонней операцией над этой комнатой")
            elif fast_callback == "So hot": updater.message.reply_text("Отклонено в связи c безопасностью, слишком горячо.\n"
                                                                       "Температура должна быть выше 10 градусов и ниже 40 градусов")
            elif fast_callback == "So cold": updater.message.reply_text("Отклонено в связи с безопасностью, слишком холодно.\n"
                                                                        "Температура должна быть выше 10 градусов и ниже 40 градусов")
            elif fast_callback: updater.message.reply_text("Отклонено. Причина: "+fast_callback)
            if calling["ready"]: calling = {}
            user_data["calling"] = calling
        else:
            if response["intents"] and response["intents"][0]["intent"] == "log_in":
                user_data["attempts"] = int(objects.Manager.Manager.getConfig().get("maxAttemps"))
                user_data["pass_input"] = True
                print(updater["message"]["chat"]["username"] + " пытается войти в систему")
                #print("Отправляем телеграмму: Хорошо! Напиши пароль")
                updater.message.reply_text("Хорошо! Скажите пароль")
            elif not response["intents"]:
                if objects.Manager.Manager.getPassHandler().LogIn(updater.message.text):
                    user_data["logged_in"] = True
                    user_data["pass_input"] = False
                    #print("Отправляем телеграмму: Вы вошли в систему!")
                    updater.message.reply_text("Вы вошли в систему!")
                    print(updater["message"]["chat"]["username"] + " вошёл в систему")
                    objects.Manager.Manager.getUsers().add_user(updater["message"]["chat"]["username"],updater)
                    return None
                elif response["intents"] and response["intents"][0]["intent"] == "cancel":
                    user_data["pass_input"] = False
                    updater.message.reply_text("ОК.")
                elif user_data.get("attempts") and user_data["attempts"] > 1 and user_data["pass_input"]:
                    user_data["attempts"] -=1
                    #print("Отправляем телеграмму: "+ "Неверный пароль! У вас осталось до иcключения из белого списка попыток: " + str(
                    #    user_data["attempts"]))
                    updater.message.reply_text("Неверный пароль! У вас осталось до иcключения из белого списка попыток: "+str(user_data["attempts"]))
                elif user_data["pass_input"]:
                    objects.Manager.Manager.getPassHandler().whitelist.pop(objects.Manager.Manager.getPassHandler().whitelist.index(updater["message"]["chat"]["username"]))
                    whitelist = objects.Manager.Manager.getConfig().getAsList("whitelist")
                    whitelist.pop(whitelist.index(updater["message"]["chat"]["username"]))
                    objects.Manager.Manager.getConfig().config["SETTINGS"]["whitelist"] = ",".join(whitelist)
                    objects.Manager.Manager.getConfig().SaveChanges()
                    #print("Отправляем телеграмму: Неверный пароль! Вы были удалены из белого списка...")
                    updater.message.reply_text("Неверный пароль! Вы были удалены из белого списка...")
                    print("ВНИМАНИЕ. "+updater["message"]["chat"]["username"]+" был удалён из белого списка за сомнительное количество попыток входа.")



    updater = Updater(objects.Manager.Manager.getConfig().get("botKey"))

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,chat_handler,pass_user_data=True))
    dp.add_handler(CommandHandler("start",starting,pass_user_data=True))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    #updater.idle()
    size = width, height = 800,600
    screen = pygame.display.set_mode(size,pygame.DOUBLEBUF)
    running = True
    fps = 2
    clock = pygame.time.Clock()
    response = assistant.message(
        workspace_id="adcfa951-1a99-4127-bfbc-e09101075716",
        input={
            'text': ''
        }
    )
    print("ОК!")
    while running:
        callback = objects.Manager.Manager.getHouse().draw(1/fps)
        screen.blit(callback[0],(0,0))
        objects.Manager.Manager.getUsers().render(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                updater.stop()
                exit(0)
        clock.tick(fps)


if __name__ == "__main__":
    main()
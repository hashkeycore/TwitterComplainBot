from TwitterBot import TwitterBot
from TwitterBot import SpeedBot


speed_bot = SpeedBot()
speed_bot.get_speed_page()
speed_bot.start_speed_test()
speed = speed_bot.get_speed_values()
speed_bot.quit()
if speed.is_low():
    bot = TwitterBot()
    bot.get_twitter_login_page()
    bot.insert_username()
    bot.insert_phone_number()
    bot.insert_password()
    bot.tweet(speed)
    bot.quit()




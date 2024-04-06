from datetime import datetime, timedelta
from math import exp
import math
import discord
from discord.ext import commands
from Dao.UserDao import UserDao
from Entities.User import User
import logging
from Leveling import Leveling

role_level_1 = "Level One"
role_level_2 = "Level Two"
role_level_3 = "Level Three"
role_level_4 = "Level Four"
role_level_5 = "Level Five"
role_level_6 = "Level Six"
role_level_7 = "Level Seven"
role_level_8 = "Level Eight"
role_level_9 = "Level Nine"
role_level_10 = "Level Ten"

logging.basicConfig(filename='/home/acosmic/Dev/acosmibot/logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class On_Message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        level_up_channel = self.bot.get_channel(1209288743912218644)
        daily_reward_channel = self.bot.get_channel(1224561092919951452)
        
        if not message.author.bot:
            logging.info(f'Message from {message.author}: {message.channel.name} - {message.content}')
            role1 = discord.utils.get(message.guild.roles, name=role_level_1)
            role2 = discord.utils.get(message.guild.roles, name=role_level_2)
            role3 = discord.utils.get(message.guild.roles, name=role_level_3)
            role4 = discord.utils.get(message.guild.roles, name=role_level_4)
            role5 = discord.utils.get(message.guild.roles, name=role_level_5)
            role6 = discord.utils.get(message.guild.roles, name=role_level_6)
            role7 = discord.utils.get(message.guild.roles, name=role_level_7)
            role8 = discord.utils.get(message.guild.roles, name=role_level_8)
            role9 = discord.utils.get(message.guild.roles, name=role_level_9)
            role10 = discord.utils.get(message.guild.roles, name=role_level_10)

            dao = UserDao()

            current_user = dao.get_user(message.author.id)
            logging.info(f'{str(current_user.discord_username)} grabbed from get_user(id) in on_message()')
            if current_user is not None:

                exp_gain = 2 + (current_user.streak * 0.05)
                current_user.exp += exp_gain
                current_user.exp_gained += exp_gain
                current_user.messages_sent += 1
                current_user.last_active = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f'CURRENT TIME = {current_user.last_active}')
                

                # if current_user.exp < 100:
                #     role = role1
                #     current_user.level = 1
                # elif current_user.exp >= 100 and current_user.exp < 200:
                #     role = role2
                #     current_user.level = 2
                # elif current_user.exp >= 200 and current_user.exp < 300:
                #     role = role3
                #     current_user.level = 3
                # elif current_user.exp >= 300 and current_user.exp < 400:
                #     role = role4
                #     current_user.level = 4
                # elif current_user.exp >= 400 and current_user.exp < 500:
                #     role = role5
                #     current_user.level = 5
                # elif current_user.exp >= 500 and current_user.exp < 600:
                #     role = role6
                #     current_user.level = 6
                # elif current_user.exp >= 600 and current_user.exp < 700:
                #     role = role7
                #     current_user.level = 7
                # elif current_user.exp >= 700 and current_user.exp < 800:
                #     role = role8
                #     current_user.level = 8
                # elif current_user.exp >= 800 and current_user.exp < 900:
                #     role = role9
                #     current_user.level = 9
                # elif current_user.exp >= 900:
                #     role = role10
                #     current_user.level = 10

                # CHECK IF - DAILY REWARD
                if current_user.daily == 0:
                    logging.info(f"{current_user.discord_username} - COMPLETED DAILY REWARD")

                    # Check if last_daily was yesterday
                    
                    today = datetime.now().date()
                    if current_user.last_daily is None:
                        current_user.streak = 0
                    else:
                        if current_user.last_daily.date() == today - timedelta(days=1):
                            # Increment streak
                            current_user.streak += 1
                            logging.info(f"{current_user.discord_username} - STREAK INCREMENTED TO {current_user.streak}")
                        elif current_user.last_daily.date() < today - timedelta(days=1):
                            # Reset streak
                            current_user.streak = 1
                            logging.info(f"{current_user.discord_username} - STREAK RESET TO {current_user.streak}")


                    # CALCULATE DAILY REWARD
                    base_daily = 100
                    streak = current_user.streak if current_user.streak < 10 else 10
                    base_bonus_multiplier = 0.05
                    streak_bonus_percentage = streak * base_bonus_multiplier
                    streak_bonus = math.ceil(base_daily * streak_bonus_percentage)
                    calculated_daily_reward = base_daily + streak_bonus
                    current_user.currency += calculated_daily_reward



                    # Set daily and last_daily
                    current_user.daily = 1
                    current_user.last_daily = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 


                    streak = current_user.streak if current_user.streak < 10 else 10
                    if streak > 0:
                        await daily_reward_channel.send(f'## {message.author.mention} You have collected your daily reward - {calculated_daily_reward} Credits! 100 + {streak_bonus} from {streak}x Streak! <:PepeCelebrate:1165105393362555021>')
                    else:
                        await daily_reward_channel.send(f'## {message.author.mention} You have collected your daily reward - 100 Credits! <:PepeCelebrate:1165105393362555021>')

                else:
                    logging.info(f"{current_user.discord_username} HAS ALREADY COMPLETED THE DAILY")


                
                # CHECK IF - LEVELING UP
                lvl = Leveling()
                new_level = lvl.calc_level(current_user.exp)
                if new_level > current_user.level:
                    
                    # CALCULATE LEVEL UP REWARD
                    base_level_up_reward = 1000
                    streak = current_user.streak if current_user.streak < 10 else 10
                    base_bonus_multiplier = 0.05
                    streak_bonus_percentage = streak * base_bonus_multiplier
                    streak_bonus = math.ceil(base_level_up_reward * streak_bonus_percentage)
                    calculated_level_reward = base_level_up_reward + streak_bonus

                    if streak > 0:
                        await level_up_channel.send(f'## {message.author.mention} LEVEL UP! You have reached level {new_level}! Gained {calculated_level_reward} Credits! 1,000 + {streak_bonus} from {streak}x Streak! <:FeelsGroovy:1199735360616407041>')
                    else:
                        await level_up_channel.send(f'## {message.author.mention} LEVEL UP! You have reached level {new_level}! Gained {calculated_level_reward} Credits! <:FeelsGroovy:1199735360616407041>')
                
                current_user.level = new_level

                
                
                try:
                    dao.update_user(current_user)
                    logging.info(f'{str(message.author)} updated in database in on_message()')
                except Exception as e: 
                    logging.error(f'Error updating {message.author} to the database: {e}')
                # await message.author.add_roles(role)

            else:
                return
                # join_date = message.author.joined_at

                # # Convert join_date to a format suitable for database insertion (e.g., as a string)
                # formatted_join_date = join_date.strftime("%Y-%m-%d %H:%M:%S")

                # new_user_data = {
                # 'id': message.author.id,
                # 'discord_username': str(message.author),
                # 'level': 1,
                # 'streak': 0,
                # 'exp': 0,
                # 'exp_gained': 0,
                # 'exp_lost': 0,
                # 'currency': 0,
                # 'messages_sent': 1,
                # 'reactions_sent': 0,
                # 'created': formatted_join_date,
                # 'last_active': formatted_join_date,
                # 'daily': 0

                # }
                # new_user = User(**new_user_data)
                # logging.info(f'{message.author} added to the database. - on_message() - DISABLED CURRENTLY nothing added to db')
                # # try:
                # #     # dao.add_user(new_user)
                # #     logging.info(f'{message.author} added to the database. - on_message() - DISABLED CURRENTLY')
                # # except Exception as e:
                # #     logging.error(f'on_message() - Error adding user to the database: {e}')


async def setup(bot: commands.Bot):
    await bot.add_cog(On_Message(bot))
        




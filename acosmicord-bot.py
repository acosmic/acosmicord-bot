#! /usr/bin/python3.8
import discord
from discord.ext import commands
from discord import Message, app_commands
from database import Database
from Entities.User import User
from datetime import datetime
import logging
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_name = os.getenv('db_name')

client_id = os.getenv('client_id')
client_secret =  os.getenv('client_secret')
TOKEN = os.getenv('TOKEN')
MY_GUILD = discord.Object(id=int(os.getenv('MY_GUILD')))

# Configure the logging settings
logging.basicConfig(filename='/root/dev/acosmicord-bot/logs/logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    logging.info(f'Logged on as {bot.user}!')
    await bot.tree.sync(guild=MY_GUILD)

@bot.event 
async def on_message(message):
    
    if not message.author.bot:
        logging.info(f'Message from {message.author}: {message.content}')

        role1 = discord.utils.get(message.guild.roles, name=role_level_1)
        role2 = discord.utils.get(message.guild.roles, name=role_level_2)
        role3 = discord.utils.get(message.guild.roles, name=role_level_3)
        role4 = discord.utils.get(message.guild.roles, name=role_level_4)
        role5 = discord.utils.get(message.guild.roles, name=role_level_5)
        role6 = discord.utils.get(message.guild.roles, name=role_level_7)
        role7 = discord.utils.get(message.guild.roles, name=role_level_1)
        role8 = discord.utils.get(message.guild.roles, name=role_level_8)
        role9 = discord.utils.get(message.guild.roles, name=role_level_9)
        role10 = discord.utils.get(message.guild.roles, name=role_level_10)


        db = Database(db_host, db_user, db_password, db_name)
        current_user = db.get_user(str(message.author))
        if current_user is not None:
            current_user.exp += 2
            current_user.exp_gained += 2
            current_user.messages_sent += 1
            current_user.last_active = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_level = current_user.level

            if current_user.exp < 100:
                role = role1
                current_user.level = 1

            elif current_user.exp >= 100 and current_user.exp < 200:
                role = role2
                current_user.level = 2

            elif current_user.exp >= 200 and current_user.exp < 300:
                role = role3
                current_user.level = 3

            elif current_user.exp >= 300 and current_user.exp < 400:
                role = role4
                current_user.level = 4

            elif current_user.exp >= 400 and current_user.exp < 500:
                role = role5
                current_user.level = 5

            elif current_user.exp >= 500 and current_user.exp < 600:
                role = role6
                current_user.level = 6

            elif current_user.exp >= 600 and current_user.exp < 700:
                role = role7
                current_user.level = 7

            elif current_user.exp >= 700 and current_user.exp < 800:
                role = role8
                current_user.level = 8

            elif current_user.exp >= 800 and current_user.exp < 900:
                role = role9
                current_user.level = 9

            elif current_user.exp >= 900:
                role = role10
                current_user.level = 10
            

            if current_user.level > current_level:
                await message.reply(f'GG! You have been promoted up to {str(role)}!')
                
            
            db.modify_user(current_user)
            await message.author.add_roles(role)
        else:
            join_date = message.author.joined_at

            # Convert join_date to a format suitable for database insertion (e.g., as a string)
            formatted_join_date = join_date.strftime("%Y-%m-%d %H:%M:%S")

            new_user_data = {
            'id': 0,
            'discord_username': str(message.author),
            'level': 1,
            'streak': 0,
            'exp': 0,
            'exp_gained': 0,
            'exp_lost': 0,
            'messages_sent': 1,
            'reactions_sent': 0,
            'created': formatted_join_date,
            'last_active': formatted_join_date
            }
            new_user = User(**new_user_data)
            try:
                db.add_new_user(new_user)
                logging.info(f'{message.author} added to the database.')
            except Exception as e:
                logging.error(f'Error adding user to the database: {e}')


@bot.event 
async def on_raw_reaction_add(payload):

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    emoji = payload.emoji

    discord_username = user.name
    db = Database(db_host, db_user, db_password, db_name)
    current_user=db.get_user(discord_username)

    current_user.reactions_sent += 1

    db.modify_user(current_user)
    logging.info(f"{discord_username} added {emoji} to {message.author}'s message .")
    logging.info(f"incremented and updated db reactions_sent for {discord_username}")
    

# This function adds new users to the database if they don't already exist and assigns the lvl1 role
@bot.event
async def on_member_join(member):
    
    
    role = discord.utils.get(member.guild.roles, name=role_level_1)
    join_date = member.joined_at

    # Convert join_date to a format suitable for database insertion (e.g., as a string)
    formatted_join_date = join_date.strftime("%Y-%m-%d %H:%M:%S")

    member_data = {
    'id': 0,
    'discord_username': member.name,
    'level': 1,
    'streak': 0,
    'exp': 0,
    'exp_gained': 0,
    'exp_lost': 0,
    'messages_sent': 0,
    'reactions_sent': 0,
    'created': formatted_join_date,
    'last_active': formatted_join_date
    }
    new_user = User(**member_data)

    # Check if the user already exists
    check_user_sql = "SELECT ID FROM Users WHERE DISCORD_USERNAME = %s"
    db = Database(db_host, db_user, db_password, db_name)
    db.mycursor.execute(check_user_sql, (new_user.discord_username,))
    existing_user = db.mycursor.fetchone()

    if existing_user is None:
        await member.add_roles(role)
        logging.info(f'Auto assigned {role} role to {member}')

        # add new user to database
        db.add_new_user(new_user)
        logging.info(f'{new_user.discord_username} added to the database.')
    else:
        logging.info(f'{new_user.discord_username} already exists, so was not added again.')

@bot.tree.command(name = "rank", description = "returns your rank based on current EXP.", guild=MY_GUILD) 
async def rank_command(interaction: discord.Interaction):
    discord_username_to_check = interaction.user.name
    db = Database(db_host, db_user, db_password, db_name)
    user_rank = db.get_user_rank(discord_username_to_check)
    

    current_user = db.get_user(discord_username_to_check)
    current_user_exp = current_user.exp
    current_user_messages_sent = current_user.messages_sent
    current_user_reactions_sent = current_user.reactions_sent
    current_user_level = current_user.level



    if user_rank is not None:
        embed = discord.Embed(
        title=f"{discord_username_to_check}'s Stats",
        description=(
        f"Ranked #{user_rank[-1]}\n"
        f"Current Level: {current_user_level}\n"
        f"Current EXP: {current_user_exp}\n"
        f"Total Messages: {current_user_messages_sent}\n"
        f"Total Reactions: {current_user_reactions_sent}\n"
        ),
        color=interaction.user.color)
        # color=discord.Color.dark_purple())  # You can choose a different color
        embed.set_thumbnail(url=interaction.user.avatar)

        await interaction.response.send_message(embed=embed)

        # await interaction.response.send_message(\
        #     f"{discord_username_to_check} is ranked #{user_rank[-1]}. "\
        #     f"Currently has {current_user_exp} EXP with {current_user_messages_sent} "\
        #     f"total messages and {current_user_reactions_sent} total reactions sent. Noice!")
    else:
        logging.info(f"The user with Discord username {discord_username_to_check} was not found in the database.")
        
        role = discord.utils.get(interaction.user.guild.roles, name=role_level_1)
        await interaction.user.add_roles(role)
        join_date = interaction.user.joined_at

        # Convert join_date to a format suitable for database insertion (e.g., as a string)
        formatted_join_date = join_date.strftime("%Y-%m-%d %H:%M:%S")

        user_data = {
        'id': 0,
        'discord_username': str(interaction.user.name),
        'level': 1,
        'streak': 0,
        'exp': 0,
        'exp_gained': 0,
        'exp_lost': 0,
        'messages_sent': 1,
        'reactions_sent': 0,
        'created': formatted_join_date,
        'last_active': formatted_join_date 
        }

        new_user = User(**user_data)
        db.add_new_user(new_user)


        logging.info(f'{new_user.discord_username} added to the database.')
        await interaction.response.send_message(f'{discord_username_to_check} was not found in the database. {new_user.discord_username} added to the database.')
    
    
    db.close_connection()
    # await interaction.response.send_message("Hello!") 
    logging.info(f"{interaction.user.name} used /rank command")
    

if __name__ == "__main__":
    bot.run(TOKEN)
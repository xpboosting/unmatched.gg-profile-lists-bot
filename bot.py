import os
import discord
import mysql.connector

intents = discord.Intents.default()
intents.members = False
intents.message_content = True

db = mysql.connector.connect(
  host='host',
  user='user',
  password='password',
  database='db'
)

client = discord.Client(intents=intents)

# Channel and message IDs
LIST_CHANNEL_ID = None  # Replace with your channel ID
LIST_MESSAGE_ID = None

# Get all profiles from the database
def get_all_profiles():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM unmatched_links")
    rows = cursor.fetchall()
    profiles = []
    for row in rows:
        profiles.append({'id': row[0], 'user_id': row[1], 'name': row[2], 'link': row[3]})
    return profiles

# Create an embed with the list of profiles
def create_embed(profiles):
    embed = discord.Embed(title="List of Profiles:")
    for profile in profiles:
        embed.add_field(name=profile['name'], value=profile['link'], inline=False)
    return embed

@client.event
async def on_message(message):
    global LIST_MESSAGE_ID

    if message.author == client.user:
        return

    if message.content.startswith('!add'):
        # Check if user has "admin" role
        if not discord.utils.get(message.author.roles, name="Admin"):
            await message.channel.send("You are not admin! :detective:")
            return
        # Parse the command
        parts = message.content.split()
        if len(parts) == 3 and parts[1].startswith('https://unmatched.gg/user/'):
            # Extract the profile link and name from the command
            link = parts[1]
            name = parts[2]

            # Insert the link and name into the database
            cursor = db.cursor()
            sql = "INSERT INTO unmatched_links (user_id, name, link) VALUES (%s, %s, %s)"
            values = (message.author.id, name, link)
            cursor.execute(sql, values)
            db.commit()
            await message.channel.send("Profile added successfully!")

            # Update the list message if it already exists
            if LIST_MESSAGE_ID is not None:
                channel = client.get_channel(LIST_CHANNEL_ID)
                list_message = await channel.fetch_message(LIST_MESSAGE_ID)
                profiles = get_all_profiles()
                embed = create_embed(profiles)
                await list_message.edit(embed=embed)
        else:
            await message.channel.send("Invalid command format. Usage: !add profile_link name")

    elif message.content.startswith('!list'):
              # Check if user has "admin" role
        if not discord.utils.get(message.author.roles, name="Admin"):
            await message.channel.send("You are not admin! :detective:")
            return
        # Get all the profiles from the database
        profiles = get_all_profiles()

        # Create an embed with the list of profiles
        embed = create_embed(profiles)

        # Send the embed to the channel
        channel = message.channel
        list_message = await channel.send(embed=embed)

        # Save the message ID for future edits
        LIST_MESSAGE_ID = list_message.id
    elif message.content.startswith('!search'):
        # Parse the command
        parts = message.content.split()
        if len(parts) == 2:
            # Extract the search query from the command
            search_query = parts[1]

            # Search for profiles in the database
            cursor = db.cursor()
            sql = "SELECT * FROM unmatched_links WHERE name LIKE %s"
            values = ('%' + search_query + '%',)
            cursor.execute(sql, values)
            rows = cursor.fetchall()

            # Check if any matching profiles were found
            if len(rows) > 0:
                # Create an embed with the list of profiles
                profiles = [{'id': row[0], 'user_id': row[1], 'name': row[2], 'link': row[3]} for row in rows]
                embed = create_embed(profiles)

                # Send the embed to the channel
                channel = message.channel
                list_message = await channel.send(embed=embed)

                # Save the message ID for future edits
                LIST_MESSAGE_ID = list_message.id
            else:
                await message.channel.send("No profiles found matching username")
        else:
            await message.channel.send("Invalid command format. Usage: !search username")

client.run('token')

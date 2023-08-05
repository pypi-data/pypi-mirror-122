# Disrank2
Simple lib to make good looking discord profile card. For any bug report, please come on my discord bot's support server : https://discord.gg/7DW9T5prRM

# Usage
```py
from disrank2.generator import Generator

args = {
	'bg_image' : '', # Background image link 
	'profile_image' : '', # User profile picture link
	'level' : 1, # User current level 
	'current_xp' : 0, # Current level minimum xp 
	'user_xp' : 10, # User current xp
	'next_xp' : 100, # xp required for next level
	'user_position' : 1, # User position in leaderboard
	'user_name' : 'Name#0001', # user name with descriminator 
	'user_status' : 'online', # User status eg. online, offline, idle, streaming, dnd
	'text_color' : '#ff7300', # Text color un HEX
}

image = Generator().generate_profile(**args)

# In a discord command
file = discord.File(fp=image, filename='image.png')
await ctx.send(file=file)
```


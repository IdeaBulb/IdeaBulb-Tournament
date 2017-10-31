import discord
import asyncio
import math

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
prefix = '-/'
check = 'I agree to the IdeaBulb terms and conditions and will adhere to the rules. In addition to that, I will also engage in learning by creating during my time on this server.'
game_staff_vote = []
game_people_vote = []

@client.event
async def on_message(message):
    if message.content == prefix + 'help':
        help = prefix + 'help: Shows this screen.' + '\n' + prefix + 'request_conference: Requests a conference with the staff.' + '\n' + prefix + 'request_game [GAME] [DESCRIPTION] [PROPOSED_ROLE_COLOR] [LINK]: Requests a game to be appended to the server list. (Link is optional but the proposed role color should be in hexadecimal like 0xFFFFFF.)'
        help_embed = discord.Embed(title='IdeaBulb Tourney Bot Help', description=help, colour=0xFFFFFF)
        await client.send_message(message.channel, embed=help_embed)
    elif message.content == check:
        await client.add_roles(message.author, discord.utils.get(message.server.roles, name='Verified'))
    elif message.content == prefix + 'request_conference':
        await client.add_roles(message.author, discord.utils.get(message.server.roles, name='Conference Request'))
        await client.send_message(discord.utils.get(message.server.channels, name='conference-request'), discord.utils.get(message.server.roles, name='Staff').mention + ' A conference has been requested by ' + message.author.name + '.')
    elif message.content.startswith(prefix + 'request_game'):
        game_param = message.content.split(' ')
        game_request_embed = discord.Embed(title=game_param[1]+' requested by '+message.author.name, description='Description: '+game_param[2]+'\n'+'Link: '+game_param[4], colour=int(game_param[3], 16))
        await client.send_message(discord.utils.get(message.server.channels, name='conference'), discord.utils.get(message.server.roles, name='Staff').mention + ' A new game addition has been requested for this server:')
        game_request_to_staff = await client.send_message(discord.utils.get(message.server.channels, name='conference'), embed=game_request_embed)
        game_staff_vote.append([game_request_to_staff, game_request_embed])
        await client.add_reaction(game_request_to_staff, '\U0001F44D')
        await client.add_reaction(game_request_to_staff, '\U0001F44E')
        await client.send_message(discord.utils.get(message.server.channels, name='conference'), 'Vote in support or in opposition to the new addition. (:thumbsup: = support and :thumbsdown: = oppose)')
        await client.send_message(message.channel, 'Your game has been requested. The staff will vote in support or in opposition to the game. If there is a majority support among staff, the vote will be passed on to the server members and a majority support among the members will allow the game to be integrated into this server.')
    elif message.content.startswith(prefix + 'purge'):
        await client.purge_from(message.channel, limit=int(message.content.split(' ')[1]), check=None, before=None, after=None, around=None)
    elif message.content.startswith(prefix):
        await client.send_message(message.channel, 'That is not a command. See `-/help` for more information.')
        
@client.event
async def on_member_join(member):
    await client.send_message(discord.utils.get(member.server.channels, name='station'), 'Welcome to the *IdeaBulb Tournament Server*! ' + member.mention + '\n\nRead the ' + discord.utils.get(member.server.channels, name='rules').mention + ' and ' + discord.utils.get(member.server.channels, name='information').mention + ' channels. Once you have done so, type (or copy) `' + check + '` \n\nIn doing so you will be verified and will be able to proceed to the main area of the server.')        

@client.event
async def on_reaction_add(reaction, user):
    staff = []
    """for i in range(len(reaction.message.server.members)):
        for j in range(len(reaction.message.server.members[i].roles)):
            if reaction.message.server.members[i].roles[j].name == 'Staff':
               staff.append(reaction.message.server.members[i])"""
    for i in range(len(game_staff_vote)):
        # discord.utils.get(reaction.message.server.roles, name='Staff').users
        if reaction.message.reactions[0].count - 1 > math.floor(len(staff)) and reaction.message.id == game_staff_vote[i][0].id:
            await client.send_message(discord.utils.get(reaction.message.server.channels, name='announcements'), discord.utils.get(reaction.message.server.roles, name='@everyone').name + ' A new game addition has been requested for this server:')
            game_request_to_people = await client.send_message(discord.utils.get(reaction.message.server.channels, name='announcements'), embed=game_staff_vote[i][1])
            game_people_vote.append(game_request_to_people)
            await client.add_reaction(game_request_to_people, '\U0001F44D')
            await client.add_reaction(game_request_to_people, '\U0001F44E')
            await client.send_message(discord.utils.get(reaction.message.server.channels, name='announcements'), 'Vote in support or in opposition to the new addition. (:thumbsup: = support and :thumbsdown: = oppose)')
            # del game_staff_vote[i]
        if reaction.message.reactions[1].count - 1 > math.floor(len(staff)) and reaction.message.id == game_staff_vote[i][0].id:
            del game_staff_vote[i]


client.run('IdeaBulb Tournament Bot Token')

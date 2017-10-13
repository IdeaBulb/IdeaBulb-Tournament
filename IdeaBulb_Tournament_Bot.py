import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
prefix = '-/'
check = 'I agree to the IdeaBulb terms and conditions and will adhere to the rules. In addition to that, I will also engage in learning by creating during my time on this server.'

@client.event
async def on_message(message):
    if message.content == prefix + 'help':
        help = prefix + 'help: Shows this screen.' + '\n' + prefix + 'request_conference: Requests a conference with the staff.'
        em = discord.Embed(title='IdeaBulb Tourney Bot Help', description = help, colour=0xFFFFFF)
        await client.send_message(message.channel, embed=em)
    elif message.content == check:
        await client.add_roles(message.author, discord.utils.get(message.server.roles, name='Verified'))
    elif message.content == prefix + 'request_conference':
        await client.add_roles(message.author, discord.utils.get(message.server.roles, name='Conference Request'))
        # Notify the staff that a conference has been requested.
    elif message.content.startswith(prefix):
        await client.send_message(message.channel, 'That is not a command. See `-/help` for more information.')
        
@client.event
async def on_member_join(member):
    await client.send_message(discord.utils.get(member.server.channels, name='station'), 'Welcome to the *IdeaBulb Tournament Server*! ' + member.mention + '\n\nRead the ' + discord.utils.get(member.server.channels, name='rules').mention + ' and ' + discord.utils.get(member.server.channels, name='information').mention + ' channels. Once you have done so, type (or copy) `' + check + '` \n\nIn doing so you will be verified and will be able to proceed to the main area of the server.')        


client.run('IdeaBulb Tournament Bot Token')

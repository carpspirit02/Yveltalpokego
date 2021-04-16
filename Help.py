import discord
import time
import json
import os
import asyncio
import asyncpg
from discord.ext import commands

emoji = '\N{Heavy Check Mark}'

async def get_prefix(self, message):
    # retrieve an individual connection from our pool, defined later
    async with self.client.pool.acquire() as connection:
        # create a transaction for that connection
        async with connection.transaction():
            try:
                search = await connection.fetchval("SELECT prefix FROM prefixes WHERE guildid = "+str(message.guild.id)+" ;")
            except:
                return '%'
            else:
                return search

async def get_delete(self, message):
    # retrieve an individual connection from our pool, defined later
    async with self.client.pool.acquire() as connection:
        # create a transaction for that connection
        async with connection.transaction():
            try:
                search = await connection.fetchval("SELECT delete FROM deletion WHERE guildid = "+str(message.guild.id)+" ;")
            except:
                return 'False'
            else:
                return search

async def guildhostchannel(self, ctx):
    # retrieve an individual connection from our pool, defined later
    async with self.client.pool.acquire() as connection:
        # create a transaction for that connection
        async with connection.transaction():
            channeltosend = await connection.fetchval("SELECT guildchannelid FROM guildhostchannel WHERE guildid = '"+str(ctx.guild.id)+"' ;")
            return channeltosend

def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help online.')

    # Commands
    @commands.Cog.listener()#(name='help', help='Displays further explaination for commands')
    async def on_message(self, message):
    #async def help (self, ctx):
        if str(message.author) == self.client.user:
            return

        if message.author.bot:
            return

        if message.content.startswith("<>help"):
            prefix = await get_prefix(self, message)
            if message.channel.type is discord.ChannelType.private:
                responce = message.content
                content = responce.split()
                try:
                    content[1]
                except:
                    help = discord.Embed(title="Nexus-Z Commandes", description="", color=0x2962FF) #name="", value="", inline=False
                    help.add_field(name="Use `<>help [command]` pour plus d'informations sur une commande", value="\u200B", inline=False)
                    help.add_field(name="__**Pokemon SW/SH:**__", value="**catch\npokedex\nnatures\nball\nden\nsprite\nhost\nconfig**", inline=False)
                    help.add_field(name="__**Pokemon Go:**__", value="**godex\ngopvp\ngorocket\ngohundo\ngopure\ngotohome\ngosearchterms**", inline=False)
                    help.add_field(name="__**Autres:**__", value="**fc\ninfo\nnexusz?\naddcommand\nfreepokemon\nping**", inline=False)
                    help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")

                    candelete = await get_delete(self, message)
                    if candelete == "True":
                        await message.delete()
                    await message.channel.send(embed = help)
                else:
                    if content[1].lower() == "catch":
                        help = discord.Embed(title="Aide Capture", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"catch (form) [pokemon](*) (ball)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Retourne les taux de capture du Pokémon", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"catch pikachu`\n`"+prefix+"catch piakchu*`\n`"+prefix+"catch alolan dugtrio`\n`"+prefix+"catch galarian meowth`\n`"+prefix+"catch gmax/gigantamax charizard`\n`"+prefix+"catch pikachu ultra/ultra ball`")
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "pokedex":
                        help = discord.Embed(title="Aide Pokedex", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"pokedex (form) [pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie les informations d'entrée Pokedex sur un Pokémon\nNotes: Les Pokémon avec des formes alternatives peuvent être trouvés dans leur entrée d'origine (i.e: `"+prefix+ "pokedex kyogre` inclura également son Primal.)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"pokedex pikachu`\n`"+prefix+"pokedex pikachu*`\n`"+prefix+"pokedex alolan dugtrio`\n`"+prefix+"pokedex galarian meowth`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "natures":
                        help = discord.Embed(title="Aide Nature", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"natures`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie une chart avec toutes les natures et leurs effets sur les statistiques Pokémon", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"natures`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "ball":
                        help = discord.Embed(title="Aide Ball", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"ball [ball_type]`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie les informations d'une Poke-ball", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"ball ultra`\n`"+prefix+"ball ultra ball`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "den":
                        help = discord.Embed(title="Aide Den", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"den [den#/pokemon(*)]`\n\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Recherche de repaire par numéro ou Pokémon\n\nNote: Les formes de Galar sont recherchées par leurs noms de forme régulière", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"den 14`\n`"+prefix+"den meowth`\n`"+prefix+"den meowth*`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "sprite":
                        help = discord.Embed(title="Aide Sprite", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"sprite [Pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie un sprite Home du Pokémon nommé", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"sprite zygarde`\n`"+prefix+"sprite ash greninja`\n`"+prefix+"sprite ash greninja*`\n`"+prefix+"sprite dawn wings necrozma`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "move":
                        help = discord.Embed(title="Aide Attaque", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"move [move_name]`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations sur une attaque Pokémon (Toute les attaques disponibles dans Gen 8)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"move protect`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "host":
                        help = discord.Embed(title="Aide Host", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"host`", inline=False)
                        help.add_field(name="Description Commande:", value="Permet de configurer et d'incorporer / l'hôte de message à envoyer à un canal désigné par le propriétaire du serveur. (si un est défini)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"host`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "config":
                        help = discord.Embed(title="Aide Configuration", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"config`", inline=False)
                        help.add_field(name="Description Commande:", value="Permet au propriétaire de voir les paramètres actuels de ce bot.", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"config`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "godex":
                        help = discord.Embed(title="Aide PokemonGo Dex", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"godex (form) [Pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations sur Pokemon Go Pokedex", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"godex charizard`\n`"+prefix+"godex charizard*`\n`"+prefix+"godex alolan dugtrio`\n`"+prefix+"godex galarian meowth`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gopvp":
                        help = discord.Embed(title="Aide PokemonGo Pvp", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gopvp (form) [Pokemon](*) [Level] [ATK_IV] [DEF_IV] [STA_IV]`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie le potentiel PVP de votre Pokémon par rapport au meilleur de chaque ligue", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gopvp pikachu 30 14 6 12`\n`"+prefix+"gopvp piakchu* 30 14 16 12`\n`"+prefix+"gopvp alolan muk 50 15 15 14`\n`"+prefix+"gopvp galarian meowth 15 10 4 13`\n`"+prefix+"gopvp mega mewtwo y 50 15 15 15`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gorocket":
                        help = discord.Embed(title="Aide PokemonGo Rocket", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gorocket [type/leader]`\n\n`[]`est nécessaire", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations sur une configuration de Pokémon Grunt / Leaders", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gorocket water`\n`"+prefix+"gorocket cliff`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gohundo":
                        help = discord.Embed(title="Aide PokemonGo Hundo", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gohundo [Pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie 100% des CP IV de chaque niveau d'un Pokémon ", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gohundo venusaur`\n`"+prefix+"gohundo venusaur*`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gopure":
                        help = discord.Embed(title="Aide PokemonGo Purifié", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gopure [Pokemon](*) [Atk_IV] [Def_IV] [Sta_IV]`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie la comparaison entre les formes obscurs et les formes purifiées du Pokémon avec les informations d'entrée", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gopure mudkip 13 6 3`\n`"+prefix+"gopure gardevoir* 15 14 12`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gotohome":
                        help = discord.Embed(title="Aide Go vers Home", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gotohome (form) [Pokemon](*) [Level] [ATK_IV] [DEF_IV] [STA_IV]`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie une estimation des statistiques d'un Pokémon lors du transfert de Home à Sword and Sheild", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gotohome pikachu 30 14 6 12`\n`"+prefix+"gotohome piakchu* 30 14 16 12`\n`"+prefix+"gotohome alolan muk 50 15 15 14`\n`"+prefix+"gotohome galarian meowth 15 10 4 13`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gosearchterms":
                        help = discord.Embed(title="Help Gosearchterms ", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gosearchterms [Pokemon/Status/Type/Combination/Advanced]`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations utiles sur les chaînes de recherche dans Pokemon Go", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gosearchterms pokemon`\n`"+prefix+"gosearchterms status`\n`"+prefix+"gosearchterms type`\n`"+prefix+"gosearchterms combination`\n`"+prefix+"gosearchterms advanced` ", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)

                    elif content[1].lower() == "fc":
                        try:
                            content[2]
                        except:
                            help = discord.Embed(title="Aide FC (Code Ami)", description="", color=0x2962FF) #name="", value="", inline=False
                            help.add_field(name="Format Commande:", value="`"+prefix+"fc (@user)`\n`() est facultatif`", inline=False)
                            help.add_field(name="Description Commande:", value="Renvoie les codes ami que vous avez sur le serveur actuel (@user vérifiera si un utilisateur ping a des codes ami)", inline=False)
                            help.add_field(name="Sub-commands:", value="set (aliases = add) `<>help fc set pour plus d'informations`\ndelete `<>help fc delete pour plus d'informations`", inline=False)
                            help.add_field(name="**Examples:**", value="`"+prefix+"fc`\n`"+prefix+"fc @Sollisnexus`", inline=False)
                            help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                            await message.channel.send(embed = help)
                        else:
                            if content[2] == "add" or content[2] == "set":
                                help = discord.Embed(title="Aide FC Set/Add ", description="", color=0x2962FF) #name="", value="", inline=False
                                help.add_field(name="Format Commande:", value="`"+prefix+"fc add [system/game] [friendcode]`", inline=False)
                                help.add_field(name="Description Commande:", value="Ajoute le code d'ami à un système / jeu au premier emplacement disponible dans votre liste de codes d'ami", inline=False)
                                help.add_field(name="Systems and Games list", value="switch (8 slots!~)\npogo (4 slots!~)\nds (2 Slots!~)\nshuffle\nmaster\nhome\ncafemix", inline=False)
                                help.add_field(name="**Examples:**", value="`"+prefix+"fc set switch xxxx-xxxx-xxxx`\n`"+prefix+"fc add pogo xxxx-xxxx-xxxx`\n`"+prefix+"fc set ds xxxx-xxxx-xxxx`\n`"+prefix+"fc add shuffle xxxx-xxxx-xxxx`\n`"+prefix+"fc set master xxxx-xxxx-xxxx`\n`"+prefix+"fc add home xxxxxxxxxxxx`\n`"+prefix+"fc set cafemix xxxx-xxxx-xxxx`", inline=False)
                                help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                                await message.channel.send(embed = help)
                            elif content[2] == "delete":
                                help = discord.Embed(title="Aide FC Delete", description="", color=0x2962FF) #name="", value="", inline=False
                                help.add_field(name="Format Commande:", value="`"+prefix+"fc delete [system][slot#]/[all]`\n\nslot# il suffit de switch, pogo et ds", inline=False)
                                help.add_field(name="Description Commande:", value="Supprime un / tous les codes d'amis de votre liste FC", inline=False)
                                help.add_field(name="**Examples:**", value="`"+prefix+"fc delete switch(1-8)`\n`"+prefix+"fc delete pogo(1-4)`\n`"+prefix+"fc delete ds(1-2)`\n`"+prefix+"fc delete shuffle`\n`"+prefix+"fc delete master`\n`"+prefix+"fc delete home`\n`"+prefix+"fc delete cafemix`\n`"+prefix+"fc delete all`", inline=False)
                                help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                                await message.channel.send(embed = help)
                            else:
                                await message.channel.send("fc n'a pas de sous-commande "+content[2]+"!")
                    elif content[1].lower() == "info":
                        help = discord.Embed(title="Aide Info", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"info`", inline=False)
                        help.add_field(name="Description Commande:", value="Statistiques avec lien vers le vote et lien vers le serveur de support", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"info`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "nexusz?":
                        help = discord.Embed(title="Aide Nexusz?", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"nexusz?`", inline=False)
                        help.add_field(name="Description Commande:", value="Est-ce le vrai Nexus-Z? (SFW)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"nexusz?`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "invite":
                        help = discord.Embed(title="Aide Invite", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"invite`", inline=False)
                        help.add_field(name="Description Commande:", value="Fournit un lien d'invitation à inviter sur votre serveur", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"invite`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "addcommand":
                        help = discord.Embed(title="Aide Addcommand ?", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"addcommand`", inline=False)
                        help.add_field(name="Description Commande:", value="Ajoute une commande? (SFW)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"addcommand`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "freepokemon":
                        help = discord.Embed(title="Aide Freepokemon ", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"freepokemon`", inline=False)
                        help.add_field(name="Description Commande:", value="Returns free pokemon? (SFW)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"freepokemon`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "ping":
                        help = discord.Embed(title="Aide Ping", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"ping`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie «Pong!» et contrôle de latence", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"ping`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    else:
                        await message.channel.send("Aucune commande nommée '"+str(content[1])+ "'trouvé")

                    candelete = await get_delete(self, message)
                    if candelete == "True":
                        await message.delete()
            else:
                responce = message.content
                content = responce.split()
                try:
                    content[1]
                except:
                    help = discord.Embed(title="Nexus-Z Commandes", description="", color=0x2962FF) #name="", value="", inline=False
                    help.add_field(name="Utilisez `<>help [commande]` pour plus d'informations sur une commande", value="\u200B", inline=False)
                    help.add_field(name="__**Pokemon SW/SH:**__", value="**catch\npokedex\nnatures\nball\nden\nsprite\nhost\nconfig**", inline=False)
                    help.add_field(name="__**Pokemon Go:**__", value="**godex\ngopvp\ngorocket\ngohundo\ngopure\ngotohome\ngosearchterms**", inline=False)
                    help.add_field(name="__**Autre:**__", value="**fc\ninfo\nnexusz?\naddcommand\nfreepokemon\nping**", inline=False)
                    help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")

                    candelete = await get_delete(self, message)
                    if candelete == "True":
                        await message.delete()
                    await message.channel.send(embed = help)
                else:
                    if content[1].lower() == "catch":
                        help = discord.Embed(title="Aide Capture", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"catch (form) [pokemon](*) (ball)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Retourne les taux de capture du Pokémon", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"catch pikachu`\n`"+prefix+"catch piakchu*`\n`"+prefix+"catch alolan dugtrio`\n`"+prefix+"catch galarian meowth`\n`"+prefix+"catch gmax/gigantamax charizard`\n`"+prefix+"catch pikachu ultra/ultra ball`")
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "pokedex":
                        help = discord.Embed(title="Aide Pokedex ", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"pokedex (form) [pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie les informations d'entrée Pokedex sur un Pokémon\nNotes: Les Pokémon avec des formes alternatives peuvent être trouvés dans leur entrée d'origine (i.e: `"+prefix+ "pokedex kyogre` inclura également son Primal.)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"pokedex pikachu`\n`"+prefix+"pokedex pikachu*`\n`"+prefix+"pokedex alolan dugtrio`\n`"+prefix+"pokedex galarian meowth`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "natures":
                        help = discord.Embed(title="Aide Nature", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"natures`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie une chart avec toutes les natures et leurs effets sur les statistiques Pokémon", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"natures`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "ball":
                        help = discord.Embed(title="Aide Ball", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"ball [ball_type]`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie les informations d'une Poke-ball", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"ball ultra`\n`"+prefix+"ball ultra ball`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "den":
                        help = discord.Embed(title="Aide Den", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"den [den#/pokemon(*)]`\n\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Recherche de repaire par numéro ou Pokémon\n\nNote: Les formes de Galar sont recherchées par leurs noms de forme régulière", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"den 14`\n`"+prefix+"den meowth`\n`"+prefix+"den meowth*`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "sprite":
                        help = discord.Embed(title="Aide Sprite", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"sprite [Pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie un sprite Home du Pokémon nommé", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"sprite zygarde`\n`"+prefix+"sprite ash greninja`\n`"+prefix+"sprite ash greninja*`\n`"+prefix+"sprite dawn wings necrozma`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "move":
                        help = discord.Embed(title="Aide Attaque", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"move [move_name]`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations sur une attaque Pokémon (Toute les attaques disponibles dans Gen 8)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"move protect`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "host":
                        help = discord.Embed(title="Aide Host", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"host`", inline=False)
                        help.add_field(name="Description Commande:", value="Permet de configurer et d'incorporer / l'hôte de message à envoyer à un canal désigné par le propriétaire du serveur. (si un est défini)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"host`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "config":
                        help = discord.Embed(title="Aide Configuration", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"config`", inline=False)
                        help.add_field(name="Description Commande:", value="Permet au propriétaire de voir les paramètres actuels de ce bot.", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"config`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "godex":
                        help = discord.Embed(title="Godex Help", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"godex (form) [Pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations sur Pokemon Go Pokedex", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"godex charizard`\n`"+prefix+"godex charizard*`\n`"+prefix+"godex alolan dugtrio`\n`"+prefix+"godex galarian meowth`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gopvp":
                        help = discord.Embed(title="Aide PokemonGo Pvp", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gopvp (form) [Pokemon](*) [Level] [ATK_IV] [DEF_IV] [STA_IV]`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie le potentiel PVP de votre Pokémon par rapport au meilleur de chaque ligue", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gopvp pikachu 30 14 6 12`\n`"+prefix+"gopvp piakchu* 30 14 16 12`\n`"+prefix+"gopvp alolan muk 50 15 15 14`\n`"+prefix+"gopvp galarian meowth 15 10 4 13`\n`"+prefix+"gopvp mega mewtwo y 50 15 15 15`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gorocket":
                        help = discord.Embed(title="Aide PokemonGo Rocket", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gorocket [type/leader]`\n\n`[]`est nécessaire", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations sur une configuration de Pokémon Grunt / Leaders", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gorocket water`\n`"+prefix+"gorocket cliff`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gohundo":
                        help = discord.Embed(title="Aide PokemonGo Hundo", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gohundo [Pokemon](*)`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie 100% des CP IV de chaque niveau d'un Pokémon ", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gohundo venusaur`\n`"+prefix+"gohundo venusaur*`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gopure":
                        help = discord.Embed(title="Aide PokemonGo Purifié", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gopure [Pokemon](*) [Atk_IV] [Def_IV] [Sta_IV]`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie la comparaison entre les formes obscurs et les formes purifiées du Pokémon avec les informations d'entrée", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gopure mudkip 13 6 3`\n`"+prefix+"gopure gardevoir* 15 14 12`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gotohome":
                        help = discord.Embed(title="Aide Go vers Home", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gotohome (form) [Pokemon](*) [Level] [ATK_IV] [DEF_IV] [STA_IV]`\n\n`()` est facultatif\n`[]` est nécessaire\n`*` si vous voulez une image Shiny", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie une estimation des statistiques d'un Pokémon lors du transfert de Home à Sword and Sheild", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gotohome pikachu 30 14 6 12`\n`"+prefix+"gotohome piakchu* 30 14 16 12`\n`"+prefix+"gotohome alolan muk 50 15 15 14`\n`"+prefix+"gotohome galarian meowth 15 10 4 13`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "gosearchterms":
                        help = discord.Embed(title="Help Gosearchterms ", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"gosearchterms [Pokemon/Status/Type/Combination/Advanced]`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie des informations utiles sur les chaînes de recherche dans Pokemon Go", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"gosearchterms pokemon`\n`"+prefix+"gosearchterms status`\n`"+prefix+"gosearchterms type`\n`"+prefix+"gosearchterms combination`\n`"+prefix+"gosearchterms advanced` ", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)

                    elif content[1].lower() == "fc":
                        try:
                            content[2]
                        except:
                            help = discord.Embed(title="Aide FC (Code Ami)", description="", color=0x2962FF) #name="", value="", inline=False
                            help.add_field(name="Format Commande:", value="`"+prefix+"fc (@user)`\n`() est facultatif`", inline=False)
                            help.add_field(name="Description Commande:", value="Renvoie les codes ami que vous avez sur le serveur actuel (@user vérifiera si un utilisateur ping a des codes ami)", inline=False)
                            help.add_field(name="Sub-commands:", value="set (aliases = add) `<>help fc set pour plus d'informations`\ndelete `<>help fc delete pour plus d'informations`", inline=False)
                            help.add_field(name="**Examples:**", value="`"+prefix+"fc`\n`"+prefix+"fc @Sollisnexus`", inline=False)
                            help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                            await message.channel.send(embed = help)
                        else:
                            if content[2] == "add" or content[2] == "set":
                                help = discord.Embed(title="Aide FC Set/Add ", description="", color=0x2962FF) #name="", value="", inline=False
                                help.add_field(name="Format Commande:", value="`"+prefix+"fc add/set [system/game] [friendcode]`", inline=False)
                                help.add_field(name="Description Commande:", value="Ajoute le code d'ami à un système / jeu au premier emplacement disponible dans votre liste de codes d'ami", inline=False)
                                help.add_field(name="Systems and Games list", value="switch (8 slots!~)\npogo (4 slots!~)\nds (2 Slots!~)\nshuffle\nmaster\nhome\ncafemix", inline=False)
                                help.add_field(name="**Examples:**", value="`"+prefix+"fc set switch xxxx-xxxx-xxxx`\n`"+prefix+"fc add pogo xxxx-xxxx-xxxx`\n`"+prefix+"fc set ds xxxx-xxxx-xxxx`\n`"+prefix+"fc add shuffle xxxx-xxxx-xxxx`\n`"+prefix+"fc set master xxxx-xxxx-xxxx`\n`"+prefix+"fc add home xxxxxxxxxxxx`\n`"+prefix+"fc set cafemix xxxx-xxxx-xxxx`", inline=False)
                                help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                                await message.channel.send(embed = help)
                            elif content[2] == "delete":
                                help = discord.Embed(title="Aide FC Delete", description="", color=0x2962FF) #name="", value="", inline=False
                                help.add_field(name="Format Commande:", value="`"+prefix+"fc delete [system][slot#]/[all]`\n\nslot# il suffit de switch, pogo et ds", inline=False)
                                help.add_field(name="Description Commande:", value="Supprime un / tous les codes d'amis de votre liste FC", inline=False)
                                help.add_field(name="**Examples:**", value="`"+prefix+"fc delete switch(1-8)`\n`"+prefix+"fc delete pogo(1-4)`\n`"+prefix+"fc delete ds(1-2)`\n`"+prefix+"fc delete shuffle`\n`"+prefix+"fc delete master`\n`"+prefix+"fc delete home`\n`"+prefix+"fc delete cafemix`\n`"+prefix+"fc delete all`", inline=False)
                                help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                                await message.channel.send(embed = help)
                            else:
                                await message.channel.send("fc n'a pas de sous-commande "+content[2]+"!")
                    elif content[1].lower() == "info":
                        help = discord.Embed(title="Aide Info", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"info`", inline=False)
                        help.add_field(name="Description Commande:", value="Statistiques avec lien vers le vote et lien vers le serveur de support", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"info`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "nexusz?":
                        help = discord.Embed(title="Aide Nexusz?", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"nexusz?`", inline=False)
                        help.add_field(name="Description Commande:", value="Est-ce le vrai Nexus-Z? (SFW)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"nexusz?`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "addcommand":
                        help = discord.Embed(title="Aide Addcommand ?", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"addcommand`", inline=False)
                        help.add_field(name="Description Commande:", value="Ajoute une commande? (SFW)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"addcommand`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "freepokemon":
                        help = discord.Embed(title="Aide Freepokemon ", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"freepokemon`", inline=False)
                        help.add_field(name="Description Commande:", value="Returns free pokemon? (SFW)", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"freepokemon`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    elif content[1].lower() == "ping":
                        help = discord.Embed(title="Aide Ping", description="", color=0x2962FF) #name="", value="", inline=False
                        help.add_field(name="Format Commande:", value="`"+prefix+"ping`", inline=False)
                        help.add_field(name="Description Commande:", value="Renvoie «Pong!» et contrôle de latence", inline=False)
                        help.add_field(name="**Examples:**", value="`"+prefix+"ping`", inline=False)
                        help.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
                        await message.channel.send(embed = help)
                    else:
                        await message.channel.send("Aucune commande nommée '"+str(content[1])+ "'trouvé")

                    candelete = await get_delete(self, message)
                    if candelete == "True":
                        await message.delete()


    @commands.command()
    async def info(self, ctx):
        activeservers = self.client.guilds
        Info = discord.Embed(title="Nexus-Z Support Server Invite", url="https://discord.gg/At2zCHv", color=0x2962FF )
        Info.set_author(name="Sollisnexus#1429", url="https://sollisnexus.github.io/NexusZ/",icon_url="https://cdn.discordapp.com/avatars/177200577430683648/a_0f28b72333cf75baea7eca74c09089ae.gif")
        Info.add_field(name="Serving:", value="**"+str(len(self.client.guilds))+"** Servers", inline=True)
        Info.add_field(name="Server invite:", value="[Link](https://discord.com/oauth2/authorize?client_id=674716932720558101&permissions=26624&scope=bot) to invite\nNexus-Z to your\nown server!~", inline=True)
        Info.add_field(name="Top.GG Upvote:", value="[Vote Here!](https://top.gg/bot/674716932720558101/vote)\nand get a 🍪", inline=True)
        Info.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
        candelete = await get_delete(self, ctx.message)
        if candelete == "True":
            await message.delete()
        await ctx.channel.send(embed=Info)

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send("Cette commande ne fonctionne pas pour obtenir de l'aide, veuillez utiliser <>help pour les commandes")

    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def config(self, ctx):
        getprefix = await get_prefix(self, ctx)
        getdelete = await get_delete(self, ctx)
        gethostchannel = await guildhostchannel(self, ctx)


        embed = discord.Embed(title="Configuration pour ce serveur", description="", color=0x2962FF)
        embed.add_field(name="Prefix:", value=str(getprefix), inline=False)
        embed.add_field(name="Suppression de message:", value=str(getdelete), inline=False)
        embed.add_field(name="Canal d'hébergement (pour Sw / Sh Dens):", value=str(gethostchannel), inline=False)
        embed.add_field(name="Comment modifier les paramètres:", value="Changer l'utilisation du préfixe `"+str(getprefix)+"changeprefix [prefix]`\nModifier l'utilisation de la suppression des messages `"+str(getprefix)+"changedelete (True/Yes/Y) or (False/No/N)`\nModifier l'utilisation du canal d'hébergement `"+str(getprefix)+"changehost [#channel]`", inline=False)
        embed.set_footer(text="Provided by Nexus-Z", icon_url="https://raw.githubusercontent.com/Sollisnexus/Sollisnexus.github.io/master/NexusZ/NexusZLogo_2.png")
        candelete = await get_delete(self, ctx)
        if candelete == "True":
            await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        Invite = discord.Embed(title="Nexus-Z Invite", url="https://discord.com/oauth2/authorize?client_id=674716932720558101&permissions=26624&scope=bot", color=0x2962FF)
        Invite.add_field(name="Server invite:", value="[Link](https://discord.com/oauth2/authorize?client_id=674716932720558101&permissions=26624&scope=bot) to invite\nNexus-Z to your\nown server!~", inline=True)
        candelete = await get_delete(self, ctx.message)
        if candelete == "True":
            await message.delete()
        await ctx.channel.send(embed=Invite)

    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def leave(self, ctx):
        to_leave = self.client.get_guild(ctx.guild.id)
        await ctx.send("Je dois y aller mes amis ont besoin de moi! _-s'envole-_")
        await to_leave.leave()

    @leave.error
    async def leave_error(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            candelete = await get_delete(self, message)
            if candelete == "True":
                await message.delete()
            await ctx.send("Seul le propriétaire du serveur peut supprimer ce bot", delete_after=5)

    @commands.command()
    async def ping(self, ctx):
        """ Pong! (avec latence) """
        candelete = await get_delete(self, message)
        if candelete == "True":
            await message.delete()
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")
        await message.add_reaction(emoji)
        print(f'Ping {int(ping)}ms')

def setup(client):
    client.add_cog(Help(client))
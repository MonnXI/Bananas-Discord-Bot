import discord
import asyncio
from discord.ext import commands, tasks
from discord import app_commands, ui, utils
import config
import random
import datetime
import json

intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
intents.members = True
intents.messages = True
intents.emojis_and_stickers = True
intents.reactions = True
intents.moderation = True

bot = commands.Bot(command_prefix='+', intents=intents)
bot.remove_command("help")



def load_progress():
    try:
        with open("progress.json", "r") as file:
            data = json.load(file)
            return data.get("progress", 0)
    except FileNotFoundError:
        print("File 'progress.json' not found. Creating a new file.")
        with open("progress.json", "w") as new_file:
            json.dump({"progress": 0}, new_file)  # Crée un fichier avec la progression initiale à 0
        return 0  # Retourne 0 car le fichier n'existait pas

def save_progress(progress):
    try:
        with open("progress.json", "r") as file:
            existing_progress = json.load(file)
    except FileNotFoundError:
        existing_progress = {"progress": 0}
    existing_progress["progress"] = progress

    with open("progress.json", "w") as file:
        json.dump(existing_progress, file, indent=4)
        

progress = load_progress()
previous_message = None
previous_image = None
ancient = None
event = 0



class feedBack(ui.Modal, title = "Idées envoyées"):
    answer = ui.TextInput(label = "Vous avez des idées ?", style = discord.TextStyle.long, placeholder = "Je voudrais que...", required = True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title = self.title, description = f"**{self.answer.label}**\n{self.answer}", color = discord.Colour.yellow())
        embed.set_author(name = interaction.user, icon_url=interaction.user.avatar)
        channel = bot.get_channel(1178118314757738537)
        await channel.send(embed = embed)
        await interaction.response.send_message("Merci de votre aide !")


@bot.tree.command(name="ideas", description="Donner des idées pour le bot !")
async def ideas(interaction: discord.Interaction):
    await interaction.response.send_modal(feedBack())

class SimpleView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label="Demander un ticket",
                       style=discord.ButtonStyle.blurple, custom_id = "ticket_button")
    async def ticketButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        check = utils.get(interaction.guild.text_channels, name = f"ticket-for-{interaction.user.name}")
        if check is not None:
            await interaction.response.send_message(f"{interaction.user.mention} Vous avez déjà un ticket", ephemeral = True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True)
            }
            channel = await interaction.guild.create_text_channel(name = f"ticket-for-{interaction.user.name}", overwrites = overwrites, reason = f"Ticket for {interaction.user}")
        await interaction.response.send_message(f"Je vous ai créé un ticket retrouvez le à {channel.mention}", ephemeral = True)
        await channel.send(f"Voici votre ticket {interaction.user.mention}")

class confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        
        @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green, custom_id = "yes")
        async def yes(self, interaction, button):
            try: await interaction.channel.delete()
            except: await interaction.response.send_message("ERREUR: CANNOT DELETE THIS CHANNEL :ERROR_CODE: 100")

class ticketMain(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label = "Close ticket", style = discord.ButtonStyle.red, custom_id = "close")
    async def close(self, interaction, button):
        embed = discord.Embed(title = "Are you sure you want to delete this ticket ?", description = "Note that its content will be transcripted.", color = dicord.Colour.blurple())
        await interaction.response.send_message(embed = embed, ephemeral = True)

@bot.tree.command(name="ticket", description="Pour ouvrir un ticket !")
async def ticket(interaction: discord.Interaction):
    await interaction.response.send_message(f"Système de ticket lancé", ephemeral = True)
    view = SimpleView()
    channel = interaction.channel
    embed = discord.Embed(title = "Pour créer un ticket appuyez ici !", color = discord.Colour.yellow())
    await channel.send(embed=embed)
    await channel.send(view=view)
    

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name} ({bot.user.id})")
    print("Prêt !")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    geo_game.start()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" I think I am the best bot ever ! 😎"))



def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Failed to load json")
        return {}
def save_data(data):
    try:
        with open("data.json", "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}

    existing_data.update(data)

    with open("data.json", "w") as file: 
        json.dump(existing_data, file, indent=4)

def load_lvl():
    try:
        with open("lvl.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Failed to load json")
        return {}
def save_lvl(lvl):
    try:
        with open("lvl.json", "r") as file:
            existing_lvl = json.load(file)
    except FileNotFoundError:
        existing_lvl = {}

    existing_data.update(data)

    with open("data.json", "w") as file: 
        json.dump(existing_data, file, indent=4)


@bot.event
async def on_message(message):
    member = message.author
    if message.content.lower() == "ping":
        await message.channel.send("Pong")
    if message.content.lower() == "tic":
        await message.channel.send("Tac")
    # if message.content.lower() == "connard" in message.content:
    #     await member.timeout(until, reason=reason)

    user_data = load_data()

    user_id = str(message.author.name)
    user_data[user_id] = user_data.get(user_id, 0) + 1

    save_data(user_data)
    print(f"{user_id} got 1 xp he is now at {user_data[user_id]}")
    
    async def xpSystem():
        user_data = load_data()
        user_lvl = load_lvl()
        user_id = str(message.author.name)
        
        if user_data[user_id] >= 50 and user_data[user_id] <= 124:
            embed = discord.Embed(title = f"Good job {user_id} you passed level 1", description = f"Already level 1 ?!", color = discord.Colour.yellow())
            if not user_lvl[user_id] == 1:
                await message.channel.send(embed=embed)
                user_lvl[user_id] = user_lvl.get(user_id, 0) + 1
    
    await xpSystem()
    
    await bot.process_commands(message)

# ICI C'EST LA COMMANDE POUR SAVOIR SON XP
@bot.tree.command(name="xp", description="Connaître son nombre de messages envoyés")
async def xp(interaction: discord.Interaction):
    user = interaction.user
    user_data = load_data()

    await interaction.response.send_message(f"Votre nombre de messages est à {user_data[user.name]}", ephemeral=True)



@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(1141114347091931147)
    if channel:
        message = f"Bienvenue {member.mention} sur le serveur !"
        await channel.send(message)





@bot.event
async def on_raw_reaction_remove(payload):
    user = await bot.fetch_user(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji

    global progress

    if not str(emoji) == "🎅":

        if progress >= 1:
            progress -= 1
            print(f"{progress} -1 par {user.name} ({user.id})")


        save_progress(progress)
        print(f"Progression_saved")
    global event

    if str(emoji) == "🎅":
        if event >= 2:
            event -= 1
            print(f"{event} -1 par {user.name} ({user.id})")
        



@bot.event
async def on_raw_reaction_add(payload):
    user = await bot.fetch_user(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji

    user_progress = load_data()

    user_progress.get("progress", 0)

    if not str(emoji) == "🎅":
        async def sendfirst():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/1on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def sendfifth():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/5on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def sendten():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/10on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send15():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/15on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send25():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/25on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send30():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/30on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send40():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/40on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send50():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/50on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send60():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/60on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send70():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/70on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send80():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/80on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send90():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/90on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        async def send100():
            channel = bot.get_channel(1154165700382953582)

            with open('/home/monntheboss/Banana/Banana/100on100.png', 'rb') as file:
                image = discord.File(file)

            return await channel.send(file=image)

        progression = bot.get_channel(1154165700382953582)

        global progress

        progress += 1
        print(f"{progress} par {user.name} ({user.id}) dans {channel.name} sur ({message.id})")

        global previous_message
        global previous_image

        if previous_message:
            await previous_message.delete()
        if previous_image:
            await previous_image.delete()

        if progress >= 1:
            current_message = f"La progression est à {progress} sur 1000"
            previous_message = await progression.send(current_message)
    
        if progress >= 10 and progress <= 49:
            previous_image = await sendfirst()
        if progress >= 50 and progress <= 99:
            previous_image = await sendfifth()
        if progress >= 100 and progress <= 149:
            previous_image = await sendten()
        if progress >= 150 and progress <= 249:
            previous_image = await send15()
        if progress >= 250 and progress <= 299:
            previous_image = await send25()
        if progress >= 300 and progress <= 399:
            previous_image = await send30()
        if progress >= 400 and progress <= 499:
            previous_image = await send40()
        if progress >= 500 and progress <= 599:
            previous_image = await send50()
        if progress >= 600 and progress <= 699:
            previous_image = await send60()
        if progress >= 700 and progress <= 799:
            previous_image = await send70()
        if progress >= 800 and progress <= 899:
            previous_image = await send80()
        if progress >= 900 and progress <= 999:
            previous_image = await send90()
        if progress >= 1000:
            previous_image = await send100()
        save_progress(progress)
        print(f"Progression_saved")

    global halloween
    global ancient
    if str(emoji) == "🎅":
        channel = bot.get_channel(1160677058377167008)
        if event <= 249:
            halloween += 1
            print(f"L'event est maintenant à {halloween} par {user}")
            if not ancient == None:
                await ancient.delete()
            ancient = await channel.send(f"Le 🎅 est content à {event}%")
        if halloween >= 250:
            if not ancient == None:
                await ancient.delete()
            ancient = await channel.send(f"Bravo le père noël est content à 100% !!!")



@bot.tree.command(name="hello", description="Pour que le bot te dise salut")
async def hello(interaction: discord.Interaction):
        user = interaction.user
        await interaction.response.send_message(f"Bonjour {interaction.user.mention} !", ephemeral=False)
        print(f"Hello used by {user.name} ({user.id}) in {interaction.channel.name}")



@bot.tree.command(name="info", description="Vos informations")
async def info(interaction):
    author_latency = round(bot.latency * 1000)
    user = interaction.user
    channel = interaction.channel
    await interaction.response.send_message(f"Voici vos informations : \nVotre ping : {author_latency} ms\nVotre id : {user.id}\nVotre pseudo : {user.name}", ephemeral=True)

    print(f"Send infos to {user.name} dans {channel.name}")




@bot.tree.command(name="night", description="Bonne nuit à tous")
async def night(interaction: discord.Interaction):
    user = interaction.user
    channel = interaction.channel

    with open('/home/monntheboss/Banana/Banana/moon.gif', 'rb') as file:
        image = discord.File(file)

    print(f"Command night ! by {user.name} ({user.id}) in {channel.name}")

    await interaction.response.send_message(f"Bonne nuit tout le monde! ")
    await channel.send(file=image)

@bot.tree.command(name="morning", description="Pour que le bot dise bon matin")
async def morning(interaction: discord.Interaction):
    user = interaction.user
    channel = interaction.channel

    with open('/home/monntheboss/Banana/Banana/sun.gif', 'rb') as file:
        image = discord.File(file)

    print(f"Command morning ! by {user.name} dans {channel.name}")

    await interaction.response.send_message(f"Bon Matin tout le monde!")
    await channel.send(file=image)

@bot.tree.command(name="find", description="Pour trouver un message avec son id")
async def find(interaction: discord.Interaction, message_id: str):

    user = interaction.user
    channel = interaction.channel

    try:
        message_id = int(message_id)
        message = await channel.fetch_message(message_id)

        if message:
            react = await interaction.response.send_message(f"<@{user.id}> ||Message trouvé : {message.content} ; Envoyé par : {message.author} ||", ephemeral=True)
        else:
            react = interaction.response.send_message(f"<@{user.id}> ||Aucun message trouvé avec cet ID.||", ephemeral=True)
    except:
        react = await interaction.response.send_message(f"<@{user.id}> ||Erreur lors de la recherche||", ephemeral=True)




    print(f"Command find ! by {user.name} dans {channel.name}")


@bot.tree.command(name="embed", description="Envoyer un embed")
async def embed(interaction: discord.Interaction, titre: str, content: str):
    channel = interaction.channel
    user = interaction.user
    embed = discord.Embed(
        title=titre,
        description=content,
        color=discord.Color.yellow()
    )

    await interaction.response.send_message(embed=embed)
    print(f"Sent an embed in {channel.name} by {user.name} ({user.id})")



@bot.tree.command(name="day", description="Pour dire coucou à tous")
async def day(interaction: discord.Interaction):
    channel = interaction.channel
    user = interaction.user
    await interaction.response.send_message(f"Coucou @everyone !")
    await channel.send("👋")

    print(f"Said hello in {channel.name} by {user.name} ({user.id})")



@bot.tree.command(name="say", description="Pour que le bot répète ce que tu dis")
async def say(interaction: discord.Interaction, content: str):
    user = interaction.user
    channel = interaction.channel
    content = await interaction.response.send_message(f"{content}")
    print(f"Repeted {content} by {user.name} ({user.id}) in {channel.name}")


@bot.tree.command(name="drawing", description="Pour que le bot fasse un petit dessin")
async def drawing(interaction: discord.Interaction):
    value = random.randint(1, 8) # Le permettre jusqu'à 8
    user = interaction.user
    channel = interaction.channel
    if value == 1:
        await interaction.response.send_message("(っ＾▿＾)")
        
    if value == 2:
        await interaction.response.send_message("(ㆆ_ㆆ)")
        
    if value == 3:
        await interaction.response.send_message("ʕ•́ᴥ•̀ʔっ")
        
    if value == 4:
        await interaction.response.send_message("( ͡° 👅 ͡°)")
        
    if value == 5:
        await interaction.response.send_message("( ͡♥  ͟ʖ ͡♥)")

    if value == 6:
        await interaction.response.send_message("(ง ^ ● ^ )ง")

    if value == 7:
        await interaction.response.send_message("(っ-̶●̃益●̶̃)っ")

    if value == 8:
        await interaction.response.send_message("≧◉◡◉≦")
        
    print(f"Sent a drawing in {channel.name} by {user.name} ({user.id})")



#messages = [
#    "Joyeux premier jour de l'Avent pendant ce mois on va ouvrir le calendrier et il va y avoir soit des messages de Noël, des blagues ou des récompenses donc ouvrez moi à chaque jour ! 🎄🎁",
#    "Deuxième jour ! Êtes-vous prêt pour Noël ? 🌟",
#    "Troisième jour ! Que le compte à rebours continue ! 🎅",
#    "Quatrième jour ! Nouvelle commande le /update pour savoir le contenu de la prochaine update ! ",
#    "Cinquième jour ! VIVE LES PATATES 🥔🥔🥔!!! ",
#    "Sixième jour ! Nouvel émoji le lapin (J'aime les lapins) !!!",
#    "Septième jour ! T'as commandé quoi comme cadeaux ?! 🎁",
#    "Huitième jour ! Je trouve que mon bot est vraiment trop bine pour arriver à faire ça !!",
#    "Neuvième jour ! Ajout de nouveaux visages à la commande /drawing ! ✏️",
#    "Dixième jour ! Premier tier du mois !!! ⅓",
#    "Onzième jour ! Que voudriez-vous ajouter au bot ?! ",
#    "Douzième jour ! Aujourd'hui on ajoute un nouvel autocollant ! ",
#    "Treizième jour ! Aujourd'hui j'ajoute un nouvel émoji : Le logo de Noël du serveur !!!",
#    "Quatorzième jour ! Qu'est ce qui est jaune et qui attend ? ||Le soleil qui attend d'exploser ! || ",
#    "Quinzième jour ! Ajout d'une nouvelle commande, le /help ! ",
#    "Seizième jour ! Avez-vous hâte à 2024 ??? ",
#    "Dix-septième jour ! On continue le DDD ! 🍆",
#    "Dix-huitième jour ! J'aime la neige (oe on s'en balek) ! ",
#    "Dix-neuvième jour ! Rôle noël 2023 à tout le monde ! ",
#    "Vingtième jour ! Deuxième tier du mois ! ",
#    "Vingt-et-unième jour ! Nouveau soundboard, le HEHEHEHA !!! ", #Voir heheheha.mp3
#    "Vingt-deuxième jour ! Recevez-vous votre famille pour Noël ?! ",
#    "Vingt-troisième jour ! Prêts pour la magie de Noël ? 🌟",
#    "C'est la veille de Noël ! Aujourd'hui la récompense finale ! L'ÉMOJI DE PÈRE NOËL 8 BITS",
#]


#@bot.tree.command(name="avent", description="Pour récupérer son calendrier de l'avent du jour !")
#async def avent(interaction: discord.Interaction):
#    now = datetime.datetime.now()
#    today = now.day
#
#    if today <= len(messages):
#        message = messages[today - 1]
#        await interaction.response.send_message(f"{message}")
#    else:
#        await interaction.response.send_message("Noël est déjà passé !")
#
@bot.tree.command(name="update", description="Pour connaitre l'update actuelle ou coming soon")
async def avent(interaction: discord.Interaction):
    await interaction.response.send_message("Je travaille en ce moment sur un système de ticket et sur la mise à jour de pâques. 🌸")

@bot.tree.command(name="help", description="Pour obtenir de l'aide")
async def avent(interaction: discord.Interaction):
    await interaction.response.send_message("``` Help command ``` \n ``` /avent pour récupérer son calendrier de l'avent (Durant décembre uniquement) 🎄 \n /update pour connaitre la mise à jour en cours. \n /morning pour dire bon matin à tout le monde. \n /night pour dire bonne nuit à tout le monde. \n /day pour dire coucou à tout le monde. \n /say pour que le bot répète ce que tu dis. \n /embed pour créer un embed. \n /drawing pour que le bot mette une réaction spéciale dans le chat. \n /info pour connaitre ses info. \n /find pour chercher un message à partir de son id. \n /ideas pour envoyer des idées pour le bot. \n /ticket (bêta) cette commande est seulement accessible aux bot tester et aux développeurs le temps que cette fonctionnalitée soit terminée. \n /msgnumber pour connaitre le nombre de message que l'on a envoyé de puis la 2.0 du bot. \n /hello pour que le bot te dise salut. \n C'est tout pour l'instant ! ``` ", ephemeral=True)

async def send_location(toChannel):
    channel = bot.get_channel(1141114347091931147)
    location = random.randint(1, 18)  # Choisir aléatoirement une destination
    embed=discord.Embed(title="Trouvez le lieu !", description="Bonne chance à vous !", color=discord.Color.yellow())
    if location == 1:
        with open('/home/monntheboss/Banana/Banana/image1.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Le Caire", image, text
    elif location == 2:
        with open('/home/monntheboss/Banana/Banana/image2.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Paris", image, text
    elif location == 3:
        with open('/home/monntheboss/Banana/Banana/image3.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Londre", image, text
    elif location == 4:
        with open('/home/monntheboss/Banana/Banana/image4.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Tokyo",image, text
    elif location == 5:
        with open('/home/monntheboss/Banana/Banana/image5.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Washington", image, text
    elif location == 6:
        with open('/home/monntheboss/Banana/Banana/image6.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Abou Dabi", image, text
    elif location == 7:
        with open('/home/monntheboss/Banana/Banana/image7.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Toronto", image, text
    elif location == 8:
        with open('/home/monntheboss/Banana/Banana/image8.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Shangai", image, text
    elif location == 9:
        with open('/home/monntheboss/Banana/Banana/image9.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Rio de Janeiro", image, text
    elif location == 10:
        with open('/home/monntheboss/Banana/Banana/image10.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Chicago", image, text
    elif location == 11:
        with open('/home/monntheboss/Banana/Banana/image11.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Hong Kong", image, text
    elif location == 12:
        with open('/home/monntheboss/Banana/Banana/image12.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Los Angeles", image, text
    elif location == 13:
        with open('/home/monntheboss/Banana/Banana/image13.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Moscou", image, text
    elif location == 14:
        with open('/home/monntheboss/Banana/Banana/image14.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Mexico", image, text
    elif location == 15:
        with open('/home/monntheboss/Banana/Banana/image15.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Jakarta", image, text
    elif location == 16:
        with open('/home/monntheboss/Banana/Banana/image16.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Chengdu", image, text
    elif location == 17:
        with open('/home/monntheboss/Banana/Banana/image17.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Singapour", image, text
    elif location == 18:
        with open('/home/monntheboss/Banana/Banana/image18.png', 'rb') as file:
            city = discord.File(file)
        image = await channel.send(file=city)
        text = await channel.send(embed=embed)
        return "Hyderabad", image, text
        
        
waitingTime = random.randint(3, 8)
@tasks.loop(hours=waitingTime, count=None)  # Répéter toutes les 3 à 8 heures
async def geo_game():
    channel = bot.get_channel(1141114347091931147)  
    location = await send_location(channel)
    location_name = location[0]
    image = location[1]
    text = location[2]
    global waitingTime
    print(f"Sent a GeoGeussr at {datetime.datetime.now()} the next one is in {waitingTime} hours ")
    
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).total_seconds() < 1800:
        async for message in channel.history(limit=1):  # Récupère le dernier message du canal
            if not message.author.bot and message.content.lower() == location_name.lower():
                await channel.send(f"Bravo à {message.author.mention} pour avoir deviné la bonne réponse ({location_name}) ! ✔️")
                user_data = load_data()

                user_id = str(message.author.name)
                
                user_data[user_id] = user_data.get(user_id, 0) + 20

                save_data(user_data)
                print(f"{user_id} got 20 xp he is now at {user_data[user_id]}")
                return
            elif not message.author.bot and not message.content.lower() == location_name.lower():
                await channel.send(f"Mauvaise réponse {message.author.mention} ❌")
        await asyncio.sleep(1)   

    await channel.send(f"Personne n'a deviné la bonne réponse en trente minutes.")

        

token = config.Token

bot.run(token)

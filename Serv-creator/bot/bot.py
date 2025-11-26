import discord
from discord.ext import commands
from discord.ui import View, Button
import json
import os
from config import DISCORD_TOKEN, STRUCTURE_PATH

# Configuration des intents Discord
intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True
intents.messages = True

# Initialisation du bot
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  

@bot.command()
async def help(ctx):
    """Affiche l'aide et les commandes disponibles du bot."""
    embed = discord.Embed(
        title="🤖 Commandes du bot",
        description="Voici les commandes disponibles pour gérer ton serveur Discord avec ce bot.",
        color=0x00ff99
    )
    embed.add_field(
        name="!create <code>", 
        value="Crée la structure du serveur à partir du code généré par le site.", 
        inline=False
    )
    embed.add_field(
        name="!nukem", 
        value="Supprime **tous les salons et catégories** du serveur (confirmation demandée).", 
        inline=False
    )
    embed.add_field(
        name="!test", 
        value="Vérifie si le bot fonctionne correctement.", 
        inline=False
    )
    embed.set_footer(text="Bot créé par MR NAB | Utilise avec précaution !")
    await ctx.send(embed=embed)


@bot.command()
async def test(ctx):
    """Teste si le bot fonctionne correctement."""
    await ctx.send("✅ Le bot fonctionne et est prêt à créer un serveur !")

@bot.command()
async def create(ctx, code: str):
    """Crée la structure du serveur à partir d'un code généré."""
    file_path = os.path.join(STRUCTURE_PATH, f"{code}.json")

    if not os.path.exists(file_path):
        await ctx.send("❌ Ce code n'existe pas ou n'a pas été généré.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        await ctx.send(f"🔧 Création de la structure pour le code `{code}`...")

        # Créer les rôles
        for role in data.get("roles", []):
            if not discord.utils.get(ctx.guild.roles, name=role):
                await ctx.guild.create_role(name=role)

        # Créer les catégories et salons associés
        for category_data in data.get("categories", []):
            category = await ctx.guild.create_category(name=category_data["name"], position=0)

            for text_channel in category_data.get("text_channels", []):
                await ctx.guild.create_text_channel(name=text_channel, category=category)

            for voice_channel in category_data.get("voice_channels", []):
                await ctx.guild.create_voice_channel(name=voice_channel, category=category)

        await ctx.send("✅ Structure créée avec succès !")

    except Exception as e:
        await ctx.send(f"❌ Une erreur est survenue : {e}")
        print(f"[ERREUR] {e}")

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def nuke(ctx):
    """Supprime tous les salons et catégories du serveur (avec confirmation)."""
    class ConfirmView(View):
        def __init__(self):
            super().__init__(timeout=20)

        @discord.ui.button(label="✅ Confirmer", style=discord.ButtonStyle.danger)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.author:
                await interaction.response.send_message("Tu n'as pas lancé la commande.", ephemeral=True)
                return

            await interaction.response.edit_message(content="🔨 Suppression des salons...", view=None)

            try:
                for channel in ctx.guild.channels:
                    await channel.delete()
                await ctx.send("🔥 Tous les salons et catégories ont été supprimés.")
            except Exception as e:
                await ctx.send(f"❌ Erreur lors de la suppression : {e}")
            self.stop()

        @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.secondary)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.author:
                await interaction.response.send_message("Tu n'as pas lancé la commande.", ephemeral=True)
                return

            await interaction.response.edit_message(content="❎ Annulé.", view=None)
            self.stop()

    view = ConfirmView()
    await ctx.send(
        "⚠️ Es-tu sûr de vouloir **supprimer tous les salons et catégories** du serveur ?", 
        view=view
    )

@bot.event
async def on_guild_join(guild):
    """Crée un salon de bienvenue quand le bot rejoint un serveur."""
    try:
        category = await guild.create_category("🛠️ Bienvenue (temporaire)", position=0)
        channel = await guild.create_text_channel("📌・instructions", category=category)

        instructions = (
            "👋 Merci d'avoir ajouté le bot !\n\n"
            "**Étapes recommandées :**\n"
            "1. Va dans **Paramètres du serveur → Activer la Communauté**\n"
            "2. Cela activera des salons comme `#annonces`, `#accueil`, `#conférence`\n"
            "3. Utilise la commande `!create <code>` pour créer ta structure\n"
            "4. Utilise `!nuke` pour tout supprimer si besoin (⚠️ avec confirmation)\n\n"
            "⚙️ Tu peux ensuite supprimer cette catégorie si tu veux."
        )

        await channel.send(instructions)
    except Exception as e:
        print(f"[ERREUR on_guild_join] {e}")

# Démarrage du bot
if __name__ == "__main__":
    print("[⏳] Connexion au bot...")
    bot.run(DISCORD_TOKEN)

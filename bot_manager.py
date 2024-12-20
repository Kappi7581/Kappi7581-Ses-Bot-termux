import os
import asyncio
from rich.console import Console
from rich.prompt import Prompt
from discord.ext import commands
import discord

# Rich konsolu
console = Console()

# Token ve Ses Kanal Bilgileri
bot_configs = []

# Menü Sistemi
def main_menu():
    while True:
        console.clear()
        console.print("[bold magenta]Kappi7581 Ses Botu[/bold magenta]")
        console.print("1. Ayarlama")
        console.print("2. Botları Başlat")
        console.print("3. Çıkış")
        choice = Prompt.ask("[bold cyan]Bir seçim yapın[/bold cyan]")

        if choice == "1":
            settings_menu()
        elif choice == "2":
            asyncio.run(start_bots())
        elif choice == "3":
            console.print("[bold red]Çıkış yapılıyor...[/bold red]")
            break
        else:
            console.print("[bold red]Geçersiz seçim![/bold red]")

# Ayarlama Menüsü
def settings_menu():
    global bot_configs
    bot_configs = []  # Eski ayarları sıfırla
    for i in range(1, 6):
        console.print(f"[bold yellow]{i}. Bot Ayarları[/bold yellow]")
        token = Prompt.ask("Bot Token")
        channel_id = Prompt.ask("Ses Kanal ID")
        bot_configs.append({"token": token, "channel_id": int(channel_id)})
    console.print("[bold green]Ayarlar kaydedildi![/bold green]")
    input("Ana menüye dönmek için Enter'a basın...")

# Botları Başlatma Fonksiyonu
async def start_bots():
    tasks = []
    for config in bot_configs:
        tasks.append(run_bot(config["token"], config["channel_id"]))
    await asyncio.gather(*tasks)

# Tek Bot Çalıştırma Fonksiyonu
async def run_bot(token, channel_id):
    intents = discord.Intents.default()
    intents.messages = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        console.print(f"[bold green]{bot.user.name} giriş yaptı![/bold green]")
        channel = bot.get_channel(channel_id)
        if channel and channel.type == discord.ChannelType.voice:
            await channel.connect()
            console.print(f"[bold blue]{bot.user.name} ses kanalına bağlandı.[/bold blue]")
        else:
            console.print(f"[bold red]{bot.user.name}: Ses kanalı bulunamadı![/bold red]")
            await bot.close()

    await bot.start(token)

# Ana Menü Başlat
if __name__ == "__main__":
    main_menu()

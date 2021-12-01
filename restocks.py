import requests, discord
from bs4 import BeautifulSoup
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix="!")

print("\nPayout tool started\n")

@client.command()
async def r(ctx, *, keyword):
    if "https://" in keyword:
        link = keyword  
    else:        
        q = {
            "q" : keyword,
            "page" : "1",
            "filters[][range][price][gte]": "1"
        }

        search = requests.get("https://restocks.net/it/shop/search?q=", params=q)
        link = search.json()["data"][0]["slug"]


        c_link = link
        s_country = c_link.split('/')
        country = s_country[3]

        link = link.replace(country,'it')
        
    product_page = requests.get(link)

    product = BeautifulSoup(product_page.text, "html.parser")

    prod_info = product.find_all('meta', property='og:title')[0]['content']
    prod_info = list(prod_info.split(" - "))
    name = prod_info[0]
    sku = prod_info[1]
    image = product.find_all('meta', property="og:image")[0]['content']

    size_list = []
    resell_list = []
    consign_list = []

    info = product.find('ul', class_="select__size__list")

    for size in info.find_all('li'):
        if 'all' in str(size):
            sizes = size.find_all('span', class_="text")[0].string
            size_list.append(sizes)
            try:
                price = size.find_all('span', class_='')[0].string
                price = price.replace('€ ', "")
                price = int(price)
                consign = price-(price*0.05)-10
                consign = format(consign, '.2f')
                resell = price-(price*0.1)-10
                resell = format(resell, '.2f')
                consign_list.append(f"{consign} €")
                resell_list.append(f"{resell} €")
            except:
                resell_list.append('N/D')
                consign_list.append('N/D')


    size_list = ('\n'.join(map(str, size_list)))
    resell_list = ('\n'.join(map(str, resell_list)))
    consign_list = ('\n'.join(map(str, consign_list)))

    restocks = discord.Embed(title=name, description="SKU: "+sku, color=discord.Color.dark_purple(), url=link)
    restocks.add_field(name="Size", value=size_list, inline=True)
    restocks.add_field(name="Resell", value=resell_list, inline=True)
    restocks.add_field(name="Consign", value=consign_list, inline=True)
    restocks.set_thumbnail(url=image)
    restocks.set_footer(text="Payout tool by Leoo", icon_url="https://res-2.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/sdx09fktwdflzc7ant9h")

    await ctx.send(embed=restocks)
    author = ctx.message.author
    print(f"{author} sent a request for {link}\n")
    await ctx.message.delete()
    
#insert here your token
client.run('')
        

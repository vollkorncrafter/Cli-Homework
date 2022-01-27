import sqlite3
import click
from rich.console import Console
from rich.table import Table
import random

#Sql
connection = sqlite3.connect('cli-homework.db')
cursor = connection.cursor()
#Table
table = Table(title="Your Homework")
table.add_column("Num", style="magenta")
table.add_column("Subject", style="cyan")
table.add_column("Description", style="magenta")
table.add_column("Due", justify="right",style="green")

#console
console = Console()

#Create Table
try:
    cursor.execute("create table homework (subject text, description text, due text, id integer)")
    #print(bcolors.OKBLUE + "Homework table Sucessfully Created!" + bcolors.ENDC)
except:
    pass

def zeigen():
    i = 0
    for row in cursor.execute("select * from homework"):
        table.add_row(str(row[3]),row[0],row[1],row[2])
        i = i + 1
    connection.close()
    console.print(table)

@click.group()
def cli():
    pass

@click.command()
@click.option("--sub", prompt="Subject?", help="The Subject.")
@click.option("--desc", prompt="Description?", help="The Description.")
@click.option("--due", prompt="Due?", help="Until When?.")
def add(sub,desc,due):
    cursor.execute("insert into homework values(?,?,?,?)",(sub, desc, due,random.randint(1,100)))
    connection.commit()
    connection.close()

@click.command()
@click.option("--deln", prompt="Delete number (x to cancel)", help="Wich row should be deletet?.")
def delete(deln):
    query = 'delete from homework where id="%s"' %deln
    print(query)
    cursor.execute(query)
    connection.commit()
    connection.close()

@click.command()
def show():
    zeigen()

cli.add_command(add)
cli.add_command(delete)
cli.add_command(show)

if __name__ == '__main__':
    cli()

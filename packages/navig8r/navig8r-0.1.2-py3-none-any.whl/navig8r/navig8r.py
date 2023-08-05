"""The Discord bot as well as functionality that allows it to run."""
import discord
from navig8r import util
import gspread
from dotenv import dotenv_values
import typer


CONFIG = dotenv_values('.env')

class MyClient(discord.Client):
    """The Navig8r Discord bot."""
    async def on_ready(self):
        global gc
        gc = gspread.service_account(filename='key.json')
        print(f'Logged on as {self.user}!')


    async def on_message(self, message):
        global gc
        global arg
        embed_color = 0x7289DA
        # Detect bot messages (keep the bot from responding to itself)
        if message.author.bot == False:
            if arg == "introduce":
                await message.delete()
                embed_color = 0x7289DA
                embed_one_text = """Welcome to the **Navig8r** channel! In this channel you can send a message--any message at all--to set up your personal direct message thread with the Navig8r!

                (All messages you enter in this channel will be promptly deleted by the Navig8r. Sending a message simply prompts the Navig8r to set up a DM thread with *your* particular Discord account.)

                So feel free to say 'hello' to the Navig8r here, and watch as it spins up a conversation between the two of you!
                """
                embed_one_object = discord.Embed(title="Getting Started With Navig8r", description=embed_one_text, color=embed_color)
                await message.channel.send(embed=embed_one_object)
                embed_two_text = """Navig8r is a tool for YOU, an Allegheny College student.

                It is *chomping* at the bit to find you all the documents you need in each of your classes to be a successful student. Simply ask Navig8r to fetch, say, a syllabus for your Data Abstraction class, and in seconds it'll have found exactly what you need!

                There's no need to use fancy commands here--just make sure each message you send Navig8r is outfitted with enough *keywords* to help it find exactly what you're looking for."""
                embed_two_object = discord.Embed(title="Using Navig8r", description=embed_two_text, color=embed_color)
                await message.channel.send(embed=embed_two_object)
                embed_three_text = """For example, if you're taking an introductory computer science course and need Navig8r to retrieve an office hours link for the course, you might send the following message in your DM thread with Navig8r:

                *computational expression office hours*

                Navig8r is more conversational than it lets on, so you could also experiment with something like:

                *Hey, Navig8r! I need to set up office hours for CMPSC100!*

                If there's ever a doubt as to what *exactly* you're looking for, Navig8r will ask you for clarification. If you're enrolled in a class with Professor Kapfhammer, and want to get the course calendar for one of his courses, you might search with:

                *Desperately need Kapfhammer class calendar NOW*

                Given that Professor Kapfhammer often teaches more than one class, Navig8r would be unsure of *which* course you need the calendar for, and will respond with suggestions to further refine your search. Search again with one of those suggestions in place and you're sure to find what you're looking for!"""
                embed_three_object = discord.Embed(title="A Few Example Searches", description=embed_three_text, color=embed_color)
                await message.channel.send(embed=embed_three_object)
                arg = "don't introduce"

            else:
                print(message)
                print(type(message.author))
                print(f"Message from {message.author}: {message.content}")
                # Bot channel boilerplate response (set up a DM channel)
                if message.channel.id == int(CONFIG["CHANNEL_ID"]):
                    greeting_embed_content = f"""Hello {message.author.display_name}! I am here to help you find all of the crucial information scattered across the many websites and repositories this college calls their own. But before I get to getting you things, I will need to get some information from *you* to ensure that I can get you **anything** you need.

                    For starters, I'll need that student ID of yours, Gator! In order for me to be able to use it to get things for you, I'll ask you nicely to send it to me in a specifically formatted way. Start with an `ID: ` tag in front, then your **full** student ID, including the leading zeros. The example below should help ...

                    ---------------
                    ID: 001234567
                    ---------------

                    Send that on over to me just like you would with any other Discord message whenever you're ready!
                    """
                    file = discord.File("images/logo.png", filename="logo.png")
                    greeting_embed = discord.Embed(title="Hello from Navig8r!", description=greeting_embed_content, color=embed_color)
                    greeting_embed.set_thumbnail(url="attachment://logo.png")
                    await message.author.send(file=file, embed=greeting_embed)
                    await message.delete()
                # DM channel response
                else:
                    # ID harvest script
                    if "ID:" in message.content:
                        sheet_id = CONFIG["STUDENT_SHEET_ID"]
                        student_id = util.strip_student_id(message.content)
                        discord_id = f"'{message.author.id}"
                        existing_ids = util.retrieve_sheet(gc, sheet_id)
                        add_id_flag = True
                        for existing_id in existing_ids:
                            if discord_id in existing_id:
                                add_id_flag = False
                        if add_id_flag:
                            util.write_data_pair(gc, sheet_id, discord_id, student_id)
                            id_success_embed_content = f"""Your Student ID, {student_id}, has been submitted to my records successfully.

                            If the above ID does not match yours, please contact Professor Kapfhammer for assistance!

                            Otherwise, I am all set to get you anything you need. Just send me a message detailing what you want from me, and I'll see if I can find it for you. If you have any questions about how to use me to my fullest, visit my channel for detailed examples!
                            """
                            id_success_embed = discord.Embed(title="Success!", description=id_success_embed_content, color=embed_color)
                            await message.author.send(embed=id_success_embed)
                        else:
                            id_failure_embed_content = f"""It seems your Discord account is already associated with a student ID in my register.
                            If this seems to be an error, please contact Professor Kapfhammer for assistance!
                            Once this error is resolved, I'll be ready to get you anything you need.
                            """
                            id_failure_embed = discord.Embed(title="I can't do that...", description=id_failure_embed_content, color=embed_color)
                            await message.author.send(embed=id_failure_embed)
                            
                    # Navig8r help script
                    elif "help" in message.content:
                        await message.author.send(f'Let me help you with that!')

                        flag = "id"
                        sheet_id = CONFIG["STARTER_SHEET_ID"]
                        nl = "\n"

                        while flag == "id":
                            sheet_data = util.retrieve_sheet(gc, sheet_id)
                            search_hits = util.search_sheet(sheet_data, message.content)
                            number_hits = len(search_hits)

                            if number_hits == 1:
                                output, flag = util.get_command_or_id(search_hits[0])
                                sheet_id = output
                                flag = "commands"

                            if flag == "commands":
                                command_help_embed_content = f"""I see you need help finding some things, so I gathered a list of commands you can use with your previous search to focus it in."""
                                command_help_field = f"""`{nl.join([command for command in util.get_command_list(gc, sheet_id)])}`"""
                                command_help_embed = discord.Embed(title="Here Is Some Help!", description=command_help_embed_content, color=embed_color)
                                command_help_embed.add_field(name="Command List", value=command_help_field)
                                await message.author.send(embed=command_help_embed)                            

                            else:
                                default_help_embed_content = f"""I see you need help finding some things, so I went ahead and got you a list of courses to kick start the process.
                                 
                                As a side note, if you were trying to get help for one of the courses below, I may not have recognized it in your previous search, so try using the course as it is listed below to help me help you!
                                """
                                default_help_field = f"""`{nl.join([course for course in util.get_command_list(gc, sheet_id)])}`"""
                                default_help_embed = discord.Embed(title="Here Is Some Help!", description=default_help_embed_content, color=embed_color)
                                default_help_embed.add_field(name="Course List", value=default_help_field)
                                await message.author.send(embed=default_help_embed)
                                flag = "helped"
                                  
                    # Navig8r search script
                    else: 
                        await message.author.send(f'Let me get that for you!')
                        flag = "id"
                        sheet_id = CONFIG["STARTER_SHEET_ID"]
                        data_store_id = CONFIG["DATA_STORE_ID"]
                        while flag == "id":
                            sheet_data = util.retrieve_sheet(gc, sheet_id)
                            search_hits = util.search_sheet(sheet_data, message.content)
                            number_hits = len(search_hits)
                            # Check if accessed sheet is a gradebook
                            if gc.open_by_key(sheet_id).sheet1.acell("A1").value == "G8R":
                                flag = "grade"
                                current_student_id = util.retrieve_student_id(gc, CONFIG["STUDENT_SHEET_ID"], f"'{message.author.id}")
                                # Student ID not yet submitted
                                if current_student_id == "not found":
                                    need_id_embed_content = f"""Sorry, I can't retrieve your grade for any courses without first having your Allegheny Student ID. Please send me a message structured in the following fashion: 
                                    
                                    ---------------
                                    ID: 001234567
                                    ---------------
                                    
                                    Once you've submitted your student ID, please ask me for your grade once again and I'll happily retrieve it for you!"""
                                    need_id_embed = discord.Embed(title="I need your Student ID for that...", description=need_id_embed_content, color=embed_color)
                                    await message.author.send(embed=need_id_embed)
                                # Student ID not associated with requested course
                                else:
                                    student, headers, grades, total_grade = util.retrieve_itemized_grade_from_gradebook(gc, sheet_id, current_student_id)
                                    if student == "not found":
                                        not_found_embed_content = f"""Sorry, it doesn't look like your Allegheny Student ID is associated with this course. The student ID I have on record for you is `{current_student_id}`. If this is incorrect, please contact Professor Kapfhammer and let him know!
                                        
                                        In the event that I have your correct student ID on file, please contact your course instructor to ensure that they have the correct ID in their own gradebook data."""
                                        not_found_embed = discord.Embed(title="Your Student ID isn't associated with this course...", description=not_found_embed_content, color=embed_color)
                                        await message.author.send(embed=not_found_embed)
                                    else:
                                        grades_embed_content = f"""I've created a grade report for you {student.title()}!\nIt contains a list of assignment grades, and a total grade."""
                                        grades_embed = discord.Embed(title="Grade Report", description=grades_embed_content, color=util.get_grade_report_color(total_grade))
                                        grades_embed.add_field(name="Assignment Grades", value=f"{util.format_grade_report(headers, grades)}")
                                        grades_embed.add_field(name="Total Grade", value=f"{total_grade}%")
                                        await message.author.send(embed=grades_embed)
                                        search_token = "success"
                                        util.write_data_pair(gc, data_store_id, message.content, search_token)
                            # Perform a regular search
                            else:
                                # Response for no hits
                                if number_hits == 0:
                                    flag = "no_hits"
                                    no_hit_embed_content = f"""I couldn't find anything related to: {message.content}"""
                                    no_hit_field= """Try using a course name as it appears on Self-Service (complete *with* course section), like so: `CMPSC*100-00` 
                                    Follow this with a space and the thing you're looking for, like the *schedule* or *syllabus*, or maybe *tl* office hours!"""
                                    no_hit_embed = discord.Embed(title="Sorry ...", description=no_hit_embed_content, color=embed_color)
                                    no_hit_embed.add_field(name="Pro-tip:", value=no_hit_field)
                                    await message.author.send(embed=no_hit_embed)
                                    search_token = "failure"
                                    util.write_data_pair(gc, data_store_id, message.content, search_token)

                                # Response for exactly one hit
                                elif number_hits == 1:
                                    output, flag = util.get_command_or_id(search_hits[0])
                                    if flag == "cmd":
                                        hit_embed_content = f"""{output}"""
                                        hit_embed = discord.Embed(title="I found this!", description=hit_embed_content, color=embed_color)
                                        await message.author.send(embed=hit_embed)
                                        search_token = "success"
                                        util.write_data_pair(gc, data_store_id, message.content, search_token)
                                    else:
                                        sheet_id = output
                                # Response for multiple hits
                                else:
                                    flag = "mult_hits"
                                    nl = "\n"
                                    mult_hits_embed_content = f"""Turns out there's several things resembling what you're looking for, including:

                                    `{nl.join([hit[0] for hit in search_hits])}`

                                    Could you use one of the above terms to clarify what you're looking for?
                                    """
                                    mult_hits_embed = discord.Embed(title="I need some clarification...", description=mult_hits_embed_content, color=embed_color)
                                    await message.author.send(embed=mult_hits_embed)
                                    search_token = "failure"
                                    util.write_data_pair(gc, data_store_id, message.content, search_token)

app = typer.Typer()
                                    
@app.command()            
def navig8r(introduce: bool = typer.Option(False, "--introduce", "-i", help="Start the bot in introduce mode to print out greeting text once.")):
    global arg
    if introduce:
        arg = "introduce"
    else:
        arg = "don't inroduce"
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(CONFIG["BOT_TOKEN"])

if __name__ == "__main__":
    app()
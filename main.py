from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from canvasapi import Canvas
import wget, pdfkit, random, requests

load_dotenv()
API_URL = os.getenv("API_URL")
access_token = os.getenv("CANVAS_TOKEN")
canvas = Canvas(API_URL, access_token)
valid_course = []
payload ={}
payload['access_token'] = access_token


def create_directory(directory_name):
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists. Renaming Directory")
        directory_name+=random.randint(0, 1000)
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return directory_name


def course_download(index):
    bFiles = True
    course = valid_course[index]
    os.system("cls")
    print(f"You have Selected \"{course.name}\"\n")
    print("Would you Like to Download the resources?")
    print("[Y]es")
    print("[N]o")
    promp = input("Choice: ")

    if promp != 'y' and promp != 'Y':
        return
    
    
    print("Course Files: ")
    files = course.get_files()
    
    #try if files section are forbidden
    try:
        for idx, file in enumerate(files):
            print(f"[{idx}] {file}")
    except Exception as e:
        print("No files or forbidden\n")
        bFiles = False
        
    
    print("Creating File Structure")
    
    #create a unique filepath name to avoid duplicates remove <>:"/\|?* as it is invalid 
    directory_name = course.name + "[" +datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "]"
    directory_name = directory_name.translate({ord(i): None for i in '<>:\"/\\|?*'})
    directory_name = create_directory(directory_name)
    
    file_directory = f"{directory_name}/files"
    file_directory = create_directory(file_directory) + "/"
    modules_directory = f"{directory_name}/modules"
    modules_directory = create_directory(modules_directory) + "/"
    
    print("======================================================================================")
    
    print("Downloading Files (If Any)")
    if bFiles:
        #save the files
        for file in files:
            file_path = file_directory + file.filename.translate({ord(i): None for i in '<>:\"/\\|?*'})
            wget.download(file.url, file_path)
    
    print("======================================================================================")
    
    #save the modules
    print("Modules/Discussion/Pages/Assignment:")
    modules = course.get_modules()
    
    for idx, module in enumerate(modules):
        print("======================================================================================")
        items = module.get_module_items()
        module_name = module.name.translate({ord(i): None for i in '<>:\"/\\|?*'})
        print("\n\n" + module.name)
        
        module_directory = f"{modules_directory}/{module_name}"
        module_directory = create_directory(module_directory) + "/"
        
        file_path = f"{module_directory}/{module_name}.txt"
        external_urls = ""
        payload['access_token'] = access_token
        
        for idx, item in enumerate(items):
            item_title = item.title.translate({ord(i): None for i in '<>:\"/\\|?*'})
            if item.type != "SubHeader":
                if item.type == "Page":
                    r = requests.get(item.url, params=payload)
                    data = r.json()
                    pdfkit.from_string(data.get("body", ""), f"{module_directory}{item_title}.pdf")
                elif item.type == "Assignment":
                    assignment = course.get_assignment(item.content_id)
                    if assignment.description != "":
                        pdfkit.from_string(assignment.description, f"{module_directory}{item_title}.pdf")        
                elif item.type == "Discussion":
                    discussion = course.get_discussion_topic(item.content_id)
                    pdfkit.from_string(discussion.message, f"{module_directory}{item_title}.pdf")
                elif item.type == "ExternalUrl":
                    external_urls += f"[{item.title}] {item.external_url}\n"
                elif item.type == "File":
                    file = course.get_file(item.content_id)
                    file_path = module_directory + file.filename.translate({ord(i): None for i in '<>:\"/\\|?*'})
                    wget.download(file.url, file_path)
                
                print(item_title + " Saved")

        if external_urls != "":
            external_file = open(file_path, 'a')
            external_file.write(external_urls)
        print("======================================================================================")
        
    print("Download Finished")
    


def main():
    while True:
        os.system("cls")
        print("All Courses in your Account")
        data = canvas.get_courses()    
        
        #reset the values of the variable
        idx = 0
        valid_course.clear()
        
        for course in data:
            name = vars(course).get('name')
            if name:
                print(f"[{idx}] {name}")  # Prints all instance attributes as a dictionary
                valid_course.append(course)
                idx += 1
        print("[-1] Exit")
        
        prompt = int(input("Enter index to Download: "))
        
        if prompt >= 0 and prompt < idx:
            course_download(prompt)
            input("Enter to continue...")
        elif prompt == -1:
            break
        else: print("Error Invalid index.")
    
    print("Thank You For Using :3 Bye!!!")

if __name__  == "__main__":
    main()
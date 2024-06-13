import sqlite3
import os

#Establishes conection to sqlite studio and the database
connection = sqlite3.connect("/Users/louisbuchanan/Documents/DIT/DataBases/Food_production_emmisions.db")
cursor = connection.cursor()

#Returns all food as a tuple
def get_all_foods():
    #cursor.execute opens a cursor to input the comant in the brackets in sqlite studio
    cursor.execute("SELECT * FROM AFP")
    foods = cursor.fetchall()
    
    return foods

#gets all names
def get_all_names():
    cursor.execute("SELECT name FROM AFP")
    return cursor.fetchall()

#Returns all feild names as a string
def get_all_fields():
    #when I looked it up it seemed too advanced to retreive the feilds from sqlite so I wrote them here scince I knew I would use them more
    return ("Id", "Name", "Avg_weight_produced_yearly_kg", "Avg_carbon_produced_yearly_kg", "Avg_carbon_per_100kg_yearly", "Avg_food_waste_yearly_kg_yearly", "Avg_food_waste_per_100kg_yearly", "Avg_packaging_weight_yearly_kg", "Avg_packaging_weight_per_100kg_yearly")

#Retuns a selected food and its data as a string
def get_one_food():
    
    #selects all names of foods and stores the infomation in "names"
    names = get_all_names()
    
    
    #Creates a string of food names and stores it in the readable_names variable
    readable_names = ""
    for i in range(len(names)):
        readable_names = readable_names + str(names[i])[2:-3] + "\n "

    #Asks the user to enter a food from the readable_names string and checks if their answer is valid
    while True:
        #user is directed to enter a food to look at which is stored in the 'food' varibale
        food = input("\n\nPlease select a food:\n \n" + readable_names + " \n\n>") 
        
        #this variable is in order to make a break affect a loop outisde the loop of the code that needs to break it
        should_break = False
        
        #checks if the inputed string is a valid name of an item
        for i in range(len(names)): 
            
            #name cycles through the different names of food items each time it loops
            name = str(names[i])
            
            #checks if the inputed name is a vaild name by checking if it is the same name as name
            if str(food.lower()) == str(name[2:-3].lower()):
                should_break = True
                break

        #breaks the bigger while loop if the inputed name was a valid name or tells the user to check for typos if not
        if should_break:
            break
        else:
            print("\n\nCheck for typos!")

    #all_foods is a list of all data
    all_foods = get_all_foods()
    #readable_foods is used to gather all data for selected food and combine it with its respective food for reading
    readable_foods = ""
    
    #
    for i in range(len(all_foods)):
        readable_foods = readable_foods + str(all_foods[i])[2:-3] + ", "
        
    cursor.execute("SELECT * FROM AFP WHERE name = '" + food[0].upper() + food[1:] + "'")
    food = cursor.fetchall()
    
    
    feilds = get_all_fields()
    readable_names = "\n\n"
    for i in range(len(feilds)):
        readable_names =  readable_names + feilds[i] + ": " + str(food[0][i]) + "\n"
        
    
    
     
    return readable_names
    
#Returns all data sorted by a chosen feild
def order_products():
    foods = get_all_names()
    print("What would you like to order your informtion by?")
    thing = ""
    for i, thing in enumerate(get_all_fields()):
        print("(" + str(i+1) + ") " + thing)
    
    while True:
        order_by_feild = input("\n\n> ")
        try:
            if int(order_by_feild) >= 1 and int(order_by_feild) <= 9:
                feild = get_all_fields()[int(order_by_feild)-1]
                break
            else:
                print("Please enter a number between 1 and 9!")
        except ValueError:
            print("Please enter a number between 1 and 9!")
    
    while True:
        ascdec = input("Would you like to order your data in ascending/alphabetical order (1) or in descending/reverse alphabetical order? (2)\n\n> ")
        if ascdec == "1":
            ascdec = "ASC"
            break
        elif ascdec == "2":
            ascdec = "DESC"
            break
        print("Please enter 1 or 2!")

            
    cursor.execute("SELECT * FROM AFP  ORDER BY " + get_all_fields()[int(order_by_feild)-1].lower() + " " + ascdec)
    
    
    return cursor.fetchall()

#makes data clear for the user
def read(data):
    
        
        
    new_data = ""
    
    
    for i in range(len(data)):
            new_data = new_data + "\n" + str(data[i])[1:-1]

    #returns readable data
    return new_data

#makes the names reaable
def read_names(data):
    new_data = ""
    
    
    for i in range(len(data)):
            new_data = new_data + "\n" + str(data[i])[2:-3]

    #returns readable data
    return new_data

#asks the user how they want to filter the data and outputs the filtered data
def filter_foods(foods):
    #asks the user would like to filter by
    print("What would you like to filter your informtion by?")

    #prints out all information of the chosen item
    for i, foods in enumerate(get_all_fields()):
        print("(" + str(i+1) + ") " + foods)

    
    #recevies the users answer for what they wnat to filster by and storses it in the filter_by variable
    while True:
        filter_by = input("\n\n> ")
        #checks to see if the users input is an int and a valid number
        try:
            if int(filter_by) >= 1 and int(filter_by) <= 9:
                feild = get_all_fields()[int(filter_by)-1]
                break
            else:
                
                #runs if user input was not between 1 and 9
                print("Please enter a number between 1 and 9!")
        
        #runs if user input was not a number
        except ValueError:
            print("Please enter a number between 1 and 9!")
    
    
    try:
        
        cursor.execute("SELECT " + get_all_fields()[int(filter_by)-1].lower() + " FROM AFP")
        selected_values = cursor.fetchall()

        #finds the biggest and smallest values of the selected field

        for i in range(len(selected_values)):
            
            min = selected_values[0]
            max = selected_values[0]
            if min > selected_values[i]:
                min = selected_values[i]
            if max < selected_values[i]:
                max = selected_values[i]

        
        while True:
            try:
                print("The lowest " + get_all_fields()[int(filter_by)-1].lower() + " is " + str(min)[1:-2])
                min = float(input("\nWhat would you like the new minimum value to be?\n\n> "))
                break
            except ValueError:
                print("Please enter a number!")
        while True:
            try:
                print("The highest " + get_all_fields()[int(filter_by)-1].lower() + " is " + str(max)[1:-2])
                max = float(input("\nWhat would you like the maximum value to be?\n\n> "))
                break
            except ValueError:
                print("Please enter a number!")
        

    except ValueError:

        return(get_one_food())


            
    cursor.execute("SELECT * FROM AFP WHERE " + get_all_fields()[int(filter_by)-1].lower() + " >= " + str(min) + " AND " + get_all_fields()[int(filter_by)-1].lower() + " <= " + str(max) + " ORDER BY " + get_all_fields()[int(filter_by)-1].lower() + " DESC")
    final_data = cursor.fetchall()
    
    try:
        final_data[0] 
    except IndexError:
        print("\n\nThere is no data with these specifications!")
    
    return final_data

#asks the user for a product and field of that prodect and lets them change its value
def replace_data():
    
    #selects all names of foods and stores the infomation in "names"
    names = get_all_names()
    
    
    #Creates a string of food names and stores it in the var variable
    readable_names = ""
    for i in range(len(names)):
        readable_names = readable_names + str(names[i])[2:-3] + "\n "

    #Asks the user to enter a food from the var string and checks if their answer is valid
    while True:
        food = input("\n\nWhich food would you like to repace the data of?\n \n" + readable_names + " \n\n>") 
        
        
        var1 = ""
        
        
        for i in range(len(names)): 
            
            thing = str(names[i])
            
            if str(food.lower()) == str(thing[2:-3].lower()):
                var1 = "i"
                break
                
        if var1 == "i":
            break
        else:
            print("\n\nCheck for typos!")

    all_foods = get_all_foods()
    readable_foods = ""
    
    for i in range(len(all_foods)):
        readable_foods = readable_foods + str(all_foods[i])[2:-3] + ", "
        
    cursor.execute("SELECT * FROM AFP WHERE name = '" + food[0].upper() + food[1:] + "'")
    food = cursor.fetchall()
    
    
    feilds = get_all_fields()
    var = "\n\n"
    for i in range(len(feilds)):
        var =  var + feilds[i] + ": " + str(food[0][i]) + "\n"
        
    os.system("clear")
    print("Which feild would you like to replace?\n")
    thing = ""
    for i, thing in enumerate(get_all_fields()):
        print("(" + str(i+1) + ") " + thing)
    
    while True:
        var1 = input("\n\n> ")

        if var1 == "1":
            print("You may not change the ID!")
            continue
        elif var1 == "2":
            print("You may not change the Name!")
            continue

        try:
            if int(var1) >= 1 and int(var1) <= 9:
                feild = get_all_fields()[int(var1)-1]
                break
            else:
                print("Please enter a number between 1 and 9!")
        except ValueError:
            print("Please enter a number between 1 and 9!")
    
    
    cursor.execute("SELECT " + get_all_fields()[int(var1)-1].lower() + " FROM AFP WHERE name = '" + food[0][1] + "'")
    data = cursor.fetchall()
    
    os.system("clear")
    while True:
        
        print(food[0][1] + "'s current " + get_all_fields()[int(var1)-1].lower() + " value is: " + str(data[0])[1:-2])
        try:
            float(str(data[0])[1:-2])
            value = int
            
        except ValueError:
            value = str
            
        
        new_data = input("\nWhat would you like to change it to?\n\n> ")
        
        try:
            float(new_data)
            value2 = int
            
        
        except ValueError:
            value2 = str
            
        os.system("clear")
        

        if value == value2:
            break
        
        if value == int:
            print("Please enter a number!\n")
        if value == str:
            print("Please enter a word!\n")
    
    cursor.execute("UPDATE AFP SET " + get_all_fields()[int(var1)-1].lower() + " = " + new_data + " WHERE name = '" + food[0][1] + "'")   
    return read(get_all_foods())

#menu
def start():
    
    os.system("clear")
    action = input("What would you like to do?\n\n(1) Show all data\n(2) Show all product names \n(3) Sort all data \n(4) Filter all data\n(5) Select one product \n(6) Replace data\n\n> ")
    os.system("clear")
    while True:
        try:
            os.system("clear")
            if action in ["3", "sort all data"]:
                print(read(order_products()))
            
            elif action.lower() in ["5", "select one product"]:
                print(get_one_food())

            
            elif action.lower() in ["2", "show all product names"]:
                print(read_names(get_all_names()))

            
            elif action.lower() in ["1", "show all data"]:
                print(read(get_all_foods()))

            
            elif action.lower() in ["4", 'filter all data']:
                print(read(filter_foods(get_all_foods())))

            elif action.lower() in ["6", 'replace data']:
                print(replace_data())
            
            else:
                os.system("clear")
                print("Please enter a number between 1 and 6!")
                action = input("\n\nWhat would you like to do?\n\nShow all data(1)\nShow all product names(2)\nSort all data (3)\nFilter all data(4)\nSelect one product (5)\n\n> ")
                
                continue
                
            input("\n\nPress Enter to Contimue ")
            break

        except ValueError:

            print("Please enter a number!")

    
while True: start()
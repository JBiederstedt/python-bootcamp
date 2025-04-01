#Greeting
welcome = "Welcome to the Band Name Generator"
print(welcome)

#Ask the user where they grew up.
city = input("What's the name of the city you grew up in?\n").capitalize()

#Ask the user for a pet's name.
pet = input("What was your pet's name? \n").capitalize()

#Combine the name of city and pet's name and show the band name.
print("Your band name could be " + city + " " + pet)

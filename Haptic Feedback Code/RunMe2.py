#################################################
# This asks the user which function they would  #
# like to see, and loads that one. Ideally,     #
# this won't be needed, and instead the choice  #
# of function and the function will all be part #
# of one file.                                  #
#################################################

if __name__ == '__main__':
    print "What function do you want? Here are your choices."
    print "2^x"
    print "sin(x)"
    print "y = x"
    print "y = x^2"
    print "xz plane"
    print "yz plane"
    retry = True
    while retry == True: #continually prompts user until they pick a recognized function
        choice = raw_input("Please pick one of these! Hit enter after typing your choice here: ").lower()
        if choice == "2^x":
            retry = False
            print "Loading..."
            execfile("exp.py") #executes the file that corresponds to the picked function
        elif choice == "sin(x)" or choice == "sinx": #can interpret it with or without parentheses
            retry = False
            print "Loading..."
            execfile("sinx.py")
        elif choice == "y = x" or choice == "y=x":
            retry = False
            print "Loading..."
            execfile("x.py")
        elif choice == "y = x^2" or choice == "y=x^2":
            retry = False
            print "Loading..."
            execfile("x2.py")
        elif choice == "yz plane":
            retry = False
            print "Loading..."
            execfile("xplane.py")
        elif choice == "xz plane":
            retry = False
            print "Loading..."
            execfile("yplane.py")
        else:
            print "I'm sorry, I didn't get that."

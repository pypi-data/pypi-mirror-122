# from TriesImplementation.TrieNode import TrieImplement
from TrieNode import TrieImplement
import sys


def main():
    if len(sys.argv) == 1:
        print("No Argument Passed!")

    else:
        T = TrieImplement()
        firsttime = True
        # loop = True
        while True:
            if firsttime == True:
                if sys.argv[1] == "--populate":
                    if len(sys.argv) != 3:
                        print("Invalid Arguments!")
                    else:
                        y = sys.argv[2].split(", ")
                        T.populate_trie(y)

                elif sys.argv[1] == "--insert":
                    if len(sys.argv) != 3:
                        print("Invalid Arguments!")
                    else:
                        T.insert(sys.argv[2])

                elif sys.argv[1] == "--display":
                    T.display()

                elif sys.argv[1] == "--search":
                    if len(sys.argv) != 3:
                        print("Invalid Arguments!")
                    else:
                        T.search(sys.argv[2])
                elif sys.argv[1] == "--delete":
                    if len(sys.argv) != 3:
                        print("Invalid Arguments!")
                    else:
                        T.delete(sys.argv[2])
                elif sys.argv[1] == "--autocomplete":
                    if len(sys.argv) != 3:
                        print("Invalid Arguments!")
                    else:
                        T.auto_complete(sys.argv[2])
                else:
                    print("Not a correct function!")
                firsttime = False
            else:
                bikhmango = input("Want to continue(T, F): ")
                if bikhmango == "T":
                    function = input("Enter the function you want to perform: ")
                    arguments = input(
                        "Enter the parameters you want to pass for the function: "
                    )
                    if function == "--populate":
                        if arguments == "":
                            print("Invalid Arguments!")
                        else:
                            y = arguments.split(", ")
                            T.populate_trie(y)

                    elif function == "--insert":
                        if arguments == "":
                            print("Invalid Arguments!")
                        else:
                            T.insert(arguments)

                    elif function == "--display":
                        T.display()

                    elif function == "--search":
                        if arguments == "":
                            print("Invalid Arguments!")
                        else:
                            # print(T.search(arguments))
                            if T.search(arguments):
                                print("Found!")
                            else:
                                print("Not Found!")
                    elif function == "--delete":
                        if arguments == "":
                            print("Invalid Arguments!")
                        else:
                            T.delete(arguments)
                    elif function == "--autocomplete":
                        if arguments == "":
                            print("Invalid Arguments!")
                        else:
                            print(T.auto_complete(arguments))
                    else:
                        print("Not a correct function!")
                else:
                    # loop = False
                    break

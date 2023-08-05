from typing import List


class TrieNode:
    """
    Trie Node class
    """

    def __init__(self):
        """
        children : dictionary containing children of the parent node
        isTerminate : boolean to check if the node is a leaf node
        """
        self.children = {}
        self.IsTerminate = False


class TrieImplement:
    def __init__(self) -> None:
        self.root = TrieNode()

    def populate_trie(self, words):
        """
        Method for populating trie with words
        """
        for word in words:
            print(word)
            self.insert(word)
        print("Trie populated with words")

    def insert(self, word):
        """
        Method for inserting a word in a trie
        Working :- This Method is going throught each char in a word and checking if the char is not in the children of the node. If not then it creates a new node and adds it to the children of the node. If the char is in the children of the node then it goes to the next node.
                   After that it checks if the node is a leaf node. If it is then it sets the IsTerminate to True.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.IsTerminate = True

    def search(self, word):
        """
        Method  for searching a word in a Trie.
        Working :- This Method is going throught each char in a word and checking if the char is not in the children of the node. If not then it returns False. If the char is in the children of the node then it goes to the next node.
        """
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        return node.IsTerminate

    def _tra_trie(self, node, word, word_list):
        """
        Method for walking through the trie
        Working:- This method is checking whether it is nodes children and if yes then looping over each char in that children and making a new word by adding the char to the word. if isterminate is True
        then it appends the word to the word_list.
        """
        if node.children:
            for char in node.children:
                word_new = word + char
                if node.children[char].IsTerminate:
                    word_list.append(word_new)
                self._tra_trie(node.children[char], word_new, word_list)

    def auto_complete(self, partial_word):
        """
        Method for auto complete given a partial word!
        Working:- This method is going through each char in partial word and checking if the char in the children of the node. If yes, it makes the nodes equals to the children of that character. if not
        returns the list of words. If isTerminate is true then it appends the partial word to the list. then it is traversing the trie and appending the words to the list.
        """
        node = self.root
        word_list = []
        for char in partial_word:
            if char in node.children:
                node = node.children[char]
            else:
                return word_list
        if node.IsTerminate:
            word_list.append(partial_word)
        self._tra_trie(node, partial_word, word_list)
        return word_list

    # delete a word from the trie
    def delete(self, word):
        """
        Method for deleting a word from the trie
        Working:- This method is going through each char in a word and checking if the char is not in the children of the node. If not then it returns False. If the char is in the children of the node then it goes to the next node.
        """
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return False
        if node.IsTerminate:
            node.IsTerminate = False
            return True
        else:
            return False

    # display trie elements
    def display(self):
        """
        Method for displaying the elements in the Trie
        """
        self._display(self.root, "")

    def _display(self, node, prefix):
        """
        Working;- If isTerminate is set to true, then it print out the prefix and it loops through each character in the children of the node and it calls the display method recursively.
        """
        if node.IsTerminate:
            print(prefix)
        for char in node.children:
            self._display(node.children[char], prefix + char)


class TestUtils:
    def __init__(self, T) -> None:
        self.T = T

    def test_populate(self, words) -> None:
        self.T.populate_trie(words)

    def test_search(self, word: str) -> bool:
        return self.T.search(word)

    def test_autocomplete(self, prefix: str) -> List[str]:
        return self.T.auto_complete(prefix)

    def test_delete(self, word: str) -> None:
        self.T.delete(word)

    def display(self) -> None:
        self.T.display()


if __name__ == "__main__":
    Trie = TrieImplement()
    words = ["the", "a", "there", "answer", "any", "by", "bye", "their"]
    T = TestUtils(Trie)
    T.test_populate(words)
    T.test_search("the")
    T.test_search("these")
    T.test_autocomplete("th")
    T.test_delete("the")
    T.display()

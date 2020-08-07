from xmlrpc.client import ServerProxy

proxy = ServerProxy('http://localhost:3000')

if __name__ == "__main__":
    text = "I hope you are also a fan of Elvis!"
    concept1 = "music"
    concept2 = "engineer"
    print("semantic similarity of:\n{}\n \tand \n{}\n {}".format(text, concept1, proxy.get_semantic_similarity_concept(text, concept1)))
    print("semantic similarity of:\n{}\n \tand \n{}\n {}".format(text, concept2, proxy.get_semantic_similarity_concept(text, concept2)))
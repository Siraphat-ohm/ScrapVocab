from vocab_attributes import *


def main() :
    vocab = Vocab('programming').__dict__
    for att in vocab:
        if( att != "user_agent" ):
            print(att, ":", vocab[att])

if __name__ == "__main__":
    main()

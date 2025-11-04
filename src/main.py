import os
import shutil
from textnode import TextNode, TextType


def main():



def copy(fromdir, todir):

    if not os.path.exists(todir):
        raise Exception(f"the destination dir does not exists!")

    
    contents = os.listdir(fromdir)





copy("static")





if __name__ == "__main__":
    main()
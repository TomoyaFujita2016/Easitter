# encoding: utf-8
import pyfiles
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--run",\
        help="Please choose a mode. \
        (fv: favorite, fl: flatter, sc: scraping, \
        uf: unfollow, fo: follow, fb: followBack)")
parser.add_argument("--tag",\
        help="When you use '--run sc', you can choose search tag.\
        example: '--tag cat,dog,mouse' (default: クラフトビール)")
parser.add_argument("--url", help="Search from hint of image url.")
parser.add_argument("-face", help="Detect face", action="store_true")
parser_args = parser.parse_args()


if __name__=='__main__':
    print("\033[92m=================================================")
    print("==== (´･ω･･`) Welcome to Easitter ! (･Д･｀) ====")
    print("=================================================\033[0m")

    MODE = None
    # mode
    if parser_args.run:
        MODE = str(parser_args.run)
    # face
    if parser_args.face:
        byFace = True
    else:
        byFace = False

    try: 

        # api setup
        CCAA = pyfiles.twitterApiSetup.getAccessKeys()
        easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3])

        if MODE == "fv":
            pyfiles.favorite.main(easitter)
            raise Exception
        if MODE == "fl":
            pyfiles.flatterFavo.main(easitter)
            raise Exception
        if MODE == "sc":
            print("MODE: scraping")
            if parser_args.tag:
                tags = parser_args.tag.replace('"', "").split(",")
                pyfiles.scrapingImages.main(easitter, TAGS=tags, byFACE=byFace)
            else:   
                pyfiles.scrapingImages.main(easitter, byFACE=byFace)
            raise Exception
        if MODE == "uf":
            pyfiles.Unfollow.main(easitter)
            raise Exception
        if MODE == "fo":
            if parser_args.tag:
                tags = parser_args.tag.replace('"', "").split(",")
                pyfiles.follow.main(easitter, tags)
            else:
                print("Please input Tag!")

            raise Exception
        if MODE == "fb":
            pyfiles.followBack.main(easitter)
            raise Exception

        print("==== ***Please choose a mode !***")
        print("==== 'python3 easitter.py --run [option]'")
        print("==== fv: favorite, fl: flatter, sc: scraping,uf: unfollow, fo: follow, fb: followBack")
    
    except Exception as e:
        print(e)
        pass




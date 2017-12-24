# encoding: utf-8
import pyfiles
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--run",\
        help="Please choose a mode. \
        (fv: favorite, fl: flatter, sc: scraping, \
        uf: unfollow, fo: follow, fb: followBack, ar: autoReply)")
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

        if MODE == "ar":
            easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3], byGetF=False)
            pyfiles.autoReply.main(easitter)
            raise Exception
        
        if MODE == "fv":
            easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3], byGetF=False)
            pyfiles.favorite.main(easitter)
            raise Exception
        
        if MODE == "fl":
            easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3], byGetF=False)
            pyfiles.flatterFavo.main(easitter)
            raise Exception
        
        if MODE == "sc":
            print("MODE: scraping")
            easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3], byGetF=False)
            if parser_args.tag:
                tags = parser_args.tag.replace('"', "").split(",")
                pyfiles.scrapingImages.main(easitter, TAGS=tags, byFACE=byFace)
            else:   
                pyfiles.scrapingImages.main(easitter, byFACE=byFace)
            raise Exception
        
        if MODE == "uf":
            easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3], byGetF=True)
            pyfiles.Unfollow.main(easitter)
            raise Exception
        
        if MODE == "fo":
            easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3], byGetF=False)
            if parser_args.tag:
                tags = parser_args.tag.replace('"', "").split(",")
                pyfiles.follow.main(easitter, tags)
            else:
                print("Please input Tag!")

            raise Exception
        
        if MODE == "fb":
            easitter = pyfiles.Easitter.Easitter(CK=CCAA[0], CS=CCAA[1], AT=CCAA[2], AS=CCAA[3], byGetF=True)
            pyfiles.followBack.main(easitter)
            raise Exception

        print("==== ***Please choose a mode !***")
        print("==== 'python3 easitter.py --run [option]'")
        print("==== fv: favorite, fl: flatter, sc: scraping,uf: unfollow, fo: follow, fb: followBack")
    
    except Exception as e:
        print(e)
        pass




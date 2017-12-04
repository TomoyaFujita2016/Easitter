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
    print("=================================================")
    print("==== (´･ω･･`) Welcome to Easitter ! (･Д･｀) ====")
    print("=================================================")
    
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
        if MODE == None:
            print("==== ***Please choose a mode !***")
            print("==== 'python3 easitter.py --run [option]'")
            print("==== fv: favorite, fl: flatter, sc: scraping,uf: unfollow, fo: follow, fb: followBack, se: search image url")
            raise Exception
        
        # api setup
        ATAS = pyfiles.twitterApiSetup.getAccessKeys()
        easitter = pyfiles.Easitter.Easitter(AT=ATAS[0], AS=ATAS[1])

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
                pyfiles.scrapingImages.main(TAGS=tags, byFACE=byFace)
            else:   
                pyfiles.scrapingImages.main(byFACE=byFace)
            raise Exception
        if MODE == "uf":
            print("MODE: unfollow")
            pyfiles.Unfollow.main()
            raise Exception
        if MODE == "fo":
            print("MODE: follow")
            if parser_args.tag:
                tags = parser_args.tag.replace('"', "").split(",")
                pyfiles.follow.main(tags)
            else:
                print("Please input Tag!")

            raise Exception
        if MODE == "fb":
            print("MODE: followBack")
            pyfiles.followBack.main()
            raise Exception
        if MODE == "se":
            print("MODE: search image url")
            if parser_args.url:
                urls = parser_args.url.split(",")
                pyfiles.searchImgUrl.main(urls)
            else:
                print("Please input url.")
                print("ex: --url jkndfac, sefbsdv")
            raise Exception
    except Exception as e:
        print(e)
        pass
    



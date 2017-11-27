# encoding: utf-8
import pyfiles
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--run", help="Please choose a mode. (fv: favorite, fl: flatter, sc: scraping, uf: unfollow, fo: follow, fb: followBack)")
parser_args = parser.parse_args()

if __name__=='__main__':
    print("Welcome to Easitter !")
    MODE = "fv"
    if parser_args.run:
        MODE = str(parser_args.run)
    try: 
        if MODE == "fv":
            print("MODE: favorite")
            pyfiles.favorite.main()
            raise Exception
        if MODE == "fl":
            print("MODE: flatter")
            pyfiles.flatterFavo.main()
            raise Exception
        if MODE == "sc":
            print("MODE: scraping")
            pyfiles.scrapingImages.main()
            raise Exception
        if MODE == "uf":
            print("MODE: unfollow")
            pyfiles.Unfollow.main()
            raise Exception
        if MODE == "fo":
            print("MODE: follow")
            pyfiles.follow.main()
            raise Exception
        if MODE == "fb":
            print("MODE: followBack")
            pyfiles.followBack.main()
            raise Exception
    except Exception:
        pass
    



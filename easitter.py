# encoding: utf-8
import pyfiles
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--run", help="Please choose a mode. (fv: favorite, fl: flatter, sc: scraping, uf: unfollow, fo: follow, fb: followBack)")
parser.add_argument("--tag", help="When you use '--run sc', you can choose search tag. example: '--tag cat,dog,mouse' (default: クラフトビール)")
parser_args = parser.parse_args()

if __name__=='__main__':
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    print(OKBLUE + "=================================================" + ENDC)
    print(OKBLUE + "\n==== (´･ω･･`)"+ENDC+OKGREEN+ " Welcome to Easitter !"+ ENDC + OKBLUE+" (･Д･｀) ====\n" + ENDC)
    print(OKBLUE + "=================================================" + ENDC)
    MODE = "none"
    if parser_args.run:
        MODE = str(parser_args.run)
    try: 
        if MODE == "none":
            print(WARNING + "==== ***Please choose a mode !***")
            print("==== 'python3 easitter.py --run [option]'")
            print("==== fv: favorite, fl: flatter, sc: scraping, uf: unfollow, fo: follow, fb: followBack" + ENDC)
            raise Exception
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
            if parser_args.tag:
                tags = parser_args.tag.split(",")
                pyfiles.scrapingImages.main(TAGS=tags)
            else:   
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
    



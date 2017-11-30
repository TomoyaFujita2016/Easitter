# encoding: utf-8
import pyfiles
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--run", help="Please choose a mode. (fv: favorite, fl: flatter, sc: scraping, uf: unfollow, fo: follow, fb: followBack)")
parser.add_argument("--tag", help="When you use '--run sc', you can choose search tag. example: '--tag cat,dog,mouse' (default: クラフトビール)")
parser.add_argument("--url", help="Search from hint of image url.")
parser.add_argument("-face", help="Detect face", action="store_true")
parser_args = parser.parse_args()


if __name__=='__main__':
    red = "\033[31m"
    OKGREEN = '\033[92m'
    end = '\033[0m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    print(OKBLUE + "=================================================" + end)
    print(OKBLUE + "==== (´･ω･･`)"+end+OKGREEN+ " Welcome to Easitter !"+ end + OKBLUE+" (･Д･｀) ====" + end)
    print(OKBLUE + "=================================================" + end)
    MODE = "none"
    
    if parser_args.run:
        MODE = str(parser_args.run)
    if parser_args.face:
        byFace = True
    else:
        byFace = False
    try: 
        if MODE == "none":
            print(WARNING + "==== ***Please choose a mode !***")
            print("==== 'python3 easitter.py --run [option]'")
            print("==== fv: favorite, fl: flatter, sc: scraping, uf: unfollow, fo: follow, fb: followBack, se: search image url" + end)
            raise Exception
        if MODE == "fv":
            print(red+"MODE: favorite"+end)
            pyfiles.favorite.main()
            raise Exception
        if MODE == "fl":
            print(red+"MODE: flatter"+end)
            pyfiles.flatterFavo.main()
            raise Exception
        if MODE == "sc":
            print(red+"MODE: scraping"+end)
            if parser_args.tag:
                tags = parser_args.tag.replace('"', "").split(",")
                pyfiles.scrapingImages.main(TAGS=tags, byFACE=byFace)
            else:   
                pyfiles.scrapingImages.main(byFACE=byFace)
            raise Exception
        if MODE == "uf":
            print(red+"MODE: unfollow"+end)
            pyfiles.Unfollow.main()
            raise Exception
        if MODE == "fo":
            print(red + "MODE: follow" + end)
            if parser_args.tag:
                tags = parser_args.tag.replace('"', "").split(",")
                pyfiles.follow.main(tags)
            else:
                print("Please input Tag!")

            raise Exception
        if MODE == "fb":
            print(red + "MODE: followBack" + end)
            pyfiles.followBack.main()
            raise Exception
        if MODE == "se":
            print(red+"MODE: search image url" + end)
            if parser_args.url:
                urls = parser_args.url.split(",")
                pyfiles.searchImgUrl.main(urls)
            else:
                print(red+"Please input url." + end)
                print("ex: --url jkndfac, sefbsdv")
            raise Exception
    except Exception as e:
        print(e)
        pass
    



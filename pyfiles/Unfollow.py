# coding: utf-8

def main(easitter):
    print("MODE: Unfollow")
    unFollowCnt = 0
    me = easitter.ME 
    friendIds = easitter.getFriendIds(me)
    print("%d friends is loaded !"%len(friendIds))
    try:

        for fId in friendIds:
            byU, messageC = easitter.byFollowBack(fId)
            message = "Not destroyed !"
            if not byU:
                code, message = easitter.unfollow(fId)
                if code == 1:
                    unFollowCnt += 1
            print("[%3d] %s %s" %(unFollowCnt, message, messageC))

    except KeyboardInterrupt:
        print("\nunFollow is done !")
        print("CNT: "+str(unFollowCnt))

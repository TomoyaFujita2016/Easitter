# coding: utf-8

def main(easitter):
    print("MODE: Follow Back")
    FollowCnt = 0
    FollowLimit = 350
    me = easitter.ME 
    try:
        followerIds = easitter.getFollowerIds(me)

        for fId in followerIds:
            
            byF, message = easitter.byFollowBack(fId)
            if byF:
                code, message = easitter.follow(fId)
                if code == 1:
                    FollowCnt += 1
            print("[%3d] %s" %(FollowCnt, message))

    except KeyboardInterrupt:
        print("\nFollowing Back is done !")
        print("CNT: "+str(FollowCnt))

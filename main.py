# imports
from instapy import InstaPy
from instapy import smart_run
import os
import pathlib



# login credentials
import keys
insta_username = keys.insta_username
insta_password = keys.insta_password

##Script para borrar las cookies antes de cada inicio de sesión, de esta forma instagram no tiene tan facil supervisar nuestra cuenta. Menos posibilidades de ser banneados.
def clear_cookies():
    file = pathlib.Path("../../../InstaPy/logs/whereisean/whereisean_cookie.pkl")   ## Deberias buscar tu carpeta de Instapy, y sustituir el path a tu cuenta.
    if file.exists ():
        os.remove("../../../InstaPy/logs/whereisean/whereisean_cookie.pkl")  ## Deberias buscar tu carpeta de Instapy, y sustituir el path a tu cuenta.
        print("cookies borradas")
    else:
        print("El archivo de cookies no existe, o no se ha encontrado")
        pass

clear_cookies()
##########################


session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False)

######Setting options that we can change
#For set_do_Like
isDoLike = True
doLikePercentage = 70

##for set_do_comment
isDoComment = False
doCommentPercentage = 20

isDoFollow = False
doFollowPercentage = 70


interactionsByUser = 2
interactionsPercentage = 80

isRelationBounds = False
MaxFollowers = 0
MinFollowers = 0
MaxFollowing = 0
MinFollowing = 0


optRelationship = input("Do you want to filter Max/min followers/following? Y/N")
if (optRelationship == "Y"):
    isRelationBounds = True

    print("Lets setup the audience you'd like to target")

    MaxFollowers = int(input("MaxFollowers: "))
    MinFollowers = int(input("MinFollowers: "))
    MaxFollowing = int(input("MaxFollowing: "))
    MinFollowing = int(input("MinFollowing: "))



with smart_run(session):
    ####Settin up the strategy############

    #### SIMULATING USER INTERACTIONS
    ##- stochastic = limita los peak follow a una cifra aleatoria, similar a la indicada.
    ##- Peak_follows /unfollows/likes.. = limita el nº de interacciones repectivamente (por hora, al dia)


    session.set_quota_supervisor(enabled=True, peak_follows_hourly=100, peak_unfollows_hourly=40, peak_likes_hourly=200, peak_server_calls_hourly=600)

    #COnfigura a que usuarios queremos seguir, dependiendo de cuantos seguidores tienen.
    # - Potency ratio -> Hace un ratio usando la formula Seguidores/siguiendo, si está por encima le sigue.
    # - Max Posts min posts -> Limita por la cantidad de posts que cuenta el usuario
    session.set_relationship_bounds(enabled=isRelationBounds, potency_ratio=None, delimit_by_numbers=True, max_followers=MaxFollowers, max_following=MaxFollowing, min_followers=MinFollowers, min_following=MinFollowing)


    #session.set_relationship_bounds(enabled=True)
    session.set_do_like(enabled=isDoLike, percentage=doLikePercentage)
    session.set_do_comment(enabled=isDoComment, percentage=doCommentPercentage)
    session.set_comments(["Masterful shot", "Chilling!", "Unbelievably great..."])
    session.set_do_follow(enabled=isDoFollow, percentage=doFollowPercentage)
    session.set_user_interact(amount=interactionsByUser, randomize=True, percentage=interactionsPercentage, media='Photo')
    option = " "
    ##############################################
    while(option!= "0"):
        print("What strategy would you like to follow?")
        print("1. Interact with followers of an user")
        print("2. Interact with commenters of a photo")
        print("3. Interact with posts by hashtag")
        print("4. Interact using ClarifAI (IA Image recognisition)")
        print("5. Interact by Locations")
        print("6. Watch Stories from a #")
        print("7. Unfollow people followed from Instapy")
        print("8. Like by hashtags")
        print("9. Interact with your feed")
        print("10. Check interactions Settings ")

        option = input("Choose a number: ")
        if(option=="1"):
            print("Interacting with followers of an user")
            userInteract = input("What user's followers would you like to interact with?")
            nInteractions = int(input("How many users would you like to interact with?"))
            print(type(userInteract.split(" ")))

            session.interact_user_followers(userInteract.split(" "), amount=nInteractions, randomize=True)


        elif(option=="2"):
            ##Esta opción, aparte de interactuar con tan solo... 1 usuario de comentario da like a la foto >.<""
            print("Interacting with commenters of a photo")
            session.set_do_reply_to_comments(enabled=False, percentage=14)
            session.set_comment_replies(replies=[u"😎😎😎", u"😁😁😁😁😁😁😁💪🏼", u"😋🎉", "😀🍬", u"😂😂😂👈🏼👏🏼👏🏼", u"🙂🙋🏼‍♂️🚀🎊🎊🎊", u"😁😁😁", u"😂", "🎉",  u"😎", u"🤓🤓🤓🤓🤓", u"👏🏼😉"], media="Photo")
            session.set_user_interact(amount=2, percentage=70, randomize=True, media="Photo")
            # also configure [at least] liking to be used while interacting with the commenters ...
            session.set_do_like(enabled=True, percentage=80)

            # start the feature
            session.interact_by_comments(usernames=["victormelida", "satunatu"], posts_amount=10,comments_per_post=5, reply=False, interact=True, randomize=True, media="Photo")

        elif(option=="3"):
            print("Interacting with posts by hashtag")
            # Like posts based on hashtags
            session.like_by_tags(['natgeo', 'world'], amount=10)
            #follow by tags and interact with user
            session.set_user_interact(amount=3, randomize=True, percentage=100, media='Photo')
            session.like_by_tags(['natgeo', 'world'], amount=10, interact=True)

        elif(option=="4"):
            print("Interacting with Clarifai")
            session.set_do_comment(True, percentage=10)
            session.set_comments(['What camera do you use?'])
            session.set_use_clarifai(enabled=True, api_key=keys.clarifai_key)
            session.clarifai_check_img_for(['people'], comment=True, comments=['Beuatiful!'])
            session.clarifai_check_img_for(['food', 'lunch', 'dinner'], comment=True, comments=['Tasty!', 'Nice!', 'Yum!'])
            session.like_by_tags(['food'], amount=10, interact=True)

        elif(option=="5"):
            print("Interacting by Locations")
            #like by locations
            session.like_by_locations(['224442573'], amount=5, skip_top_posts=False)
            #comment by locations
            session.comment_by_locations(['224442573'], amount=5, skip_top_posts=False)

        elif (option == "6"):
            print("watching histories")
            tagsWatch = input("What tags do you want to watch stories from?")
            session.story_by_tags(tagsWatch.split(" "))

        elif (option =="7"):
            print("Starting unfollowing people")
            session.unfollow_users(amount=60, InstapyFollowed=(True, "all"), style="FIFO", unfollow_after=90*60*60, sleep_delay=501)

        elif (option =="8"):
            print("Like by Hashtags")
            session.like_by_tags(["madrid", "rasta", "like4like"], amount=10, interact= False)

        elif (option =="9"):
            print("Liking your feed")
            session.like_by_feed(amount=25, randomize=True, unfollow=False, interact=False)


        elif (option =="10"):
            print("Settings")
            print("1. Interactions possible by user grabbed: " + str(interactionsByUser) + " and probability of interacting " + str(interactionsPercentage) + "%")
            print("2. Is like enabled?  " + str(isDoLike) + " and probability of liking is " + str(doLikePercentage) + "%")
            print("3. Is follow enabled?  " + str(isDoFollow) + " and probability of liking is " + str(doFollowPercentage) + "%")
            print("4. Are comments enabled?  " + str(isDoComment) + " and probability of liking is " + str(doCommentPercentage) + "%")
            print("Select an option if you want to change it parameters, if not type 0")
            optSetting = input("What would you like to change?")
            if(optSetting !="0"):
                if(optSetting =="1"):
                    print("Changing interactionsByUser")
                    interactionsByUser = int(input("How many posts would you like to interact with every user?"))
                    interactionsPercentage = int(input("What's the probability for each action?"))
                    session.set_user_interact(amount=interactionsByUser, randomize=True, percentage=interactionsPercentage, media='Photo')

                elif(optSetting =="2"):
                    print("Changing liking setup")
                    optLikes = input("Do you want to activate likes? y/n")
                    if(optLikes == "y"):
                        print("Likes activated")
                        isDoLike = True
                    else:
                        print("Likes deactivated")
                        isDoLike = False

                    doLikePercentage = int(input("What's the probability for each like?"))
                    session.set_do_like(enabled=isDoLike, percentage=doLikePercentage)


                elif(optSetting =="3"):
                    print("Changing Following setup")
                    optFollow = input("Do you want to activate follows? y/n")
                    if(optFollow == "y"):
                        print("Follows activated")
                        isDoFollow = True
                    else:
                        print("Follows deactivated")
                        isDoFollow = False

                    doFollowPercentage = int(input("What's the probability for each Follow?"))
                    session.set_do_follow(enabled=isDoFollow, percentage=doFollowPercentage)

                elif(optSetting =="4"):
                    print("Changing commenting setup")
                    optComments = input("Do you want to activate comments? y/n")
                    if(optComments == "y"):
                        print("comments activated")
                        isDoComment = True
                    else:
                        print("Comments deactivated")
                        isDoComment = False

                    doCommentPercentage = int(input("What's the probability for each comment?"))
                    session.set_do_comment(enabled=isDoComment, percentage=doCommentPercentage)








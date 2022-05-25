import cv2
import os


class siftDetector:
    def __init__(self, refpath):
        self.sift = cv2.SIFT_create()
        self.refpath = refpath
        # self.imgpath = imgpath
        self.finalval = -1
        # Define parameters for our Flann Matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        # Create the Flann Matcher object
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)


    def import_images(self):
        self.images = []
        self.imgNames = []
        mylist = os.listdir(self.refpath)

        for img in mylist:
            im = cv2.imread(f'{self.refpath}/{img}', 0)
            # im = cv2.resize(im, (640, 480))
            self.images.append(im)
            self.imgNames.append(os.path.splitext(img)[0])
            # print(self.imgNames)
        return self.images, self.imgNames


    def findDes(self):
        self.images,self.imgNames = self.import_images()
        self.deslist = []

        for img in self.images:
            kp, des = self.sift.detectAndCompute(img, None)
            print(des.shape)

            self.deslist.append(des)
        return self.deslist, self.imgNames

    def findID(self, deslist, imgpath, thres=130):

        img1_gray = cv2.imread(imgpath, 0)

        kp2, des2 = self.sift.detectAndCompute(img1_gray, None)
        # print(des2.shape)

        matchlist = []
        self.finalval = -1
        try:
            for des in deslist:
                # Obtain matches using K-Nearest Neighbor Method
                # the result 'matchs' is the number of similar matches found in both images
                matches = self.flann.knnMatch(des, des2, k=2)

                good = []
                for m, n in matches:
                    if m.distance < 0.7 * n.distance:
                        good.append([m])
                matchlist.append(len(good))
                print(f"{len(good)} >>> {len(matchlist)}")

        except:
            pass

        if len(matchlist) != 0:
            if max(matchlist) > thres:
                self.finalval = matchlist.index(max(matchlist))

        return self.finalval


class orbDetector:
    def __init__(self, refpath):
        self.orb = cv2.ORB_create(nfeatures=3000)
        self.refpath = refpath
        # self.imgpath = imgpath
        # self.finalval = -1
        self.bf = cv2.BFMatcher()


    def import_images(self):
        self.images = []
        self.imgNames = []
        mylist = os.listdir(self.refpath)

        for img in mylist:
            im = cv2.imread(f'{self.refpath}/{img}', 0)#####################################
            # im = cv2.resize(im ,(0,0), None, 0.5, 0.5)#######################################
            self.images.append(cv2.imread(f'{self.refpath}/{img}', 0))
            self.imgNames.append(os.path.splitext(img)[0])
            # print(self.imgNames)
        return self.images, self.imgNames


    def findDes(self):
        self.images,self.imgNames = self.import_images()
        self.deslist = []
        for img in self.images:
            kp, des = self.orb.detectAndCompute(img, None)
            print(des.shape)
            self.deslist.append(des)
        return self.deslist, self.imgNames

    def findID(self, deslist, img, thres=130):
        # self.deslist = self.findDes()
        # img1 = cv2.imread(imgpath)
        # img = cv2.resize(img, (640, 480))####################################
        img1_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kp2, des2 = self.orb.detectAndCompute(img1_gray, None)
        # print(des2.shape)

        matchlist = []
        self.finalval = -1
        try:
            for des in deslist:
                matches = self.bf.knnMatch(des, des2, k=2)
                good = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                print(len(good))
                matchlist.append(len(good))
        except:
            pass

        if len(matchlist) != 0:
            if max(matchlist) > thres:
                self.finalval = matchlist.index(max(matchlist))

        # return finalval
        return self.finalval

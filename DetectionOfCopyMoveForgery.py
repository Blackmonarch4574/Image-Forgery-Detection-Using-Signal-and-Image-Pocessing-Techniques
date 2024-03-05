import cv2
import numpy as np
from math import sqrt



class DetectionofCopyMoveForgery:

    def __init__(self, img, height, width, blocksize,oklid_threshold,correlation_threshold,vec_len_threshold,num_ofvector_threshold):
        self.img = img
        self.height=height
        self.width=width
        self.blocksize = blocksize
        self.oklid_threshold = oklid_threshold
        self.correlation_threshold = correlation_threshold
        self.vec_len_threshold = vec_len_threshold
        self.num_ofvector_threshold = num_ofvector_threshold

        self.block_vector=[]
        self.sizeof_vector=16
        self.hough_space = (self.height, self.width,2)
        self.hough_space = np.zeros(self.hough_space)
        self.shiftvector=[]


    def detection_forgery(self):

        self.dct_of_img()
        self.lexicographically_sort_of_vectors()
        self.correlation_of_vectors()

        
        # Finally, according to the determined threshold value, fake areas are determined according to the number of shift vectors in the same direction.
        max=-1
        for i in range(self.height):
            for j in range(self.width):
                for h in range(2):
                    if(self.hough_space[i][j][h]) > max:
                        max = self.hough_space[i][j][h]
        for i in range(self.height):
            for j in range(self.width):
                self.img[i][j]=0

        for i in range(self.height):
            for j in range(self.width):
                for h in range(2):
                    if (self.hough_space[i][j][h]) >= (max - (max*self.num_ofvector_threshold/100)):
                        for k in range(len(self.shiftvector)):
                            if (self.shiftvector[k][0]==j and self.shiftvector[k][1]==i and self.shiftvector[k][2]==h):
                                cv2.rectangle(self.img,(self.shiftvector[k][3], self.shiftvector[k][4]),(self.shiftvector[k][3]+self.blocksize, self.shiftvector[k][4]+self.blocksize), (255), -1)
                                cv2.rectangle(self.img, (self.shiftvector[k][5], self.shiftvector[k][6]),(self.shiftvector[k][5] + self.blocksize, self.shiftvector[k][6] + self.blocksize), (255), -1)
        cv2.imshow("sonuc",self.img)


    def dct_of_img(self):

        for r in range(0, self.height-self.blocksize, 1):
            for c in range(0, self.width-self.blocksize,1):

                block = self.img[r:r + self.blocksize, c:c + self.blocksize]
                imf = np.float32(block)
                dct = cv2.dct(imf)       #We apply block by block dst



                QUANTIZATION_MAT_90 = np.array([[3, 2, 2, 3, 5, 8, 10, 12], [2, 2, 3, 4, 5, 12, 12, 11],
                                               [3, 3, 3, 5 ,8, 11, 14, 11], [3, 3, 4, 6, 10, 17, 16, 12],
                                               [4, 4, 7, 11, 14, 22, 21, 15], [5, 7, 11, 13, 16, 12, 23, 18],
                                               [10, 13, 16, 17, 21, 24, 24, 21], [14, 18, 19, 20, 22, 20, 20, 20]])

                # We can compress the dct transformation by dividing it into the quantization matrix. 
                # This may not be necessary since we are looking at relationships.                
                dct= np.round(np.divide(dct, QUANTIZATION_MAT_90)).astype(int)
                dct = (dct/4).astype(int)
                self.significant_part_extraction(self.zigzag(dct),c,r)



    def zigzag(self,matrix):
        """Scan matrix of zigzag algorithm"""

        vector = []
        n = len(matrix) - 1
        i = 0
        j = 0

        for _ in range(n * 2):
            vector.append(matrix[i][j])

            if j == n:   # right border
                i += 1     # shift
                while i != n:   # diagonal passage
                    vector.append(matrix[i][j])
                    i += 1
                    j -= 1
            elif i == 0:  # top border
                j += 1
                while j != 0:
                    vector.append(matrix[i][j])
                    i += 1
                    j -= 1
            elif i == n:   # bottom border
                j += 1
                while j != n:
                    vector.append(matrix[i][j])
                    i -= 1
                    j += 1
            elif j == 0:   # left border
                i += 1
                while i != 0:
                    vector.append(matrix[i][j])
                    i -= 1
                    j += 1

        vector.append(matrix[i][j])

        return vector

    def significant_part_extraction(self,vector,x,y):

        # In order to extract only the low frequency, that is, the significant part, from the 1x64 sized vector, the del operation is performed up to the specified value (16)..
        del vector[self.sizeof_vector:(self.blocksize*self.blocksize)]
        vector.append(x)  #The x point of the start coordinate of the blog is added to the end of the vector
        vector.append(y)  # Y point is added in the same way
        # We assign each block result to our vector list.
        self.block_vector.append(vector)


    def lexicographically_sort_of_vectors(self,):
        #Since it is in the order of the columns, we need to turn them upside down and sort them.
        #At the same time, we have coordinate information in the last two lines, that is, in the first two lines when we turn them upside down, we will not list them..
        self.block_vector=np.array(self.block_vector)
        self.block_vector= self.block_vector[np.lexsort(np.rot90(self.block_vector)[2:(self.sizeof_vector + 1) + 2 , :])]



    def correlation_of_vectors(self):

        for i in range(len(self.block_vector)):
            if(i+self.correlation_threshold >= len(self.block_vector)):
                self.correlation_threshold -=1
                #We examine the vectors according to their Euclidean similarity down to the specified threshold.
            for j in range(i+1, i + self.correlation_threshold + 1):
                if(self.oklid(self.block_vector[i], self.block_vector[j], self.sizeof_vector) <= self.oklid_threshold):
                #We keep the positions of similar vectors in their last index in a new vector.                    
                    v1=[]
                    v2=[]
                    v1.append(int(self.block_vector[i][-2])) #x1
                    v1.append(int(self.block_vector[i][-1])) #y1
                    v2.append(int(self.block_vector[j][-2])) #x2
                    v2.append(int(self.block_vector[j][-1])) #y2
                    self.elimination_of_weak_vectors(v1,v2,2)


    def elimination_of_weak_vectors(self,vector1,vector2,size):
        #By finding the lengths of the related vectors using Euclidean, we eliminate the short ones according to the determined threshold value.
        if(self.oklid(vector1,vector2,size) >= self.vec_len_threshold):
            self.elimination_of_weak_area(vector1,vector2)

    def elimination_of_weak_area(self,vector1,vector2):
        #Finally, the directions of the determined vectors are calculated and the position of this direction in Hough space is increased by one.
        #In order not to lose which block vectors increase which direction, a new vector is created and then the direction is increased.
        #Its own coordinates are kept in the vector, and block by block shift in these vectors is assigned to the vector.
        c = abs(vector2[0]-vector1[0])
        r = abs(vector2[1]-vector1[1])
        if (vector2[0]>=vector1[0]):
            if(vector2[1]>=vector1[1]):
                z = 0
            else:
                z = 1

        if (vector1[0] > vector2[0]):
            if (vector1[1] >= vector2[1]):

                z = 0
            else:
                z = 1
        self.hough_space[r][c][z] +=1
        vector=[]
        vector.append(c)
        vector.append(r)
        vector.append(z)
        vector.append(vector1[0])
        vector.append(vector1[1])
        vector.append(vector2[0])
        vector.append(vector2[1])
        self.shiftvector.append(vector)          
        # though coordinate, coordinate of the 1st vector, coordinate of the 2nd vector, respectively



    def oklid(self,vector1,vector2,size):
        sum=0
        for i in range(size):
            sum += (vector2[i]-vector1[i])**2

        return sqrt(sum)

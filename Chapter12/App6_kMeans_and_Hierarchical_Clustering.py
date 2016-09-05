""" Chapter 12 Programming Collective Intelligence: Kmeans and Hierarchical clustering.

    As the chapter has no exercises in it I have decided to create a practical
    application for each of the Algorithms and Methods described.
    Next up K-means and Hierarchical clustering.

    Well, here I am still on the Titanic dataset. This is just something I made after looking back
    over cluster.py and thinking how to apply it to the dataset.
    I perform k-means clustering on the whole data set, then I take the smallest
    cluster produced perform k-means clustering on it. I perform hierarchical clustering
    on the smallest returned cluster and output a Dendrogram jpeg and a 2D Cluster jpeg.
    The dendrogram often shows a lot of family groupings, and survivor groupings :)

    see *end for dataset details.
    "0" for died, "1" for survived.
"""

from math import sqrt
from PIL import Image, ImageDraw
import random as random


def manhattan(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += abs(v1[i]-v2[i])
    return d


def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])
    num = pSum-(sum1*sum2/len(v1))
    den = sqrt((sum1Sq-pow(sum1, 2)/len(v1))*(sum2Sq-pow(sum2, 2)/len(v1)))
    
    if den == 0: 
        return 0
    return 1.0-num/den


class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance 


def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]
    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]
                if d < closest:
                    closest = d
                    lowestpair = (i, j)
        
        mergevec = [(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest, id=currentclustid)
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    
    return clust[0]


def getheight(clust):
    if clust.left == None and clust.right == None: 
        return 1
    return getheight(clust.left)+getheight(clust.right)


def getdepth(clust):
    if clust.left == None and clust.right == None: 
        return 0
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    h = getheight(clust)*20
    w = 1200
    depth = getdepth(clust)
    scaling = float(w-150)/depth
    img = Image.new('RGB',(w, h),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.line((0,h/2,10,h/2),fill=(255,0,0))
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')


def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id<0:
        h1 = getheight(clust.left)*20
        h2 = getheight(clust.right)*20
        top = y-(h1+h2)/2
        bottom = y+(h1+h2)/2
        ll = clust.distance*scaling
        draw.line((x,top+h1/2, x, bottom-h2/2), fill=(255,0,0)) 
        draw.line((x,top+h1/2, x+ll, top+h1/2), fill=(255,0,0))
        draw.line((x,bottom-h2/2, x+ll, bottom-h2/2), fill=(255,0,0))
        drawnode(draw, clust.left, x+ll, top+h1/2, scaling, labels)
        drawnode(draw, clust.right, x+ll, bottom-h2/2, scaling, labels)
    else:
        draw.text((x+5,y-7), labels[clust.id],(0,0,0))


def kcluster(rows, distance=pearson, k=4):
    ranges = [(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
    clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]
    lastmatches=None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]
        
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i],row)
                if d < distance(clusters[bestmatch],row): bestmatch = i
            bestmatches[bestmatch].append(j)
        
        if bestmatches == lastmatches: 
            break
        
        lastmatches = bestmatches
        
        for i in range(k):
            avgs = [0.0]*len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i] = avgs
                
    return bestmatches


def scaledown(data, distance=pearson, rate=0.01):
    n = len(data)
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]
    outersum = 0.0
    loc = [[random.random(),random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]
    lasterror = None
    
    for m in range(0, 1000):
        for i in range(n):
            for j in range(n):
                fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) for x in range(len(loc[i]))]))
        grad = [[0.0, 0.0] for i in range(n)]
        errorterm = 0
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                try:
                    errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]
                    grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
                    grad[k][1] += ((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
                except: 
                    pass
                totalerror += abs(errorterm)
        
        print totalerror
        
        if lasterror and lasterror<totalerror: 
            break
        
        lasterror = totalerror
        
        for k in range(n):
            loc[k][0] -= rate*grad[k][0]
            loc[k][1] -= rate*grad[k][1]
    return loc


def draw2d(data, labels, jpeg='mds2d.jpg'):
    img=Image.new('RGB',(2000,2000),(255,255,255))
    draw=ImageDraw.Draw(img)
    
    for i in range(len(data)):
        x=(data[i][0]+0.5)*1000
        y=(data[i][1]+0.5)*1000
        draw.text((x,y),labels[i],(0,0,0))
    
    img.save(jpeg,'JPEG')


# This ensures that kclustering returns fully populated lists
def find_good_clusters(data1):
    k=7
    while True:
        for i in range(3):
            kclust = kcluster(data1, manhattan, k=3) 
            list1=[]
            for a in kclust:
                b=len(a)
                list1.append(b)
            if min(list1)>0: 
                return kclust
        k-=1
        if k==0:
            print "unable to cluster data"
            return 0


def main():
    global names, data
    for a in range(len(data)): 
        del data[a][2]  # Remove the age variable (just for S.A.G)
        
    kclust=find_good_clusters(data)
    
    if kclust==0: 
        print "unable to cluster data"
    
    mini, f = 10000, 0
    
    for a in range(len(kclust)):
        if len(kclust[a])<mini:
            mini=len(kclust[a])
            f=a
    
    data1=[data[r] for r in kclust[a]]
    names1=[names[r] for r in kclust[a]]
    kclust1=find_good_clusters(data1)
    
    if kclust1==0: 
        print "unable to cluster data"
    
    mini, f = 10000, 0
    
    for a in range(len(kclust1)):
        if len(kclust1[a])<mini:
            mini=len(kclust1[a])
            f=a
    
    data2=[data1[r] for r in kclust1[a]]
    names2=[names1[r] for r in kclust1[a]]
    
    # print a dendrogram
    clust=hcluster(data2)
    drawdendrogram(clust,names2,jpeg='titanic_dendrogram.jpg')
    print "'titanic_dendrogram.jpg' created"
    
    # print a 2d cluster
    coords=scaledown(data2)
    draw2d(coords,names2,jpeg='titanic_2dCluster.jpg')
    print "'titanic_2dCluster.jpg' created"


names=['0 Braund Mr. Owen Harris', '1 Cumings Mrs. John Bradley (Florence Briggs Thayer)', '1 Heikkinen Miss. Laina', '1 Futrelle Mrs. Jacques Heath (Lily May Peel)', '0 Allen Mr. William Henry', '0 Moran Mr. James', '0 McCarthy Mr. Timothy J', '0 Palsson Master. Gosta Leonard', '1 Johnson Mrs. Oscar W (Elisabeth Vilhelmina Berg)', '1 Nasser Mrs. Nicholas (Adele Achem)', '1 Sandstrom Miss. Marguerite Rut', '1 Bonnell Miss. Elizabeth', '0 Saundercock Mr. William Henry', '0 Andersson Mr. Anders Johan', '0 Vestrom Miss. Hulda Amanda Adolfina', '1 Hewlett Mrs. (Mary D Kingcome) ', '0 Rice Master. Eugene', '1 Williams Mr. Charles Eugene', '0 Vander Planke Mrs. Julius (Emelia Maria Vandemoortele)', '1 Masselmani Mrs. Fatima', '0 Fynney Mr. Joseph J', '1 Beesley Mr. Lawrence', '1 McGowan Miss. Anna Annie', '1 Sloper Mr. William Thompson', '0 Palsson Miss. Torborg Danira', '1 Asplund Mrs. Carl Oscar (Selma Augusta Emilia Johansson)', '0 Emir Mr. Farred Chehab', '0 Fortune Mr. Charles Alexander', "1 O'Dwyer Miss. Ellen Nellie", '0 Todoroff Mr. Lalio', '0 Uruchurtu Don. Manuel E', '1 Spencer Mrs. William Augustus (Marie Eugenie)', '1 Glynn Miss. Mary Agatha', '0 Wheadon Mr. Edward H', '0 Meyer Mr. Edgar Joseph', '0 Holverson Mr. Alexander Oskar', '1 Mamee Mr. Hanna', '0 Cann Mr. Ernest Charles', '0 Vander Planke Miss. Augusta Maria', '1 Nicola-Yarred Miss. Jamila', '0 Ahlin Mrs. Johan (Johanna Persdotter Larsson)', '0 Turpin Mrs. William John Robert (Dorothy Ann Wonnacott)', '0 Kraeff Mr. Theodor', '1 Laroche Miss. Simonne Marie Anne Andree', '1 Devaney Miss. Margaret Delia', '0 Rogers Mr. William John', '0 Lennon Mr. Denis', "1 O'Driscoll Miss. Bridget", '0 Samaan Mr. Youssef', '0 Arnold-Franchi Mrs. Josef (Josefine Franchi)', '0 Panula Master. Juha Niilo', '0 Nosworthy Mr. Richard Cater', '1 Harper Mrs. Henry Sleeper (Myna Haxtun)', '1 Faunthorpe Mrs. Lizzie (Elizabeth Anne Wilkinson)', '0 Ostby Mr. Engelhart Cornelius', '1 Woolner Mr. Hugh', '1 Rugg Miss. Emily', '0 Novel Mr. Mansouer', '1 West Miss. Constance Mirium', '0 Goodwin Master. William Frederick', '0 Sirayanian Mr. Orsen', '1 Icard Miss. Amelie', '0 Harris Mr. Henry Birkhardt', '0 Skoog Master. Harald', '0 Stewart Mr. Albert A', '1 Moubarek Master. Gerios', '1 Nye Mrs. (Elizabeth Ramell)', '0 Crease Mr. Ernest James', '1 Andersson Miss. Erna Alexandra', '0 Kink Mr. Vincenz', '0 Jenkin Mr. Stephen Curnow', '0 Goodwin Miss. Lillian Amy', '0 Hood Mr. Ambrose Jr', '0 Chronopoulos Mr. Apostolos', '1 Bing Mr. Lee', '0 Moen Mr. Sigurd Hansen', '0 Staneff Mr. Ivan', '0 Moutal Mr. Rahamin Haim', '1 Caldwell Master. Alden Gates', '1 Dowdell Miss. Elizabeth', '0 Waelens Mr. Achille', '1 Sheerlinck Mr. Jan Baptist', '1 McDermott Miss. Brigdet Delia', '0 Carrau Mr. Francisco M', '1 Ilett Miss. Bertha', '1 Backstrom Mrs. Karl Alfred (Maria Mathilda Gustafsson)', '0 Ford Mr. William Neal', '0 Slocovski Mr. Selman Francis', '1 Fortune Miss. Mabel Helen', '0 Celotti Mr. Francesco', '0 Christmann Mr. Emil', '0 Andreasson Mr. Paul Edvin', '0 Chaffee Mr. Herbert Fuller', '0 Dean Mr. Bertram Frank', '0 Coxon Mr. Daniel', '0 Shorney Mr. Charles Joseph', '0 Goldschmidt Mr. George B', '1 Greenfield Mr. William Bertram', '1 Doling Mrs. John T (Ada Julia Bone)', '0 Kantor Mr. Sinai', '0 Petranec Miss. Matilda', '0 Petroff Mr. Pastcho (Pentcho)', '0 White Mr. Richard Frasar', '0 Johansson Mr. Gustaf Joel', '0 Gustafsson Mr. Anders Vilhelm', '0 Mionoff Mr. Stoytcho', '1 Salkjelsvik Miss. Anna Kristine', '1 Moss Mr. Albert Johan', '0 Rekic Mr. Tido', '1 Moran Miss. Bertha', '0 Porter Mr. Walter Chamberlain', '0 Zabour Miss. Hileni', '0 Barton Mr. David John', '0 Jussila Miss. Katriina', '0 Attalah Miss. Malake', '0 Pekoniemi Mr. Edvard', '0 Connors Mr. Patrick', '0 Turpin Mr. William John Robert', '0 Baxter Mr. Quigg Edmond', '0 Andersson Miss. Ellis Anna Maria', '0 Hickman Mr. Stanley George', '0 Moore Mr. Leonard Charles', '0 Nasser Mr. Nicholas', '1 Webber Miss. Susan', '0 White Mr. Percival Wayland', '1 Nicola-Yarred Master. Elias', '0 McMahon Mr. Martin', '1 Madsen Mr. Fridtjof Arne', '1 Peter Miss. Anna', '0 Ekstrom Mr. Johan', '0 Drazenoic Mr. Jozef', '0 Coelho Mr. Domingos Fernandeo', '0 Robins Mrs. Alexander A (Grace Charity Laury)', '1 Weisz Mrs. Leopold (Mathilde Francoise Pede)', '0 Sobey Mr. Samuel James Hayden', '0 Richard Mr. Emile', '1 Newsom Miss. Helen Monypeny', '0 Futrelle Mr. Jacques Heath', '0 Osen Mr. Olaf Elon', '0 Giglio Mr. Victor', '0 Boulos Mrs. Joseph (Sultana)', '1 Nysten Miss. Anna Sofia', '1 Hakkarainen Mrs. Pekka Pietari (Elin Matilda Dolck)', '0 Burke Mr. Jeremiah', '0 Andrew Mr. Edgardo Samuel', '0 Nicholls Mr. Joseph Charles', '1 Andersson Mr. August Edvard (Wennerstrom)', '0 Ford Miss. Robina Maggie Ruby', '0 Navratil Mr. Michel (Louis M Hoffman)', '0 Byles Rev. Thomas Roussel Davids', '0 Bateman Rev. Robert James', '1 Pears Mrs. Thomas (Edith Wearne)', '0 Meo Mr. Alfonzo', '0 van Billiard Mr. Austin Blyler', '0 Olsen Mr. Ole Martin', '0 Williams Mr. Charles Duane', '1 Gilnagh Miss. Katherine Katie', '0 Corn Mr. Harry', '0 Smiljanic Mr. Mile', '0 Sage Master. Thomas Henry', '0 Cribb Mr. John Hatfield', '1 Watt Mrs. James (Elizabeth Bessie Inglis Milne)', '0 Bengtsson Mr. John Viktor', '0 Calic Mr. Jovo', '0 Panula Master. Eino Viljami', '1 Goldsmith Master. Frank John William Frankie', '1 Chibnall Mrs. (Edith Martha Bowerman)', '0 Skoog Mrs. William (Anna Bernhardina Karlsson)', '0 Baumann Mr. John D', '0 Ling Mr. Lee', '0 Van der hoef Mr. Wyckoff', '0 Rice Master. Arthur', '1 Johnson Miss. Eleanor Ileen', '0 Sivola Mr. Antti Wilhelm', '0 Smith Mr. James Clinch', '0 Klasen Mr. Klas Albin', '0 Lefebre Master. Henry Forbes', '0 Isham Miss. Ann Elizabeth', '0 Hale Mr. Reginald', '0 Leonard Mr. Lionel', '0 Sage Miss. Constance Gladys', '0 Pernot Mr. Rene', '0 Asplund Master. Clarence Gustaf Hugo', '1 Becker Master. Richard F', '1 Kink-Heilmann Miss. Luise Gretchen', '0 Rood Mr. Hugh Roscoe', "1 O'Brien Mrs. Thomas (Johanna Hannah Godfrey)", '1 Romaine Mr. Charles Hallace (Mr C Rolmane)', '0 Bourke Mr. John', '0 Turcin Mr. Stjepan', '1 Pinsky Mrs. (Rosa)', '0 Carbines Mr. William', '1 Andersen-Jensen Miss. Carla Christine Nielsine', '1 Navratil Master. Michel M', '1 Brown Mrs. James Joseph (Margaret Tobin)', '1 Lurette Miss. Elise', '0 Mernagh Mr. Robert', '0 Olsen Mr. Karl Siegwart Andreas', '1 Madigan Miss. Margaret Maggie', '0 Yrois Miss. Henriette (Mrs Harbeck)', '0 Vande Walle Mr. Nestor Cyriel', '0 Sage Mr. Frederick', '0 Johanson Mr. Jakob Alfred', '0 Youseff Mr. Gerious', '1 Cohen Mr. Gurshon Gus', '0 Strom Miss. Telma Matilda', '0 Backstrom Mr. Karl Alfred', '1 Albimona Mr. Nassef Cassem', '1 Carr Miss. Helen Ellen', '1 Blank Mr. Henry', '0 Ali Mr. Ahmed', '1 Cameron Miss. Clear Annie', '0 Perkin Mr. John Henry', '0 Givard Mr. Hans Kristensen', '0 Kiernan Mr. Philip', '1 Newell Miss. Madeleine', '1 Honkanen Miss. Eliina', '0 Jacobsohn Mr. Sidney Samuel', '1 Bazzani Miss. Albina', '0 Harris Mr. Walter', '1 Sunderland Mr. Victor Francis', '0 Bracken Mr. James H', '0 Green Mr. George Henry', '0 Nenkoff Mr. Christo', '1 Hoyt Mr. Frederick Maxfield', '0 Berglund Mr. Karl Ivar Sven', '1 Mellors Mr. William John', '0 Lovell Mr. John Hall (Henry)', '0 Fahlstrom Mr. Arne Jonas', '0 Lefebre Miss. Mathilde', '1 Harris Mrs. Henry Birkhardt (Irene Wallach)', '0 Larsson Mr. Bengt Edvin', '0 Sjostedt Mr. Ernst Adolf', '1 Asplund Miss. Lillian Gertrud', '0 Leyson Mr. Robert William Norman', '0 Harknett Miss. Alice Phoebe', '0 Hold Mr. Stephen', '1 Collyer Miss. Marjorie Lottie', '0 Pengelly Mr. Frederick William', '0 Hunt Mr. George Henry', '0 Zabour Miss. Thamine', '1 Murphy Miss. Katherine Kate', '0 Coleridge Mr. Reginald Charles', '0 Maenpaa Mr. Matti Alexanteri', '0 Attalah Mr. Sleiman', '0 Minahan Dr. William Edward', '0 Lindahl Miss. Agda Thorilda Viktoria', '1 Hamalainen Mrs. William (Anna)', '1 Beckwith Mr. Richard Leonard', '0 Carter Rev. Ernest Courtenay', '0 Reed Mr. James George', '0 Strom Mrs. Wilhelm (Elna Matilda Persson)', '0 Stead Mr. William Thomas', '0 Lobb Mr. William Arthur', '0 Rosblom Mrs. Viktor (Helena Wilhelmina)', '1 Touma Mrs. Darwis (Hanne Youssef Razi)', '1 Thorne Mrs. Gertrude Maybelle', '1 Cherry Miss. Gladys', '1 Ward Miss. Anna', '1 Parrish Mrs. (Lutie Davis)', '0 Smith Mr. Thomas', '1 Asplund Master. Edvin Rojj Felix', '0 Taussig Mr. Emil', '0 Harrison Mr. William', '0 Henry Miss. Delia', '0 Reeves Mr. David', '0 Panula Mr. Ernesti Arvid', '1 Persson Mr. Ernst Ulrik', '1 Graham Mrs. William Thompson (Edith Junkins)', '1 Bissette Miss. Amelia', '0 Cairns Mr. Alexander', '1 Tornquist Mr. William Henry', '1 Mellinger Mrs. (Elizabeth Anne Maidment)', '0 Natsch Mr. Charles H', '1 Healy Miss. Hanora Nora', '1 Andrews Miss. Kornelia Theodosia', '0 Lindblom Miss. Augusta Charlotta', '0 Parkes Mr. Francis Frank', '0 Rice Master. Eric', '1 Abbott Mrs. Stanton (Rosa Hunt)', '0 Duane Mr. Frank', '0 Olsson Mr. Nils Johan Goransson', '0 de Pelsmaeker Mr. Alfons', '1 Dorking Mr. Edward Arthur', '0 Smith Mr. Richard William', '0 Stankovic Mr. Ivan', '1 de Mulder Mr. Theodore', '0 Naidenoff Mr. Penko', '1 Hosono Mr. Masabumi', '1 Connolly Miss. Kate', '1 Barber Miss. Ellen Nellie', '1 Bishop Mrs. Dickinson H (Helen Walton)', '0 Levy Mr. Rene Jacques', '0 Haas Miss. Aloisia', '0 Mineff Mr. Ivan', '0 Lewy Mr. Ervin G', '0 Hanna Mr. Mansour', '0 Allison Miss. Helen Loraine', '1 Saalfeld Mr. Adolphe', '1 Baxter Mrs. James (Helene DeLaudeniere Chaput)', '1 Kelly Miss. Anna Katherine Annie Kate', '1 McCoy Mr. Bernard', '0 Johnson Mr. William Cahoone Jr', '1 Keane Miss. Nora A', '0 Williams Mr. Howard Hugh Harry', '1 Allison Master. Hudson Trevor', '1 Fleming Miss. Margaret', '1 Penasco y Castellana Mrs. Victor de Satode (Maria Josefa Perez de Soto y Vallejo)', '0 Abelson Mr. Samuel', '1 Francatelli Miss. Laura Mabel', '1 Hays Miss. Margaret Bechstein', '1 Ryerson Miss. Emily Borie', '0 Lahtinen Mrs. William (Anna Sylfven)', '0 Hendekovic Mr. Ignjac', '0 Hart Mr. Benjamin', '1 Nilsson Miss. Helmina Josefina', '1 Kantor Mrs. Sinai (Miriam Sternin)', '0 Moraweck Dr. Ernest', '1 Wick Miss. Mary Natalie', '1 Spedden Mrs. Frederic Oakley (Margaretta Corning Stone)', '0 Dennis Mr. Samuel', '0 Danoff Mr. Yoto', '1 Slayter Miss. Hilda Mary', '1 Caldwell Mrs. Albert Francis (Sylvia Mae Harbaugh)', '0 Sage Mr. George John Jr', '1 Young Miss. Marie Grice', '0 Nysveen Mr. Johan Hansen', '1 Ball Mrs. (Ada E Hall)', '1 Goldsmith Mrs. Frank John (Emily Alice Brown)', '1 Hippach Miss. Jean Gertrude', '1 McCoy Miss. Agnes', '0 Partner Mr. Austen', '0 Graham Mr. George Edward', '0 Vander Planke Mr. Leo Edmondus', '1 Frauenthal Mrs. Henry William (Clara Heinsheimer)', '0 Denkoff Mr. Mitto', '0 Pears Mr. Thomas Clinton', '1 Burns Miss. Elizabeth Margaret', '1 Dahl Mr. Karl Edwart', '0 Blackwell Mr. Stephen Weart', '1 Navratil Master. Edmond Roger', '1 Fortune Miss. Alice Elizabeth', '0 Collander Mr. Erik Gustaf', '0 Sedgwick Mr. Charles Frederick Waddington', '0 Fox Mr. Stanley Hubert', '1 Brown Miss. Amelia Mildred', '1 Smith Miss. Marion Elsie', '1 Davison Mrs. Thomas Henry (Mary E Finck)', '1 Coutts Master. William Loch William', '0 Dimic Mr. Jovan', '0 Odahl Mr. Nils Martin', '0 Williams-Lambert Mr. Fletcher Fellows', '0 Elias Mr. Tannous', '0 Arnold-Franchi Mr. Josef', '0 Yousif Mr. Wazli', '0 Vanden Steen Mr. Leo Peter', '1 Bowerman Miss. Elsie Edith', '0 Funk Miss. Annie Clemmer', '1 McGovern Miss. Mary', '1 Mockler Miss. Helen Mary Ellie', '0 Skoog Mr. Wilhelm', '0 del Carlo Mr. Sebastiano', '0 Barbara Mrs. (Catherine David)', '0 Asim Mr. Adola', "0 O'Brien Mr. Thomas", '0 Adahl Mr. Mauritz Nils Martin', '1 Warren Mrs. Frank Manley (Anna Sophia Atkinson)', '1 Moussa Mrs. (Mantoura Boulos)', '1 Jermyn Miss. Annie', '1 Aubart Mme. Leontine Pauline', '1 Harder Mr. George Achilles', '0 Wiklund Mr. Jakob Alfred', '0 Beavan Mr. William Thomas', '0 Ringhini Mr. Sante', '0 Palsson Miss. Stina Viola', '1 Meyer Mrs. Edgar Joseph (Leila Saks)', '1 Landergren Miss. Aurora Adelia', '0 Widener Mr. Harry Elkins', '0 Betros Mr. Tannous', '0 Gustafsson Mr. Karl Gideon', '1 Bidois Miss. Rosalie', '1 Nakid Miss. Maria (Mary)', '0 Tikkanen Mr. Juho', '1 Holverson Mrs. Alexander Oskar (Mary Aline Towner)', '0 Plotcharsky Mr. Vasil', '0 Davies Mr. Charles Henry', '0 Goodwin Master. Sidney Leonard', '1 Buss Miss. Kate', '0 Sadlier Mr. Matthew', '1 Lehmann Miss. Bertha', '1 Carter Mr. William Ernest', '1 Jansson Mr. Carl Olof', '0 Gustafsson Mr. Johan Birger', '1 Newell Miss. Marjorie', '1 Sandstrom Mrs. Hjalmar (Agnes Charlotta Bengtsson)', '0 Johansson Mr. Erik', '0 Olsson Miss. Elina', '0 McKane Mr. Peter David', '0 Pain Dr. Alfred', '1 Trout Mrs. William H (Jessie L)', '1 Niskanen Mr. Juha', '0 Adams Mr. John', '0 Jussila Miss. Mari Aina', '0 Hakkarainen Mr. Pekka Pietari', '0 Oreskovic Miss. Marija', '0 Gale Mr. Shadrach', '0 Widegren Mr. Carl/Charles Peter', '1 Richards Master. William Rowe', '0 Birkeland Mr. Hans Martin Monsen', '0 Lefebre Miss. Ida', '0 Sdycoff Mr. Todor', '0 Hart Mr. Henry', '1 Minahan Miss. Daisy E', '0 Cunningham Mr. Alfred Fleming', '1 Sundman Mr. Johan Julian', '0 Meek Mrs. Thomas (Annie Louise Rowley)', '1 Drew Mrs. James Vivian (Lulu Thorne Christian)', '1 Silven Miss. Lyyli Karoliina', '0 Matthews Mr. William John', '0 Van Impe Miss. Catharina', '0 Gheorgheff Mr. Stanio', '0 Charters Mr. David', '0 Zimmerman Mr. Leo', '0 Danbom Mrs. Ernst Gilbert (Anna Sigrid Maria Brogren)', '0 Rosblom Mr. Viktor Richard', '0 Wiseman Mr. Phillippe', '1 Clarke Mrs. Charles V (Ada Maria Winfield)', '1 Phillips Miss. Kate Florence (Mrs Kate Louise Phillips Marshall)', '0 Flynn Mr. James', '1 Pickard Mr. Berk (Berk Trembisky)', '1 Bjornstrom-Steffansson Mr. Mauritz Hakan', '1 Thorneycroft Mrs. Percival (Florence Kate White)', '1 Louch Mrs. Charles Alexander (Alice Adelaide Slow)', '0 Kallio Mr. Nikolai Erland', '0 Silvey Mr. William Baird', '1 Carter Miss. Lucile Polk', '0 Ford Miss. Doolina Margaret Daisy', '1 Richards Mrs. Sidney (Emily Hocking)', '0 Fortune Mr. Mark', '0 Kvillner Mr. Johan Henrik Johannesson', '1 Hart Mrs. Benjamin (Esther Ada Bloomfield)', '0 Hampe Mr. Leon', '0 Petterson Mr. Johan Emil', '1 Reynaldo Ms. Encarnacion', '1 Johannesen-Bratthammer Mr. Bernt', '1 Dodge Master. Washington', '1 Mellinger Miss. Madeleine Violet', '1 Seward Mr. Frederic Kimber', '1 Baclini Miss. Marie Catherine', '1 Peuchen Major. Arthur Godfrey', '0 West Mr. Edwy Arthur', '0 Hagland Mr. Ingvald Olai Olsen', '0 Foreman Mr. Benjamin Laventall', '1 Goldenberg Mr. Samuel L', '0 Peduzzi Mr. Joseph', '1 Jalsevac Mr. Ivan', '0 Millet Mr. Francis Davis', '1 Kenyon Mrs. Frederick R (Marion)', '1 Toomey Miss. Ellen', "0 O'Connor Mr. Maurice", '1 Anderson Mr. Harry', '0 Morley Mr. William', '0 Gee Mr. Arthur H', '0 Milling Mr. Jacob Christian', '0 Maisner Mr. Simon', '0 Goncalves Mr. Manuel Estanslas', '0 Campbell Mr. William', '0 Smart Mr. John Montgomery', '0 Scanlan Mr. James', '1 Baclini Miss. Helene Barbara', '0 Keefe Mr. Arthur', '0 Cacic Mr. Luka', '1 West Mrs. Edwy Arthur (Ada Mary Worth)', '1 Jerwan Mrs. Amin S (Marie Marthe Thuillard)', '0 Strandberg Miss. Ida Sofia', '0 Clifford Mr. George Quincy', '0 Renouf Mr. Peter Henry', '0 Braund Mr. Lewis Richard', '0 Karlsson Mr. Nils August', '1 Hirvonen Miss. Hildur E', '0 Goodwin Master. Harold Victor', '0 Frost Mr. Anthony Wood Archie', '0 Rouse Mr. Richard Henry', '1 Turkula Mrs. (Hedwig)', '1 Bishop Mr. Dickinson H', '0 Lefebre Miss. Jeannie', '1 Hoyt Mrs. Frederick Maxfield (Jane Anne Forby)', '0 Kent Mr. Edward Austin', '0 Somerton Mr. Francis William', '1 Coutts Master. Eden Leslie Neville', '0 Hagland Mr. Konrad Mathias Reiersen', '0 Windelov Mr. Einar', '0 Molson Mr. Harry Markland', '0 Artagaveytia Mr. Ramon', '0 Stanley Mr. Edward Roland', '0 Yousseff Mr. Gerious', '1 Eustis Miss. Elizabeth Mussey', '0 Shellard Mr. Frederick William', '0 Allison Mrs. Hudson J C (Bessie Waldo Daniels)', '0 Svensson Mr. Olof', '0 Calic Mr. Petar', '0 Canavan Miss. Mary', "0 O'Sullivan Miss. Bridget Mary", '0 Laitinen Miss. Kristina Sofia', '1 Maioni Miss. Roberta', '0 Penasco y Castellana Mr. Victor de Satode', '1 Quick Mrs. Frederick Charles (Jane Richards)', '1 Bradley Mr. George (George Arthur Brayton)', '0 Olsen Mr. Henry Margido', '1 Lang Mr. Fang', '1 Daly Mr. Eugene Patrick', '0 Webber Mr. James', '1 McGough Mr. James Robert', '1 Rothschild Mrs. Martin (Elizabeth L. Barrett)', '0 Coleff Mr. Satio', '0 Walker Mr. William Anderson', '1 Lemore Mrs. (Amelia Milley)', '0 Ryan Mr. Patrick', '1 Angle Mrs. William A (Florence Mary Agnes Hughes)', '0 Pavlovic Mr. Stefo', '1 Perreault Miss. Anne', '0 Vovk Mr. Janko', '0 Lahoud Mr. Sarkis', '1 Hippach Mrs. Louis Albert (Ida Sophia Fischer)', '0 Kassem Mr. Fared', '0 Farrell Mr. James', '1 Ridsdale Miss. Lucy', '0 Farthing Mr. John', '0 Salonen Mr. Johan Werner', '0 Hocking Mr. Richard George', '1 Quick Miss. Phyllis May', '0 Toufik Mr. Nakli', '0 Elias Mr. Joseph Jr', '1 Peter Mrs. Catherine (Catherine Rizk)', '0 Cacic Miss. Marija', '1 Hart Miss. Eva Miriam', '0 Butt Major. Archibald Willingham', '1 LeRoy Miss. Bertha', '0 Risien Mr. Samuel Beard', '1 Frolicher Miss. Hedwig Margaritha', '1 Crosby Miss. Harriet R', '0 Andersson Miss. Ingeborg Constanzia', '0 Andersson Miss. Sigrid Elisabeth', '1 Beane Mr. Edward', '0 Douglas Mr. Walter Donald', '0 Nicholson Mr. Arthur Ernest', '1 Beane Mrs. Edward (Ethel Clarke)', '1 Padro y Manent Mr. Julian', '0 Goldsmith Mr. Frank John', '1 Davies Master. John Morgan Jr', '1 Thayer Mr. John Borland Jr', '0 Sharp Mr. Percival James R', "0 O'Brien Mr. Timothy", '1 Leeni Mr. Fahim (Philip Zenni)', '1 Ohman Miss. Velin', '0 Wright Mr. George', '1 Duff Gordon Lady. (Lucille Christiana Sutherland) (Mrs Morgan)', '0 Robbins Mr. Victor', '1 Taussig Mrs. Emil (Tillie Mandelbaum)', '1 de Messemaeker Mrs. Guillaume Joseph (Emma)', '0 Morrow Mr. Thomas Rowan', '0 Sivic Mr. Husein', '0 Norman Mr. Robert Douglas', '0 Simmons Mr. John', '0 Meanwell Miss. (Marion Ogden)', '0 Davies Mr. Alfred J', '0 Stoytcheff Mr. Ilia', '0 Palsson Mrs. Nils (Alma Cornelia Berglund)', '0 Doharr Mr. Tannous', '1 Jonsson Mr. Carl', '1 Harris Mr. George', '1 Appleton Mrs. Edward Dale (Charlotte Lamson)', '1 Flynn Mr. John Irwin (Irving)', '1 Kelly Miss. Mary', '0 Rush Mr. Alfred George John', '0 Patchett Mr. George', '1 Garside Miss. Ethel', '1 Silvey Mrs. William Baird (Alice Munger)', '0 Caram Mrs. Joseph (Maria Elias)', '1 Jussila Mr. Eiriik', '1 Christy Miss. Julie Rachel', '1 Thayer Mrs. John Borland (Marian Longstreth Morris)', '0 Downton Mr. William James', '0 Ross Mr. John Hugo', '0 Paulner Mr. Uscher', '1 Taussig Miss. Ruth', '0 Jarvis Mr. John Denzil', '1 Frolicher-Stehli Mr. Maxmillian', '0 Gilinski Mr. Eliezer', '0 Murdlin Mr. Joseph', '0 Rintamaki Mr. Matti', '1 Stephenson Mrs. Walter Bertram (Martha Eustis)', '0 Elsbury Mr. William James', '0 Bourke Miss. Mary', '0 Chapman Mr. John Henry', '0 Van Impe Mr. Jean Baptiste', '1 Leitch Miss. Jessie Wills', '0 Johnson Mr. Alfred', '0 Boulos Mr. Hanna', '1 Duff Gordon Sir. Cosmo Edmund (Mr Morgan)', '1 Jacobsohn Mrs. Sidney Samuel (Amy Frances Christy)', '0 Slabenoff Mr. Petco', '0 Harrington Mr. Charles H', '0 Torber Mr. Ernst William', '1 Homer Mr. Harry (Mr E Haven)', '0 Lindell Mr. Edvard Bengtsson', '0 Karaic Mr. Milan', '1 Daniel Mr. Robert Williams', '1 Laroche Mrs. Joseph (Juliette Marie Louise Lafargue)', '1 Shutes Miss. Elizabeth W', '0 Andersson Mrs. Anders Johan (Alfrida Konstantia Brogren)', '0 Jardin Mr. Jose Neto', '1 Murphy Miss. Margaret Jane', '0 Horgan Mr. John', '0 Brocklebank Mr. William Alfred', '1 Herman Miss. Alice', '0 Danbom Mr. Ernst Gilbert', '0 Lobb Mrs. William Arthur (Cordelia K Stanlick)', '1 Becker Miss. Marion Louise', '0 Gavey Mr. Lawrence', '0 Yasbeck Mr. Antoni', '1 Kimball Mr. Edwin Nelson Jr', '1 Nakid Mr. Sahid', '0 Hansen Mr. Henry Damsgaard', '0 Bowen Mr. David John Dai', '0 Sutton Mr. Frederick', '0 Kirkland Rev. Charles Leonard', '1 Longley Miss. Gretchen Fiske', '0 Bostandyeff Mr. Guentcho', "0 O'Connell Mr. Patrick D", '1 Barkworth Mr. Algernon Henry Wilson', '0 Lundahl Mr. Johan Svensson', '1 Stahelin-Maeglin Dr. Max', '0 Parr Mr. William Henry Marsh', '0 Skoog Miss. Mabel', '1 Davis Miss. Mary', '0 Leinonen Mr. Antti Gustaf', '0 Collyer Mr. Harvey', '0 Panula Mrs. Juha (Maria Emilia Ojala)', '0 Thorneycroft Mr. Percival', '0 Jensen Mr. Hans Peder', '1 Sagesser Mlle. Emma', '0 Skoog Miss. Margit Elizabeth', '1 Foo Mr. Choong', '1 Baclini Miss. Eugenie', '1 Harper Mr. Henry Sleeper', '0 Cor Mr. Liudevit', '1 Simonius-Blumer Col. Oberst Alfons', '0 Willey Mr. Edward', '1 Stanley Miss. Amy Zillah Elsie', '0 Mitkoff Mr. Mito', '1 Doling Miss. Elsie', '0 Kalvik Mr. Johannes Halvorsen', "1 O'Leary Miss. Hanora Norah", '0 Hegarty Miss. Hanora Nora', '0 Hickman Mr. Leonard Mark', '0 Radeff Mr. Alexander', '0 Bourke Mrs. John (Catherine)', '0 Eitemiller Mr. George Floyd', '0 Newell Mr. Arthur Webster', '1 Frauenthal Dr. Henry William', '0 Badt Mr. Mohamed', '0 Colley Mr. Edward Pomeroy', '0 Coleff Mr. Peju', '1 Lindqvist Mr. Eino William', '0 Hickman Mr. Lewis', '0 Butler Mr. Reginald Fenton', '0 Rommetvedt Mr. Knud Paust', '0 Cook Mr. Jacob', '1 Taylor Mrs. Elmer Zebley (Juliet Cummins Wright)', '1 Brown Mrs. Thomas William Solomon (Elizabeth Catherine Ford)', '0 Davidson Mr. Thornton', '0 Mitchell Mr. Henry Michael', '1 Wilhelms Mr. Charles', '0 Watson Mr. Ennis Hastings', '0 Edvardsson Mr. Gustaf Hjalmar', '0 Sawyer Mr. Frederick Charles', '1 Turja Miss. Anna Sofia', '0 Goodwin Mrs. Frederick (Augusta Tyler)', '1 Cardeza Mr. Thomas Drake Martinez', '0 Peters Miss. Katie', '1 Hassab Mr. Hammad', '0 Olsvigen Mr. Thor Anderson', '0 Goodwin Mr. Charles Edward', '0 Brown Mr. Thomas William Solomon', '0 Laroche Mr. Joseph Philippe Lemercier', '0 Panula Mr. Jaako Arnold', '0 Dakic Mr. Branko', '0 Fischer Mr. Eberhard Thelander', '1 Madill Miss. Georgette Alexandra', '1 Dick Mr. Albert Adrian', '1 Karun Miss. Manca', '1 Lam Mr. Ali', '0 Saad Mr. Khalil', '0 Weir Col. John', '0 Chapman Mr. Charles Henry', '0 Kelly Mr. James', '1 Mullens Miss. Katherine Katie', '0 Thayer Mr. John Borland', '0 Humblen Mr. Adolf Mathias Nicolai Olsen', '1 Astor Mrs. John Jacob (Madeleine Talmadge Force)', '1 Silverthorne Mr. Spencer Victor', '0 Barbara Miss. Saiide', '0 Gallagher Mr. Martin', '0 Hansen Mr. Henrik Juul', '0 Morley Mr. Henry Samuel (Mr Henry Marshall)', '1 Kelly Mrs. Florence Fannie', '1 Calderhead Mr. Edward Pennington', '1 Cleaver Miss. Alice', '1 Moubarek Master. Halim Gonios (William George)', '1 Mayne Mlle. Berthe Antonine (Mrs de Villiers)', '0 Klaber Mr. Herman', '1 Taylor Mr. Elmer Zebley', '0 Larsson Mr. August Viktor', '0 Greenberg Mr. Samuel', '0 Soholt Mr. Peter Andreas Lauritz Andersen', '1 Endres Miss. Caroline Louise', '1 Troutt Miss. Edwina Celia Winnie', '0 McEvoy Mr. Michael', '0 Johnson Mr. Malkolm Joackim', '1 Harper Miss. Annie Jessie Nina', '0 Jensen Mr. Svend Lauritz', '0 Gillespie Mr. William Henry', '0 Hodges Mr. Henry Price', '1 Chambers Mr. Norman Campbell', '0 Oreskovic Mr. Luka', '1 Renouf Mrs. Peter Henry (Lillian Jefferys)', '1 Mannion Miss. Margareth', '0 Bryhl Mr. Kurt Arnold Gottfrid', '0 Ilmakangas Miss. Pieta Sofia', '1 Allen Miss. Elisabeth Walton', '0 Hassan Mr. Houssein G N', '0 Knight Mr. Robert J', '0 Berriman Mr. William John', '0 Troupiansky Mr. Moses Aaron', '0 Williams Mr. Leslie', '0 Ford Mrs. Edward (Margaret Ann Watson)', '1 Lesurer Mr. Gustave J', '0 Ivanoff Mr. Kanio', '0 Nankoff Mr. Minko', '1 Hawksford Mr. Walter James', '0 Cavendish Mr. Tyrell William', '1 Ryerson Miss. Susan Parker Suzette', '0 McNamee Mr. Neal', '1 Stranden Mr. Juho', '0 Crosby Capt. Edward Gifford', '0 Abbott Mr. Rossmore Edward', '1 Sinkkonen Miss. Anna', '0 Marvin Mr. Daniel Warner', '0 Connaghton Mr. Michael', '1 Wells Miss. Joan', '1 Moor Master. Meier', '0 Vande Velde Mr. Johannes Joseph', '0 Jonkoff Mr. Lalio', '1 Herman Mrs. Samuel (Jane Laver)', '1 Hamalainen Master. Viljo', '0 Carlsson Mr. August Sigfrid', '0 Bailey Mr. Percy Andrew', '0 Theobald Mr. Thomas Leonard', '1 Rothes the Countess. of (Lucy Noel Martha Dyer-Edwards)', '0 Garfirth Mr. John', '0 Nirva Mr. Iisakki Antino Aijo', '1 Barah Mr. Hanna Assi', '1 Carter Mrs. William Ernest (Lucile Polk)', '0 Eklund Mr. Hans Linus', '1 Hogeboom Mrs. John C (Anna Andrews)', '0 Brewe Dr. Arthur Jackson', '0 Mangan Miss. Mary', '0 Moran Mr. Daniel J', '0 Gronnestad Mr. Daniel Danielsen', '0 Lievens Mr. Rene Aime', '0 Jensen Mr. Niels Peder', '0 Mack Mrs. (Mary)', '0 Elias Mr. Dibo', '1 Hocking Mrs. Elizabeth (Eliza Needs)', '0 Myhrman Mr. Pehr Fabian Oliver Malkolm', '0 Tobin Mr. Roger', '1 Emanuel Miss. Virginia Ethel', '0 Kilgannon Mr. Thomas J', '1 Robert Mrs. Edward Scott (Elisabeth Walton McMillan)', '1 Ayoub Miss. Banoura', '1 Dick Mrs. Albert Adrian (Vera Gillespie)', '0 Long Mr. Milton Clyde', '0 Johnston Mr. Andrew G', '0 Ali Mr. William', '0 Harmer Mr. Abraham (David Lishin)', '1 Sjoblom Miss. Anna Sofia', '0 Rice Master. George Hugh', '1 Dean Master. Bertram Vere', '0 Guggenheim Mr. Benjamin', '0 Keane Mr. Andrew Andy', '0 Gaskell Mr. Alfred', '0 Sage Miss. Stella Anna', '0 Hoyt Mr. William Fisher', '0 Dantcheff Mr. Ristiu', '0 Otter Mr. Richard', '1 Leader Dr. Alice (Farnham)', '1 Osman Mrs. Mara', '0 Ibrahim Shawah Mr. Yousseff', '0 Van Impe Mrs. Jean Baptiste (Rosalie Paula Govaert)', '0 Ponesell Mr. Martin', '1 Collyer Mrs. Harvey (Charlotte Annie Tate)', '1 Carter Master. William Thornton II', '1 Thomas Master. Assad Alexander', '1 Hedman Mr. Oskar Arvid', '0 Johansson Mr. Karl Johan', '0 Andrews Mr. Thomas Jr', '0 Pettersson Miss. Ellen Natalia', '0 Meyer Mr. August', '1 Chambers Mrs. Norman Campbell (Bertha Griggs)', '0 Alexander Mr. William', '0 Lester Mr. James', '0 Slemen Mr. Richard James', '0 Andersson Miss. Ebba Iris Alfrida', '0 Tomlin Mr. Ernest Portage', '0 Fry Mr. Richard', '0 Heininen Miss. Wendla Maria', '0 Mallet Mr. Albert', '0 Holm Mr. John Fredrik Alexander', '0 Skoog Master. Karl Thorsten', '1 Hays Mrs. Charles Melville (Clara Jennings Gregg)', '1 Lulic Mr. Nikola', '0 Reuchlin Jonkheer. John George', '1 Moor Mrs. (Beila)', '0 Panula Master. Urho Abraham', '0 Flynn Mr. John', '0 Lam Mr. Len', '1 Mallet Master. Andre', '1 McCormack Mr. Thomas Joseph', '1 Stone Mrs. George Nelson (Martha Evelyn)', '1 Yasbeck Mrs. Antoni (Selini Alexander)', '1 Richards Master. George Sibley', '0 Saad Mr. Amin', '0 Augustsson Mr. Albert', '0 Allum Mr. Owen George', '1 Compton Miss. Sara Rebecca', '0 Pasic Mr. Jakob', '0 Sirota Mr. Maurice', '1 Chip Mr. Chang', '1 Marechal Mr. Pierre', '0 Alhomaki Mr. Ilmari Rudolf', '0 Mudd Mr. Thomas Charles', '1 Serepeca Miss. Augusta', '0 Lemberopolous Mr. Peter L', '0 Culumovic Mr. Jeso', '0 Abbing Mr. Anthony', '0 Sage Mr. Douglas Bullen', '0 Markoff Mr. Marin', '0 Harper Rev. John', '1 Goldenberg Mrs. Samuel L (Edwiga Grabowska)', '0 Andersson Master. Sigvard Harald Elias', '0 Svensson Mr. Johan', '0 Boulos Miss. Nourelain', '1 Lines Miss. Mary Conover', '0 Carter Mrs. Ernest Courtenay (Lilian Hughes)', '1 Aks Mrs. Sam (Leah Rosen)', '1 Wick Mrs. George Dennick (Mary Hitchcock)', '1 Daly Mr. Peter Denis ', '1 Baclini Mrs. Solomon (Latifa Qurban)', '0 Razi Mr. Raihed', '0 Hansen Mr. Claus Peter', '0 Giles Mr. Frederick Edward', '1 Swift Mrs. Frederick Joel (Margaret Welles Barron)', '0 Sage Miss. Dorothy Edith Dolly', '0 Gill Mr. John William', '1 Bystrom Mrs. (Karolina)', '1 Duran y More Miss. Asuncion', '0 Roebling Mr. Washington Augustus II', '0 van Melkebeke Mr. Philemon', '1 Johnson Master. Harold Theodor', '0 Balkic Mr. Cerin', '1 Beckwith Mrs. Richard Leonard (Sallie Monypeny)', '0 Carlsson Mr. Frans Olof', '0 Vander Cruyssen Mr. Victor', '1 Abelson Mrs. Samuel (Hannah Wizosky)', '1 Najib Miss. Adele Kiamie Jane', '0 Gustafsson Mr. Alfred Ossian', '0 Petroff Mr. Nedelio', '0 Laleff Mr. Kristo', '1 Potter Mrs. Thomas Jr (Lily Alexenia Wilson)', '1 Shelley Mrs. William (Imanita Parrish Hall)', '0 Markun Mr. Johann', '0 Dahlberg Miss. Gerda Ulrika', '0 Banfield Mr. Frederick James', '0 Sutehall Mr. Henry Jr', '0 Rice Mrs. William (Margaret Norton)', '0 Montvila Rev. Juozas', '1 Graham Miss. Margaret Edith', '0 Johnston Miss. Catherine Helen Carrie', '1 Behr Mr. Karl Howell', '0 Dooley Mr. Patrick']

data=[[3, 0, 22.0, 1, 0, 2], [1, 1, 38.0, 1, 0, 0], [3, 1, 26.0, 0, 0, 2], [1, 1, 35.0, 1, 0, 2], [3, 0, 35.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 0, 54.0, 0, 0, 2], [3, 0, 2.0, 3, 1, 2], [3, 1, 27.0, 0, 2, 2], [2, 1, 14.0, 1, 0, 0], [3, 1, 4.0, 1, 1, 2], [1, 1, 58.0, 0, 0, 2], [3, 0, 20.0, 0, 0, 2], [3, 0, 39.0, 1, 5, 2], [3, 1, 14.0, 0, 0, 2], [2, 1, 55.0, 0, 0, 2], [3, 0, 2.0, 4, 1, 1], [2, 0, 0.0, 0, 0, 2], [3, 1, 31.0, 1, 0, 2], [3, 1, 0.0, 0, 0, 0], [2, 0, 35.0, 0, 0, 2], [2, 0, 34.0, 0, 0, 2], [3, 1, 15.0, 0, 0, 1], [1, 0, 28.0, 0, 0, 2], [3, 1, 8.0, 3, 1, 2], [3, 1, 38.0, 1, 5, 2], [3, 0, 0.0, 0, 0, 0], [1, 0, 19.0, 3, 2, 2], [3, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [1, 0, 40.0, 0, 0, 0], [1, 1, 0.0, 1, 0, 0], [3, 1, 0.0, 0, 0, 1], [2, 0, 66.0, 0, 0, 2], [1, 0, 28.0, 1, 0, 0], [1, 0, 42.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 2], [3, 1, 18.0, 2, 0, 2], [3, 1, 14.0, 1, 0, 0], [3, 1, 40.0, 1, 0, 2], [2, 1, 27.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 0], [2, 1, 3.0, 1, 2, 0], [3, 1, 19.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 1, 0, 1], [3, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 2, 0, 0], [3, 1, 18.0, 1, 0, 2], [3, 0, 7.0, 4, 1, 2], [3, 0, 21.0, 0, 0, 2], [1, 1, 49.0, 1, 0, 0], [2, 1, 29.0, 1, 0, 2], [1, 0, 65.0, 0, 1, 0], [1, 0, 0.0, 0, 0, 2], [2, 1, 21.0, 0, 0, 2], [3, 0, 28.5, 0, 0, 0], [2, 1, 5.0, 1, 2, 2], [3, 0, 11.0, 5, 2, 2], [3, 0, 22.0, 0, 0, 0], [1, 1, 38.0, 0, 0, 2], [1, 0, 45.0, 1, 0, 2], [3, 0, 4.0, 3, 2, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 0.0, 1, 1, 0], [2, 1, 29.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [3, 1, 17.0, 4, 2, 2], [3, 0, 26.0, 2, 0, 2], [2, 0, 32.0, 0, 0, 2], [3, 1, 16.0, 5, 2, 2], [2, 0, 21.0, 0, 0, 2], [3, 0, 26.0, 1, 0, 0], [3, 0, 32.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 0, 0.82999999999999996, 0, 2, 2], [3, 1, 30.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [1, 0, 28.0, 0, 0, 2], [2, 1, 17.0, 0, 0, 2], [3, 1, 33.0, 3, 0, 2], [3, 0, 16.0, 1, 3, 2], [3, 0, 0.0, 0, 0, 2], [1, 1, 23.0, 3, 2, 2], [3, 0, 24.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 2], [3, 0, 20.0, 0, 0, 2], [1, 0, 46.0, 1, 0, 2], [3, 0, 26.0, 1, 2, 2], [3, 0, 59.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 71.0, 0, 0, 0], [1, 0, 23.0, 0, 1, 0], [2, 1, 34.0, 0, 1, 2], [2, 0, 34.0, 1, 0, 2], [3, 1, 28.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 21.0, 0, 1, 2], [3, 0, 33.0, 0, 0, 2], [3, 0, 37.0, 2, 0, 2], [3, 0, 28.0, 0, 0, 2], [3, 1, 21.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 38.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 1], [1, 0, 47.0, 0, 0, 2], [3, 1, 14.5, 1, 0, 0], [3, 0, 22.0, 0, 0, 2], [3, 1, 20.0, 1, 0, 2], [3, 1, 17.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 70.5, 0, 0, 1], [2, 0, 29.0, 1, 0, 2], [1, 0, 24.0, 0, 1, 0], [3, 1, 2.0, 4, 2, 2], [2, 0, 21.0, 2, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 0, 32.5, 1, 0, 0], [2, 1, 32.5, 0, 0, 2], [1, 0, 54.0, 0, 1, 2], [3, 0, 12.0, 1, 0, 0], [3, 0, 0.0, 0, 0, 1], [3, 0, 24.0, 0, 0, 2], [3, 1, 0.0, 1, 1, 0], [3, 0, 45.0, 0, 0, 2], [3, 0, 33.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [3, 1, 47.0, 1, 0, 2], [2, 1, 29.0, 1, 0, 2], [2, 0, 25.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 0], [1, 1, 19.0, 0, 2, 2], [1, 0, 37.0, 1, 0, 2], [3, 0, 16.0, 0, 0, 2], [1, 0, 24.0, 0, 0, 0], [3, 1, 0.0, 0, 2, 0], [3, 1, 22.0, 0, 0, 2], [3, 1, 24.0, 1, 0, 2], [3, 0, 19.0, 0, 0, 1], [2, 0, 18.0, 0, 0, 2], [2, 0, 19.0, 1, 1, 2], [3, 0, 27.0, 0, 0, 2], [3, 1, 9.0, 2, 2, 2], [2, 0, 36.5, 0, 2, 2], [2, 0, 42.0, 0, 0, 2], [2, 0, 51.0, 0, 0, 2], [1, 1, 22.0, 1, 0, 2], [3, 0, 55.5, 0, 0, 2], [3, 0, 40.5, 0, 2, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 51.0, 0, 1, 0], [3, 1, 16.0, 0, 0, 1], [3, 0, 30.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 8, 2, 2], [3, 0, 44.0, 0, 1, 2], [2, 1, 40.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 17.0, 0, 0, 2], [3, 0, 1.0, 4, 1, 2], [3, 0, 9.0, 0, 2, 2], [1, 1, 0.0, 0, 1, 2], [3, 1, 45.0, 1, 4, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 28.0, 0, 0, 2], [1, 0, 61.0, 0, 0, 2], [3, 0, 4.0, 4, 1, 1], [3, 1, 1.0, 1, 1, 2], [3, 0, 21.0, 0, 0, 2], [1, 0, 56.0, 0, 0, 0], [3, 0, 18.0, 1, 1, 2], [3, 0, 0.0, 3, 1, 2], [1, 1, 50.0, 0, 0, 0], [2, 0, 30.0, 0, 0, 2], [3, 0, 36.0, 0, 0, 2], [3, 1, 0.0, 8, 2, 2], [2, 0, 0.0, 0, 0, 0], [3, 0, 9.0, 4, 2, 2], [2, 0, 1.0, 2, 1, 2], [3, 1, 4.0, 0, 2, 2], [1, 0, 0.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 1], [1, 0, 45.0, 0, 0, 2], [3, 0, 40.0, 1, 1, 1], [3, 0, 36.0, 0, 0, 2], [2, 1, 32.0, 0, 0, 2], [2, 0, 19.0, 0, 0, 2], [3, 1, 19.0, 1, 0, 2], [2, 0, 3.0, 1, 1, 2], [1, 1, 44.0, 0, 0, 0], [1, 1, 58.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 1], [3, 0, 42.0, 0, 1, 2], [3, 1, 0.0, 0, 0, 1], [2, 1, 24.0, 0, 0, 2], [3, 0, 28.0, 0, 0, 2], [3, 0, 0.0, 8, 2, 2], [3, 0, 34.0, 0, 0, 2], [3, 0, 45.5, 0, 0, 0], [3, 0, 18.0, 0, 0, 2], [3, 1, 2.0, 0, 1, 2], [3, 0, 32.0, 1, 0, 2], [3, 0, 26.0, 0, 0, 0], [3, 1, 16.0, 0, 0, 1], [1, 0, 40.0, 0, 0, 0], [3, 0, 24.0, 0, 0, 2], [2, 1, 35.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [2, 0, 30.0, 0, 0, 2], [3, 0, 0.0, 1, 0, 1], [1, 1, 31.0, 1, 0, 0], [3, 1, 27.0, 0, 0, 2], [2, 0, 42.0, 1, 0, 2], [1, 1, 32.0, 0, 0, 0], [2, 0, 30.0, 0, 0, 2], [3, 0, 16.0, 0, 0, 2], [2, 0, 27.0, 0, 0, 2], [3, 0, 51.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 38.0, 1, 0, 2], [3, 0, 22.0, 0, 0, 2], [2, 0, 19.0, 0, 0, 2], [3, 0, 20.5, 0, 0, 2], [2, 0, 18.0, 0, 0, 2], [3, 1, 0.0, 3, 1, 2], [1, 1, 35.0, 1, 0, 2], [3, 0, 29.0, 0, 0, 2], [2, 0, 59.0, 0, 0, 2], [3, 1, 5.0, 4, 2, 2], [2, 0, 24.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 2], [2, 0, 44.0, 1, 0, 2], [2, 1, 8.0, 0, 2, 2], [2, 0, 19.0, 0, 0, 2], [2, 0, 33.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 0], [3, 1, 0.0, 1, 0, 1], [2, 0, 29.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 0, 30.0, 0, 0, 0], [1, 0, 44.0, 2, 0, 1], [3, 1, 25.0, 0, 0, 2], [2, 1, 24.0, 0, 2, 2], [1, 0, 37.0, 1, 1, 2], [2, 0, 54.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 29.0, 1, 1, 2], [1, 0, 62.0, 0, 0, 2], [3, 0, 30.0, 1, 0, 2], [3, 1, 41.0, 0, 2, 2], [3, 1, 29.0, 0, 2, 0], [1, 1, 0.0, 0, 0, 0], [1, 1, 30.0, 0, 0, 2], [1, 1, 35.0, 0, 0, 0], [2, 1, 50.0, 0, 1, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 3.0, 4, 2, 2], [1, 0, 52.0, 1, 1, 2], [1, 0, 40.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [2, 0, 36.0, 0, 0, 2], [3, 0, 16.0, 4, 1, 2], [3, 0, 25.0, 1, 0, 2], [1, 1, 58.0, 0, 1, 2], [1, 1, 35.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [2, 1, 41.0, 0, 1, 2], [1, 0, 37.0, 0, 1, 0], [3, 1, 0.0, 0, 0, 1], [1, 1, 63.0, 1, 0, 2], [3, 1, 45.0, 0, 0, 2], [2, 0, 0.0, 0, 0, 2], [3, 0, 7.0, 4, 1, 1], [3, 1, 35.0, 1, 1, 2], [3, 0, 65.0, 0, 0, 1], [3, 0, 28.0, 0, 0, 2], [3, 0, 16.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 33.0, 0, 0, 0], [3, 0, 30.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [2, 0, 42.0, 0, 0, 2], [3, 1, 22.0, 0, 0, 1], [1, 1, 26.0, 0, 0, 2], [1, 1, 19.0, 1, 0, 0], [2, 0, 36.0, 0, 0, 0], [3, 1, 24.0, 0, 0, 2], [3, 0, 24.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 23.5, 0, 0, 0], [1, 1, 2.0, 1, 2, 2], [1, 0, 0.0, 0, 0, 2], [1, 1, 50.0, 0, 1, 0], [3, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 2, 0, 1], [3, 0, 19.0, 0, 0, 2], [2, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [1, 0, 0.92000000000000004, 1, 2, 2], [1, 1, 0.0, 0, 0, 0], [1, 1, 17.0, 1, 0, 0], [2, 0, 30.0, 1, 0, 0], [1, 1, 30.0, 0, 0, 0], [1, 1, 24.0, 0, 0, 0], [1, 1, 18.0, 2, 2, 0], [2, 1, 26.0, 1, 1, 2], [3, 0, 28.0, 0, 0, 2], [2, 0, 43.0, 1, 1, 2], [3, 1, 26.0, 0, 0, 2], [2, 1, 24.0, 1, 0, 2], [2, 0, 54.0, 0, 0, 2], [1, 1, 31.0, 0, 2, 2], [1, 1, 40.0, 1, 1, 0], [3, 0, 22.0, 0, 0, 2], [3, 0, 27.0, 0, 0, 2], [2, 1, 30.0, 0, 0, 1], [2, 1, 22.0, 1, 1, 2], [3, 0, 0.0, 8, 2, 2], [1, 1, 36.0, 0, 0, 0], [3, 0, 61.0, 0, 0, 2], [2, 1, 36.0, 0, 0, 2], [3, 1, 31.0, 1, 1, 2], [1, 1, 16.0, 0, 1, 0], [3, 1, 0.0, 2, 0, 1], [1, 0, 45.5, 0, 0, 2], [1, 0, 38.0, 0, 1, 2], [3, 0, 16.0, 2, 0, 2], [1, 1, 0.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 29.0, 1, 0, 2], [1, 1, 41.0, 0, 0, 0], [3, 0, 45.0, 0, 0, 2], [1, 0, 45.0, 0, 0, 2], [2, 0, 2.0, 1, 1, 2], [1, 1, 24.0, 3, 2, 2], [2, 0, 28.0, 0, 0, 2], [2, 0, 25.0, 0, 0, 2], [2, 0, 36.0, 0, 0, 2], [2, 1, 24.0, 0, 0, 2], [2, 1, 40.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 2], [3, 0, 3.0, 1, 1, 2], [3, 0, 42.0, 0, 0, 2], [3, 0, 23.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 15.0, 1, 1, 0], [3, 0, 25.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 28.0, 0, 0, 2], [1, 1, 22.0, 0, 1, 2], [2, 1, 38.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [3, 1, 0.0, 0, 0, 1], [3, 0, 40.0, 1, 4, 2], [2, 0, 29.0, 1, 0, 0], [3, 1, 45.0, 0, 1, 0], [3, 0, 35.0, 0, 0, 2], [3, 0, 0.0, 1, 0, 1], [3, 0, 30.0, 0, 0, 2], [1, 1, 60.0, 1, 0, 0], [3, 1, 0.0, 0, 0, 0], [3, 1, 0.0, 0, 0, 1], [1, 1, 24.0, 0, 0, 0], [1, 0, 25.0, 1, 0, 0], [3, 0, 18.0, 1, 0, 2], [3, 0, 19.0, 0, 0, 2], [1, 0, 22.0, 0, 0, 0], [3, 1, 3.0, 3, 1, 2], [1, 1, 0.0, 1, 0, 0], [3, 1, 22.0, 0, 0, 2], [1, 0, 27.0, 0, 2, 0], [3, 0, 20.0, 0, 0, 0], [3, 0, 19.0, 0, 0, 2], [1, 1, 42.0, 0, 0, 0], [3, 1, 1.0, 0, 2, 0], [3, 0, 32.0, 0, 0, 2], [1, 1, 35.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 0, 18.0, 0, 0, 2], [3, 0, 1.0, 5, 2, 2], [2, 1, 36.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [2, 1, 17.0, 0, 0, 0], [1, 0, 36.0, 1, 2, 2], [3, 0, 21.0, 0, 0, 2], [3, 0, 28.0, 2, 0, 2], [1, 1, 23.0, 1, 0, 0], [3, 1, 24.0, 0, 2, 2], [3, 0, 22.0, 0, 0, 2], [3, 1, 31.0, 0, 0, 2], [2, 0, 46.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 2], [2, 1, 28.0, 0, 0, 2], [3, 0, 39.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 1, 21.0, 1, 0, 2], [3, 0, 28.0, 1, 0, 2], [3, 1, 20.0, 0, 0, 2], [2, 0, 34.0, 1, 0, 2], [3, 0, 51.0, 0, 0, 2], [2, 0, 3.0, 1, 1, 2], [3, 0, 21.0, 0, 0, 2], [3, 1, 0.0, 3, 1, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 1, 33.0, 1, 0, 1], [2, 0, 0.0, 0, 0, 2], [3, 0, 44.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 2], [2, 1, 34.0, 1, 1, 2], [2, 1, 18.0, 0, 2, 2], [2, 0, 30.0, 0, 0, 2], [3, 1, 10.0, 0, 2, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 1], [3, 0, 29.0, 0, 0, 2], [3, 1, 28.0, 1, 1, 2], [3, 0, 18.0, 1, 1, 2], [3, 0, 0.0, 0, 0, 2], [2, 1, 28.0, 1, 0, 2], [2, 1, 19.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 32.0, 0, 0, 2], [1, 0, 28.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 2], [2, 1, 42.0, 1, 0, 2], [3, 0, 17.0, 0, 0, 2], [1, 0, 50.0, 1, 0, 2], [1, 1, 14.0, 1, 2, 2], [3, 1, 21.0, 2, 2, 2], [2, 1, 24.0, 2, 3, 2], [1, 0, 64.0, 1, 4, 2], [2, 0, 31.0, 0, 0, 2], [2, 1, 45.0, 1, 1, 2], [3, 0, 20.0, 0, 0, 2], [3, 0, 25.0, 1, 0, 2], [2, 1, 28.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 4.0, 0, 2, 2], [2, 1, 13.0, 0, 1, 2], [1, 0, 34.0, 0, 0, 2], [3, 1, 5.0, 2, 1, 0], [1, 0, 52.0, 0, 0, 2], [2, 0, 36.0, 1, 2, 2], [3, 0, 0.0, 1, 0, 2], [1, 0, 30.0, 0, 0, 0], [1, 0, 49.0, 1, 0, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 0], [1, 0, 65.0, 0, 0, 2], [1, 1, 0.0, 1, 0, 2], [2, 1, 50.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 0, 48.0, 0, 0, 2], [3, 0, 34.0, 0, 0, 2], [1, 0, 47.0, 0, 0, 2], [2, 0, 48.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 38.0, 0, 0, 2], [2, 0, 0.0, 0, 0, 2], [1, 0, 56.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 1, 0.75, 2, 1, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 38.0, 0, 0, 2], [2, 1, 33.0, 1, 2, 2], [2, 1, 23.0, 0, 0, 0], [3, 1, 22.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [2, 0, 34.0, 1, 0, 2], [3, 0, 29.0, 1, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 1, 2.0, 0, 1, 2], [3, 0, 9.0, 5, 2, 2], [2, 0, 0.0, 0, 0, 2], [3, 0, 50.0, 0, 0, 2], [3, 1, 63.0, 0, 0, 2], [1, 0, 25.0, 1, 0, 0], [3, 1, 0.0, 3, 1, 2], [1, 1, 35.0, 1, 0, 2], [1, 0, 58.0, 0, 0, 0], [3, 0, 30.0, 0, 0, 2], [3, 0, 9.0, 1, 1, 2], [3, 0, 0.0, 1, 0, 2], [3, 0, 21.0, 0, 0, 2], [1, 0, 55.0, 0, 0, 2], [1, 0, 71.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [1, 1, 54.0, 1, 0, 0], [3, 0, 0.0, 0, 0, 2], [1, 1, 25.0, 1, 2, 2], [3, 0, 24.0, 0, 0, 2], [3, 0, 17.0, 0, 0, 2], [3, 1, 21.0, 0, 0, 1], [3, 1, 0.0, 0, 0, 1], [3, 1, 37.0, 0, 0, 2], [1, 1, 16.0, 0, 0, 2], [1, 0, 18.0, 1, 0, 0], [2, 1, 33.0, 0, 2, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 28.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [1, 0, 36.0, 0, 0, 2], [1, 1, 54.0, 1, 0, 0], [3, 0, 24.0, 0, 0, 2], [1, 0, 47.0, 0, 0, 2], [2, 1, 34.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [2, 1, 36.0, 1, 0, 2], [3, 0, 32.0, 0, 0, 2], [1, 1, 30.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [1, 1, 44.0, 0, 1, 0], [3, 0, 0.0, 0, 0, 0], [3, 0, 40.5, 0, 0, 1], [2, 1, 50.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 39.0, 0, 0, 2], [2, 0, 23.0, 2, 1, 2], [2, 1, 2.0, 1, 1, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 17.0, 1, 1, 0], [3, 1, 0.0, 0, 2, 0], [3, 1, 30.0, 0, 0, 2], [2, 1, 7.0, 0, 2, 2], [1, 0, 45.0, 0, 0, 2], [1, 1, 30.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 2], [1, 1, 22.0, 0, 2, 0], [1, 1, 36.0, 0, 2, 2], [3, 1, 9.0, 4, 2, 2], [3, 1, 11.0, 4, 2, 2], [2, 0, 32.0, 1, 0, 2], [1, 0, 50.0, 1, 0, 0], [1, 0, 64.0, 0, 0, 2], [2, 1, 19.0, 1, 0, 2], [2, 0, 0.0, 0, 0, 0], [3, 0, 33.0, 1, 1, 2], [2, 0, 8.0, 1, 1, 2], [1, 0, 17.0, 0, 2, 0], [2, 0, 27.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 22.0, 0, 0, 0], [3, 1, 22.0, 0, 0, 2], [1, 0, 62.0, 0, 0, 2], [1, 1, 48.0, 1, 0, 0], [1, 0, 0.0, 0, 0, 0], [1, 1, 39.0, 1, 1, 2], [3, 1, 36.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 40.0, 0, 0, 2], [2, 0, 28.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 2], [3, 0, 24.0, 2, 0, 2], [3, 0, 19.0, 0, 0, 2], [3, 1, 29.0, 0, 4, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 32.0, 0, 0, 2], [2, 0, 62.0, 0, 0, 2], [1, 1, 53.0, 2, 0, 2], [1, 0, 36.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [3, 0, 16.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [2, 1, 34.0, 0, 0, 2], [1, 1, 39.0, 1, 0, 2], [3, 1, 0.0, 1, 0, 0], [3, 0, 32.0, 0, 0, 2], [2, 1, 25.0, 1, 1, 2], [1, 1, 39.0, 1, 1, 0], [2, 0, 54.0, 0, 0, 2], [1, 0, 36.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 0], [1, 1, 18.0, 0, 2, 2], [2, 0, 47.0, 0, 0, 2], [1, 0, 60.0, 1, 1, 0], [3, 0, 22.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 35.0, 0, 0, 2], [1, 1, 52.0, 1, 0, 0], [3, 0, 47.0, 0, 0, 2], [3, 1, 0.0, 0, 2, 1], [2, 0, 37.0, 1, 0, 2], [3, 0, 36.0, 1, 1, 2], [2, 1, 0.0, 0, 0, 2], [3, 0, 49.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [1, 0, 49.0, 1, 0, 0], [2, 1, 24.0, 2, 1, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 44.0, 0, 0, 2], [1, 0, 35.0, 0, 0, 0], [3, 0, 36.0, 1, 0, 2], [3, 0, 30.0, 0, 0, 2], [1, 0, 27.0, 0, 0, 2], [2, 1, 22.0, 1, 2, 0], [1, 1, 40.0, 0, 0, 2], [3, 1, 39.0, 1, 5, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 1], [3, 0, 0.0, 0, 0, 1], [3, 0, 35.0, 0, 0, 2], [2, 1, 24.0, 1, 2, 2], [3, 0, 34.0, 1, 1, 2], [3, 1, 26.0, 1, 0, 2], [2, 1, 4.0, 2, 1, 2], [2, 0, 26.0, 0, 0, 2], [3, 0, 27.0, 1, 0, 0], [1, 0, 42.0, 1, 0, 2], [3, 0, 20.0, 1, 1, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 21.0, 0, 0, 2], [1, 0, 61.0, 0, 0, 2], [2, 0, 57.0, 0, 0, 1], [1, 1, 21.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 0, 80.0, 0, 0, 2], [3, 0, 51.0, 0, 0, 2], [1, 0, 32.0, 0, 0, 0], [1, 0, 0.0, 0, 0, 2], [3, 1, 9.0, 3, 2, 2], [2, 1, 28.0, 0, 0, 2], [3, 0, 32.0, 0, 0, 2], [2, 0, 31.0, 1, 1, 2], [3, 1, 41.0, 0, 5, 2], [3, 0, 0.0, 1, 0, 2], [3, 0, 20.0, 0, 0, 2], [1, 1, 24.0, 0, 0, 0], [3, 1, 2.0, 3, 2, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 0.75, 2, 1, 0], [1, 0, 48.0, 1, 0, 0], [3, 0, 19.0, 0, 0, 2], [1, 0, 56.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 2], [3, 1, 23.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 1, 18.0, 0, 1, 2], [3, 0, 21.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [3, 1, 18.0, 0, 0, 1], [2, 0, 24.0, 2, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 32.0, 1, 1, 1], [2, 0, 23.0, 0, 0, 2], [1, 0, 58.0, 0, 2, 0], [1, 0, 50.0, 2, 0, 2], [3, 0, 40.0, 0, 0, 0], [1, 0, 47.0, 0, 0, 2], [3, 0, 36.0, 0, 0, 2], [3, 0, 20.0, 1, 0, 2], [2, 0, 32.0, 2, 0, 2], [2, 0, 25.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 43.0, 0, 0, 2], [1, 1, 0.0, 1, 0, 2], [2, 1, 40.0, 1, 1, 2], [1, 0, 31.0, 1, 0, 2], [2, 0, 70.0, 0, 0, 2], [2, 0, 31.0, 0, 0, 2], [2, 0, 0.0, 0, 0, 2], [3, 0, 18.0, 0, 0, 2], [3, 0, 24.5, 0, 0, 2], [3, 1, 18.0, 0, 0, 2], [3, 1, 43.0, 1, 6, 2], [1, 0, 36.0, 0, 1, 0], [3, 1, 0.0, 0, 0, 1], [1, 0, 27.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [3, 0, 14.0, 5, 2, 2], [2, 0, 60.0, 1, 1, 2], [2, 0, 25.0, 1, 2, 0], [3, 0, 14.0, 4, 1, 2], [3, 0, 19.0, 0, 0, 2], [3, 0, 18.0, 0, 0, 2], [1, 1, 15.0, 0, 1, 2], [1, 0, 31.0, 1, 0, 2], [3, 1, 4.0, 0, 1, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 0], [1, 0, 60.0, 0, 0, 2], [2, 0, 52.0, 0, 0, 2], [3, 0, 44.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [1, 0, 49.0, 1, 1, 0], [3, 0, 42.0, 0, 0, 2], [1, 1, 18.0, 1, 0, 0], [1, 0, 35.0, 0, 0, 2], [3, 1, 18.0, 0, 1, 0], [3, 0, 25.0, 0, 0, 1], [3, 0, 26.0, 1, 0, 2], [2, 0, 39.0, 0, 0, 2], [2, 1, 45.0, 0, 0, 2], [1, 0, 42.0, 0, 0, 2], [1, 1, 22.0, 0, 0, 2], [3, 0, 0.0, 1, 1, 0], [1, 1, 24.0, 0, 0, 0], [1, 0, 0.0, 0, 0, 2], [1, 0, 48.0, 1, 0, 2], [3, 0, 29.0, 0, 0, 2], [2, 0, 52.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [1, 1, 38.0, 0, 0, 0], [2, 1, 27.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 33.0, 0, 0, 2], [2, 1, 6.0, 0, 1, 2], [3, 0, 17.0, 1, 0, 2], [2, 0, 34.0, 0, 0, 2], [2, 0, 50.0, 0, 0, 2], [1, 0, 27.0, 1, 0, 2], [3, 0, 20.0, 0, 0, 2], [2, 1, 30.0, 3, 0, 2], [3, 1, 0.0, 0, 0, 1], [2, 0, 25.0, 1, 0, 2], [3, 1, 25.0, 1, 0, 2], [1, 1, 29.0, 0, 0, 2], [3, 0, 11.0, 0, 0, 0], [2, 0, 0.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 2], [3, 0, 28.5, 0, 0, 2], [3, 1, 48.0, 1, 3, 2], [1, 0, 35.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [1, 0, 36.0, 1, 0, 2], [1, 1, 21.0, 2, 2, 0], [3, 0, 24.0, 1, 0, 2], [3, 0, 31.0, 0, 0, 2], [1, 0, 70.0, 1, 1, 2], [3, 0, 16.0, 1, 1, 2], [2, 1, 30.0, 0, 0, 2], [1, 0, 19.0, 1, 0, 2], [3, 0, 31.0, 0, 0, 1], [2, 1, 4.0, 1, 1, 2], [3, 0, 6.0, 0, 1, 2], [3, 0, 33.0, 0, 0, 2], [3, 0, 23.0, 0, 0, 2], [2, 1, 48.0, 1, 2, 2], [2, 0, 0.67000000000000004, 1, 1, 2], [3, 0, 28.0, 0, 0, 2], [2, 0, 18.0, 0, 0, 2], [3, 0, 34.0, 0, 0, 2], [1, 1, 33.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 41.0, 0, 0, 2], [3, 0, 20.0, 0, 0, 0], [1, 1, 36.0, 1, 2, 2], [3, 0, 16.0, 0, 0, 2], [1, 1, 51.0, 1, 0, 2], [1, 0, 0.0, 0, 0, 0], [3, 1, 30.5, 0, 0, 1], [3, 0, 0.0, 1, 0, 1], [3, 0, 32.0, 0, 0, 2], [3, 0, 24.0, 0, 0, 2], [3, 0, 48.0, 0, 0, 2], [2, 1, 57.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [2, 1, 54.0, 1, 3, 2], [3, 0, 18.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 1, 5.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 1, 43.0, 0, 1, 2], [3, 1, 13.0, 0, 0, 0], [1, 1, 17.0, 1, 0, 2], [1, 0, 29.0, 0, 0, 2], [3, 0, 0.0, 1, 2, 2], [3, 0, 25.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [3, 1, 18.0, 0, 0, 2], [3, 0, 8.0, 4, 1, 1], [3, 0, 1.0, 1, 2, 2], [1, 0, 46.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 1], [2, 0, 16.0, 0, 0, 2], [3, 1, 0.0, 8, 2, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 25.0, 0, 0, 2], [2, 0, 39.0, 0, 0, 2], [1, 1, 49.0, 0, 0, 2], [3, 1, 31.0, 0, 0, 2], [3, 0, 30.0, 0, 0, 0], [3, 1, 30.0, 1, 1, 2], [2, 0, 34.0, 0, 0, 2], [2, 1, 31.0, 1, 1, 2], [1, 0, 11.0, 1, 2, 2], [3, 0, 0.41999999999999998, 0, 1, 0], [3, 0, 27.0, 0, 0, 2], [3, 0, 31.0, 0, 0, 2], [1, 0, 39.0, 0, 0, 2], [3, 1, 18.0, 0, 0, 2], [2, 0, 39.0, 0, 0, 2], [1, 1, 33.0, 1, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 39.0, 0, 0, 2], [2, 0, 35.0, 0, 0, 2], [3, 1, 6.0, 4, 2, 2], [3, 0, 30.5, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 1, 23.0, 0, 0, 2], [2, 0, 31.0, 1, 1, 0], [3, 0, 43.0, 0, 0, 2], [3, 0, 10.0, 3, 2, 2], [1, 1, 52.0, 1, 1, 2], [3, 0, 27.0, 0, 0, 2], [1, 0, 38.0, 0, 0, 2], [3, 1, 27.0, 0, 1, 2], [3, 0, 2.0, 4, 1, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [2, 0, 1.0, 0, 2, 0], [3, 0, 0.0, 0, 0, 1], [1, 1, 62.0, 0, 0, 2], [3, 1, 15.0, 1, 0, 0], [2, 0, 0.82999999999999996, 1, 1, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 23.0, 0, 0, 2], [3, 0, 18.0, 0, 0, 2], [1, 1, 39.0, 1, 1, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 32.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [2, 0, 16.0, 0, 0, 2], [1, 1, 30.0, 0, 0, 0], [3, 0, 34.5, 0, 0, 0], [3, 0, 17.0, 0, 0, 2], [3, 0, 42.0, 0, 0, 2], [3, 0, 0.0, 8, 2, 2], [3, 0, 35.0, 0, 0, 0], [2, 0, 28.0, 0, 1, 2], [1, 1, 0.0, 1, 0, 0], [3, 0, 4.0, 4, 2, 2], [3, 0, 74.0, 0, 0, 2], [3, 1, 9.0, 1, 1, 0], [1, 1, 16.0, 0, 1, 2], [2, 1, 44.0, 1, 0, 2], [3, 1, 18.0, 0, 1, 2], [1, 1, 45.0, 1, 1, 2], [1, 0, 51.0, 0, 0, 2], [3, 1, 24.0, 0, 3, 0], [3, 0, 0.0, 0, 0, 0], [3, 0, 41.0, 2, 0, 2], [2, 0, 21.0, 1, 0, 2], [1, 1, 48.0, 0, 0, 2], [3, 1, 0.0, 8, 2, 2], [2, 0, 24.0, 0, 0, 2], [2, 1, 42.0, 0, 0, 2], [2, 1, 27.0, 1, 0, 0], [1, 0, 31.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 4.0, 1, 1, 2], [3, 0, 26.0, 0, 0, 2], [1, 1, 47.0, 1, 1, 2], [1, 0, 33.0, 0, 0, 2], [3, 0, 47.0, 0, 0, 2], [2, 1, 28.0, 1, 0, 0], [3, 1, 15.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 1, 56.0, 0, 1, 0], [2, 1, 25.0, 0, 1, 2], [3, 0, 33.0, 0, 0, 2], [3, 1, 22.0, 0, 0, 2], [2, 0, 28.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [3, 1, 39.0, 0, 5, 1], [2, 0, 27.0, 0, 0, 2], [1, 1, 19.0, 0, 0, 2], [3, 1, 0.0, 1, 2, 2], [1, 0, 26.0, 0, 0, 0], [3, 0, 32.0, 0, 0, 1]]

if __name__ == "__main__":
    main()

"""
------------------------------------------------------------------------------------------
-------------------------------
--- Titanic passengers data ---
-------------------------------
 
names list
 0 0:died 1:survived | name

data list
 0 1:upper,2:middle,3:lower class
 1 0:male 1:female
 2 age
 3 number of spouses and siblings onboard
 4 number of parents and children onboard
 5 point of departure 0:Cherbourg 1:Queenstown 2:Southhampton

"""

word_list= [[1,25,30,45,50,62,55,75],
           [14,15,19,31,47,51] , 
           [6,7,20,38,40,53,60,61] ] 

def traverse( pos_list ) : 

    idx_list = [ 0 for l in pos_list ] 
    min_idx_list = idx_list
    min_idx_dist = 100000

    while 1: 
        words = sorted( [ (i,pos_list[i][ pos ],pos) for i,pos in enumerate( idx_list ) ] , key=lambda v:v[1] ) 
        print words
        cost = words[-1][1] - words[0][1]
        
        if  cost < min_idx_dist : 
            min_idx_dist = cost 
            min_idx_list = list(idx_list)
        idx, dist, pos = words[0]
        if pos >= len( pos_list[ idx ] )  -1  :
            break 

        idx_list[ idx ] = pos + 1
    
    print min_idx_list, min_idx_dist


        

traverse( word_list ) 
